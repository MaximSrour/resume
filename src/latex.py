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

def paragraph(content: str, header: str = "") -> str:
    """
    Create a latex paragraph

    @params {str} content - The content of the paragraph
    @params {str} header - The header of the paragraph
    @returns {str} - The latex string
    """
    
    return f"\\paragraph{{{header}}}{content}"

def new_saved_item(id, content):
    return f"\\newsaveditem{{{id}}}{{{content}\n}}"

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