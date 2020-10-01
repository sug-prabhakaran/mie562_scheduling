def load_data(instance):
    """
    Loads an instance into a dictionary for analysis

    Args:
        (str) instance - variable storing 'filename.txt'

    Returns:
        (int) jobs       - number of jobs
        (int) machines   - number of machines (resources)
        (int) tasks      - number of tasks total
        (dict) task_data - hold for each job/task key: (job, task, machine, processing time)
    """

    #read file with: instance = "filename.txt"
    with open(instance) as f:
        data = f.read().splitlines()

    #convert job rows into lists of form: [r1, p1, r2, p2, ...] for each task
    for i in range(2,len(data)):
        data[i] = data[i].split('  ')

    #convert row 1 into form: [job, machines]
    data[1] = data[1].split('  ')

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

    return jobs, machines, tasks, task_data

def initialize_dicts(task_data):
    """
    Loads task data and create dicts with initial values (start state at time =0)
    for: unavailable tasks, resource queue, in-progress tasks, completed tasks

    Args:
        (dict) task_data      - contains master task data

    Returns:
        (dict) unavail_tasks - tasks not able to start at time = 0
        (dict) res_queue     - tasks able to start at time = 0 for each rj
    """

    #initialize empty containers
    unavail_tasks = {} #tasks not avail to start (ie. predecessors not compl)
    res_queue = {}     #tasks avail. by resource (ie. no outstanding predecessors)

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

    return unavail_tasks, res_queue

def machine_activate(time, task_data, res_queue, ip_tasks):
    """
    identifies Shortest Processing Time (SPT) task in resource queue for each
    resource and activates it into In-Progress

    Args:
        (dict) task_data - contains master task data
        (dict) res_queue - contains task queue for each resource
        (dict) ip_tasks  - contains current tasks in progress

    Returns:
        (dict) res_queue - updated resource queue
        (dict) ip_tasks  - updated with activated tasks
    """

    # loop through each resource (r0, r1, ...) in resource queue
    for key in res_queue.copy():
        #first check if resource currently has a task in-progress
        if key in ip_tasks != []:
            #resource not free (task in-progress) so skip to next key = 'rj'
            continue

        #if resource is free:
        else:
            min_key = []    #will store list of pjs for each task in res_que[key]

            #check if we have a list of tasks
            if len(res_queue[key]) == 0:
                #no tasks in our list so we skip to next key = 'rj'
                continue

            #if list has only 1 item, it is automatically min_key
            elif len(res_queue[key]) == 1:
                #set min_key to list item value
                min_key = [res_queue[key][0]]

            #if list is not 0 or 1, must have value > 1. Must find min.
            else:
                min_dict = {}   #initialize.  Will be used to determine min pj task
                # loop through each task in res_queue task list
                for i in range(len(res_queue[key])):
                    #add job/task key + pj to min_dict so we can compare them
                    min_dict[res_queue[key][i]] = task_data[res_queue[key][i]][3]

                # find the minimum pj task for resoure r:
                temp = min(min_dict.values())
                #find the key(s) corresponding to minimum value in min_dicdt
                min_key = [key2 for key2 in min_dict if min_dict[key2] == temp]

                #Option 1: min_key has >1 items:  #TIE BREAKER REQUIRED#
                if len(min_key) > 1:

                    min_job = {}    #need to compare job # to break tie

                    #loop through each value in min_key list
                    for k in min_key:
                        #store job number in min_job dictionary
                        min_job[k] = task_data[k][0]

                    #determine minimum job # value
                    temp2 = min(min_job.values())
                    #find corresponding key to min job value and set as min_key
                    min_key = [key3 for key3 in min_job if min_job[key3] == temp2]

            #now that we have the min_key for each key 'rj': adjust lists
            ip_tasks[key] = [min_key[0], time, time + int(task_data[min_key[0]][3])]
            res_queue[key].remove(min_key[0])   # remove task from resource queue

    return res_queue, ip_tasks

def find_next_time(time, ip_tasks):
    """
    Calculates next time based on shortest task currently in-progress

    Args:
        (int) time       - current time
        (dict) task_data - contains master task data
        (dict) ip_tasks  - contains current tasks in progress

    Returns:
        (int) next_time  - next time that entire loop needs to run
    """

    time_list = []

    # loop through each in progress task:
    for key in ip_tasks:

        #add the 'end-times' for each in-progress task to the time_list
        time_list.append(int(ip_tasks[key][2]))

    # find the minimum pj task for resoure r:
    if len(time_list) != 0:
        next_time = int(min(time_list))

        return next_time

    # if ip list is empty, time_list will be empty and therefore, time remains
    else:
        return time

def update_ip_to_completed(time, time_new, ip_tasks, compl_tasks, task_data, schedule):
    """
    Update completed tasks and in-progress tasks based on new time

    Args:
        (int) time_new     - update time
        (dict) ip_tasks    - contains current tasks in progress
        (dict) task_data   - contains master data
        (dict) schedule    - stores task start times for results

    Returns:
        (dict) ip_tasks    - updated current tasks in progress
        (dict) compl_tasks - updated completed tasks
        (dict) schedule    - store compl task start values for final result
    """

    #loop through each task in ip_tasks and compare with new time
    for key in ip_tasks.copy():

        # if task end time = current time
        if int(ip_tasks[key][2]) == time:

            # task is complete. Add to compl_tasks
            compl_tasks[ip_tasks[key][0]] = [ip_tasks[key][1], time]

            if task_data[ip_tasks[key][0]][0] not in schedule:
                schedule[task_data[ip_tasks[key][0]][0]] = [ip_tasks[key][1]]

            else:
                schedule[task_data[ip_tasks[key][0]][0]].append(ip_tasks[key][1])

            # remove from in-progress
            del ip_tasks[key]

    return ip_tasks, compl_tasks, schedule

def update_res_queue(task_data, unavail_tasks, res_queue, compl_tasks):
    """
    Update unavailable tasks and resource queue based on what is complete

    Args:
        (dict) unavail_tasks - contains tasks unable to start (due to predecessor)
        (dict) res_queue     - contains queue of avail tasks by resource
        (dict) compl_tasks   - contains completed tasks

    Returns:
        (dict) unavail_tasks - updated unavail tasks
        (dict) res_queue     - updated res_queue
    """

    for key in unavail_tasks.copy():

        j = unavail_tasks[key][0]
        t = unavail_tasks[key][1]

        if "j{}t{}".format(j,t-1) in compl_tasks:

            if "r{}".format(unavail_tasks[key][2]) not in res_queue:
                res_queue["r{}".format(task_data[key][2])] = []

            # add task to res_queue, organized by machine 'r'
            res_queue["r{}".format(unavail_tasks[key][2])].append(key)

            #remove task from unvail and move to avail
            del unavail_tasks[key]

    return unavail_tasks, res_queue

def run_SPT(instance):
    """
    Update unavailable tasks and resource queue based on what is complete

    Args:
        (str) instance - store file name as 'file_name.txt'

    Returns:
        (tuple) result - in format: (makespan, {job0:[s01, s02,..],... })
        where s01, s02,... are respective start times for each job- operation
    """

    #read 'instance' file and extract master data
    jobs, machines, tasks, task_data = load_data(instance)

    #Step 0. Initialize key variables for duaration of algority
    time = 0
    ip_tasks = {}       #store task in each resource that is in-progress
    compl_tasks = {}    #store tasks that are complete
    schedule = {}       #store dict of start time by operation {Jj:[ta,tb,tc,..]}

    #Step 1. set initial values for dicts: no-predecessor tasks moved to res_queue
    unavail_tasks, res_queue = initialize_dicts(task_data)

    #Step 2. Loop through algorithm until all tasks are complete
    while len(compl_tasks) < tasks:

        #Step 2A. activate Shortest Processing Time (SPT) tasks from res_queue
        res_queue, ip_tasks = machine_activate(time, task_data, res_queue, ip_tasks)

        #Step 2B. Find task with closest completion time and set as new time
        time_new = find_next_time(time, ip_tasks)
        time = time_new

        #Step 2C. update completed tasks from new time
        ip_tasks, compl_tasks, schedule = update_ip_to_completed(time, time_new, ip_tasks, compl_tasks, task_data, schedule)

        #if number of completed tasks = tasks in instance, we are done:
        if len(compl_tasks) == tasks:
            break

        #Step 2D. update res_queue with tasks with predecessors complete
        unavail_tasks, res_queue = update_res_queue(task_data, unavail_tasks, res_queue, compl_tasks)

    #Step 3A. final output dict of task start times organized as: {job: [t1, t2, ..]}
    schedule = {key : schedule[key] for key in sorted(schedule)}

    #Step 3B. convert into format required by marking guide.
    # makespan is current time (ie. time of final task completion)
    result = (time, schedule)

    print("Result:", result)

    return result

instance = "selftest0.txt"

run_SPT(instance)
