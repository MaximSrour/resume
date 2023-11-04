from dotenv import load_dotenv
import os
import MySQLdb
from datetime import datetime

import latex

from local_types import *

FILE_NAME = "Maxim Srour - Resume"
FILE_NAME = FILE_NAME.replace(" ", "\\ ")

load_dotenv()

class Connection:
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.connection = MySQLdb.connect(
            host= os.getenv("DB_HOST"),
            user=os.getenv("DB_USERNAME"),
            passwd= os.getenv("DB_PASSWORD"),
            db= os.getenv("DB_NAME"),
            autocommit = True,
            ssl_mode = "VERIFY_IDENTITY",
            ssl      = {
                "ca": "/etc/ssl/certs/ca-certificates.crt"
            }
        )

def process_query_data(query: str, data_shape: type) -> list[type]:
    """
    Process the data from a query into a list of objects

    @params {string} query - The query to run
    @params {type} data_shape - The class to shape the data into
    @returns {list[type]} - A list of objects
    """

    cursor = Connection().connection.cursor()

    cursor.execute(query)
    data = cursor.fetchall()

    out = []
    for element in data:
        out.append(data_shape(element))
    
    return out

def query_work() -> list[Position]:
    """
    Get the work experience data
    
    @returns {list[Position]} - The work experience data
    """

    works = process_query_data("SELECT * FROM WorkExperience", WorkExperience)

    positions = process_query_data("SELECT * FROM Position", Position)    

    position_texts = process_query_data("SELECT * FROM PositionText", PositionText)

    for position in positions:
        for work in works:
            if work.id == position.work_id:
                position.set_work(work)
                break
        
        for position_text in position_texts:
            if position_text.position_id == position.id:
                position.add_text(position_text)

        position.text = sorted(position.text, key=lambda x: x.order, reverse=False)
    
    def sorting_key(position):
        if position.end == "Current":
            return datetime.now()
        else:
            return position.end
        
    positions = sorted(positions, key=lambda x: x.start, reverse=False)
    positions = sorted(positions, key=lambda x: sorting_key(x), reverse=True)

    return positions

def query_education() -> list[Education]:
    """
    Get the education data

    @returns {list[Education]} - The education data
    """
    
    educations = process_query_data("SELECT * FROM Education", Education)

    educations = sorted(educations, key=lambda x: x.start, reverse=True)

    return educations

def get_data(query: str, id: str, generator_func: callable) -> str:
    """
    Get the data from a query

    @params {str} query - The query to run
    @params {str} id - The latex id to use
    @params {callable} generator_func - The function to generate the latex

    @returns {str} - The latex string
    """
    
    rows = query()

    tex = ""
    command_string = f"\\newcommand\\{id}{{\n"

    for row in rows:
        if row.hidden:
            continue

        tex += "\n" + generator_func(row)
        command_string += f"\t\\printsaveditem{{{row.id}}}\n"

    tex += "\n" + command_string + "}\n\n"

    return tex

def generate_tex() -> str:
    """
    Generate the tex string

    @returns {str} - The tex string
    """

    latex_out = "\\NeedsTeXFormat{LaTeX2e}\n\\ProvidesPackage{resumeitems}[Maxim]\n\\usepackage{resumeassets}\n\n"

    latex_out += get_data(query_work, "workexperience", latex.work_experience)
    latex_out += get_data(query_education, "education", latex.education)

    latex_out = latex.escape_characters(latex_out)

    return latex_out

def clean_files() -> None:
    """
    Clean the files in the tex directory
    """

    extensions = ["aux", "log", "out", "glo", "xdy"]

    for extension in extensions:
        os.system(f"rm ./tex/{FILE_NAME}.{extension}")

    os.system(f"rm ./tex/texput.log")

def main() -> None:
    """
    The main function
    """
    
    latex_out = generate_tex()

    with open("./tex/resumeitems.sty", "w") as file:
        file.write(latex_out)

    os.system(f"pdflatex -output-directory ./tex ./tex/{FILE_NAME}.tex")

    #clean_files()

if __name__ == "__main__":
    main()