instance = "answer0.txt"

#read file with instance = "filename.txt"
with open(instance) as f:
    data = f.read().splitlines()

print(data)

#convert job rows into lists
for i in range(2,len(data)):
    data[i] = data[i].split('  ')

print(data)

jobs = int(data[1][0])  #number of jobs 'j'(rows)
r = int(data[1][2])     #number of machines 'r'

task_data = {}          #initialize dictionary to contain all master task data

#loop through each job row
for i in range(0,jobs):
    #loop through each pair in a row
    for k in range(0,int(len(data[2])/2)):
        #create a dictionary of format: {'job/task# key': (job, task, rj, pj) }
        task_data["j{}t{}".format(i,k)] = (i, k, data[i+2][2*k], data[i+2][2*k+1])

tasks = len(task_data)  #calculate number of tasks total to know when complete

print("# of jobs j:", jobs)
print("# of tasks t:", tasks)
print("# of machines r:", r)
print("Task data format: {'job/task key', (job, task, rj, pj)}")
print("Task data:", task_data)

#Step 1. Create a list 'S' of all available operations
time = 0   #intialize time t = 0

unavail_list = [] #list of tasks not avail to start (ie. predecessors not compl)
avail_list = {}   #list of all avail. tasks (ie. no outstanding predecessors)
compl_list = []   #Initialize compl. list to compare if predecessor is done

#1A.
#initialize avail_list with all tasks with no predecessors (ie. operation 0)
#initialize unavail_list with all other tasks

#loop through each task in task_data
for key in task_data:

    #check if task is a task 0 (no predecessors)
    if task_data[key][1] == 0:

        # initialize dictionary key as 'r0', 'r1', ... etc.
        if "r{}".format(task_data[key][2]) not in avail_list:
                avail_list["r{}".format(task_data[key][2])] = []

        # task 0s gets added to avail_list, organized by machine 'r'
        avail_list["r{}".format(task_data[key][2])].append(key)

    else:
        #if not a task 0, add to unavail_list
        unavail_list.append(key)

print("Task data format: {'key': (j, t, rj, pj)}")
print("Task data:", task_data)
print("Unavailable List:", unavail_list)
print("Available List:", avail_list)
print("Compl. List:", compl_list)

#Step 2. Find avail task with min pj for each resource and add to in-progress (ip)

ip_list = {}    #initialize

# loop through each resource (r0, r1, ...) in avail_list
for key in avail_list.copy():

    min_list = {}   #initialize.  Will be used to calculate min pj task

    # loop through each task in the task list for resource r:
    for i in range(len(avail_list[key])):

        #add the pj for each task to the min_list
        min_list[avail_list[key][i]] = task_data[avail_list[key][i]][3]

    # find the minimum pj task for resoure r:
    if len(min_list) != 0:
        min_key = min(min_list, key=min_list.get)

        ip_list["r{}".format(task_data[avail_list[key][0]][2])] = [min_key, time]  # add task to in-progress list
        del avail_list[key][i]           # remove task from avail list queue

print("Unavailable List:", unavail_list)
print("Available List:", avail_list)
print("In Progress List:", ip_list)
print("Compl. List:", compl_list)

# Step 3. Find in-progress process with shortest time as next time

time_list = []

# loop through each in progress task:
for key in ip_list:

    #add the pj for each in-progress task to the time_list
    time_list.append(int(task_data[ip_list[key][0]][3]))

# find the minimum pj task for resoure r:
if len(time_list) != 0:
    time_new = int(min(time_list))

print("Unavailable List:", unavail_list)
print("Available List:", avail_list)
print("In Progress List:", ip_list)
print("Compl. List:", compl_list)

print("New Time =", time_new)

# Step 4. Calculate all tasks in ip_list that are complete at time = time_new
# Step 5. Adjust all lists and repeat

while len(compl_list) < tasks:

    #loop through each task in ip_list and compare with time_delta
    for key in ip_list.copy():

        # if task start time + task duration (pj) is less than current time
        if (int(ip_list[key][1]) + int(task_data[ip_list[key][0]][3])) <= time_new:

            # task is complete
            compl_list.append(ip_list[key][0])

            # remove from in-progress
            del ip_list[key]

    for key in unavail_list.copy():

        j = task_data[key][0]
        t = task_data[key][1]

        if "j{}t{}".format(j,t-1) in compl_list:

            #remove task from unvail and move to avail
            unavail_list.remove(key)

            if "r{}".format(task_data[key][2]) not in avail_list.copy():
                avail_list["r{}".format(task_data[key][2])] = []

            # task 0s gets added to avail_list, organized by machine 'r'
            avail_list["r{}".format(task_data[key][2])].append(key)

    # loop through each resource (r0, r1, ...) in avail_list
    for key in avail_list.copy():

        min_list = {}   #initialize.  Will be used to calculate min pj task

        # loop through each task in the task list for resource r:
        for i in range(len(avail_list[key])):

            #add the pj for each task to the min_list
            min_list[avail_list[key][i]] = task_data[avail_list[key][i]][3]

        # find the minimum pj task for resoure r:
        if len(min_list) != 0:
            min_key = min(min_list, key=min_list.get)

            ip_list["r{}".format(task_data[avail_list[key][0]][2])] = [min_key, time]  # add task to in-progress list
            del avail_list[key][i]           # remove task from avail list queue

    time_list = []

    # loop through each in progress task:
    for key in ip_list:

        #add the pj for each in-progress task to the time_list
        time_list.append(int(task_data[ip_list[key][0]][3]))

    # find the minimum pj task for resoure r:
    if len(time_list) != 0:
        time_new = int(min(time_list))

    time = time_new

print("Time =", time)

print("Unavailable List:", unavail_list)
print("Available List:", avail_list)
print("In Progress List:", ip_list)
print("Compl. List:", compl_list)
