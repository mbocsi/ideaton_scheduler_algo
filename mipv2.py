import gurobipy as gp
from gurobipy import GRB
from data import REQ, COURSES

# Extract courses, prerequisites, and credits dynamically
courses = list(COURSES.keys())
prereqs = {course: COURSES[course]["prerequisites"] for course in courses}
gpa = {course: COURSES[course]["gpa"] for course in courses}
print(gpa)
credits = {course: COURSES[course]["credits"] for course in courses}

def get_required_courses():
    required, optional, required_count = [], [], {}
    for category, details in REQ["Computer Science"].items():
        if details["type"] == "required":
            required.extend(details["courses"])
        elif details["type"] == "choose":
            optional.extend(details["courses"])
            required_count[category] = details["amount"]
    return required, optional, required_count

required_courses, optional_courses, opt_requirements = get_required_courses()

print(required_courses)
print(optional_courses)

semesters = list(range(1, 9))  # Assuming 8 semesters max
max_credits_per_semester = 18
min_credits_per_semester = 12

model = gp.Model("CollegeCourseScheduling")

# Decision variables
x = model.addVars(courses, semesters, vtype=GRB.BINARY, name="x")

def add_schedule_constraints():
    # Required courses must be taken exactly once
    model.addConstrs(gp.quicksum(x[i, t] for t in semesters) == 1 for i in required_courses)
    
    # Optional courses constraints
    for category, amount in opt_requirements.items():
        model.addConstr(gp.quicksum(x[i, t] for t in semesters for i in REQ["Computer Science"][category]["courses"]) >= amount)
    
    # Optional courses must be taken at most once
    model.addConstrs(gp.quicksum(x[i, t] for t in semesters) <= 1 for i in courses if i not in required_courses)
    
    # Prerequisites enforcement
    for i in courses:
        for prereq in prereqs.get(i, []):
            for t in semesters:
                model.addConstr(x[i, t] <= gp.quicksum(x[prereq, t_prime] for t_prime in semesters if t_prime < t))
    
    # Credit load constraints per semester
    model.addConstrs(gp.quicksum(credits[i] * x[i, t] for i in courses) <= max_credits_per_semester for t in semesters)
    model.addConstrs(gp.quicksum(credits[i] * x[i, t] for i in courses) >= min_credits_per_semester for t in semesters)

def add_gpa_constraints():
   # Grade variables (continuous between 0 and 4)
    grades = model.addVars(courses, vtype=GRB.CONTINUOUS, lb=0, ub=4, name="grades")

    # GPA calculation
    total_credits_taken = model.addVar(vtype=GRB.CONTINUOUS, name="total_credits")
    weighted_gpa_sum = model.addVar(vtype=GRB.CONTINUOUS, name="weighted_gpa")
    lambda_var = model.addVar(vtype=GRB.CONTINUOUS, name="lambda", lb=0)

    model.setObjective(weighted_gpa_sum * lambda_var, GRB.MAXIMIZE) 
    
    # Add GPA for each class as a constraint:
    model.addConstrs(grades[i] == gpa[i] for i in courses)

    # Constraint to calculate total credits taken
    model.addConstr(total_credits_taken == gp.quicksum(credits[i] * gp.quicksum(x[i, t] for t in semesters) for i in courses))

    # Constraint to calculate weighted GPA sum
    model.addConstr(weighted_gpa_sum == gp.quicksum(credits[i] * grades[i] * gp.quicksum(x[i, t] for t in semesters) for i in courses))

    # Scaling constraints to handle fractional objective function
    model.addConstr(lambda_var * total_credits_taken == 1)  # Normalize division

add_schedule_constraints()
add_gpa_constraints()

# Solve the model
model.optimize()
    
# Output results
if model.status == GRB.OPTIMAL:
    print("Optimal Solution Found:")
    semester_schedule = {t: [] for t in semesters}
    for i in courses:
        for t in semesters:
            if x[i, t].x > 0.5:
                semester_schedule[t].append(i)
    
    for t in sorted(semester_schedule.keys()):
        if semester_schedule[t]:
            print(f"Semester {t}: {', '.join(semester_schedule[t])}")
else:
    print("No optimal solution found")