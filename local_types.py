"""
This file contains the classes that are used to represent the data in the database.

TODO: Replace with prisma schema
"""

class WorkExperience:
    def __init__(self, data: tuple) -> None:
        self.id = data[0]
        self.organisation = data[1]
        self.logo = data[2]
        self.hidden = bool(data[3])
        self.order = data[4]

class PositionText:
    def __init__(self, data: tuple) -> None:
        self.id = data[0]
        self.text = data[1]
        self.position_id = data[2]
        self.order = data[3]

class Position:
    def __init__(self, data: tuple) -> None:
        self.id = data[0]
        self.title = data[1]
        self.department = data[2]
        self.start = data[3]
        self.end = data[4]
        self.hidden = bool(data[5])
        self.work_id = data[6]

        self.text = []

        if self.end == None:
            self.end = "Current"

    def set_work(self, work: WorkExperience) -> None:
        self.work = work

    def add_text(self, text: PositionText) -> None:
        self.text.append(text)

        # TODO: Don't do this every time. This assumes that the sort algorithm is fast and that there isn't much data. Not safe
        self.sort_text()

    def sort_text(self) -> None:
        self.text = sorted(self.text, key=lambda x: x.order, reverse=False)

class Education:
    def __init__(self, data: tuple) -> None:
        self.id = data[0]
        self.title = data[1]
        self.organisation = data[2]
        self.logo = data[3]
        self.start = data[4]
        self.end = data[5]
        self.description = data[6]
        self.hidden = bool(data[7])

        if self.end == "":
            self.end = "Current"