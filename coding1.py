def load_data(instance):
    """
    Loads an instance into a dictionary for analysis

    Args:
        (str) instance - variable storing 'filename.txt'

    Returns:
        (int) jobs       - number of jobs 'j'
        (int) machines   - number of machines (resources - 'r')
        (int) tasks      - number of tasks total 'temp'
        (dict) task_data - hold for each job/task key: (j, t, rj, proc. time pj)
    """

    #read file with: instance = "filename.txt"
    with open(instance) as f:
        data = f.read().splitlines()

    print("Raw data:", data)

    #convert job rows into lists of form: [r1, p1, r2, p2, ...] for each task
    for i in range(2,len(data)):
        data[i] = data[i].split('  ')

    #convert row 1 into form: [job, machines]
    data[1] = data[1].split(' ')

    jobs = int(data[1][0])      #access 1st item in item 1 list
    machines = int(data[1][1])  #access 2nd item in item 1 list

    task_data = {}          #initialize dictionary to contain all master task data

    #loop through each job row
    for i in range(0,jobs):
        #loop through each pair in a row: (r1, p1), (r2, p2), ...
        for k in range(0,int(len(data[2])/2)):
            #create dict of format: {'job/task# key': (job, task, rj, pj) }
            task_data["j{}t{}".format(i,k)] = (i, k, data[i+2][2*k], data[i+2][2*k+1])

    tasks = len(task_data)  #number of tasks total

    print("# of jobs (j):", jobs)
    print("# of machines (r):", machines)
    print("# of tasks (t):", tasks)
    print("Task data format: {'key', (j, t, rj, pj)}")
    print("Task data:", task_data)

    return jobs, machines, tasks, task_data

def initialize_dicts(task_data):
    """
    Loads task data and create dicts with initial values (start state at time =0)
    for: unavailable tasks, resource queue, in-progress tasks, completed tasks

    Args:
        (str) instance - variable storing 'filename.txt'

    Returns:
        (dict) unavail_tasks  - tasks not able to start at time = 0
        (dict) resource_queue - tasks able to start at time = 0 for each rj
        (dict) ip_tasks       - tasks currently in-progress for each resource
        (dict) compl_tasks    - tasks completed
    """

    #initialize empty containers
    unavail_tasks = {} #tasks not avail to start (ie. predecessors not compl)
    res_queue = {}     #tasks avail. by resource (ie. no outstanding predecessors)
    ip_tasks = {}      #task in-progress for each resource
    compl_tasks = {}   #Initialize compl. list to compare if predecessor is done

    #loop through each task in task_data
    for key in task_data:
        #check if task is a task 0 (no predecessors)
        if task_data[key][1] == 0:

            # initialize dictionary key as 'r0', 'r1', ... etc.
            if "r{}".format(task_data[key][2]) not in res_queue:
                    res_queue["r{}".format(task_data[key][2])] = []

            # task 0s gets added to avail_list, organized by machine 'r'
            res_queue["r{}".format(task_data[key][2])].append(key)

        else:
            #if not a task 0, add to unavail_tasks
            unavail_tasks[key] = task_data[key]

    print("\nUnavailable List:", unavail_tasks)
    print("Resource Queue:", res_queue)
    print("In-progress Tasks:", ip_tasks)
    print("Compl. List:", compl_tasks)

    return unavail_tasks, res_queue, ip_tasks, compl_tasks

instance = "answer0.txt"

jobs, machines, tasks, task_data = load_data(instance)

time = 0

unavail_tasks, res_queue, ip_tasks, compl_tasks = initialize_dicts(task_data)
