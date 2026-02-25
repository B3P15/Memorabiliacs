import streamlit as st
import BackendMethods.auth_functions as authFuncs

login_color_flag = 0

def create_page_dict(page_list: list[str]) -> list[str]:
    
    sanitized_names = []
    
    # convert names of collections to their corresponding
    # page name by making them lowercase and snake case
    for page in page_list:
        sanitized_names.append(snake_name(page))
    
    # return a dictionary in the form of "name" : "file_name" 
    # Note: the file name does not have the file extension as of yet
    return dict(zip(page_list, sanitized_names))


def snake_name(name: str) -> str:
    return name.lower().replace(" ", "_")

def rename(old:str, new:str, l:list[str]):
    for i in range(len(l)):
        if l[i] == old:
            l[i] = new

def update_config_val(conf:str, var:str, new:str) -> None:
    with open(conf, "r") as f:
        config_lines = f.readlines()

        line_number = 0
        for line in config_lines:
            if var in line:
                config_lines[line_number] = f"{var}=\"{new}\"\n"
            line_number += 1

    with open(conf, "w") as f:
        f.writelines(config_lines)

def update_settings(conf:str, diction:dict) -> None:
    for setting in diction:
        if setting != "theme":
            update_config_val(conf, setting, diction[setting])

def read_config_val(conf:str, var:str) -> str:
    with open(conf, "r") as f:
        config_lines = f.readlines()

        for line in config_lines:
            if var in line:
                result_list = line.split('"')

    return result_list[1]

def page_initialization():
    st.set_page_config(layout="wide")
    st.title("Memorabiliacs", text_alignment="center")
    with st.container(horizontal=True, vertical_alignment="top"):
        with st.container(horizontal_alignment="left", vertical_alignment="top"):
            if st.button("Home"):
                st.switch_page("pages/home_page.py")
        with st.container(horizontal_alignment="center", vertical_alignment="top"):
            if st.button("Search"):
                st.switch_page("pages/search.py")
        with st.container(horizontal_alignment="right", vertical_alignment="top"):
            if st.button("Settings"):
                st.switch_page("pages/settings.py")
        