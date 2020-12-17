import pickle

import pandas as pd
import statsmodels.api as sm


def regression(data):
    result = []

    for measure in filter(lambda m: m != 'iterations', data.columns.tolist()):
        x = data['iterations']
        y = data[measure]
        x = sm.add_constant(x)

        model = sm.OLS(y, x).fit()

        result.append([model.params.iterations, model.rsquared, pickle.dumps(model)])

    return result


def calc_metrics(data):
    result = []

    for measure in filter(lambda x: x != 'iterations', data.columns.tolist()):
        r = {}
        value = (data[measure] / data['iterations'])
        r['mean'] = [value.mean(), 0, 0]
        r['std'] = [value.std(), 0, 0]
        r['median'] = [value.median(), 0, 0]
        r['mad'] = [value.mad(), 0, 0]
        result.append(r)

    return result


def remove_overhead(measurements, data, max_depth, depth=0):
    if depth == 0:
        for index, row in data.iterrows():
            for measure in measurements:
                row[measure + "-metrics"]['adj_slope'] = row[measure + "-metrics"]['slope'][0]
    else:
        for index, row in data.iterrows():
            for measure in measurements:
                if len(row['overhead']) == depth:
                    for current_id in row['overhead']:
                        try:
                            value = data.loc[data['id'] == current_id, measure + "-metrics"].iloc[0]['adj_slope']
                            row[measure + "-metrics"]['adj_slope'] = row[measure + "-metrics"]['adj_slope'] - value
                        except (KeyError, IndexError):
                            print("Cannot calculate adjusted slope for '" + current_id + "'! Setting to -1!")
                            row[measure + "-metrics"]['adj_slope'] = -1
                            raise

    if depth == max_depth:
        return data
    else:
        return remove_overhead(measurements, data, max_depth, depth + 1)


def analyze(data):
    measurements = list(filter(lambda x: x != 'iterations', data['data'][0].columns.tolist()))

    metrics = data['data'].apply(lambda x: calc_metrics(x)).to_list()
    data[list(map(lambda x: x + "-metrics", measurements))] = pd.DataFrame(metrics, index=data.index)

    regressions = data['data'].apply(lambda x: regression(x)).to_list()
    data[list(map(lambda x: x + "-reg_model", measurements))] = pd.DataFrame(regressions, index=data.index)

    for measure in measurements:
        data.apply(lambda r: r[measure + "-metrics"].update(
            {'slope': [r[measure + "-reg_model"][0], 0, 0], 'r2': [r[measure + "-reg_model"][1], 0, 0]}), axis=1)
        data[measure + '-reg_model'] = data[measure + '-reg_model'].apply(lambda r: r[2])

    remove_overhead(measurements, data, data['overhead'].map(len).max())

    for measure in measurements:
        data.apply(lambda r: r[measure + "-metrics"].update(
            {'ratio': r[measure + "-metrics"]['adj_slope'] / r["gas-metrics"]['adj_slope']}), axis=1)


    return data
