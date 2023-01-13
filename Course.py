import prettytable
import random
from typing import *

Gene = list
Schedule = list[Gene]


class Course:
    def __init__(self, attributes, teachers):
        self.code = attributes[0].strip()
        self.name = attributes[1]
        self.sections = int(attributes[2].strip("\n"))
        self.credit = int(attributes[0][5])
        self.year = int(attributes[0][4])
        self.type = "Lecture" if self.credit == 3 else "Lab"
        self.teachers = teachers

    def __str__(self):
        return " ".join([self.code, self.name, str(self.sections)])


lecture_slots = [("M", "W", "08:30 - 09:45"), ("S", "W", "08:30 - 09:45"), ("S", "M", "08:30 - 09:45"), ("T", "R", "08:30 - 09:45"),
                 ("M", "W", "10:00 - 11:15"), ("S", "W", "10:00 - 11:15"), ("S", "M", "10:00 - 11:15"), ("T", "R", "10:00 - 11:15"),
                 ("M", "W", "11:25 - 12:40"), ("S", "W", "11:25 - 12:40"), ("S", "M", "11:25 - 12:40"), ("T", "R", "11:25 - 12:40"),
                 ("M", "W", "12:50 - 14:05"), ("S", "W", "12:50 - 14:05"), ("S", "M", "12:50 - 14:05"), ("T", "R", "12:50 - 14:05")]
lab_slots = [("S", "08:30 - 11:10"), ("M", "08:30 - 11:10"), ("T", "08:30 - 11:10"), ("W", "08:30 - 11:10"), ("R", "08:30 - 11:10"),
             ("S", "11:25 - 14:05"), ("M", "11:25 - 14:05"), ("T", "11:25 - 14:05"), ("W", "11:25 - 14:05"), ("R", "11:25 - 14:05"),
             ("S", "14:15 - 16:55"), ("M", "14:15 - 16:55"), ("T", "14:15 - 16:55"), ("W", "14:15 - 16:55"), ("R", "14:15 - 16:55")]
courses = []
with open("data.txt", "r") as f:
    data = f.readlines()
    for course in data[1:]:
        line = course.split(";")
        line[3] = line[3].strip("\n")
        res = eval(line[3])
        courses.append(Course(line[:3], res))


def generate_chromosome() -> Schedule:
    schedule = []
    for course in courses:
        gene = [course.year, course.type]
        if course.type == "Lecture":
            sections = random.choices(lecture_slots, k=course.sections)
        else:
            sections = random.sample(lab_slots, k=course.sections)
        l = []
        for key, value in course.teachers.items():
            l.extend([key] * value)
        sections = list(map(list, zip(l, sections)))
        gene.append(sections)
        schedule.append(gene)
    return schedule


def print_schedule(schedule: Schedule) -> None:
    schedule = schedule.courses
    pt = prettytable.PrettyTable()
    pt.hrules = prettytable.ALL
    pt.add_autoindex = True
    pt.set_style(prettytable.DOUBLE_BORDER)
    pt.field_names = ["Course Code", "Course Name",
                    "# Sections", "Year", "Type", "Sections", "Time"]
    for i, course in enumerate(courses):
        sections = "\n".join([f"{slot[0]}" for slot in sorted(schedule[i][2], key=lambda x: x[1][0])])
        time = "\n".join([f"{slot[1][0]}, {slot[1][1]} : {slot[1][2]}" for slot in sorted(schedule[i][2], key=lambda x: x[1][0])] if course.type == "Lecture" else [f"{slot[1][0]} : {slot[1][1]}" for slot in sorted(schedule[i][2], key=lambda x: x[1][0])])
        # check_boxex = "\n".join(["<input type='checkbox' name='{}' value='{}'>".format((course.code,slot[0]),str(slot[1])) for slot in sorted(schedule[i][2], key=lambda x: x[1][0])])
        # check_boxex = "<div style='display: flex; flex-direction: column; justify-content: center; align-items: center;'>{}</div>".format(check_boxex)
        pt.add_row([course.code, course.name, course.sections,course.year, course.type, sections, time])
    pt.sortby = "Year"
    with open("templates/index.html", "w") as f:
        f.write("<html>")
        f.write("<head>")
        f.write("""
        <style>
        :root {
        --maincolor: #222831;
        --secondcolor: #393E46;
        --thirdcolor: #0078ab;
        --fourthcolor: #EEEEEE;
        }
        body {
        margin: 0;
        color: var(--fourthcolor);
        height: 100vh;
        background: var(--thirdcolor);
        font-family: 'Poppins', sans-serif;
        overflow-x: hidden;
        }
        table {
            font-family: Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }
        
        table td, table th {
            text-align: center;
            padding: 12px;
        }
        
        table tr:nth-child(even){background-color: var(--secondcolor);}
        table tr:nth-child(odd){background-color: var(--maincolor);}
        td:nth-child(5) {
            text-align: left;
        }
        td:nth-child(6) {
            text-align: left;
        }
        td:nth-child(7) {
            text-align: left;
        }
        table th {
            padding-top: 12px;
            padding-bottom: 12px;
            background-color: var(--thirdcolor);
            color: var(--fourthcolor);
        }
        </style>
        """)
        f.write("</head>")
        f.write("<body>")
        f.write("<div>")
        f.write(pt.get_html_string())
        f.write("</div>")
        f.write("</body>")
        f.write("</html>")
    # pt_year2 = prettytable.PrettyTable()
    # pt_year3 = prettytable.PrettyTable()
    # pt_year4 = prettytable.PrettyTable()
    # pt_year5 = prettytable.PrettyTable()
    # pt_year2_enee = prettytable.PrettyTable()
    # pt_year3_enee = prettytable.PrettyTable()
    # pt_year4_enee = prettytable.PrettyTable()
    # pt_year5_enee = prettytable.PrettyTable()
    # # add lines between rows
    # for pt in [pt_year2, pt_year3, pt_year4, pt_year5, pt_year2_enee, pt_year3_enee, pt_year4_enee, pt_year5_enee]:
    #     pt.hrules = prettytable.ALL
    #     pt.add_autoindex = True
    #     pt.set_style(prettytable.DOUBLE_BORDER)
    #     pt.field_names = ["Course Code", "Course Name",
    #                     "Sections", "Year", "Type", "Slots"]
    # pt = None
    # for i, course in enumerate(courses):
    #     if course.year == 2:
    #         if course.code[3] == "E":
    #             pt = pt_year2_enee
    #         else:
    #             pt = pt_year2
    #     if course.year == 3:
    #         if course.code[3] == "E":
    #             pt = pt_year3_enee
    #         else:
    #             pt = pt_year3
    #     if course.year == 4:
    #         if course.code[3] == "E":
    #             pt = pt_year4_enee
    #         else:
    #             pt = pt_year4
    #     if course.year == 5:
    #         if course.code[3] == "E":
    #             pt = pt_year5_enee
    #         else:
    #             pt = pt_year5
        
    #     slots = "\n".join([str(slot) for slot in sorted(
    #         schedule[i][2], key=lambda x: x[1][0])])
    #     pt.add_row([course.code, course.name, course.sections,
    #             course.year, course.type, slots])
    # with open("f.html", "w") as f:
    #     f.write("<html>")
    #     f.write("<head>")
    #     f.write("""
    #     <style>
    #     table {
    #       font-family: Arial, Helvetica, sans-serif;
    #       border-collapse: collapse;
    #       width: 100%;
    #     }
        
    #     table td, table th {
    #       border: 1px solid #ddd;
    #       padding: 8px;
    #     }
        
    #     table tr:nth-child(even){background-color: #f2f2f2;}
        
    #     table tr:hover {background-color: #ddd;}
        
    #     table th {
    #       padding-top: 12px;
    #       padding-bottom: 12px;
    #       text-align: left;
    #       background-color: #04AA6D;
    #       color: white;
    #     }
    #     </style>
    #     """)
    #     f.write("</head>")
    #     f.write("<body>")
    #     arr = [pt_year2, pt_year2_enee, pt_year3, pt_year3_enee, pt_year4, pt_year4_enee, pt_year5, pt_year5_enee]
    #     for i, table in enumerate(arr):
    #         f.write(f"<div id='table{i+1}'>")
    #         f.write(table.get_html_string())
    #         f.write("</div>")
    #     f.write("</body>")
    #     f.write("</html>")


class Chromosome:
    def __init__(self, courses_list: Schedule) -> None:
        # generate a new chromomse if no courses_list is given
        if courses_list is None:
            self.courses = generate_chromosome()
        else:
            self.courses = courses_list
        self.attributes = self.calc(self.courses)
        if self.attributes[0]:
            self.fitness = round(self.attributes[0], 4)
            self.teacher_slots = self.attributes[1]
            self.conflict_sum = self.attributes[2][0]
            self.early_penalty = self.attributes[2][2]
            self.late_penalty = self.attributes[2][3]
            self.saturday_penalty = self.attributes[2][4]
            self.sequenctial_pelanty = self.attributes[2][1]
        else:
            self.fitness = None

    def calc(self, schedule: Schedule) -> Tuple[float, dict, list[int]]:
        fitness = 0
        teacher_slots = {}
        lab_days = {}
        unique_slots = set()
        early_penalty = 0
        late_penalty = 0
        saturday_penalty = 0
        sequenctial_pelanty = 0
        conflicts = {2: {}, 3: {}, 4: {}, 5: {}}
        for course in schedule:
            local_lab_slots = {}  # For checking lab conflicts
            days_set = set()
            days_count = {}
            slots_set = set()
            for (teacher, slot) in course[2]:
                if teacher in teacher_slots:
                    if slot in teacher_slots[teacher]:
                        return None, 0, 0
                    else:
                        teacher_slots[teacher].append(slot)
                else:
                    teacher_slots[teacher] = [slot]
                if course[1] == "Lab":
                    if slot in local_lab_slots:
                        return None, 0, 0
                    else:
                        local_lab_slots[slot] = True
                if course[1] == "Lab":
                    days_set.add(slot[0])
                    slots_set.add(slot[1])
                    lab_days[slot[0]] = lab_days.get(slot[0], 0) + 1
                elif course[1] == "Lecture":
                    days_count[(slot[0],slot[1])] = days_count.get((slot[0],slot[1]), 0) + 1
                    days_set.add(slot[0])
                    days_set.add(slot[0])
                    slots_set.add(slot[2])
                    for i in range(len(course[2])):
                        for j in range(i+1, len(course[2])):
                            if abs(lecture_slots.index(course[2][i][1]) - lecture_slots.index(course[2][j][1])) % len(lecture_slots) == 4:
                                sequenctial_pelanty += 1
                if slot[-1] in ["08:30 - 9:45", "08:30 - 11:10"]:
                    early_penalty += 1
                if slot[-1] == "14:15 - 16:55":
                    late_penalty += 1
                if slot[0] == "S":
                    saturday_penalty += 1
                conflicts[course[0]][slot] = conflicts[course[0]].get(slot, 0) + 1
                unique_slots.add(slot)
                fitness = fitness + 15*(len(slots_set)+len(days_set))/len(course[2])
                if course[1] == "Lecture":
                    fitness = fitness - abs(1*days_count.get(("M", "W"), 0)+0.5*days_count.get(("S", "M"), 0)+0.5*days_count.get(("S", "W"), 0) - 2*days_count.get(("T", "R"),0))*10
        conflict_sum = 0
        for conflict in conflicts.values():
            for value in conflict.values():
                conflict_sum += value - 1
        fitness = fitness + (-1*early_penalty - 15*late_penalty - 12*saturday_penalty  - 20*conflict_sum)
        fitness *= (len(unique_slots)/(len(lecture_slots)+len(lab_slots)))
        fitness /= len(schedule)
        return fitness, teacher_slots, [conflict_sum, sequenctial_pelanty, early_penalty, late_penalty, saturday_penalty]
