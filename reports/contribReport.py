import csv
import json
import os

from Utilities.flatten import flat
from metrics.rowFunctions import add_minus_del, total_contrib
from reports.eventReport import preprocessing, header, applyMetrics

output_csv = "Output/OutContribReport.csv"
output_file = "Output/OutContribReport.json"

def get(config):
    weights = {}
    comments = {}

    #Open special commits and get url of the commits
    if os.path.isfile(config['pathSpecialCommits']):
        with open(config['pathSpecialCommits']) as d_file:
            reader = csv.reader(d_file, quotechar='"')
            for line in reader:
                comment, url, weight = line
                weights[url] = float(weight)
                comments[url] = comment

    # Open config file
    with open('Output/output.json') as data_file:
        data = json.load(data_file)

    tabla = preprocessing(data)


    filtroCommit = lambda f, r: f(r) if r['type'] == 'COMMIT' else None
    weighted_contrib = lambda r : weights[url] * total_contrib(r) if (r['url'] in weights) else total_contrib(r)
    weighted_comment = lambda r : comments[url] if (r['url'] in weights) else ""

    listaFun = [("add_minus_del", add_minus_del),
                ("total_contrib", total_contrib),
                ("weighted_contrib", weighted_contrib),
                ("weighted_comment", weighted_comment)]

    # Apply the defined functions and add to dict as new columns
    tabla = applyMetrics(tabla, listaFun, filtroCommit)

    # Save to json

    with  open(output_file, "w") as toWrite:
        toWrite.write(json.dumps(tabla))

    # Save to csv
    headerExt = header + [columnName for (columnName, fun) in listaFun]
    flat(output_csv, headerExt, tabla)


