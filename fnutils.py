from typing import Optional
import re
import aiofiles


def is_match(regex: str, path: str, file_name: Optional[str]) -> bool:
    """
    This function read the content from a file and returns True if
    the content matches with the regular expression, if it does not, returns False.
    """
    file = open(f'{path}/{file_name}')
    content = file.read()
    if re.match(regex, content):
        return True
    else:
        return False


async def async_is_match(regex: str, file_with_path: str) -> bool:
    """
    This function read the content from a file and returns True if
    the content matches with the regular expression, if it does not, returns False.
    """
    async with aiofiles.open(file_with_path, mode="r") as file:
        content = await file.read()
        if re.match(regex, content):
            return True
        else:
            return False


async def show_data(projects_list: dict) -> None:
    """
    This function show the dictionary data in the command line
    """
    for project in projects_list:
        print("_________________________________________________________")
        print(" "*5, project.get('name'), " "*5)
        print("_________________________________________________________\n")
        columns_list = project.get('columns_list')
        if columns_list:
            print("#############")
            print("   COLUMNS   ")
            print("#############")
            for column in columns_list:
                print("*", column.get('name'), '\n')
                cards_list = column.get('cards_list')
                if cards_list:
                    for card in cards_list:
                        print("\t|", card.get('content_url'), "|")
                else:
                    print("\tThis column does not have any card")
        else:
            print("This project does not have any column")
