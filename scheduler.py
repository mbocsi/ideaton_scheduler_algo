from collections import deque
import random
from data import COURSES 

def topological_sort(courses):
    # Build adjacency list and in-degree count
    graph = {course: [] for course in courses}
    in_degree = {course: 0 for course in courses}
    
    prerequisites = []
    for c in courses:
        for r in courses[c]["prerequisites"]:
            prerequisites.append((r, c))
    
    for pre, course in prerequisites:
        graph[pre].append(course)
        in_degree[course] += 1
    
    # Find courses with no prerequisites
    queue = deque([course for course in courses if in_degree[course] == 0])
    order = []
    
    while queue:
        course = queue.popleft()
        order.append(course)
        
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) == len(courses):
        return order  # Valid topological order
    else:
        return []  # Cycle detected, invalid input

def generate_schedule(courses, prerequisites, electives, elective_prerequisites, elective_credits_required, min_credits=12, max_credits=18):
    all_courses = {**courses, **electives}
    all_prereq = prerequisites + elective_prerequisites
    order = deque(topological_sort(courses, prerequisites))
    if not order:
        return "Error: Cycle detected in prerequisites."
    
    schedule = []
    semester = []
    semester_credits = 0
    taken_courses = set()
    elective_credits_taken = 0
    
    while order or elective_credits_taken < elective_credits_required:
        print(elective_credits_taken)
        if order:
            course = order[0]
            credits = courses[course]
            prerequisites_met = all(pre in taken_courses for pre, c in prerequisites if c == course)
        else:
            print(electives)
            course, credits = random.choice(list(electives.items()))
            elective_credits_taken += credits
            prerequisites_met = True
            electives.pop(course)
        
        if not prerequisites_met:
            for c in semester:
                taken_courses.add(c)
            schedule.append(semester)
            semester = []
            semester_credits = 0
        
        if semester_credits + credits > max_credits:
            for c in semester:
                taken_courses.add(c)
            schedule.append(semester)
            semester = []
            semester_credits = 0
        
        semester.append(course)
        semester_credits += credits
        
        if course in courses:
            order.popleft()
    
    if semester:
        schedule.append(semester)
    
    return schedule

# schedule = generate_schedule(COURSES, PREREQUISITES, ELECTIVES, ELECTIVE_PREREQUISITES, 10)
# for i, sem in enumerate(schedule, 1):
#     print(f"Semester {i}: {', '.join(sem)}")

if __name__ == "__main__":
    courses = topological_sort(COURSES)
    print(courses)