from pypdf import PdfReader
import re
from pathlib import Path
import os

def get_files_list():
    dir_path = "Files"
    print(dir_path)
    file_names = []
    paths = list(Path(dir_path).rglob('*.pdf'))
    file_names = [str(path.parent / path.name ).replace("Files/","") for path in paths]
    file_names.sort(key=len)
    return file_names

def load_pdf(file_path):
    """
    Reads the text content from a PDF file and returns it as a single string.

    Parameters:

    - file_path (str): The file path to the PDF file.

    Returns:
    - str: The concatenated text content of all pages in the PDF.
    """
    # Logic to read pdf
    reader = PdfReader(file_path)

    # Loop over each page and store it in a variable
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text

def split_text(text: str):
    """
    Splits a text string into a list of non-empty substrings based on the specified pattern.
    The "\n\n\n" pattern will split the document para by para
    Parameters:
    - text (str): The input text to be split.

    Returns:
    - List[str]: A list containing non-empty substrings obtained by splitting the input text.

    """
    split_text = re.split('\n\n\n', text)
    return [i for i in split_text if i != ""]


def group_files(files_list):
    result = []
    for file_path in files_list:
        # Extract directory path without the filename
        folder_path = os.path.dirname(file_path)
        folder_list = folder_path.split("/",1)
        # If the folder is the root, parent ID is None
        if len(folder_list) == 1:
            parent_id = None
        else:
            #Get the parent id by searching the result list
            req_obj = [item for item in result if item['value'].rsplit("/",1)[0] == folder_path.rsplit("/",1)[0]][0]
            parent_id = req_obj["id"]
            
        # Add file data to result
        file_data = {
            'id': str(len(result) + 1),  # Unique ID for each file
            'label': os.path.basename(file_path),
            'value': file_path,
            'parentId': parent_id,
            'hasChild': False
        }  
        result.append(file_data)

        #Check if children exists based on parent_id
        for file in result:
          childExists = [item for item in result if item['parentId'] == file["id"]]
          if len(childExists) > 0:
            file["hasChild"] = True
    return result

def build_hierarchy(data):
    id_map = {item['id']: item for item in data}
    root_items = []
    
    for item in data:
        parent_id = item['parentId']
        if parent_id:
            parent = id_map.get(parent_id)
            if parent:
                if 'children' not in parent:
                    parent['children'] = []
                
                parent['children'].append(item)
        else:
            root_items.append(item)
    
    return root_items


