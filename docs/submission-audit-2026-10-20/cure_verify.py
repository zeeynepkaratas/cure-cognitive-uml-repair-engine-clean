import sys
sys.dont_write_bytecode=True
import json,csv,re,hashlib,subprocess
from pathlib import Path
import argparse
_parser = argparse.ArgumentParser()
_parser.add_argument('--results-dir', type=Path, default=Path(__file__).resolve().parents[2] / 'backend/evaluation/results')
_parser.add_argument('--output-dir', type=Path, default=Path.cwd() / 'audit-output')
_args = _parser.parse_args()
_args.output_dir.mkdir(parents=True, exist_ok=True)
R=Path(__file__).resolve().parents[2]
O=_args.output_dir
report={}
for prefix in ['shared_benchmark','pure_external']:
    for method in ['llm','deterministic']:
        stem=prefix+'_'+method+'_experiment'
        p=_args.results_dir
        j=json.loads((p/(stem+'.json')).read_text(encoding='utf-8'))
        c=list(csv.DictReader((p/(stem+'.csv')).open(encoding='utf-8',newline='')))
        cm={x['case_id']:x for x in c}
        mdlines=(p/(stem+'.md')).read_text(encoding='utf-8').splitlines()
        mdrows={parts[0]:(n,parts) for n,line in enumerate(mdlines,1) if re.match(r'^\| [SP]\d\d \|',line) for parts in [[x.strip() for x in line.strip('|').split('|')]]}
        issues=[]
        for x in j['cases']:
            cid=x['case_id'];y=cm[cid]
            pf='project_defined_basarili' if method=='llm' else 'project_defined_final_success'
            vf='plantuml_validated_basarili' if method=='llm' else 'plantuml_validated_final_success'
            for f,actual in [(pf,x['final_compile']['project_defined_success']),(vf,x['final_compile']['plantuml_validated_success'])]:
                if y[f]!=str(actual):issues.append([cid,f,y[f],actual])
            tf='sure_saniye' if method=='llm' else 'elapsed_seconds'
            if float(y[tf])!=x[tf]:issues.append([cid,tf])
            md=mdrows[cid][1]
            idx=3 if prefix=='shared_benchmark' and method=='deterministic' else 2 if prefix=='shared_benchmark' else 3
            if md[idx]!=str(x['final_compile']['project_defined_success']) or md[idx+1]!=str(x['final_compile']['plantuml_validated_success']):issues.append([cid,'MD validity',md])
            if prefix=='pure_external':
                for metric in ['class_f1','relationship_f1']:
                    if float(y[metric])!=x['reference_metrics'][metric]:issues.append([cid,metric])
        report[stem]={'json_rows':len(j['cases']),'csv_rows':len(c),'md_rows':len(mdrows),'differences':issues}
shared=json.loads((R/'backend/evaluation/results/shared_benchmark_deterministic_experiment.json').read_text())['cases']
pure=json.loads((R/'backend/evaluation/results/pure_external_llm_experiment.json').read_text())['cases']
baseline=list(csv.DictReader((O/'baseline_none.csv').open(encoding='utf-8')))
old={x['case_id']:x['initial_compile']['plantuml_validated_success'] for x in shared}
old.update({x['case_id']:x['raw_response']['iterasyonlar'][0]['compile_result']['plantuml_validated_success'] for x in pure})
report['fresh_baseline_vs_retained_initial_runtime']={'differences':[x['case_id'] for x in baseline if str(old[x['case_id']])!=x['plantuml_valid']]}
report['repo_verification']={}
for args in [['git','diff','--exit-code'],['git','status','--short']]:
    p=subprocess.run(args,cwd=R,capture_output=True,text=True)
    report['repo_verification'][' '.join(args)]={'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
names=['cure_audit.py','cure_verify.py','cases.csv','baseline_none.csv','baseline_runtime_raw.json','audit_results.json','audit_stdout.txt','audit_stderr.txt','source_evidence.txt','pure_counts.csv','CURE_README_paper-submission-v2.md']
report['files']=[{'path':str(O/name),'bytes':(O/name).stat().st_size,'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest()} for name in names]
(O/'crosscheck.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
