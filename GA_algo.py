# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:24:51 2018

Author: cheng-man wu
LinkedIn: www.linkedin.com/in/chengmanwu
Github: https://github.com/wurmen

"""

'''==========Solving job shop scheduling problem by gentic algorithm in python======='''
# importing required modules
import pandas as pd
import numpy as np
import time
import copy
pt_tmp = pd.read_excel(
    "JSP_dataset.xlsx", sheet_name="Processing Time", index_col=[0])
ms_tmp = pd.read_excel(
    "JSP_dataset.xlsx", sheet_name="Machines Sequence", index_col=[0])

dfshape = pt_tmp.shape
num_mc = dfshape[1]  # number of machines
num_job = dfshape[0]  # number of jobs
num_gene = num_mc*num_job  # number of genes in a chromosome

pt = [list(map(int, pt_tmp.iloc[i])) for i in range(num_job)]
ms = [list(map(int, ms_tmp.iloc[i])) for i in range(num_job)]


# raw_input is used in python 2
# default value is 30
population_size = int(input('Please input the size of population: ') or 30)
# default value is 0.8
crossover_rate = float(
    input('Please input the size of Crossover Rate: ') or 0.8)
# default value is 0.2
mutation_rate = float(input('Please input the size of Mutation Rate: ') or 0.2)
mutation_selection_rate = float(
    input('Please input the mutation selection rate: ') or 0.2)
num_mutation_jobs = round(num_gene*mutation_selection_rate)
num_iteration = int(input('Please input number of iteration: ')
                    or 2000)  # default value is 2000

start_time = time.time()

'''==================== main code ==============================='''
'''----- generate initial population -----'''
Tbest = 999999999999999
best_list, best_obj = [], []
population_list = []
makespan_record = []
for i in range(population_size):
    # generate a random permutation of 0 to num_job*num_mc-1
    nxm_random_num = list(np.random.permutation(num_gene))
    population_list.append(nxm_random_num)  # add to the population_list
    for j in range(num_gene):
        # convert to job number format, every job appears m times
        population_list[i][j] = population_list[i][j] % num_job

for n in range(num_iteration):
    Tbest_now = 99999999999

    '''-------- two point crossover --------'''
    parent_list = copy.deepcopy(population_list)
    offspring_list = copy.deepcopy(population_list)
    # generate a random sequence to select the parent chromosome to crossover
    S = list(np.random.permutation(population_size))

    for m in range(int(population_size/2)):
        crossover_prob = np.random.rand()
        if crossover_rate >= crossover_prob:
            parent_1 = population_list[S[2*m]][:]
            parent_2 = population_list[S[2*m+1]][:]
            child_1 = parent_1[:]
            child_2 = parent_2[:]
            cutpoint = list(np.random.choice(num_gene, 2, replace=False))
            cutpoint.sort()

            child_1[cutpoint[0]:cutpoint[1]
                    ] = parent_2[cutpoint[0]:cutpoint[1]]
            child_2[cutpoint[0]:cutpoint[1]
                    ] = parent_1[cutpoint[0]:cutpoint[1]]
            offspring_list[S[2*m]] = child_1[:]
            offspring_list[S[2*m+1]] = child_2[:]

    '''----------repairment-------------'''
    for m in range(population_size):
        job_count = {}
        # 'larger' record jobs appear in the chromosome more than m times, and 'less' records less than m times.
        larger, less = [], []
        for i in range(num_job):
            if i in offspring_list[m]:
                count = offspring_list[m].count(i)
                pos = offspring_list[m].index(i)
                # store the above two values to the job_count dictionary
                job_count[i] = [count, pos]
            else:
                count = 0
                job_count[i] = [count, 0]
            if count > num_mc:
                larger.append(i)
            elif count < num_mc:
                less.append(i)

        for k in range(len(larger)):
            chg_job = larger[k]
            while job_count[chg_job][0] > num_mc:
                for d in range(len(less)):
                    if job_count[less[d]][0] < num_mc:
                        offspring_list[m][job_count[chg_job][1]] = less[d]
                        job_count[chg_job][1] = offspring_list[m].index(
                            chg_job)
                        job_count[chg_job][0] = job_count[chg_job][0]-1
                        job_count[less[d]][0] = job_count[less[d]][0]+1
                    if job_count[chg_job][0] == num_mc:
                        break

    '''--------mutatuon--------'''
    for m in range(len(offspring_list)):
        mutation_prob = np.random.rand()
        if mutation_rate >= mutation_prob:
            # chooses the position to mutation
            m_chg = list(np.random.choice(
                num_gene, num_mutation_jobs, replace=False))
            # save the value which is on the first mutation position
            t_value_last = offspring_list[m][m_chg[0]]
            for i in range(num_mutation_jobs-1):
                # displacement
                offspring_list[m][m_chg[i]] = offspring_list[m][m_chg[i+1]]

            # move the value of the first mutation position to the last mutation position
            offspring_list[m][m_chg[num_mutation_jobs-1]] = t_value_last

    '''--------fitness value(calculate makespan)-------------'''
    total_chromosome = copy.deepcopy(
        parent_list)+copy.deepcopy(offspring_list)  # parent and offspring chromosomes combination
    chrom_fitness, chrom_fit = [], []
    total_fitness = 0
    for m in range(population_size*2):
        j_keys = [j for j in range(num_job)]
        key_count = {key: 0 for key in j_keys}
        j_count = {key: 0 for key in j_keys}
        m_keys = [j+1 for j in range(num_mc)]
        m_count = {key: 0 for key in m_keys}

        for i in total_chromosome[m]:
            gen_t = int(pt[i][key_count[i]])
            gen_m = int(ms[i][key_count[i]])
            j_count[i] = j_count[i]+gen_t
            m_count[gen_m] = m_count[gen_m]+gen_t

            if m_count[gen_m] < j_count[i]:
                m_count[gen_m] = j_count[i]
            elif m_count[gen_m] > j_count[i]:
                j_count[i] = m_count[gen_m]

            key_count[i] = key_count[i]+1

        makespan = max(j_count.values())
        chrom_fitness.append(1/makespan)
        chrom_fit.append(makespan)
        total_fitness = total_fitness+chrom_fitness[m]

    '''----------selection(roulette wheel approach)----------'''
    pk, qk = [], []

    for i in range(population_size*2):
        pk.append(chrom_fitness[i]/total_fitness)
    for i in range(population_size*2):
        cumulative = 0
        for j in range(0, i+1):
            cumulative = cumulative+pk[j]
        qk.append(cumulative)

    selection_rand = [np.random.rand() for i in range(population_size)]

    for i in range(population_size):
        if selection_rand[i] <= qk[0]:
            population_list[i] = copy.deepcopy(total_chromosome[0])
        else:
            for j in range(0, population_size*2-1):
                if selection_rand[i] > qk[j] and selection_rand[i] <= qk[j+1]:
                    population_list[i] = copy.deepcopy(total_chromosome[j+1])
                    break
    '''----------comparison----------'''
    for i in range(population_size*2):
        if chrom_fit[i] < Tbest_now:
            Tbest_now = chrom_fit[i]
            sequence_now = copy.deepcopy(total_chromosome[i])
    if Tbest_now <= Tbest:
        Tbest = Tbest_now
        sequence_best = copy.deepcopy(sequence_now)

    makespan_record.append(Tbest)
'''----------result----------'''
print("optimal sequence", sequence_best)
print("optimal value:%f" % Tbest)
print('the elapsed time:%s' % (time.time() - start_time))
