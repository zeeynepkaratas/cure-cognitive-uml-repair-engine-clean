import sys
sys.dont_write_bytecode = True
import os, json, csv, statistics, hashlib, ast, collections, subprocess
from pathlib import Path

ROOT=Path(r'C:/Users/zeyne/Documents/Codex/2026-10-20/https-github-com-zeeynepkaratas-cure-cognitive/work/repo')
OUT=Path('C:/tmp')
sys.path.insert(0,str(ROOT/'backend/src'))
sys.path.insert(0,str(ROOT/'backend/evaluation'))
from evaluators.semantic_eval import calculate_semantic_fidelity, extract_srs_entities, extract_uml_entities
from ocl_engine.error_handler import plantuml_syntax_kontrol
from ocl_engine.ocl_validator import validate_ocl
from pure_external_metrics import compare_to_reference

def literal_cases(filename,name):
    tree=ast.parse((ROOT/'backend/evaluation'/filename).read_text(encoding='utf-8'))
    return next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))

sources={}
for dataset,prefix in [('shared','shared_benchmark'),('pure','pure_external')]:
    for method in ['llm','deterministic']:
        rel=f'backend/evaluation/results/{prefix}_{method}_experiment.json'
        obj=json.loads((ROOT/rel).read_text(encoding='utf-8'))
        sources[dataset,method]=(rel,obj)

def source_line(rel,case_id):
    lines=(ROOT/rel).read_text(encoding='utf-8').splitlines()
    return next(i for i,l in enumerate(lines,1) if f'"case_id": "{case_id}"' in l)

rows=[]
for (dataset,method),(rel,obj) in sources.items():
    for c in obj['cases']:
        fc=c['final_compile']; m=c.get('reference_metrics',{})
        rows.append(dict(dataset=dataset,method=method,case_id=c['case_id'],
           project_valid=fc['project_defined_success'],plantuml_valid=fc['plantuml_validated_success'],
           agent_is_valid=c.get('agent_is_valid',''),agent_repair_attempt_count=c.get('agent_repair_attempt_count',''),
           time_field='sure_saniye' if method=='llm' else 'elapsed_seconds',
           time_seconds=c['sure_saniye'] if method=='llm' else c['elapsed_seconds'],
           class_f1=m.get('class_f1',''),rel_f1=m.get('relationship_f1','')))
with (OUT/'cases.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

result={}
shared=sources['shared','llm'][1]['cases']
for metric in ['project_defined_success','plantuml_validated_success']:
    matrix={str(critic):{str(valid):sum(c['agent_is_valid']==critic and c['final_compile'][metric]==valid for c in shared) for valid in [True,False]} for critic in [True,False]}
    result['critic_x_'+metric]=matrix
result['critic_true_cases']=[{'case_id':c['case_id'],'project':c['final_compile']['project_defined_success'],'plantuml':c['final_compile']['plantuml_validated_success'],'attempts':c['agent_repair_attempt_count']} for c in shared if c['agent_is_valid']]
result['S43']={k:next(c for c in shared if c['case_id']=='S43')[k] for k in ['agent_is_valid','agent_repair_attempt_count']}
result['budget']={}
for dataset in ['shared','pure']:
    obj=sources[dataset,'llm'][1]; cs=obj['cases']; cap=obj['metadata']['max_iterations']
    result['budget'][dataset]={'max_iterations':cap,'attempts_at_cap':sum(c['agent_repair_attempt_count']==cap for c in cs),'at_cap_and_invalid':sum(c['agent_repair_attempt_count']==cap and not c['agent_is_valid'] for c in cs),'attempt_distribution':dict(collections.Counter(c['agent_repair_attempt_count'] for c in cs))}

from scipy.stats import binomtest
result['scipy_version']=__import__('scipy').__version__
for metric in ['project_defined_success','plantuml_validated_success']:
    det={c['case_id']:c for c in sources['shared','deterministic'][1]['cases']}
    llm={c['case_id']:c for c in shared}
    table=[[sum(det[k]['final_compile'][metric]==d and llm[k]['final_compile'][metric]==l for k in det) for l in [True,False]] for d in [True,False]]
    b,c=table[0][1],table[1][0]
    result['mcnemar_'+metric]={'table_rows_det_T_F_cols_llm_T_F':table,'b':b,'c':c,'p_exact_two_sided':binomtest(b,b+c,p=0.5,alternative='two-sided').pvalue if b+c else 1.0}

s02=next(c for c in shared if c['case_id']=='S02')
evaluation=calculate_semantic_fidelity(s02['srs_metni'],s02['final_plantuml'])
result['S02']={'source_line':source_line(sources['shared','llm'][0],'S02'),'srs':s02['srs_metni'],'final_plantuml':s02['final_plantuml'],'calculated':evaluation,'stored':s02.get('raw_response',{}).get('semantik')}

pure_rows=[]; result['pure_differences']={}
for l in sources['pure','llm'][1]['cases']:
    d=next(c for c in sources['pure','deterministic'][1]['cases'] if c['case_id']==l['case_id'])
    lm=compare_to_reference(l['reference_plantuml'],l['final_plantuml'])
    dm=compare_to_reference(d['reference_plantuml'],d['final_plantuml'])
    pure_rows.append({'case_id':l['case_id'],'pure_row':l['pure_row'],'reference_class_count':lm['reference_class_count'],'reference_relationship_count':lm['reference_relationship_count'],'llm_class_count':lm['repaired_class_count'],'llm_relationship_count':lm['repaired_relationship_count'],'det_class_count':dm['repaired_class_count'],'det_relationship_count':dm['repaired_relationship_count'],'llm_class_f1':lm['class_f1'],'llm_rel_f1':lm['relationship_f1']})
    result['pure_differences'][l['case_id']]={'llm':lm,'deterministic':dm,'llm_source_line':source_line(sources['pure','llm'][0],l['case_id']),'det_source_line':source_line(sources['pure','deterministic'][0],l['case_id'])}
    if l['case_id']=='P07':
        result['P07']={'reference':l['reference_plantuml'],'llm':l['final_plantuml']}
with (OUT/'pure_counts.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(pure_rows[0]));w.writeheader();w.writerows(pure_rows)
result['pure_counts']=pure_rows
result['pure_stats']={}
for method in ['llm','deterministic']:
    for exclude in [False,True]:
        cs=[c for c in sources['pure',method][1]['cases'] if not(exclude and c['case_id']=='P04')]
        result['pure_stats'][f'{method}_exclude_P04_{exclude}']={}
        for metric in ['class_f1','relationship_f1']:
            vals=[c['reference_metrics'][metric] for c in cs]
            result['pure_stats'][f'{method}_exclude_P04_{exclude}'][metric]={'n':len(vals),'mean':statistics.mean(vals),'std_sample_ddof1':statistics.stdev(vals),'std_population_ddof0':statistics.pstdev(vals),'min':min(vals),'max':max(vals)}

sc=literal_cases('shared_repair_benchmark_cases.py','SHARED_REPAIR_BENCHMARK_CASES')
pc=literal_cases('pure_external_repair_cases.py','PURE_EXTERNAL_REPAIR_CASES')
result['categories']=dict(collections.Counter(c['category'] for c in sc))
result['pure_rows']={c['case_id']:c['pure_row'] for c in pc}

# No repair; only the two exact validators used by repository compile_check.
jar=os.environ.get('CURE_AUDIT_JAR')
result['jar']={'path':jar,'sha256':hashlib.sha256(Path(jar).read_bytes()).hexdigest().upper()} if jar else {'status':'BULUNAMADI'}
if jar:
    os.environ['PLANTUML_JAR']=jar
    from plantuml_runtime import validate_with_plantuml
    v=subprocess.run(['java','-jar',jar,'-version'],capture_output=True,text=True)
    result['jar']['version_stdout']=v.stdout;result['jar']['version_stderr']=v.stderr
    os.environ['TMP']=str(OUT);os.environ['TEMP']=str(OUT)
    import tempfile
    tempfile.tempdir=str(OUT)
baseline=[]; raw_runtime={}
for dataset,cs in [('shared',sc),('pure',pc)]:
    for c in cs:
        code=c.get('plantuml_kodu',c.get('initial_plantuml'))
        syntax=plantuml_syntax_kontrol(code);ocl=validate_ocl(code)
        runtime=validate_with_plantuml(code) if jar else {'available':False,'successful':None,'errors':['BULUNAMADI: local PlantUML JAR']}
        baseline.append({'dataset':dataset,'case_id':c['case_id'],'project_valid':syntax['gecerli'] and ocl['gecerli_mi'],'plantuml_valid':runtime['successful'] if jar else 'BULUNAMADI'})
        raw_runtime[c['case_id']]={'project_syntax':syntax,'project_ocl':ocl,'runtime':runtime}
with (OUT/'baseline_none.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(baseline[0]));w.writeheader();w.writerows(baseline)
(OUT/'baseline_runtime_raw.json').write_text(json.dumps(raw_runtime,ensure_ascii=False,indent=2),encoding='utf-8')
result['baseline']={dataset:{'n':len(cs),'project_valid':sum(c['project_valid'] for c in baseline if c['dataset']==dataset),'plantuml_valid':sum(c['plantuml_valid'] is True for c in baseline if c['dataset']==dataset) if jar else 'BULUNAMADI','plantuml_passing_ids':[c['case_id'] for c in baseline if c['dataset']==dataset and c['plantuml_valid'] is True]} for dataset,cs in [('shared',sc),('pure',pc)]}

result['summary_recomputed']={}
for (dataset,method),(rel,obj) in sources.items():
    cs=obj['cases']
    result['summary_recomputed'][dataset+'_'+method]={'n':len(cs),'project_valid':sum(c['final_compile']['project_defined_success'] for c in cs),'plantuml_valid':sum(c['final_compile']['plantuml_validated_success'] is True for c in cs),'critic_valid':sum(c.get('agent_is_valid') is True for c in cs) if method=='llm' else None,'mean_time':statistics.mean(c['sure_saniye'] if method=='llm' else c['elapsed_seconds'] for c in cs)}
    result['summary_recomputed'][dataset+'_'+method]['source']=rel
result['case_source_lines']={dataset+'_'+method:{c['case_id']:source_line(rel,c['case_id']) for c in obj['cases']} for (dataset,method),(rel,obj) in sources.items()}

files=['backend/src/evaluators/semantic_eval.py','backend/src/utils/plantuml_parser.py','backend/src/ocl_engine/ocl_validator.py','backend/src/ocl_engine/error_handler.py','backend/src/plantuml_runtime.py','backend/evaluation/repair_benchmark_utils.py','backend/evaluation/shared_repair_benchmark_cases.py','backend/evaluation/pure_external_repair_cases.py','backend/src/api/endpoints.py','ai_core/src/ai/agent_workflow.py','ai_core/src/rag/ocl_retriever.py','ai_core/src/ai/workflow_control.py','docs/final-experiment-report.md','docs/features/pure-external-pilot.md','data_pipeline/README.md','data_pipeline/preprocessing/xml_to_csv.py']
with (OUT/'source_evidence.txt').open('w',encoding='utf-8') as f:
    for rel in files:
        f.write('\n### '+rel+'\n')
        for n,line in enumerate((ROOT/rel).read_text(encoding='utf-8').splitlines(),1):f.write(f'{rel}:{n}: {line}\n')
    rel='README.md@paper-submission-v2'
    for n,line in enumerate((OUT/'CURE_README_paper-submission-v2.md').read_text(encoding='utf-8').splitlines(),1):f.write(f'{rel}:{n}: {line}\n')
(OUT/'audit_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True,indent=2))
