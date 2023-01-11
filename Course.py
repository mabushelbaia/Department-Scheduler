import prettytable

Chromosome = list
class Course:
    def __init__(self, attributes, teachers):
        self.code = attributes[0].strip()
        self.name = attributes[1]
        self.sections = int(attributes[2].strip("\n"))
        self.credit = int(attributes[0][5])
        self.year   = int(attributes[0][4])
        self.type = "Lecture" if self.credit == 3 else "Lab"
        self.teachers = teachers
    def __str__(self):
        return " ".join([self.code, self.name, str(self.sections)])

lecture_slots = [("M", "W", "08:30 - 9:45"),("S", "W", "08:30 - 09:45"), ("S", "M", "08:30 - 09:45"), ("T", "R", "08:30 - 09:45"),
                ("M", "W", "10:00 - 11:15"),("S", "W", "10:00 - 11:15"), ("S", "M", "10:00 - 11:15"), ("T", "R", "10:00 - 11:15"),
                ("M", "W", "11:25 - 12:40"),("S", "W", "11:25 - 12:40"), ("S", "M", "11:25 - 12:40"), ("T", "R", "11:25 - 12:40"),
                ("M", "W", "12:50 - 14:05"),("S", "W", "12:50 - 14:05"), ("S", "M", "12:50 - 14:05"), ("T", "R", "12:50 - 14:05")]
lab_slots = [("S", "08:30 - 11:10"), ("M", "08:30 - 11:10"), ("T", "08:30 - 11:10"), ("W", "8:30 - 11:10"),("R", "08:30 - 11:10"),
             ("S", "11:25 - 14:05"), ("M", "11:25 - 14:05"), ("T", "11:25 - 14:05"), ("W", "11:25 - 14:05"),("R", "11:25 - 14:05"),
             ("S", "14:15 - 16:55"), ("M", "14:15 - 16:55"), ("T", "14:15 - 16:55"), ("W", "14:15 - 16:55"),("R", "14:15 - 16:55")]
# Tem
courses = []
with open("data.txt", "r") as f:
    data = f.readlines()
    for course in data[1:]:
        line = course.split(";")
        line[3] = line[3].strip("\n")
        res = eval(line[3])
        courses.append(Course(line[:3], res))
def print_schedule(schedule: Chromosome) -> None:
    pt = prettytable.PrettyTable()
    # add lines between rows
    pt.hrules = prettytable.ALL
    pt.add_autoindex = True
    pt.set_style(prettytable.DOUBLE_BORDER)
    pt.field_names = ["Course Code", "Course Name", "Sections", "Year", "Type", "Slots"]
    for i, course in enumerate(courses):
        slots = "\n".join([str(slot) for slot in sorted(schedule[i][2], key=lambda x: x[1][0])])
        pt.add_row([course.code, course.name, course.sections, course.year, course.type, slots])
    pt.sortby = "Year"
    print(pt)
