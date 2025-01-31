import gurobipy as gp
from gurobipy import GRB

# Data (example values)
courses = ["C1", "C2", "C3", "C4", "C5", "CC1", "CC2", "CC3", "CC4"]
option_course = ["CC1", "CC2", "CC3", "CC4"] # Select two courses to complete (Elective)
semesters = [1, 2, 3]  # 3 semesters

credits = {"C1": 3, "C2": 4, "C3": 3, "C4": 3, "C5": 3, "CC1": 4, "CC2": 3, "CC3": 3, "CC4": 4}  # course credits
prereqs = {"C2": ["C1"], "C3": ["C1"], "C4": ["C2"], "C5": [], "CC1": ["C1", "C3"], "CC2": [], "CC3": ["C1"], "CC4": ["C2"]}  # course prerequisites
gpa = {"C1": 2, "C2": 4, "C3": 3, "C4": 3.8, "C5": 3.2, "CC1": 4, "CC2": 3.2, "CC3": 3.1, "CC4": 3.3} # course GPA from madgrades

# Maximum credits per semester
max_credits_per_semester = 18
min_credits_per_semester = 6 # For now, not enough courses yet to increase

# Initialize the model
model = gp.Model("CollegeCourseScheduling")

# Decision Variables
# x[i, t] = 1 if course i is taken in semester t
x = model.addVars(courses, semesters, vtype=GRB.BINARY, name="x")

# Grade variables (continuous between 0 and 4)
grades = model.addVars(courses, vtype=GRB.CONTINUOUS, lb=0, ub=4, name="grades")

# GPA calculation
total_credits_taken = model.addVar(vtype=GRB.CONTINUOUS, name="total_credits")
weighted_gpa_sum = model.addVar(vtype=GRB.CONTINUOUS, name="weighted_gpa")
lambda_var = model.addVar(vtype=GRB.CONTINUOUS, name="lambda", lb=0)

# Objective: Maximize the average GPA
# Sum of credits * grades, normalized by total credits taken
model.setObjective(weighted_gpa_sum * lambda_var, GRB.MAXIMIZE)

# Constraints
# Each required course must be taken exactly once in one of the semesters
model.addConstrs(gp.quicksum(x[i, t] for t in semesters) == 1 for i in courses if i not in option_course)

# Each optional course must be taken at most once
model.addConstrs(gp.quicksum(x[i, t] for t in semesters) <= 1 for i in option_course)

# Must take 2 option courses
model.addConstr(gp.quicksum(x[i, t] for t in semesters for i in option_course) == 2)

# Prerequisite constraints (if course j is a prerequisite of course i)
for i in courses:
    for prereq in prereqs.get(i, []):
        for t in semesters:
            model.addConstr(x[i, t] <= gp.quicksum(x[prereq, t_prime] for t_prime in semesters if t_prime < t))

# Credit load constraint (maximum credits per semester)
model.addConstrs(gp.quicksum(credits[i] * x[i, t] for i in courses) <= max_credits_per_semester for t in semesters)
model.addConstrs(gp.quicksum(credits[i] * x[i, t] for i in courses) >= min_credits_per_semester for t in semesters)

# Add GPA for each class as a constraint:
model.addConstrs(grades[i] == gpa[i] for i in courses)

# Constraint to calculate total credits taken
model.addConstr(total_credits_taken == gp.quicksum(credits[i] * gp.quicksum(x[i, t] for t in semesters) for i in courses))

# Constraint to calculate weighted GPA sum
model.addConstr(weighted_gpa_sum == gp.quicksum(credits[i] * grades[i] * gp.quicksum(x[i, t] for t in semesters) for i in courses))

# Scaling constraints to handle fractional objective function
model.addConstr(lambda_var * total_credits_taken == 1)  # Normalize division

# Solve the model
model.optimize()

# Output results
if model.status == GRB.OPTIMAL:
    print("Optimal Solution Found:")
    for i in courses:
        for t in semesters:
            if x[i, t].x > 0.5:  # course i is taken in semester t
                print(f"Course {i} is taken in semester {t} with grade {grades[i].x:.2f}")
else:
    print("No optimal solution found")

