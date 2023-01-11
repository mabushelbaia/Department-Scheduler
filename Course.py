import prettytable
from random import random
from typing import *


Gene = list
Schedule = list[Gene]
class Course:
    def __init__(self, attributes, teachers):
        self.code = attributes[0].strip()
        self.name = attributes[1]
        self.sections = int(attributes[2].strip("\n"))
        self.credit = int(attributes[0][5])
        self.year   = int(attributes[0][4])
        self.type = "Lecture" if self.credit == 3 else "Lab"
        teachers = teachers
    def __str__(self):
        return " ".join([self.code, self.name, str(self.sections)])

lecture_slots = [("M", "W", "08:30 - 9:45"),("S", "W", "08:30 - 09:45"), ("S", "M", "08:30 - 09:45"), ("T", "R", "08:30 - 09:45"),
                ("M", "W", "10:00 - 11:15"),("S", "W", "10:00 - 11:15"), ("S", "M", "10:00 - 11:15"), ("T", "R", "10:00 - 11:15"),
                ("M", "W", "11:25 - 12:40"),("S", "W", "11:25 - 12:40"), ("S", "M", "11:25 - 12:40"), ("T", "R", "11:25 - 12:40"),
                ("M", "W", "12:50 - 14:05"),("S", "W", "12:50 - 14:05"), ("S", "M", "12:50 - 14:05"), ("T", "R", "12:50 - 14:05")]
lab_slots = [("S", "08:30 - 11:10"), ("M", "08:30 - 11:10"), ("T", "08:30 - 11:10"), ("W", "8:30 - 11:10"),("R", "08:30 - 11:10"),
             ("S", "11:25 - 14:05"), ("M", "11:25 - 14:05"), ("T", "11:25 - 14:05"), ("W", "11:25 - 14:05"),("R", "11:25 - 14:05"),
             ("S", "14:15 - 16:55"), ("M", "14:15 - 16:55"), ("T", "14:15 - 16:55"), ("W", "14:15 - 16:55"),("R", "14:15 - 16:55")]
courses = []
with open("data.txt", "r") as f:
    data = f.readlines()
    for course in data[1:]:
        line = course.split(";")
        line[3] = line[3].strip("\n")
        res = eval(line[3])
        courses.append(Course(line[:3], res))
def print_schedule(schedule: Schedule) -> None:
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

class Chromosome:
    def __init__(self, courses_list: Schedule) -> None:
        # generate a new chromomse if no courses_list is given
        if courses_list is None:
            self.courses = self.generate_chromosome(courses)
        else:
            courses = courses_list
        self.attributes = self.calc(courses)
        self.fitness = self.attributes[0]
        self.teacher_slots = self.attributes[1]     
        self.conflict_sum = self.attributes[2][0]
        self.early_penalty = self.attributes[2][2]
        self.late_penalty = self.attributes[2][3]
        self.saturday_penalty = self.attributes[2][4]
        self.sequenctial_pelanty = self.attributes[2][1]

    def generate_chromosome(self,courses: list[Course]) -> Schedule:
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

    def calc(self,schedule: Schedule) -> Tuple[float, dict, list[int]]:
        fitness = 0
        teacher_slots = {}
        unique_slots = set()          
        early_penalty = 0
        late_penalty = 0
        saturday_penalty = 0
        sequenctial_pelanty = 0
        conflicts = {2: {}, 3: {}, 4: {}, 5: {}}
        for course in schedule:
            local_lab_slots = {} # For checking lab conflicts
            local_days = {} 
            local_slots = set()
            for (teacher, slot) in course[2]:
                if teacher in teacher_slots:
                    if slot in teacher_slots[teacher]:
                        return 0, 0, 0
                    else:
                        teacher_slots[teacher].append(slot)
                else:
                    teacher_slots[teacher] = [slot]
                if course[1] == "Lab":
                    if slot in local_lab_slots:
                        return 0, 0, 0
                    else:
                        local_lab_slots[slot] = True
                if course[1] == "Lab":
                    local_days[slot[0]] = local_days.get(slot[0], 0) + 1
                elif course[1] == "Lecture":
                    local_days[slot[0]] = local_days.get(slot[0], 0) + 1
                    local_days[slot[1]] = local_days.get(slot[1], 0) + 1
                    for i in range(len(course[2])):
                        for j in range(i+1, len(course[2])):
                            if abs(lecture_slots.index(course[2][i][1]) - lecture_slots.index(course[2][j][1]))%len(lecture_slots) == 4: # 2 Slots together
                                sequenctial_pelanty += 1
                if slot[-1] in ["08:30 - 9:45", "08:30 - 11:10"]:
                        early_penalty += 1
                if slot[-1] == "14:15 - 16:55":
                    late_penalty += 1
                if slot[0] == "S":
                    saturday_penalty += 1
                conflicts[course[0]][slot] = conflicts[course[0]].get(slot, 0) + 1
                local_slots.add(slot)
                unique_slots.add(slot)
            fitness += 2*len(local_slots) / len(course[2]) # How many slots does a course cover relative to it section count
            fitness += 3*len(local_days) / len(course[2])  # How many days does a course cover relative to it section count
        conflict_sum = 0
        for conflict in conflicts.values():
            for value in conflict.values():
                conflict_sum += value - 1
        fitness -= (2*early_penalty + 1*late_penalty + 4*saturday_penalty + 0.5*sequenctial_pelanty+ 5*conflict_sum)
        ratio = len(unique_slots) / len(lab_slots + lecture_slots)
        fitness *= ratio
        return fitness, teacher_slots, [conflict_sum, sequenctial_pelanty, early_penalty, late_penalty, saturday_penalty]