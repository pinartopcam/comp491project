import TeachingAssistant, Instructor
class Course:

    def __init__(self, id, name, department, instructor, ta_need):
        self.id = id
        self.name = name
        self.department = department
        self.instructor = instructor
        self.ta_need = ta_need
        self.assigned_tas = []