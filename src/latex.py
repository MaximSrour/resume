from local_types import Education, Position

def date_to_tex(date_object: str) -> str:
    """
    Convert a date object to a latex string

    @params {str} date_object - The date object to convert
    @returns {str} - The latex string
    """

    if(date_object == "Current"):
        return "Current"
    
    else:
        out_string = "\\customdate{{{}}}".format(date_object.day)
        out_string += "{{{}}}".format(date_object.month)
        out_string += "{{{}}}".format(date_object.year)

        return out_string

def escape_character(string_to_clean: str, character: str) -> str:
    """
    Escape a character in a string

    @params {str} string_to_clean - The string to clean
    @params {str} character - The character to escape
    @returns {str} - The cleaned string
    """

    temp_array = string_to_clean.split(character)
    temp_string = temp_array[0]

    for stringlet in temp_array[1:]:
        temp_string += "\\{}".format(character)
        temp_string += stringlet
    
    return temp_string

def escape_characters(string_to_clean: str) -> str:
    """
    Escape all the characters in a string

    @params {str} string_to_clean - The string to clean
    @returns {str} - The cleaned string
    """

    characters = ["&", "#", "%"]

    for character in characters:
        string_to_clean = escape_character(string_to_clean, character)
    
    return string_to_clean

def tex(command: str, *args: str) -> str:
    """
    Create a latex string

    @params {str} args - The arguments to join
    @returns {str} - The latex string
    """

    #return f"\\{command}" + "".join(f"{{{escape_characters(arg)}}}" for arg in args)
    return f"\\{command}" + "".join(f"{{{arg}}}" for arg in args)

def section(title: str, numbered: bool = False) -> str:
    """
    Create a latex section

    @params {str} title - The title of the section
    @params {bool} numbered - Whether the section should be numbered
    @returns {str} - The latex string
    """
    
    return tex("section", title) if numbered else tex("section*", title)

def paragraph(content: str, label: str = "") -> str:
    """
    Create a latex paragraph

    @params {str} content - The content of the paragraph
    @params {str} label - The label of the paragraph
    @returns {str} - The latex string
    """
    
    return tex("paragraph", label) + content

def new_saved_item(id: str, item: str) -> str:
    """
    Create a new saved item

    @params {str} id - The id of the item
    @params {str} item - The item to save
    @returns {str} - The latex string
    """
    
    return tex("newsaveditem", id, f"{item}\n")

def item(content: str, label: str = "") -> str:
    """
    Create a latex item

    @params {str} content - The content of the item
    @params {str} label - The label of the item
    @returns {str} - The latex string
    """
    
    return tex("item", label) + content

def work_experience(data: Position):

    #TODO: Add assertion

    text = ""

    data.start = date_to_tex(data.start)
    data.end = date_to_tex(data.end)

    text += f"\n\t\workexperienceitem{{{data.title}}}{{{data.work.organisation}}}{{{data.start}}}{{{data.end}}}{{\n\t\t\\begin{{itemize}}"

    for i in data.text:
        text += f"\n\t\t\t\\item {i.text}"

    text += f"\n\t\t\\end{{itemize}}\n\t}}"

    return new_saved_item(data.id, text)

def education(data: Education):

    #TODO: Add assertion
    
    text = ""

    text += f"\n\t\educationitem{{{data.title}}}{{{data.organisation}}}{{{data.start}}}{{{data.end}}}{{\n\t\t{paragraph(data.description)}\n\t}}"

    return new_saved_item(data.id, text)
