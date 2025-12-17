

def create_page_dict(page_list: list[str]) -> list[str]:
    
    sanitized_names = []
    
    # convert names of collections to their corresponding
    # page name by making them lowercase and snake case
    for page in page_list:
        sanitized_names.append(page.lower().replace(" ", "_"))
    
    # return a dictionary in the form of "name" : "file_name" 
    # Note: the file name does not have the file extension as of yet
    return dict(zip(page_list, sanitized_names))
