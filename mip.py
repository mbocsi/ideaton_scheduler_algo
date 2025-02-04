import gurobipy as gp
from gurobipy import GRB
from database import REQ, COURSES

class MIP:
    def __init__(self, major, college, optimize="gpa", semesters=8, min_credits=12, max_credits=18):
        self.model = gp.Model("CollegeCourseScheduling")
        # self.model.setParam('OptimalityTol', 1e-2)
        self.model.setParam('MIPGap', 1e-2) # Reduce bound gap required to finish optimization
        
        self.courses, self.prereqs, self.gpa, self.credits = self.fetch_courses()
        self.required_courses, self.optional_courses, self.opt_requirements = self.fetch_requirements(major, college)
        self.semesters = list(range(1, semesters+1))
        
        #=============== Schedule constraints ==============
        
        self.x = self.model.addVars(self.courses, self.semesters, vtype=GRB.BINARY, name="x") 
        # Could try to limit domain of courses to only those relevant to the major
        
        self.add_schedule_constraints(min_credits, max_credits)
        
        #================ GPA constraints =================
        self.grades = self.model.addVars(self.courses, vtype=GRB.CONTINUOUS, lb=0, ub=4, name="grades")

        # GPA calculation
        self.total_credits_taken = self.model.addVar(vtype=GRB.CONTINUOUS, name="total_credits")
        self.weighted_gpa_sum = self.model.addVar(vtype=GRB.CONTINUOUS, name="weighted_gpa")
        self.lambda_var = self.model.addVar(vtype=GRB.CONTINUOUS, name="lambda", lb=0)
        
        self.add_gpa_constraints()
        
    
    def fetch_courses(self):
        courses = list(COURSES.keys())
        prereqs = {course: COURSES[course]["prerequisites"] for course in courses}
        gpa = {course: COURSES[course]["gpa"] for course in courses}
        credits = {course: COURSES[course]["credits"] for course in courses}
        
        return courses, prereqs, gpa, credits
    
    def fetch_requirements(self, major, college):
        required, optional, required_count = [], [], {}
        for category, details in REQ[major].items():
            if details["type"] == "required":
                required.extend(details["courses"])
            elif details["type"] == "choose":
                optional.extend(details["courses"])
                required_count[category] = details["amount"]
        return required, optional, required_count
    
    def add_schedule_constraints(self, min_credits_per_semester, max_credits_per_semester):
        # Required courses must be taken exactly once
        self.model.addConstrs(gp.quicksum(self.x[i, t] for t in self.semesters) == 1 for i in self.required_courses)
        
        # Optional courses constraints
        for category, amount in self.opt_requirements.items():
            self.model.addConstr(gp.quicksum(self.x[i, t] for t in self.semesters for i in REQ["Computer Science"][category]["courses"]) >= amount)
        
        # Optional courses must be taken at most once
        self.model.addConstrs(gp.quicksum(self.x[i, t] for t in self.semesters) <= 1 for i in self.courses if i not in self.required_courses)
        
        # Prerequisites enforcement
        for i in self.courses:
            for prereq in self.prereqs.get(i, []):
                for t in self.semesters:
                    self.model.addConstr(self.x[i, t] <= gp.quicksum(self.x[prereq, t_prime] for t_prime in self.semesters if t_prime < t))
        
        # Credit load constraints per semester
        self.model.addConstrs(gp.quicksum(self.credits[i] * self.x[i, t] for i in self.courses) <= max_credits_per_semester for t in self.semesters)
        self.model.addConstrs(gp.quicksum(self.credits[i] * self.x[i, t] for i in self.courses) >= min_credits_per_semester for t in self.semesters)

    def add_gpa_constraints(self):
        self.model.setObjective(self.weighted_gpa_sum * self.lambda_var, GRB.MAXIMIZE) 
        
        # Add GPA for each class as a constraint:
        self.model.addConstrs(self.grades[i] == self.gpa[i] for i in self.courses)

        # Constraint to calculate total credits taken
        self.model.addConstr(self.total_credits_taken == gp.quicksum(self.credits[i] * gp.quicksum(self.x[i, t] for t in self.semesters) for i in self.courses))

        # Constraint to calculate weighted GPA sum
        self.model.addConstr(self.weighted_gpa_sum == gp.quicksum(self.credits[i] * self.grades[i] * gp.quicksum(self.x[i, t] for t in self.semesters) for i in self.courses))

        # Scaling constraints to handle fractional objective function
        self.model.addConstr(self.lambda_var * self.total_credits_taken == 1)  # Normalize division
    
    def run(self):
        self.model.optimize()
        if self.model.status == GRB.OPTIMAL:
            print("Optimal Solution Found:")
            semester_schedule = {t: [] for t in self.semesters}
            for i in self.courses:
                for t in self.semesters:
                    if self.x[i, t].x > 0.5:
                        semester_schedule[t].append({"code": i, "GPA": self.gpa[i], "credits": self.credits[i]})
            return {"Average GPA": self.model.ObjVal, "semesters": semester_schedule} 
        else:
            print("No optimal solution found")