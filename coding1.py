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
