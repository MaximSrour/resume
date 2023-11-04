class WorkExperience:
    def __init__(self, data):
        self.id = data[0]
        self.organisation = data[1]
        self.logo = data[2]
        self.hidden = bool(data[3])
        self.order = data[4]

class PositionText:
    def __init__(self, data):
        self.id = data[0]
        self.text = data[1]
        self.position_id = data[2]
        self.order = data[3]

class Position:
    def __init__(self, data):
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

    def set_work(self, work: WorkExperience):
        self.work = work

    def add_text(self, text: PositionText):
        self.text.append(text)

class Education:
    def __init__(self, data):
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