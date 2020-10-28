import gurobipy as gp
from gurobipy import *

def run_disjunctive(instance: str):
    """
    Solve a job shop scheduling problem (JSP) using a Mixed Integer Linear
    Programming (MILP) formulation built into GurobiPy module.

    Notes:
    1. Gurobi is an industrial solver for MILP, which I am using an academic
    license.

    Arguments:
        (str) instance - filename ("filename.txt") of standard JSP format\
        instance (see references)

    Returns:
        (tuple) solution - JSP solution in format (makespan, schedule) where\
        schedule is a dictionary in format:
            {job#:[ordered list of start time of each operation],...}

    Author:  Sugumar Prabhakaran
    Course:  MIE562 - Scheduling
    Professor: Dr. JC Beck
    Institution:  University of Toronto

    References:
    1. JSP format at link below:
        (http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/jobshop1.txt)
    """

    #LOAD INSTANCE DATA:
    with open(instance) as f:
        next(f)
        #n: # of jobs and m: # of machines in instance
        n, m = (int(item) for item in next(f).split())

        #create tasks list in list of jobs [job0:[task0,task1,...],...]
        #each task is a tuple of (machine k, processing time p)
        tasks = [[(int(line.split()[i]),int(line.split()[i+1]))
                for i in range(0,m*2,2)] for line in f]

    #CREATE PARAMETERS:
    Jobs = [job for job in range(n)]    #set of all jobs from 0 to n-1
    K = [k for k in range(m)]           #set of all machines from 0 to m-1

    #Create set of operations (J), where each operation will be a tuple:
    #(job,task) Note.  task and operation are equivalent terms
    J = [(job,task) for job in range(n) for task in range(m)]

    # dict p[j] to access processing time for each operation j
    p = {j:tasks[j[0]][j[1]][1] for j in J}

    #Some large constant we arbitrarily set = sum(all P_js)
    M = sum(p.values())

    #Sets of all operations on each machine k
    #Each list inside J_k is a list of operations for a respective resource
    J_k = [[] for _ in range(m)]
    for j in J:
            for k in K:
                if tasks[j[0]][j[1]][0]==k:
                    J_k[k].append((j))

    #Set of all precedence constraints
    #ie. all operation pairs (j,i) s.t. i is constrained to be after j
    Epsilon = [(J[i-1],j) for i,j in enumerate(J) if i > 0 if j[0] == J[i-1][0]]

    #A will be set of all possible operation combinations in each J_k
    A = [(j,i) for k in K for j in J_k[k] for i in J_k[k] if j !=i]

    #CREATE GUROBI MODEL
    model = gp.Model()
    model.params.TimeLimit = 180 #set time limit in seconds

    #CREATE DECISION VARIABLES
    S = model.addVars(J, vtype=GRB.INTEGER, name="S_j")  #start time of op j
    z = model.addVars(A, vtype=GRB.BINARY, name="Z_ji")  #if op j before i
    Cmax = model.addVar(vtype=GRB.INTEGER, name="C_max") #makespan

    #CREATE CONSTRAINTS
    #1. Makespan Constraints
    #Cmax must be largest end-time of any op j in set J (all operations)
    model.addConstrs(Cmax >= (S[j] + p[j]) for j in J);

    #2. Precedence Constraints
    #Start time of operation i must be greater than
    #End time of operation j for all (j,i) pairs in Epsilon
    #Epsilon is the set of all adjacent operation pairs in each job
    model.addConstrs(S[i]>=(S[j]+p[j]) for j,i in Epsilon);

    #3. & #4. Resource Constraints
    #for each operation pair (j,i) for each resource k, if j is before i
    #then Start time of i is greater than finish time of j
    #otherwise: Start time of j is greater than finish time of i
    model.addConstrs(S[j] >= (S[i] + p[i] - M * z[j,i]) for j, i in A);
    model.addConstrs(S[i] >= (S[j] + p[j] - M * (1-z[j,i])) for j,i in A);

    #5. Start time must be greater than 0
    model.addConstrs(S[j] >= 0 for j in J);

    #CREATE OBJECTIVE FUNCTION AND EXECUTE MODEL
    model.setObjective(Cmax, GRB.MINIMIZE);  #MINIMIZE Makespan (Cmax)
    model.optimize();

    #STORE SOLUTIONS
    makespan = int(model.Objval)
    schedule = {job:[int(S[j].x) for j in J if j[0]==job] for job in Jobs}
    solution = (makespan, schedule)
    print(solution)

    return solution

if __name__ == "__main__":
    instance = "./quercus_instances/selftest8.txt"

    run_disjunctive(instance)
