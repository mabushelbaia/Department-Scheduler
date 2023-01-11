from bs4 import BeautifulSoup
import re 
class Course:
    def __init__(self, attributes, teachers):
        self.code = attributes[0]
        self.name = attributes[1]
        self.sections = attributes[2]
        self.credit = attributes[0][5]
        self.year   = attributes[0][4]
        self.teachers = teachers
    def __str__(self):
        return [self.code, self.name, str(self.sections), self.teachers]
with open('index.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')
tables = soup.find_all(lambda tag: tag.name=='table' and tag.has_attr('style') and tag['style']=="padding:0.4em;")
tables = tables[1:]
my_courses = []
for table in tables:
    teachers = {}
    rows = table.find_all('tr')
    rows = rows[:2]
    labels = rows[0].find_all('td')
    labels = [ele.text.strip() for ele in labels]
    labels = [ele for ele in labels if ele]
    db = []
    rows_2 = rows[1].find_all('tr')
    for i, row in enumerate(rows_2[1:]):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols if ele.text.strip()]
        if cols[0] in ["Lecture", "Lab"]:
            teachers[cols[2]] = teachers.get(cols[2], 0) + 1
        db.append(cols)
    sections = len(db)//2
    if labels[0][5] != '1' and labels[0][5] != '3':
        continue
    my_courses.append(Course([labels[0], labels[2], sections], teachers))
print(len(my_courses))
print("course_code", "course_name", "sections", sep=";")
for course in my_courses:
    print(*course.__str__(), sep=';')