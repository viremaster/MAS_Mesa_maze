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

replicates = 10
max_steps = 3000
distinct_samples = 5

model_reporters = {
                "Finished Cyan Walkers": lambda m: m.schedule.get_finished_count(CyanWalker),
                "Finished Red Walkers": lambda m: m.schedule.get_finished_count(RedWalker),
                }

data = {}

for i, var in enumerate(problem['names']):
    # Get the bounds for this variable and get <distinct_samples> samples within this space (uniform)
    samples = np.linspace(*problem['bounds'][i], num=distinct_samples)

    # Keep in mind that wolf_gain_from_food should be integers. You will have to change
    # your code to acommidate for this or sample in such a way that you only get integers.
    if var == 'cyan_noise' or var == 'red_noise':
        samples = np.linspace(*problem['bounds'][i], num=distinct_samples, dtype=int)

    batch = BatchRunner(WalkerModel,
                        max_steps=max_steps,
                        iterations=replicates,
                        variable_parameters={var: samples},
                        model_reporters=model_reporters,
                        display_progress=True)

    batch.run_all()

    data[var] = batch.get_model_vars_dataframe()


def plot_param_var_conf(ax, df, in_var, in_param, i):
    x = df.groupby(in_var).mean().reset_index()[in_var]
    y = df.groupby(in_var).mean()[in_param]

    inner_replicates = df.groupby(in_var)[in_param].count()
    err = (1.96 * df.groupby(in_var)[in_param].std()) / np.sqrt(inner_replicates)

    ax.plot(x, y, c='k')
    ax.fill_between(x, y - err, y + err)

    ax.set_xlabel(in_var)
    ax.set_ylabel(in_param)


def plot_all_vars(df, in_param):
    f, axs = plt.subplots(2, figsize=(7, 10))

    for in_i, in_var in enumerate(problem['names']):
        plot_param_var_conf(axs[in_i], df[in_var], in_var, in_param, i)


for param in ('Finished Cyan Walkers', 'Finished Red Walkers'):
    plot_all_vars(data, param)
    plt.show()
