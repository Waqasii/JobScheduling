

def job_shop_scheduling(jobs, machine_order):
    # Initialization
    num_jobs = len(jobs)
    num_machines = len(machine_order[0])
    job_completion = [0] * num_jobs  # Completion time for each job
    # Next available time for each machine
    machine_completion = [0] * num_machines

    # Sequence of jobs
    job_sequence = []
    for _ in range(num_jobs * num_machines):
        next_job = None
        earliest_time = float('inf')

        # Find the job that can be done next
        for i in range(num_jobs):
            if jobs[i]:  # If there are operations left for the job
                machine = machine_order[i][0]  # Next machine for the job
                time = max(
                    job_completion[i], machine_completion[machine]) + jobs[i][0]

                # Select the job that can be finished the earliest
                if time < earliest_time:
                    earliest_time = time
                    next_job = i

        # Schedule the job
        if next_job is not None:
            next_machine, next_time = machine_order[next_job].pop(
                0), jobs[next_job].pop(0)
            start_time = max(
                job_completion[next_job], machine_completion[next_machine])
            end_time = start_time + next_time
            job_completion[next_job] = end_time
            machine_completion[next_machine] = end_time
            job_sequence.append(
                (f'J{next_job+1}', f'M{next_machine+1}', start_time, end_time))

    return job_sequence, job_completion, max(machine_completion)


# Jobs data, each job is a list of its operations' processing times
jobs = [
    [29, 78, 9, 36, 49, 11, 62, 56, 44, 21],
    [43, 90, 75, 11, 69, 28, 46, 46, 72, 30],
    [91, 85, 39, 74, 90, 10, 10, 89, 45, 33],
    [81, 95, 71, 99, 9, 52, 85, 98, 22, 43],
    [14, 6, 22, 61, 26, 69, 21, 49, 72, 53],
    [84, 2, 52, 95, 48, 72, 47, 65, 6, 25],
    [46, 37, 61, 13, 32, 21, 32, 89, 30, 55],
    [31, 86, 46, 74, 32, 88, 19, 48, 36, 79],
    [76, 69, 76, 51, 85, 11, 40, 89, 26, 74],
    [85, 13, 61, 7, 64, 76, 47, 52, 90, 45]
]

# Machine order for each job, list of lists of machine indexes
machine_order = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [0, 2, 4, 9, 3, 1, 6, 5, 7, 8],
    [1, 0, 3, 2, 8, 5, 7, 6, 9, 4],
    [1, 2, 0, 4, 6, 8, 7, 3, 9, 5],
    [2, 0, 1, 5, 3, 4, 8, 7, 9, 6],
    [2, 1, 5, 3, 8, 9, 0, 6, 4, 7],
    [1, 0, 3, 2, 6, 5, 9, 8, 7, 4],
    [2, 0, 1, 5, 4, 6, 8, 9, 7, 3],
    [0, 1, 3, 5, 2, 9, 6, 7, 4, 8],
    [1, 0, 2, 6, 8, 9, 5, 3, 4, 7]
]


# Run the greedy job shop scheduling algorithm
sequence, completion, makespan = job_shop_scheduling(jobs, machine_order)

# Output results
for job in sequence:
    print(f"{job[0]} is processed on {job[1]} from {job[2]} to {job[3]}")
print(f"Job completion times: {completion}")
print(f"Makespan: {makespan}")
