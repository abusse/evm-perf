import ntpath
import os
import pathlib
import pickle

from mako.template import Template
from matplotlib import rcParams
from tqdm import tqdm

from core.meta_fields import META_FIELDS

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np


def create_output_dirs(output_dir, data):
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    for i in data.index:
        pathlib.Path(output_dir + os.sep + os.path.dirname(data['asm_path_rel'][i])).mkdir(parents=True, exist_ok=True)


def write_data_to_csv(output_dir, measurements, data):
    print("Writing data to csv...")

    for measure in measurements:
        temp = data.filter(['asm_path_rel'] + META_FIELDS, axis=1)
        temp = pd.concat([temp, data[measure + "-metrics"].apply(pd.Series)], axis=1)
        temp.to_csv(output_dir + os.sep + measure + '-results.csv')

    for i in data.index:
        pathlib.Path(output_dir + os.sep + os.path.dirname(data['asm_path_rel'][i])).mkdir(parents=True, exist_ok=True)

        # Save measurements to CSV
        data['data'][i].to_csv(output_dir + os.sep + data['asm_path_rel'][i] + ".csv")


def write_plots(output_dir, measurements, data):
    print("Creating and writing plots...")

    rcParams.update({'figure.autolayout': True})

    for measure in measurements:
        plt.figure(figsize=(15, 8), dpi=300)
        plt.xticks(rotation=90)
        plt.plot(data['id'], data[measure + "-metrics"].map(lambda r: r['ratio']))
        plt.savefig(output_dir + os.sep + measure + '-ratio-large.svg')
        plt.close()

    for i in tqdm(data.index):
        # Create regression plots
        for measure in measurements:
            model = pickle.loads(data[measure + '-reg_model'][i])

            sns.set_style("darkgrid", {"grid.color": 'black'})
            sns.set_context("notebook")
            sns.regplot(x="iterations", y=measure, data=data['data'][i], color='b', x_estimator=np.mean)
            plt.title("(intercept: " + '{:.3f}'.format(model.params['const']) + ", coef: " + '{:.3f}'.format(
                model.params['iterations']) + ", r^2: " + '{:.5f}'.format(model.rsquared) + ")")
            plt.savefig(output_dir + os.sep + data['asm_path_rel'][i] + "-" + measure + '-regression.svg')
            plt.close()

            plt.figure(figsize=(15, 12), dpi=300)
            sns.set_style("darkgrid", {"grid.color": 'black'})
            sns.set_context("poster")
            sns.regplot(x="iterations", y=measure, data=data['data'][i], color='b', x_estimator=np.mean)
            plt.title("(intercept: " + '{:.3f}'.format(model.params['const']) + ", coef: " + '{:.3f}'.format(
                model.params['iterations']) + ", r^2: " + '{:.5f}'.format(model.rsquared) + ")")
            plt.savefig(output_dir + os.sep + data['asm_path_rel'][i] + "-" + measure + '-regression-large.svg')
            plt.close()

            sns.set_style("darkgrid", {"grid.color": 'black'})
            sns.set_context("notebook")
            sns.boxplot(x="iterations", y=measure, data=data['data'][i], color='b')
            plt.savefig(output_dir + os.sep + data['asm_path_rel'][i] + "-" + measure + '-boxplot.svg')
            plt.close()

            plt.figure(figsize=(15, 12), dpi=300)
            sns.set_style("darkgrid", {"grid.color": 'black'})
            sns.set_context("poster")
            sns.boxplot(x="iterations", y=measure, data=data['data'][i], color='b')
            plt.savefig(output_dir + os.sep + data['asm_path_rel'][i] + "-" + measure + '-boxplot-large.svg')
            plt.close()

            data['data'][i][measure + "-avg"] = data['data'][i][measure] / data['data'][i]['iterations']

            sns.set_style("darkgrid", {"grid.color": 'black'})
            sns.set_context("notebook")
            sns.relplot(x="iterations", y=measure + "-avg", data=data['data'][i], color='b', kind="line")
            plt.savefig(output_dir + os.sep + data['asm_path_rel'][i] + "-" + measure + '-distplot.svg')
            plt.close()


def write_html(output_dir, measurements, data, timestamp):
    print("Writing html...")

    results = []

    for i in data.index:
        m_types = []
        m_list = {}

        for measure in measurements:
            values = {'measure': measure,
                      'img': ntpath.basename(output_dir + os.sep + data['asm_path_rel'][i] + "-" + measure),
                      'metrics': data[measure + '-metrics'][i]}

            model = pickle.loads(data[measure + '-reg_model'][i])
            values['summary'] = model.summary()

            m_types.append(values)
            m_list.update({measure: data[measure + '-metrics'][i]})

        mytemplate = Template(filename='templates/measurement.html')
        filled_template = mytemplate.render(title=(data['id'][i]), m_types=m_types, code=data['code'][i],
                                            names=data['names'][0], overhead=data['overhead'][i])

        file_name = output_dir + os.sep + data['asm_path_rel'][i] + "-report.html"
        f = open(file_name, "w+")
        f.write(filled_template)
        f.close()

        results.append((data['id'][i], data['asm_path_rel'][i] + "-report.html", m_list))

    mytemplate = Template(filename='templates/index.html')
    filled_template = mytemplate.render(results=results, measurements=measurements, names=data['names'][0],
                                        units=data['units'][0], host=data['hosts'][0][measurements[0]],
                                        timestamp=timestamp.strftime('%d-%m-%Y %H:%M'))

    file_name = output_dir + os.sep + "index.html"
    f = open(file_name, "w+")
    f.write(filled_template)
    f.close()


def output(data, directory, timestamp):
    measurements = list(filter(lambda x: x != 'iterations', data['data'][0].columns.tolist()))

    output_dir = "{}{}{}{}{}".format(directory, os.sep, data['hosts'][0][measurements[0]], os.sep,
                                     timestamp.strftime('%Y-%m-%d_%H-%M'))

    create_output_dirs(output_dir, data)

    write_data_to_csv(output_dir, measurements, data)

    write_html(output_dir, measurements, data, timestamp)

    write_plots(output_dir, measurements, data)