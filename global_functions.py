

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