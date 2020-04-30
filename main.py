# scrapes the UWaterloo CS course offerings from the
# UWaterlo Undergrad Calendar (2020-21),
# and saves it to a csv file

import requests
from courseparser import Courses

if __name__ == '__main__':
    course_url = "http://www.ucalendar.uwaterloo.ca/2021/COURSE/course-CS.html"
    course_page = requests.get(course_url)

    courses = Courses(course_page.content)
    courses.save_to("cscourses.csv")

