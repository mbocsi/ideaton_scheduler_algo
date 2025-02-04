REQ = {
    "Computer Science": {
        "Art": {"courses" : ["ART101", "MUSIC101", "ART102", "ART201", "ART202", "ART240", "MUSIC102"], "type": "credit", "amount": 15},
        "Basic Computer Science": {"courses": ["CS240", "CS300", "CS400", "CS252", "CS354"], "type": "required"},
        "Basic Calculus": {"courses": ["MATH221", "MATH222"], "type":"required"},
        "Linear Algebra": {"courses": ["MATH320", "MATH340", "MATH341", "MATH375"], "type": "choose", "amount": 1},
        "Software and Hardware": {"courses": ["CS407", "CS506", "CS536", "CS537", "CS542", "CS544", "CS552", "CS564", "CS640", "CS642"], "type":"choose", "amount": 2},
        "Applications": {"courses": [ "CS412", "CS425", "CS513", "CS514", "CS524", "CS525", "CS534", "CS540", "CS541", "CS559", "CS565", "CS566", "CS570", "CS571"], "type": "choose", "amount": 1},
        "Electives": {"courses": [
            "CS407", "CS412", "CS425", "CS435", "CS471", "CS475", "CS506", "CS513", "CS514", 
            "CS518", "CS520", "CS524", "CS525", "CS526", "CS532", "CS533", "CS534", "CS536", 
            "CS537", "CS538", "CS539", "CS540", "CS541", "CS542", "CS544", "CS552", "CS558", 
            "CS559", "CS561", "CS564", "CS565", "CS566", "CS567", "CS570", "CS571", "CS576", 
            "CS577", "CS579", "CS620", "CS635", "CS640", "CS642", "CS639"
        ], "type": "choose", "amount": 2},
    }
}
COURSES = {
    "ART101": {"credits": 4, "prerequisites": []},
    "MUSIC101": {"credits": 4, "prerequisites": []},
    "ART102": {"credits": 4, "prerequisites": ["ART101"]},
    "ART201": {"credits": 4, "prerequisites": []},
    "ART202": {"credits": 4, "prerequisites": ["ART201"]},
    "ART240": {"credits": 3, "prerequisites": ["ART102"]},
    "MUSIC102": {"credits": 4, "prerequisites": ["MUSIC101"]},
    "CS240": {"credits": 3, "prerequisites": ["MATH221"]},
    "CS300": {"credits": 3, "prerequisites": []},
    "CS400": {"credits": 3, "prerequisites": ["CS300"]},
    "CS252": {"credits": 3, "prerequisites": []},
    "CS352": {"credits": 3, "prerequisites": ["CS252"]},
    "CS354": {"credits": 3, "prerequisites": ["CS400"]},
    "MATH221": {"credits": 3, "prerequisites": []},
    "MATH222": {"credits": 3, "prerequisites": ["MATH221"]},
    "MATH234": {"credits": 3, "prerequisites": ["MATH222"]},
    "MATH320": {"credits": 3, "prerequisites": ["MATH222"]},
    "MATH340": {"credits": 3, "prerequisites": ["MATH222"]},
    "MATH341": {"credits": 3, "prerequisites": ["MATH234"]},
    "MATH375": {"credits": 5, "prerequisites": ["MATH234"]},
    "CS407": {"credits": 4, "prerequisites": ["CS400"]},
    "CS506": {"credits": 3, "prerequisites": ["CS400", "CS564"]},
    "CS536": {"credits": 3, "prerequisites": ["CS400", "CS354"]},
    "CS537": {"credits": 4, "prerequisites": ["CS400", "CS354"]},
    "CS542": {"credits": 3, "prerequisites": ["CS400"]},
    "CS544": {"credits": 3, "prerequisites": ["CS400"]},
    "CS552": {"credits": 3, "prerequisites": ["CS352", "CS354"]},
    "CS564": {"credits": 4, "prerequisites": ["CS400", "CS354"]},
    "CS640": {"credits": 3, "prerequisites": ["CS537"]},
    "CS642": {"credits": 3, "prerequisites": ["CS537"]},
    "CS412": {"credits": 3, "prerequisites": ["MATH222", "CS240", "CS300"]},
    "CS425": {"credits": 3, "prerequisites": ["MATH340", "CS300"]},
    "CS513": {"credits": 3, "prerequisites": ["MATH340"]},
    "CS514": {"credits": 3, "prerequisites": ["MATH340", "CS300"]},
    "CS524": {"credits": 3, "prerequisites": ["CS300", "MATH340"]},
    "CS525": {"credits": 3, "prerequisites": ["MATH340"]},
    "CS534": {"credits": 3, "prerequisites": ["CS300", "MATH221"]},
    "CS540": {"credits": 3, "prerequisites": ["CS300", "MATH221"]},
    "CS541": {"credits": 3, "prerequisites": ["MATH340"]},
    "CS559": {"credits": 3, "prerequisites": ["CS400", "MATH222"]},
    "CS565": {"credits": 3, "prerequisites": ["CS400"]},
    "CS566": {"credits": 3, "prerequisites": ["CS400", "MATH340"]},
    "CS570": {"credits": 3, "prerequisites": []},
    "CS571": {"credits": 3, "prerequisites": ["CS400"]},
    "CS435": {"credits": 3, "prerequisites": ["MATH340"]},
    "CS471": {"credits": 3, "prerequisites": ["MATH340"]},
    "CS475": {"credits": 3, "prerequisites": ["MATH340"]},
    "CS518": {"credits": 3, "prerequisites": []},
    "CS520": {"credits": 3, "prerequisites": ["CS240", "CS300"]},
    "CS526": {"credits": 3, "prerequisites": ["CS525", "CS300"]},
    "CS532": {"credits": 3, "prerequisites": ["MATH234", "CS300"]},
    "CS533": {"credits": 3, "prerequisites": ["MATH340"]},
    "CS534": {"credits": 3, "prerequisites": ["CS300", "MATH221"]},
    "CS538": {"credits": 3, "prerequisites": ["CS354", "CS400"]},
    "CS539": {"credits": 3, "prerequisites": ["CS300"]},
    "CS542": {"credits": 3, "prerequisites": ["CS400"]},
    "CS544": {"credits": 3, "prerequisites": ["CS400"]},
    "CS558": {"credits": 3, "prerequisites": ["CS400", "MATH234"]},
    "CS561": {"credits": 3, "prerequisites": ["MATH340"]},
    "CS567": {"credits": 3, "prerequisites": ["MATH340"]},
    "CS576": {"credits": 3, "prerequisites": ["CS400", "MATH222"]},
    "CS577": {"credits": 4, "prerequisites": ["CS240", "CS400"]},
    "CS579": {"credits": 3, "prerequisites": []},
    "CS620": {"credits": 3, "prerequisites": ["CS400"]},
    "CS635": {"credits": 3, "prerequisites": ["MATH340", "CS300"]},
    "CS639": {"credits": 3, "prerequisites": []},
}

import random
random.seed(42)

import re
def ecn(course_code):
    match = re.search(r'\d+', course_code)
    return match.group() if match else None

for course_code, course_info in COURSES.items():
    course_info["gpa"] = round(random.uniform(3.0 - float(ecn(course_code)) / 1000, 4.0 - float(ecn(course_code)) / 1000), 2)