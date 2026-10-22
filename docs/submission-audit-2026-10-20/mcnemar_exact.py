import sys
sys.dont_write_bytecode=True
import json
from pathlib import Path
import argparse
_parser = argparse.ArgumentParser()
_parser.add_argument('--results-dir', type=Path, default=Path(__file__).resolve().parents[2] / 'backend/evaluation/results')
_parser.add_argument('--output-dir', type=Path, default=Path.cwd() / 'audit-output')
_args = _parser.parse_args()
_args.output_dir.mkdir(parents=True, exist_ok=True)
from scipy.stats import binomtest

R=_args.results_dir
def load(name):
    return {x['case_id']:x for x in json.loads((R/name).read_text(encoding='utf-8'))['cases']}
d=load('shared_benchmark_deterministic_experiment.json')
l=load('shared_benchmark_llm_experiment.json')
assert d.keys()==l.keys()
for metric in ['plantuml_validated_success','project_defined_success']:
    table=[[sum(d[k]['final_compile'][metric]==dv and l[k]['final_compile'][metric]==lv for k in d) for lv in [True,False]] for dv in [True,False]]
    b,c=table[0][1],table[1][0]
    p=binomtest(b,n=b+c,p=0.5,alternative='two-sided').pvalue if b+c else 1.0
    print(metric,table,'b=',b,'c=',c,'p=',p)
