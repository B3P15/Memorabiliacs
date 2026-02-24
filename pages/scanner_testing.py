import io
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


# messing around with scanning and image uploading for upc, isbn should be removed but the rest I believe are good

#import global_functions as gfuncs

try:
	from pyzbar import pyzbar

	PYZBAR_AVAILABLE = True
except Exception:
	PYZBAR_AVAILABLE = False


def _decode_barcodes(image: Image.Image) -> list[dict[str, str]]:
	if not PYZBAR_AVAILABLE:
		return []

	decoded = pyzbar.decode(image)
	results: list[dict[str, str]] = []
	for barcode in decoded:
		data = barcode.data.decode("utf-8", errors="ignore").strip()
		if data:
			results.append({"type": barcode.type, "data": data})
	return results


def _enhance_variants(image: Image.Image) -> list[Image.Image]:
	variants: list[Image.Image] = []

	gray = ImageOps.grayscale(image)
	variants.append(gray)
	variants.append(ImageOps.autocontrast(gray))
	variants.append(ImageOps.autocontrast(gray, cutoff=2))

	contrast = ImageEnhance.Contrast(gray).enhance(2.0)
	variants.append(contrast)

	sharp = contrast.filter(ImageFilter.UnsharpMask(radius=2, percent=200, threshold=3))
	variants.append(sharp)
	variants.append(sharp.filter(ImageFilter.SHARPEN))

	for scale in (0.75, 1.25, 1.5, 2.0):
		w, h = gray.size
		scaled = gray.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
		variants.append(scaled)

	rotated: list[Image.Image] = []
	for img in variants:
		rotated.append(img)
		rotated.append(img.rotate(90, expand=True))
		rotated.append(img.rotate(180, expand=True))
		rotated.append(img.rotate(270, expand=True))

	return rotated


def _decode_with_enhancements(image: Image.Image) -> list[dict[str, str]]:
	for variant in _enhance_variants(image):
		decoded = _decode_barcodes(variant)
		if decoded:
			return decoded
	return []


def _normalize_payload(payload: str) -> str:
	return payload.replace("-", "").replace(" ", "").strip()


def _classify_code(code: str, barcode_type: str) -> str:
	barcode_type = (barcode_type or "").upper()
	known = {
		"UPCA": "UPC-A",
		"UPCE": "UPC-E",
		"EAN13": "EAN-13",
		"EAN8": "EAN-8",
		"ISBN10": "ISBN-10",
		"ISBN13": "ISBN-13",
	}
	if barcode_type in known:
		return known[barcode_type]

	if len(code) == 8:
		return "UPC-E / EAN-8"
	if len(code) == 10:
		return "ISBN-10"
	if len(code) == 12:
		return "UPC-A"
	if len(code) == 13:
		return "ISBN-13" if code.startswith(("978", "979")) else "EAN-13"
	return "Unknown"


def _extract_supported_codes(decoded: list[dict[str, str]]) -> list[dict[str, str]]:
	seen: set[str] = set()
	matches: list[dict[str, str]] = []
	for item in decoded:
		raw = _normalize_payload(item["data"])
		if not raw:
			continue

		code = raw
		if len(raw) == 10 and raw[:-1].isdigit() and raw[-1] in "Xx":
			code = raw[:-1] + "X"
		elif not raw.isdigit():
			continue

		if len(code) not in {8, 10, 12, 13}:
			continue
		if code in seen:
			continue

		seen.add(code)
		matches.append({
			"code": code,
			"label": _classify_code(code, item.get("type", "")),
		})
	return matches


def _load_image(uploaded_file: st.runtime.uploaded_file_manager.UploadedFile) -> Image.Image:
	data = uploaded_file.getvalue()
	return Image.open(io.BytesIO(data)).convert("RGB")



if 1==1:
	#gfuncs.page_initialization()

	st.title("Barcode Scanner", text_alignment="center")
	st.caption("Scan a barcode with your camera or upload an image. Supports UPC, EAN, and ISBN.")

	input_mode = st.radio("Input source", options=["Camera", "Upload"], horizontal=True)
	enhanced = st.toggle("Enhanced decode (slower)", value=False)
	uploaded = None

	if input_mode == "Camera":
		uploaded = st.camera_input("Scan barcode")
	else:
		uploaded = st.file_uploader("Upload barcode image", type=["png", "jpg", "jpeg"])

	if not PYZBAR_AVAILABLE:
		st.error("Barcode decoding is unavailable. Install 'pyzbar' and the system 'zbar' library.")
		st.stop()

	decoded: list[dict[str, str]] = []
	if uploaded is not None:
		try:
			image = _load_image(uploaded)
			decoded = _decode_barcodes(image)
			if enhanced and not decoded:
				decoded = _decode_with_enhancements(image)
		except Exception as exc:
			st.error(f"Failed to read image: {exc}")

	if decoded:
		supported_codes = _extract_supported_codes(decoded)
		if supported_codes:
			st.success("Supported code(s) detected")
			options = [f"{item['code']} ({item['label']})" for item in supported_codes]
			selected = st.selectbox("Detected codes", options=options)
			st.session_state["last_code"] = selected.split(" ")[0]
		else:
			st.warning("Barcode detected, but no UPC/EAN/ISBN code found.")
	elif uploaded is not None:
		st.warning("No barcode detected. Try a clearer image with the code centered.")

	st.divider()
	manual_code = st.text_input("Manual entry (UPC/EAN/ISBN)", value=st.session_state.get("last_code", ""))
	if manual_code:
		normalized = _normalize_payload(manual_code)
		if len(normalized) == 10 and normalized[:-1].isdigit() and normalized[-1] in "Xx":
			code = normalized[:-1] + "X"
			label = _classify_code(code, "ISBN10")
			st.success(f"{label} ready for use: {code}")
		elif normalized.isdigit() and len(normalized) in {8, 12, 13}:
			label = _classify_code(normalized, "")
			st.success(f"{label} ready for use: {normalized}")
		else:
			st.info("Enter a valid UPC (8/12), EAN (8/13), or ISBN (10/13).")
