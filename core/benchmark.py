import glob
import json
import os
import re
from functools import reduce
from subprocess import Popen, PIPE

import pandas as pd
from pyevmasm import assemble_hex
from tqdm import tqdm

from core.meta_fields import META_FIELDS
from core.token_converter import convert_token


def multiply_string(string, n):
    result = ""

    for i in range(n):
        result += string

    return result


def replace_token(code):
    result = ""

    for line in code.splitlines():
        result += re.sub(r'#(\w+)', lambda x: convert_token(x.group(1)), line)

    return result


def split_code(code: str):
    head_block = ""
    current = ""

    for line in code.splitlines(keepends=True):
        if '// #START-ITER' in line:
            head_block = current
            current = ""
            continue
        if not line.startswith('//'):
            current += line

    return head_block, current + "\n"


def prepare_code(string, n):
    head_block, tail_block = split_code(string)
    tail_block = multiply_string(tail_block, n)
    code = (head_block + tail_block).split("\n")

    code_string = ""

    for line in code:
        code_string += "\n" + re.sub(r'#([\w,]+)', lambda x: convert_token(x.group(1)), line)

    return code_string


def get_infos(code):
    infos = {}
    for token in META_FIELDS:
        m = re.findall(r'^//\s*.*' + token + r':[\t ]*(.*)$', code, re.I + re.M)
        code = re.sub(r'//\s*.*' + token + r':[\t ]*.*\n?', '', code, flags=re.I)
        if m:
            if not m[0] == '':
                infos[token] = m[0]
    return infos


def run_benchmark(iut, code, iterations, runs):
    hex_assembly = assemble_hex(prepare_code(code, iterations))
    p = Popen([iut], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    exec_results = p.communicate(bytes(json.dumps({'iterations': runs, 'code': hex_assembly}), encoding='utf-8'))

    try:
        results = json.loads(exec_results[0].decode("utf-8"))
    except json.decoder.JSONDecodeError:
        print("Unable to read results:")
        print("STDERR: {0}".format(exec_results[1].decode("utf-8")))
        print("STDOUT: {0}".format(exec_results[0].decode("utf-8")))

        raise

    names = {}
    units = {}
    hosts = {}
    df = pd.DataFrame(index=range(0, len(results[0]['values'])))

    for r in results:
        df[r['id']] = pd.DataFrame(r['values'])
        names.update({r['id']: r['name']})
        units.update({r['id']: r['unit']})
        hosts.update({r['id']: r['hostname']})

    # for now we use the gas consumption of the first metric
    df['gas'] = pd.DataFrame(int(value, 0) for value in results[0]['gas'])
    names.update({'gas': 'Gas'})
    units.update({'gas': 'gwei'})
    hosts.update({'gas': results[0]['hostname']})

    df['iterations'] = iterations

    return {'names': names, 'units': units, 'hosts': hosts, 'values': df}


def benchmark(iut, runs, benchmarks_path):
    asm_list = pd.DataFrame(glob.glob(benchmarks_path + os.sep + '**' + os.sep + '*.asm', recursive=True))
    asm_list.set_axis(['asm_path_abs'], axis=1, inplace=True)

    asm_list['asm_path_rel'] = asm_list.apply(lambda r: r['asm_path_abs'][len(benchmarks_path + os.sep):][:-4], axis=1)
    asm_list['code'] = asm_list.apply(lambda current_row: open(current_row['asm_path_abs'], "r").read(), axis=1)

    # Extract infos from code and create rows accordingly
    asm_list = pd.concat([asm_list,
                          asm_list['code'].apply(lambda current_cell: get_infos(current_cell)).to_frame()['code'].apply(
                              pd.Series)], axis=1)
    asm_list = asm_list.reindex(asm_list.columns.union(META_FIELDS, sort=False), axis=1)

    # Generate an ID from the filename if not given in meta data
    asm_list['id'] = asm_list.apply(
        lambda r: reduce((lambda x, y: x + '-' + y),
                         r['asm_path_abs'][len(benchmarks_path + os.sep):].split(os.sep))[:-4] if pd.isnull(r['id']) else r[
            'id'],
        axis=1)

    # Check if IDs are unique
    if not asm_list['id'].is_unique:
        print("Found a duplicated benchmarks:")
        duplicates = asm_list[asm_list.duplicated(subset=['id'], keep=False)]
        print(duplicates[['id', 'asm_path_abs']])
        raise

    # Split iter values to array
    asm_list['iter'] = asm_list['iter'].apply(lambda cell: cell.split(','))

    asm_list['overhead'] = asm_list['overhead'].apply(lambda cell: [] if pd.isnull(cell) else list(map(str.strip, cell.split(','))))

    asm_list['data'] = -1
    asm_list['data'] = asm_list['data'].astype(object)
    asm_list['names'] = asm_list['data'].apply(lambda x: {})
    asm_list['units'] = asm_list['data'].apply(lambda x: {})
    asm_list['hosts'] = asm_list['data'].apply(lambda x: {})

    print("List of Benchmarks:")
    asm_list['asm_path_abs'].apply(lambda asm: print('\t' + asm))
    print("{} runs for each benchmark.".format(runs))

    # we use an iterator here to make absolutely sure everything is sequential
    for index, row in tqdm(asm_list.iterrows(), total=asm_list.shape[0], desc='total'):
        asm_list.at[index, 'data'] = pd.DataFrame()

        for n in tqdm(list(map(int, asm_list.at[index, 'iter'])), desc=row['id']):
            results = run_benchmark(iut, row['code'], n, runs)
            asm_list.at[index, 'units'] = {**row['units'], **results['units']}
            asm_list.at[index, 'names'] = {**row['names'], **results['names']}
            asm_list.at[index, 'hosts'] = {**row['hosts'], **results['hosts']}
            asm_list.at[index, 'data'] = pd.DataFrame(row['data']).append(results['values'])

    return asm_list
