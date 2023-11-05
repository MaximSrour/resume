"""
This file renders a PDF resume from a latex template and a database.

Usage:
    python generate_resume.py [-s] [-q]

Options:
    -s, --skip    Skip regenerating the resumeitems.sty file. Render based on the cached version
    -q, --quiet   Don't print the output of the latex compiler

Exit codes:
    0 - Program ran successfully
    2 - Invalid arguments passed into the program
    10 - Error connecting to database
    11 - Error writing to file
"""

from dotenv import load_dotenv
import os
import MySQLdb
from datetime import datetime
import sys
import getopt

import latex

from logger import Logger

from local_types import *

# Get root directory of git repo
DIR_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_SRC = os.path.join(DIR_ROOT, "src")
DIR_TEX = os.path.join(DIR_ROOT, "tex")

FILE_STY_NAME = "resumeitems"
FILE_NAME = "Maxim Srour - Resume"
FILE_NAME = FILE_NAME.replace(" ", "\\ ")

FILE_STY = f"{os.path.join(DIR_TEX, FILE_STY_NAME)}.sty"
FILE_TEX = f"{os.path.join(DIR_TEX, FILE_NAME)}.tex"

load_dotenv()

def help() -> None:
    """
    Print the help message
    """

    print("Usage:")
    print("\tpython generate_resume.py [-h] [-s] [-q]")
    print("")
    print("Options:")
    print("\t-h, --help    Print this help message")
    print("\t-s, --skip    Skip regenerating the resumeitems.sty file. Render based on the cached version")
    print("\t-q, --quiet   Don't print the output of the latex compiler")
    print("")
    print("Exit codes:")
    print("\t0 - Program ran successfully")
    print("\t2 - Invalid arguments passed into the program")
    print("\t10 - Error connecting to database")
    print("\t11 - Error writing to file")

def get_arguments(argv: list[str]) -> dict[str, str]:
    """
    Gets the arguments passed into the program

    @param {list[str]} argv - The arguments passed into the program
    @returns {dict[str, str]} - A dictionary containing the arguments passed into the program
    """

    arguments = {}

    try:
        opts, args = getopt.getopt(argv, "hqs", ["help", "quiet", "skip"])

    except getopt.GetoptError:
        Logger.error("Invalid arguments passed into the program")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit(0)
        elif opt in ("-q", "--quiet"):
            arguments["quiet"] = arg
        elif opt in ("-s", "--skip"):
            arguments["skip"] = arg

    return arguments

PROGRAM_ARGS = get_arguments(sys.argv[1:])

class Connection:
    """
    A singleton class to handle the connection to the database
    """

    _self = None

    def __new__(cls):
        """
        Create a new instance of the class

        @returns {Connection} - The connection object

        @classmethod
        """
        
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        """
        Initialize the connection
        """
        
        try:
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
        except Exception as e:
            Logger.error(f"Error connecting to database:\n{e}")
            exit(10)

def process_query_data(query: str, data_shape: type) -> list[type]:
    """
    Process the data from a query into a list of objects based on the specified shape

    @params {string} query - The query to run
    @params {type} data_shape - The class to shape the data into
    @returns {list[type]} - A list of objects
    """

    cursor = Connection().connection.cursor()

    cursor.execute(query)
    data = cursor.fetchall()

    out = []
    for row in data:
        out.append(data_shape(row))
    
    return out

def query_work() -> list[Position]:
    """
    Get the work experience data
    
    @returns {list[Position]} - The work experience data
    """

    works = process_query_data("SELECT * FROM WorkExperience", WorkExperience)
    positions = process_query_data("SELECT * FROM Position", Position)    
    position_texts = process_query_data("SELECT * FROM PositionText", PositionText)

    # Create a join between the positions and relevant work/text objects
    for position in positions:
        
        # Join the work object to the position
        # TODO: Don't loop through everything every single time. Be better
        for work in works:
            if work.id == position.work_id:
                position.set_work(work)
                break
        
        # Join the text objects to the positions
        # TODO: Don't loop through everything every single time. Be better
        for position_text in position_texts:
            if position_text.position_id == position.id:
                position.add_text(position_text)
    
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

def get_data(query: callable, id: str, generator_func: callable) -> str:
    """
    Get the data from a query

    @params {callable} query - The query to run
    @params {str} id - The latex id to use
    @params {callable} generator_func - The function to generate the latex

    @returns {str} - The latex string
    """

    Logger.info(f"Running query: {query.__name__}")
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

    Logger.info("Generating tex string")

    latex_out = "\\NeedsTeXFormat{LaTeX2e}\n\\ProvidesPackage{resumeitems}[Maxim]\n\\usepackage{resumeassets}\n\n"

    latex_out += get_data(query_work, "workexperience", latex.work_experience)
    latex_out += get_data(query_education, "education", latex.education)

    latex_out = latex.escape_characters(latex_out)

    return latex_out

def compile_tex() -> None:
    """
    Compile the tex file
    """

    Logger.info("Compiling tex file")
    
    if "quiet" not in PROGRAM_ARGS:
        os.system(f"xelatex -output-directory {DIR_TEX} {FILE_TEX}")
    else:
        os.system(f"xelatex -output-directory {DIR_TEX} {FILE_TEX} > /dev/null")

    Logger.info("Finished compiling tex file")

def clean_files() -> None:
    """
    Clean the files in the tex directory
    """
    Logger.info("Removing excess files")

    extensions = ["aux", "log", "out", "glo", "xdy", "synctex.gz"]
    for extension in extensions:
        os.system(f"rm {os.path.join(DIR_TEX, FILE_NAME)}.{extension}")

    os.system(f"rm {os.path.join(DIR_TEX, 'texput')}.log")

def main() -> None:
    """
    The main function
    """
    
    if "skip" not in PROGRAM_ARGS:
        latex_out = generate_tex()

        try:
            with open(FILE_STY, "w") as file:
                file.write(latex_out)
        
        except Exception as e:
            Logger.error(f"Error writing to file:\n{e}")
            exit(11)
    
    compile_tex()

    #clean_files()

if __name__ == "__main__":
    Logger.init()
    Logger.header("Generating resume")

    main()