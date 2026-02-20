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

def update_config_val(conf:str, var:str, new:str):
    with open(conf, "r") as f:
        config_lines = f.readlines()

        line_number = 0
        for line in config_lines:
            if var in line:
                config_lines[line_number] = f"{var}=\"{new}\"\n"
            line_number += 1

    with open(conf, "w") as f:
        f.writelines(config_lines)

def read_config_val(conf:str, var:str) -> str:
    with open(conf, "r") as f:
        config_lines = f.readlines()

        for line in config_lines:
            if var in line:
                result_list = line.split('"')

    return result_list[1]