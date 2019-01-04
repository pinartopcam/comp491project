import Preference as p, TeachingAssistant, Course
class Instructor:

    def __init__(self, id, name, course_list, advisee_list, department):
        self.id = id
        self.name = name
        self.courses = course_list
        self.students = advisee_list
        self.department = department
        self.preferences = []

    def createPreference(self, id, ta_id, course_id, rank):
        pref = p.Preference(id, ta_id, course_id, rank)
        self.preferences.append(pref)
