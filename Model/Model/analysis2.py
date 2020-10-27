from SALib.sample import saltelli
from Model.Model.model import WalkerModel
from Model.Model.efficient_agents import RedWalker, CyanWalker
from mesa.batchrunner import BatchRunner
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

problem = {
    'num_vars': 2,
    'names': ['cyan_noise', 'red_noise'],
    'bounds': [[1, 100], [1, 100]]
}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 10
max_steps = 3000
distinct_samples = 5

model_reporters = {
                "Finished Cyan Walkers": lambda m: m.schedule.get_finished_count(CyanWalker),
                "Finished Red Walkers": lambda m: m.schedule.get_finished_count(RedWalker),
                }

# We get all our samples here
param_values = saltelli.sample(problem, distinct_samples)

# READ NOTE BELOW CODE
batch = BatchRunner(WalkerModel,
                    max_steps=max_steps,
                    variable_parameters={name: [] for name in problem['names']},
                    model_reporters=model_reporters)

count = 0
for i in range(replicates):
    for vals in param_values:
        # Change parameters that should be integers
        vals = list(vals)
        vals[1] = int(vals[1])
        vals[0] = int(vals[0])

        # Transform to dict with parameter names and their values
        variable_parameters = {}
        for name, val in zip(problem['names'], vals):
            variable_parameters[name] = val

        batch.run_iteration(variable_parameters, tuple(vals), count)
        count += 1

        print(f'{count / (len(param_values) * (replicates)) * 100:.2f}% done')

data = batch.get_model_vars_dataframe()

print(data)

Si_sheep = sobol.analyze(problem, data['Finished Cyan Walkers'].as_matrix(), print_to_console=True)
Si_wolves = sobol.analyze(problem, data['Finished Red Walkers'].as_matrix(), print_to_console=True)


def plot_index(s, params, inner_i, title=''):

    if inner_i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + inner_i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + inner_i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
    else:
        indices = s['S' + inner_i]
        errors = s['S' + inner_i + '_conf']
        plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')


for Si in (Si_sheep, Si_wolves):
    # First order
    plot_index(Si, problem['names'], '1', 'First order sensitivity')
    plt.show()

    # Second order
    plot_index(Si, problem['names'], '2', 'Second order sensitivity')
    plt.show()

    # Total order
    plot_index(Si, problem['names'], 'T', 'Total order sensitivity')
    plt.show()