# Based on Oxigraph's analysis script: https://github.com/oxigraph/oxigraph/blob/main/bench/bsbm-plot.py

import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from collections import defaultdict
from glob import glob
from numpy import array
import sys

def plot_y_per_x_per_plot(data, xlabel, ylabel, file, log=False):
    plt.figure(file)

    bar_width = 1 / (len(data) + 1)
    for i, (label, xys) in enumerate(sorted(data.items())):
        plt.bar(array(list(xys.keys())) + bar_width * (i + 1 - len(data) / 2), array(list(xys.values())), bar_width,
                label=label)

    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.yscale('log')
    if log:
        plt.yscale('log')
    plt.savefig(file)


def plot_usecase(results_dir, name):
    aqet = defaultdict(dict)
    avgresults_by_query = defaultdict(lambda: defaultdict(dict))
    for file in glob(f'{results_dir}/{name}/*.xml'):
        run = file
        for query in ET.parse(file).getroot().find('queries').findall('query'):
            query_id = int(query.attrib['nr'])
            for child in query.iter():
                if child.tag == "aqet":
                    val = float(query.find('aqet').text)
                    if val > 0:
                        aqet[run][query_id] = val
                elif child.tag == "avgresults":
                    # TDOO load size
                    avgresults_by_query[query_id][10000][run] = float(query.find('avgresults').text)
    plot_y_per_x_per_plot(aqet, 'Query', 'Average Query Execution Time (s)', f"{results_dir}/{name}/bsbm.{name}.svg")

    # we check if avgresults seems consistent
    for query, t in avgresults_by_query.items():
        for size, value_by_run in t.items():
            avg = sum(value_by_run.values()) / len(value_by_run)
            if not all(abs(v - avg) < 1 for v in value_by_run.values()):
                print(
                    f'Strange value for average results for usecase {name} of size {size} and query {query}: {value_by_run}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <results_dir> <usecase>")
        sys.exit(1)
    results_dir = sys.argv[1]
    name = sys.argv[2]
    plot_usecase(results_dir, name)