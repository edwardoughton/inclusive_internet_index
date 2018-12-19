import os
import csv

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

dir_path = os.path.dirname(os.path.realpath(__file__))

def read_index_data():

    index_data = []

    with open(os.path.join(dir_path, 'internet_inclusiveness_index', 'internet_inclusiveness_index.csv'), 'r') as my_file:
        reader = csv.reader(my_file)
        next(reader, None)
        for row in reader:
            if row[2] == 'availability':
                index_data.append({
                    'country': row[0].lower(),
                    'score': float(row[1]),
                    'metric': row[2]
                })

    return index_data

def read_population_data():

    pop_data = []

    with open(os.path.join(dir_path, 'un_population.csv'), 'r') as my_file:
        reader = csv.reader(my_file)
        next(reader, None)
        for row in reader:
            try:
                pop_data.append({
                'country': row[0].lower(),
                'population': int(row[1])
                })
            except:
                print(row)

    return pop_data

def correct_country_names(population_data):
    
    corrected_data = []

    for country in population_data:
        if country['country'] == 'congo':
            correct_name = 'congo (drc)'
        elif country['country'] == 'russian federation':
            correct_name = 'russia'
        elif country['country'] == 'iran (islamic republic of)':
            correct_name = 'iran'
        elif country['country'] == 'republic of korea':
            correct_name = 'south korea'
        elif country['country'] == 'china, taiwan province of china':
            correct_name = 'taiwan'
        elif country['country'] == 'united republic of tanzania':
            correct_name = 'tanzania'
        elif country['country'] == 'united arab emirates':
            correct_name = 'uae'
        elif country['country'] == 'united states of america':
            correct_name = 'united states'
        elif country['country'] == 'venezuela (bolivarian republic of)':
            correct_name = 'venezuela'
        elif country['country'] == 'viet nam':
            correct_name = 'vietnam'
        else:
            correct_name = country['country']

        corrected_data.append({
            'country': correct_name,
            'population': country['population']
        })      

    return corrected_data

def merge_data(index_data, pop_data):

    matched_data = []
    unmatched_country_data = []
    unmatched_population_data = []

    for country_index in index_data:
        for country_pop in pop_data:
            if country_index['country'] == country_pop['country']:
                
                matched_data.append({
                    'country': country_index['country'],
                    'score': country_index['score'],
                    'metric': country_index['metric'],
                    'population': country_pop['population'],
                })
            else:
                unmatched_country_data.append(country_index['country'])
                unmatched_population_data.append(country_pop['country'])

    return matched_data

def plot_data(data):

    population = []
    availability = []
    affordability = []
    relevance = []
    readiness = []

    for datum in data:
        print(datum)
        if datum['metric'] == 'availability':
            availability.append(datum['score'])
            population.append(datum['population'])

    plt.plot(population, availability, 'bo')

    # fig, ax = plt.subplots()
    # ax.scatter(delta1[:-1], delta1[1:], c=close, s=volume, alpha=0.5)

    # ax.set_xlabel(r'$\Delta_i$', fontsize=15)
    # ax.set_ylabel(r'$\Delta_{i+1}$', fontsize=15)
    # ax.set_title('Volume and percent change')

    # ax.grid(True)
    # fig.tight_layout()

    plt.show()

def csv_writer(data, filename, fieldnames):
    """
    Write data to a CSV file path
    """
    with open(os.path.join(dir_path, filename), 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames, lineterminator = '\n')
        writer.writeheader()
        writer.writerows(data)

################################
#run functions 
################################

#import index data
index_data = read_index_data()

#import population data
pop_data = read_population_data()

#correct non-matching names
pop_data = correct_country_names(pop_data)

#merge all data
all_data = merge_data(index_data, pop_data)

plot_data(all_data)

#write out for validation
fieldnames = ['country','score','metric', 'population']
csv_writer(all_data, 'output.csv', fieldnames)

#print(all_data)




