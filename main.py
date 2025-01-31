import random
from data import REQ, COURSES

def check_prerequisites(course, completed_courses, courses_data):
    """Helper function to check if prerequisites are met for a course."""
    prerequisites = courses_data[course]["prerequisites"]
    return all(prerequisite in completed_courses for prerequisite in prerequisites)

def backtrack(selected_courses, completed_courses, req_data, courses_data, category_idx=0, credits_needed=0):
    if category_idx >= len(req_data):
        return selected_courses, sum(courses_data[course]["credits"] for course in selected_courses)
    
    category_name, category_data = list(req_data.items())[category_idx]
    
    if category_data["type"] == "required":
        for course in category_data["courses"]:
            if course not in completed_courses:
                selected_courses.append(course)
                completed_courses.add(course)
        result = backtrack(selected_courses, completed_courses, req_data, courses_data, category_idx + 1, credits_needed)
        if result:  # If solution found, return it
            return result

    elif category_data["type"] == "credit":
        total_credits_needed = category_data["amount"]
        credit_courses = category_data["courses"]
        total_credits_in_category = 0
        
        for course in credit_courses:
            if course not in completed_courses:
                selected_courses.append(course)
                completed_courses.add(course)
                total_credits_in_category += courses_data[course]["credits"]
                
                if total_credits_in_category >= total_credits_needed:
                    result = backtrack(selected_courses, completed_courses, req_data, courses_data, category_idx + 1, credits_needed)
                    if result:
                        return result
                selected_courses.remove(course)
                completed_courses.remove(course)

    elif category_data["type"] == "choose":
        available_courses = []
        for course in category_data["courses"]:
            if course not in completed_courses and check_prerequisites(course, completed_courses, courses_data):
                available_courses.append(course)
        
        available_courses = sorted(available_courses, key=lambda c: courses_data[c]["credits"], reverse=True)

        for course in available_courses:
            if course not in completed_courses:
                selected_courses.append(course)
                completed_courses.add(course)
                result = backtrack(selected_courses, completed_courses, req_data, courses_data, category_idx + 1, credits_needed)
                if result:
                    return result
                selected_courses.remove(course)
                completed_courses.remove(course)
        
    return None  # If no solution, return None

def generate_courses_for_graduation_backtrack(req_data, courses_data):
    selected_courses = []
    completed_courses = set()

    result = backtrack(selected_courses, completed_courses, req_data, courses_data)
    if result:
        selected_courses, total_credits = result
        return selected_courses, total_credits
    else:
        return [], 0  # Return empty if no solution

# Call the backtracking solver function
graduation_courses_backtrack, total_credits_backtrack = generate_courses_for_graduation_backtrack(REQ["Computer Science"], COURSES)

# Print the results
print(f"Selected courses for graduation (with backtracking): {graduation_courses_backtrack}")
print(f"Total credits: {total_credits_backtrack}")
