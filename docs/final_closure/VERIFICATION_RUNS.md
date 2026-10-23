# Executed final verification

Times are Europe/Istanbul (+03:00); exact recorded exit codes, stdout/stderr and durations are retained. Network was used only for authorized dependency installation. No model calls.

## help tools/finalize_v4.py — PASS

Command: `../closure-clean-env/Scripts/python.exe tools/finalize_v4.py --help`; cwd `.`.

Start `2026-10-23T21:24:41.226726+03:00`; finish `2026-10-23T21:24:53.851034+03:00`; exit `0`.

stdout:
```text
usage: finalize_v4.py [-h] --run-dir RUN_DIR --audit-dir AUDIT_DIR

Derive and audit a complete frozen matrix. No model/API calls or Git
mutations.

options:
  -h, --help            show this help message and exit
  --run-dir RUN_DIR
  --audit-dir AUDIT_DIR
```

stderr:
```text

```

## help tools/check_numbers.py — PASS

Command: `../closure-clean-env/Scripts/python.exe tools/check_numbers.py --help`; cwd `.`.

Start `2026-10-23T21:24:53.852036+03:00`; finish `2026-10-23T21:24:56.151614+03:00`; exit `0`.

stdout:
```text
usage: check_numbers.py [-h] --run-dir RUN_DIR

Recompute all derived v4 numbers from retained raw cases and verify hashes.

options:
  -h, --help         show this help message and exit
  --run-dir RUN_DIR
```

stderr:
```text

```

## help tools/verify_retained_evidence.py — PASS

Command: `../closure-clean-env/Scripts/python.exe tools/verify_retained_evidence.py --help`; cwd `.`.

Start `2026-10-23T21:24:56.152647+03:00`; finish `2026-10-23T21:24:56.352427+03:00`; exit `0`.

stdout:
```text
usage: verify_retained_evidence.py [-h] --output OUTPUT

Read-only verification against the v3 evidence baseline.

options:
  -h, --help       show this help message and exit
  --output OUTPUT
```

stderr:
```text

```

## independent and preservation verification — PASS

Command: `../closure-clean-env/Scripts/python.exe tools/verify_v4_artifact.py --output docs/final_closure/verification`; cwd `.`.

Start `2026-10-23T21:24:56.352427+03:00`; finish `2026-10-23T21:26:04.688535+03:00`; exit `0`.

stdout:
```text
{"checks": 13, "failed": [], "paired_comparisons": 208}
{"status": "PASS", "protected_files": 4660, "changed": [], "read_only_numbers": {"status": "passed", "raw_case_runs": 2800, "all_derived_numbers_recomputed": true}, "generation_freeze": "PASS", "model_calls": 0}
```

stderr:
```text

```

## original check_numbers CLI — PASS

Command: `../closure-clean-env/Scripts/python.exe tools/check_numbers.py --run-dir backend/evaluation/results_v4/test-frozen-20261022`; cwd `.`.

Start `2026-10-23T21:26:04.689557+03:00`; finish `2026-10-23T21:27:04.318505+03:00`; exit `0`.

stdout:
```text
{"status": "passed", "raw_case_runs": 2800, "all_derived_numbers_recomputed": true}
```

stderr:
```text

```

## original retained verifier CLI — PASS

Command: `../closure-clean-env/Scripts/python.exe tools/verify_retained_evidence.py --output docs/final_closure/RETAINED_VERIFICATION.json`; cwd `.`.

Start `2026-10-23T21:27:04.320487+03:00`; finish `2026-10-23T21:27:07.284604+03:00`; exit `0`.

stdout:
```text
{"base_commit": "b9bee1d78bbdda14d9a1b07585f865b18aa5ef0d", "status": "passed", "protected_file_count": 51, "original_pure_csv": "identical content; line-ending normalisation allowed", "clarification": "The A1 report is the historical sanitization log; its after-hashes describe that stage. This report verifies the current state independently against v3."}
```

stderr:
```text

```

## fresh Python venv — PASS

Command: `../closure-clean-env/Scripts/python.exe -m venv ../final-close-env`; cwd `.`.

Start `2026-10-23T21:24:43.818364+03:00`; finish `2026-10-23T21:24:59.271801+03:00`; exit `0`.

stdout:
```text

```

stderr:
```text

```

## fresh locked Python install — PASS

Command: `../final-close-env/Scripts/python.exe -m pip --isolated install --index-url https://pypi.org/simple -r requirements.lock.txt -r requirements-dev.txt --disable-pip-version-check`; cwd `.`.

Start `2026-10-23T21:24:59.272800+03:00`; finish `2026-10-23T21:30:46.877296+03:00`; exit `0`.

stdout:
```text
Collecting aiohappyeyeballs==2.7.1 (from -r requirements.lock.txt (line 1))
  Using cached aiohappyeyeballs-2.7.1-py3-none-any.whl.metadata (5.9 kB)
Collecting aiohttp==3.14.5 (from -r requirements.lock.txt (line 2))
  Using cached aiohttp-3.14.5-cp312-cp312-win_amd64.whl.metadata (8.5 kB)
Collecting aiosignal==1.4.0 (from -r requirements.lock.txt (line 3))
  Using cached aiosignal-1.4.0-py3-none-any.whl.metadata (3.7 kB)
Collecting annotated-doc==0.0.5 (from -r requirements.lock.txt (line 4))
  Using cached annotated_doc-0.0.5-py3-none-any.whl.metadata (6.5 kB)
Collecting annotated-types==0.8.0 (from -r requirements.lock.txt (line 5))
  Using cached annotated_types-0.8.0-py3-none-any.whl.metadata (15 kB)
Collecting anyio==4.15.1 (from -r requirements.lock.txt (line 6))
  Using cached anyio-4.15.1-py3-none-any.whl.metadata (4.7 kB)
Collecting attrs==26.1.0 (from -r requirements.lock.txt (line 7))
  Using cached attrs-26.1.0-py3-none-any.whl.metadata (8.8 kB)
Collecting certifi==2026.10.19 (from -r requirements.lock.txt (line 8))
  Using cached certifi-2026.10.19-py3-none-any.whl.metadata (2.5 kB)
Collecting charset-normalizer==3.5.2 (from -r requirements.lock.txt (line 9))
  Using cached charset_normalizer-3.5.2-cp312-cp312-win_amd64.whl.metadata (47 kB)
Collecting click==8.5.0 (from -r requirements.lock.txt (line 10))
  Using cached click-8.5.0-py3-none-any.whl.metadata (2.6 kB)
Collecting cloudpickle==3.1.2 (from -r requirements.lock.txt (line 11))
  Using cached cloudpickle-3.1.2-py3-none-any.whl.metadata (7.1 kB)
Collecting colorama==0.4.6 (from -r requirements.lock.txt (line 12))
  Using cached colorama-0.4.6-py2.py3-none-any.whl.metadata (17 kB)
Collecting contourpy==1.4.0 (from -r requirements.lock.txt (line 13))
  Using cached contourpy-1.4.0-cp312-cp312-win_amd64.whl.metadata (3.8 kB)
Collecting cycler==0.12.1 (from -r requirements.lock.txt (line 14))
  Using cached cycler-0.12.1-py3-none-any.whl.metadata (3.8 kB)
Collecting distro==1.9.0 (from -r requirements.lock.txt (line 15))
  Using cached distro-1.9.0-py3-none-any.whl.metadata (6.8 kB)
Collecting faiss-cpu==1.15.1 (from -r requirements.lock.txt (line 16))
  Using cached faiss_cpu-1.15.1-cp312-cp312-win_amd64.whl.metadata (7.8 kB)
Collecting fastapi==0.159.1 (from -r requirements.lock.txt (line 17))
  Using cached fastapi-0.159.1-py3-none-any.whl.metadata (26 kB)
Collecting fonttools==4.67.0 (from -r requirements.lock.txt (line 18))
  Using cached fonttools-4.67.0-cp312-cp312-win_amd64.whl.metadata (139 kB)
Collecting frozenlist==1.8.0 (from -r requirements.lock.txt (line 19))
  Using cached frozenlist-1.8.0-cp312-cp312-win_amd64.whl.metadata (21 kB)
Collecting h11==0.16.0 (from -r requirements.lock.txt (line 20))
  Using cached h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting httpcore==1.0.9 (from -r requirements.lock.txt (line 21))
  Using cached httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Collecting httpcore2==2.16.0 (from -r requirements.lock.txt (line 22))
  Using cached httpcore2-2.16.0-py3-none-any.whl.metadata (27 kB)
Collecting httpx==0.28.1 (from -r requirements.lock.txt (line 23))
  Using cached httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting httpx-sse==0.4.3 (from -r requirements.lock.txt (line 24))
  Using cached httpx_sse-0.4.3-py3-none-any.whl.metadata (9.7 kB)
Collecting httpx2==2.16.0 (from -r requirements.lock.txt (line 25))
  Using cached httpx2-2.16.0-py3-none-any.whl.metadata (10 kB)
Collecting idna==3.20 (from -r requirements.lock.txt (line 26))
  Using cached idna-3.20-py3-none-any.whl.metadata (7.2 kB)
Collecting iniconfig==2.3.1 (from -r requirements.lock.txt (line 27))
  Using cached iniconfig-2.3.1-py3-none-any.whl.metadata (2.8 kB)
Collecting jiter==0.17.0 (from -r requirements.lock.txt (line 28))
  Using cached jiter-0.17.0-cp312-cp312-win_amd64.whl.metadata (5.3 kB)
Collecting joblib==1.6.0 (from -r requirements.lock.txt (line 29))
  Using cached joblib-1.6.0-py3-none-any.whl.metadata (6.5 kB)
Collecting jsonpatch==1.36 (from -r requirements.lock.txt (line 30))
  Using cached jsonpatch-1.36-py3-none-any.whl.metadata (3.7 kB)
Collecting jsonpointer==3.4 (from -r requirements.lock.txt (line 31))
  Using cached jsonpointer-3.4-py3-none-any.whl.metadata (2.6 kB)
Collecting kiwisolver==1.5.1 (from -r requirements.lock.txt (line 32))
  Using cached kiwisolver-1.5.1-cp312-cp312-win_amd64.whl.metadata (5.2 kB)
Collecting langchain==1.4.7 (from -r requirements.lock.txt (line 33))
  Using cached langchain-1.4.7-py3-none-any.whl.metadata (6.2 kB)
Collecting langchain-classic==1.0.8 (from -r requirements.lock.txt (line 34))
  Using cached langchain_classic-1.0.8-py3-none-any.whl.metadata (5.1 kB)
Collecting langchain-community==0.4.2 (from -r requirements.lock.txt (line 35))
  Using cached langchain_community-0.4.2-py3-none-any.whl.metadata (3.4 kB)
Collecting langchain-core==1.6.13 (from -r requirements.lock.txt (line 36))
  Using cached langchain_core-1.6.13-py3-none-any.whl.metadata (4.8 kB)
Collecting langchain-openai==1.7.2 (from -r requirements.lock.txt (line 37))
  Using cached langchain_openai-1.7.2-py3-none-any.whl.metadata (3.6 kB)
Collecting langchain-protocol==0.0.20 (from -r requirements.lock.txt (line 38))
  Using cached langchain_protocol-0.0.20-py3-none-any.whl.metadata (2.4 kB)
Collecting langchain-text-splitters==1.1.3 (from -r requirements.lock.txt (line 39))
  Using cached langchain_text_splitters-1.1.3-py3-none-any.whl.metadata (3.6 kB)
Collecting langgraph==1.2.16 (from -r requirements.lock.txt (line 40))
  Using cached langgraph-1.2.16-py3-none-any.whl.metadata (4.9 kB)
Collecting langgraph-checkpoint==4.3.0 (from -r requirements.lock.txt (line 41))
  Using cached langgraph_checkpoint-4.3.0-py3-none-any.whl.metadata (6.7 kB)
Collecting langgraph-prebuilt==1.1.1 (from -r requirements.lock.txt (line 42))
  Using cached langgraph_prebuilt-1.1.1-py3-none-any.whl.metadata (6.9 kB)
Collecting langgraph-sdk==0.4.8 (from -r requirements.lock.txt (line 43))
  Using cached langgraph_sdk-0.4.8-py3-none-any.whl.metadata (5.1 kB)
Collecting langsmith==0.14.12 (from -r requirements.lock.txt (line 44))
  Using cached langsmith-0.14.12-py3-none-any.whl.metadata (38 kB)
Collecting matplotlib==3.11.2 (from -r requirements.lock.txt (line 45))
  Using cached matplotlib-3.11.2-cp312-cp312-win_amd64.whl.metadata (80 kB)
Collecting multidict==7.1.0 (from -r requirements.lock.txt (line 46))
  Using cached multidict-7.1.0-cp312-cp312-win_amd64.whl.metadata (6.4 kB)
Collecting nltk==3.9.2 (from -r requirements.lock.txt (line 47))
  Using cached nltk-3.9.2-py3-none-any.whl.metadata (3.2 kB)
Collecting numpy==2.5.4 (from -r requirements.lock.txt (line 48))
  Using cached numpy-2.5.4-cp312-cp312-win_amd64.whl.metadata (6.6 kB)
Collecting openai==3.36.0 (from -r requirements.lock.txt (line 49))
  Using cached openai-3.36.0-py3-none-any.whl.metadata (44 kB)
Collecting opentelemetry-api==1.45.1 (from -r requirements.lock.txt (line 50))
  Using cached opentelemetry_api-1.45.1-py3-none-any.whl.metadata (1.4 kB)
Collecting orjson==3.13.0 (from -r requirements.lock.txt (line 51))
  Using cached orjson-3.13.0-cp312-cp312-win_amd64.whl.metadata (43 kB)
Collecting ormsgpack==1.13.0 (from -r requirements.lock.txt (line 52))
  Using cached ormsgpack-1.13.0-cp312-cp312-win_amd64.whl.metadata (3.3 kB)
Collecting packaging==26.3 (from -r requirements.lock.txt (line 53))
  Using cached packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
Collecting pillow==13.0.0 (from -r requirements.lock.txt (line 54))
  Using cached pillow-13.0.0-cp312-cp312-win_amd64.whl.metadata (9.3 kB)
Collecting pluggy==1.7.0 (from -r requirements.lock.txt (line 55))
  Using cached pluggy-1.7.0-py3-none-any.whl.metadata (5.0 kB)
Collecting propcache==0.5.4 (from -r requirements.lock.txt (line 56))
  Using cached propcache-0.5.4-cp312-cp312-win_amd64.whl.metadata (25 kB)
Collecting pydantic==2.14.1 (from -r requirements.lock.txt (line 57))
  Using cached pydantic-2.14.1-py3-none-any.whl.metadata (133 kB)
Collecting pydantic-settings==2.16.1 (from -r requirements.lock.txt (line 58))
  Using cached pydantic_settings-2.16.1-py3-none-any.whl.metadata (4.0 kB)
Collecting pydantic_core==2.50.1 (from -r requirements.lock.txt (line 59))
  Using cached pydantic_core-2.50.1-cp312-cp312-win_amd64.whl.metadata (6.7 kB)
Collecting Pygments==2.21.0 (from -r requirements.lock.txt (line 60))
  Using cached pygments-2.21.0-py3-none-any.whl.metadata (2.5 kB)
Collecting pyparsing==3.3.3 (from -r requirements.lock.txt (line 61))
  Using cached pyparsing-3.3.3-py3-none-any.whl.metadata (5.9 kB)
Collecting pytest==9.1.1 (from -r requirements.lock.txt (line 62))
  Using cached pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
Collecting python-dateutil==2.9.0.post0 (from -r requirements.lock.txt (line 63))
  Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting python-dotenv==1.2.4 (from -r requirements.lock.txt (line 64))
  Using cached python_dotenv-1.2.4-py3-none-any.whl.metadata (29 kB)
Collecting PyYAML==6.0.3 (from -r requirements.lock.txt (line 65))
  Using cached pyyaml-6.0.3-cp312-cp312-win_amd64.whl.metadata (2.4 kB)
Collecting regex==2026.9.29 (from -r requirements.lock.txt (line 66))
  Using cached regex-2026.9.29-cp312-cp312-win_amd64.whl.metadata (41 kB)
Collecting requests==2.34.2 (from -r requirements.lock.txt (line 67))
  Using cached requests-2.34.2-py3-none-any.whl.metadata (4.8 kB)
Collecting requests-toolbelt==1.0.0 (from -r requirements.lock.txt (line 68))
  Using cached requests_toolbelt-1.0.0-py2.py3-none-any.whl.metadata (14 kB)
Collecting ruff==0.17.1 (from -r requirements.lock.txt (line 69))
  Using cached ruff-0.17.1-py3-none-win_amd64.whl.metadata (21 kB)
Collecting scipy==1.18.1 (from -r requirements.lock.txt (line 70))
  Using cached scipy-1.18.1-cp312-cp312-win_amd64.whl.metadata (61 kB)
Collecting six==1.17.0 (from -r requirements.lock.txt (line 71))
  Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Collecting sniffio==1.3.1 (from -r requirements.lock.txt (line 72))
  Using cached sniffio-1.3.1-py3-none-any.whl.metadata (3.9 kB)
Collecting SQLAlchemy==2.1.6 (from -r requirements.lock.txt (line 73))
  Using cached sqlalchemy-2.1.6-cp312-cp312-win_amd64.whl.metadata (9.9 kB)
Collecting starlette==1.9.0 (from -r requirements.lock.txt (line 74))
  Using cached starlette-1.9.0-py3-none-any.whl.metadata (6.6 kB)
Collecting tenacity==9.2.1 (from -r requirements.lock.txt (line 75))
  Using cached tenacity-9.2.1-py3-none-any.whl.metadata (1.4 kB)
Collecting tiktoken==0.14.0 (from -r requirements.lock.txt (line 76))
  Using cached tiktoken-0.14.0-cp312-cp312-win_amd64.whl.metadata (6.8 kB)
Collecting tqdm==4.70.1 (from -r requirements.lock.txt (line 77))
  Using cached tqdm-4.70.1-py3-none-any.whl.metadata (57 kB)
Collecting truststore==0.10.5 (from -r requirements.lock.txt (line 78))
  Using cached truststore-0.10.5-py3-none-any.whl.metadata (4.5 kB)
Collecting typing-inspection==0.4.4 (from -r requirements.lock.txt (line 79))
  Using cached typing_inspection-0.4.4-py3-none-any.whl.metadata (2.6 kB)
Collecting typing_extensions==4.16.0 (from -r requirements.lock.txt (line 80))
  Using cached typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Collecting urllib3==2.8.0 (from -r requirements.lock.txt (line 81))
  Using cached urllib3-2.8.0-py3-none-any.whl.metadata (7.4 kB)
Collecting uuid_utils==0.18.0 (from -r requirements.lock.txt (line 82))
  Using cached uuid_utils-0.18.0-cp312-cp312-win_amd64.whl.metadata (6.5 kB)
Collecting uvicorn==0.54.0 (from -r requirements.lock.txt (line 83))
  Using cached uvicorn-0.54.0-py3-none-any.whl.metadata (6.6 kB)
Collecting websockets==16.1.1 (from -r requirements.lock.txt (line 84))
  Using cached websockets-16.1.1-cp312-cp312-win_amd64.whl.metadata (7.0 kB)
Collecting xxhash==4.0.2 (from -r requirements.lock.txt (line 85))
  Using cached xxhash-4.0.2-cp312-cp312-win_amd64.whl.metadata (18 kB)
Collecting yarl==1.25.1 (from -r requirements.lock.txt (line 86))
  Using cached yarl-1.25.1-cp312-cp312-win_amd64.whl.metadata (115 kB)
Collecting zstandard==0.25.0 (from -r requirements.lock.txt (line 87))
  Using cached zstandard-0.25.0-cp312-cp312-win_amd64.whl.metadata (3.3 kB)
Using cached aiohappyeyeballs-2.7.1-py3-none-any.whl (15 kB)
Using cached aiohttp-3.14.5-cp312-cp312-win_amd64.whl (506 kB)
Using cached aiosignal-1.4.0-py3-none-any.whl (7.5 kB)
Using cached annotated_doc-0.0.5-py3-none-any.whl (5.3 kB)
Using cached annotated_types-0.8.0-py3-none-any.whl (13 kB)
Using cached anyio-4.15.1-py3-none-any.whl (132 kB)
Using cached attrs-26.1.0-py3-none-any.whl (67 kB)
Using cached certifi-2026.10.19-py3-none-any.whl (136 kB)
Using cached charset_normalizer-3.5.2-cp312-cp312-win_amd64.whl (207 kB)
Using cached click-8.5.0-py3-none-any.whl (125 kB)
Using cached cloudpickle-3.1.2-py3-none-any.whl (22 kB)
Using cached colorama-0.4.6-py2.py3-none-any.whl (25 kB)
Using cached contourpy-1.4.0-cp312-cp312-win_amd64.whl (234 kB)
Using cached cycler-0.12.1-py3-none-any.whl (8.3 kB)
Using cached distro-1.9.0-py3-none-any.whl (20 kB)
Using cached faiss_cpu-1.15.1-cp312-cp312-win_amd64.whl (16.3 MB)
Using cached fastapi-0.159.1-py3-none-any.whl (149 kB)
Using cached fonttools-4.67.0-cp312-cp312-win_amd64.whl (2.5 MB)
Using cached frozenlist-1.8.0-cp312-cp312-win_amd64.whl (44 kB)
Using cached h11-0.16.0-py3-none-any.whl (37 kB)
Using cached httpcore-1.0.9-py3-none-any.whl (78 kB)
Using cached httpcore2-2.16.0-py3-none-any.whl (85 kB)
Using cached httpx-0.28.1-py3-none-any.whl (73 kB)
Using cached httpx_sse-0.4.3-py3-none-any.whl (9.0 kB)
Using cached httpx2-2.16.0-py3-none-any.whl (97 kB)
Using cached idna-3.20-py3-none-any.whl (69 kB)
Using cached iniconfig-2.3.1-py3-none-any.whl (7.6 kB)
Using cached jiter-0.17.0-cp312-cp312-win_amd64.whl (227 kB)
Using cached joblib-1.6.0-py3-none-any.whl (306 kB)
Using cached jsonpatch-1.36-py3-none-any.whl (17 kB)
Using cached jsonpointer-3.4-py3-none-any.whl (9.0 kB)
Using cached kiwisolver-1.5.1-cp312-cp312-win_amd64.whl (70 kB)
Using cached langchain-1.4.7-py3-none-any.whl (170 kB)
Using cached langchain_classic-1.0.8-py3-none-any.whl (1.0 MB)
Using cached langchain_community-0.4.2-py3-none-any.whl (2.4 MB)
Using cached langchain_core-1.6.13-py3-none-any.whl (574 kB)
Using cached langchain_openai-1.7.2-py3-none-any.whl (146 kB)
Using cached langchain_protocol-0.0.20-py3-none-any.whl (7.3 kB)
Using cached langchain_text_splitters-1.1.3-py3-none-any.whl (38 kB)
Using cached langgraph-1.2.16-py3-none-any.whl (260 kB)
Using cached langgraph_checkpoint-4.3.0-py3-none-any.whl (58 kB)
Using cached langgraph_prebuilt-1.1.1-py3-none-any.whl (42 kB)
Using cached langgraph_sdk-0.4.8-py3-none-any.whl (164 kB)
Using cached langsmith-0.14.12-py3-none-any.whl (883 kB)
Using cached matplotlib-3.11.2-cp312-cp312-win_amd64.whl (9.3 MB)
Using cached multidict-7.1.0-cp312-cp312-win_amd64.whl (93 kB)
Using cached nltk-3.9.2-py3-none-any.whl (1.5 MB)
Using cached numpy-2.5.4-cp312-cp312-win_amd64.whl (12.6 MB)
Using cached openai-3.36.0-py3-none-any.whl (2.3 MB)
Using cached opentelemetry_api-1.45.1-py3-none-any.whl (60 kB)
Using cached orjson-3.13.0-cp312-cp312-win_amd64.whl (121 kB)
Using cached ormsgpack-1.13.0-cp312-cp312-win_amd64.whl (157 kB)
Using cached packaging-26.3-py3-none-any.whl (129 kB)
Using cached pillow-13.0.0-cp312-cp312-win_amd64.whl (7.3 MB)
Using cached pluggy-1.7.0-py3-none-any.whl (27 kB)
Using cached propcache-0.5.4-cp312-cp312-win_amd64.whl (46 kB)
Using cached pydantic-2.14.1-py3-none-any.whl (488 kB)
Using cached pydantic_settings-2.16.1-py3-none-any.whl (80 kB)
Using cached pydantic_core-2.50.1-cp312-cp312-win_amd64.whl (2.2 MB)
Using cached pygments-2.21.0-py3-none-any.whl (1.3 MB)
Using cached pyparsing-3.3.3-py3-none-any.whl (126 kB)
Using cached pytest-9.1.1-py3-none-any.whl (386 kB)
Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Using cached python_dotenv-1.2.4-py3-none-any.whl (23 kB)
Using cached pyyaml-6.0.3-cp312-cp312-win_amd64.whl (154 kB)
Using cached regex-2026.9.29-cp312-cp312-win_amd64.whl (280 kB)
Using cached requests-2.34.2-py3-none-any.whl (73 kB)
Using cached requests_toolbelt-1.0.0-py2.py3-none-any.whl (54 kB)
Using cached ruff-0.17.1-py3-none-win_amd64.whl (10.1 MB)
Using cached scipy-1.18.1-cp312-cp312-win_amd64.whl (36.7 MB)
Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Using cached sniffio-1.3.1-py3-none-any.whl (10 kB)
Using cached sqlalchemy-2.1.6-cp312-cp312-win_amd64.whl (2.4 MB)
Using cached starlette-1.9.0-py3-none-any.whl (80 kB)
Using cached tenacity-9.2.1-py3-none-any.whl (32 kB)
Using cached tiktoken-0.14.0-cp312-cp312-win_amd64.whl (941 kB)
Using cached tqdm-4.70.1-py3-none-any.whl (80 kB)
Using cached truststore-0.10.5-py3-none-any.whl (19 kB)
Using cached typing_inspection-0.4.4-py3-none-any.whl (14 kB)
Using cached typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Using cached urllib3-2.8.0-py3-none-any.whl (135 kB)
Using cached uuid_utils-0.18.0-cp312-cp312-win_amd64.whl (175 kB)
Using cached uvicorn-0.54.0-py3-none-any.whl (87 kB)
Using cached websockets-16.1.1-cp312-cp312-win_amd64.whl (180 kB)
Using cached xxhash-4.0.2-cp312-cp312-win_amd64.whl (37 kB)
Using cached yarl-1.25.1-cp312-cp312-win_amd64.whl (102 kB)
Using cached zstandard-0.25.0-cp312-cp312-win_amd64.whl (506 kB)
Installing collected packages: zstandard, xxhash, websockets, uuid_utils, urllib3, typing_extensions, truststore, tenacity, sniffio, six, ruff, regex, PyYAML, python-dotenv, pyparsing, Pygments, propcache, pluggy, pillow, packaging, ormsgpack, orjson, numpy, multidict, kiwisolver, jsonpointer, jiter, iniconfig, idna, httpx-sse, h11, frozenlist, fonttools, distro, cycler, colorama, cloudpickle, click, charset-normalizer, certifi, attrs, annotated-types, annotated-doc, aiohappyeyeballs, yarl, uvicorn, typing-inspection, tqdm, SQLAlchemy, scipy, requests, python-dateutil, pytest, pydantic_core, opentelemetry-api, langchain-protocol, jsonpatch, joblib, httpcore2, httpcore, faiss-cpu, contourpy, anyio, aiosignal, tiktoken, starlette, requests-toolbelt, pydantic, nltk, matplotlib, httpx2, httpx, aiohttp, pydantic-settings, openai, langsmith, fastapi, langchain-core, langgraph-sdk, langgraph-checkpoint, langchain-text-splitters, langchain-openai, langgraph-prebuilt, langchain-classic, langgraph, langchain-community, langchain
Successfully installed PyYAML-6.0.3 Pygments-2.21.0 SQLAlchemy-2.1.6 aiohappyeyeballs-2.7.1 aiohttp-3.14.5 aiosignal-1.4.0 annotated-doc-0.0.5 annotated-types-0.8.0 anyio-4.15.1 attrs-26.1.0 certifi-2026.10.19 charset-normalizer-3.5.2 click-8.5.0 cloudpickle-3.1.2 colorama-0.4.6 contourpy-1.4.0 cycler-0.12.1 distro-1.9.0 faiss-cpu-1.15.1 fastapi-0.159.1 fonttools-4.67.0 frozenlist-1.8.0 h11-0.16.0 httpcore-1.0.9 httpcore2-2.16.0 httpx-0.28.1 httpx-sse-0.4.3 httpx2-2.16.0 idna-3.20 iniconfig-2.3.1 jiter-0.17.0 joblib-1.6.0 jsonpatch-1.36 jsonpointer-3.4 kiwisolver-1.5.1 langchain-1.4.7 langchain-classic-1.0.8 langchain-community-0.4.2 langchain-core-1.6.13 langchain-openai-1.7.2 langchain-protocol-0.0.20 langchain-text-splitters-1.1.3 langgraph-1.2.16 langgraph-checkpoint-4.3.0 langgraph-prebuilt-1.1.1 langgraph-sdk-0.4.8 langsmith-0.14.12 matplotlib-3.11.2 multidict-7.1.0 nltk-3.9.2 numpy-2.5.4 openai-3.36.0 opentelemetry-api-1.45.1 orjson-3.13.0 ormsgpack-1.13.0 packaging-26.3 pillow-13.0.0 pluggy-1.7.0 propcache-0.5.4 pydantic-2.14.1 pydantic-settings-2.16.1 pydantic_core-2.50.1 pyparsing-3.3.3 pytest-9.1.1 python-dateutil-2.9.0.post0 python-dotenv-1.2.4 regex-2026.9.29 requests-2.34.2 requests-toolbelt-1.0.0 ruff-0.17.1 scipy-1.18.1 six-1.17.0 sniffio-1.3.1 starlette-1.9.0 tenacity-9.2.1 tiktoken-0.14.0 tqdm-4.70.1 truststore-0.10.5 typing-inspection-0.4.4 typing_extensions-4.16.0 urllib3-2.8.0 uuid_utils-0.18.0 uvicorn-0.54.0 websockets-16.1.1 xxhash-4.0.2 yarl-1.25.1 zstandard-0.25.0
```

stderr:
```text

```

## Python version — PASS

Command: `../final-close-env/Scripts/python.exe --version`; cwd `.`.

Start `2026-10-23T21:30:46.881416+03:00`; finish `2026-10-23T21:30:46.983108+03:00`; exit `0`.

stdout:
```text
Python 3.12.14
```

stderr:
```text

```

## pip check — PASS

Command: `../final-close-env/Scripts/python.exe -m pip check`; cwd `.`.

Start `2026-10-23T21:30:46.986360+03:00`; finish `2026-10-23T21:30:56.832934+03:00`; exit `0`.

stdout:
```text
No broken requirements found.
```

stderr:
```text

```

## pytest — PASS

Command: `../final-close-env/Scripts/python.exe -m pytest -q`; cwd `.`.

Start `2026-10-23T21:30:56.835826+03:00`; finish `2026-10-23T21:31:58.185819+03:00`; exit `0`.

stdout:
```text
.........................ss............................................. [ 38%]
........................................................................ [ 76%]
............................................                             [100%]
186 passed, 2 skipped in 45.71s
```

stderr:
```text

```

## ruff — PASS

Command: `../final-close-env/Scripts/python.exe -m ruff check .`; cwd `.`.

Start `2026-10-23T21:31:58.187817+03:00`; finish `2026-10-23T21:32:01.051937+03:00`; exit `0`.

stdout:
```text
All checks passed!
```

stderr:
```text

```

## node version — PASS

Command: `node --version`; cwd `.`.

Start `2026-10-23T21:24:44.042537+03:00`; finish `2026-10-23T21:24:44.080538+03:00`; exit `0`.

stdout:
```text
v22.12.0
```

stderr:
```text

```

## npm version — PASS

Command: `cmd /d /c npm --version`; cwd `.`.

Start `2026-10-23T21:24:44.080538+03:00`; finish `2026-10-23T21:24:44.674525+03:00`; exit `0`.

stdout:
```text
11.0.0
```

stderr:
```text

```

## fresh npm ci offline — PASS

Command: `cmd /d /c npm ci --offline --no-audit --no-fund`; cwd `frontend`.

Start `2026-10-23T21:24:44.675525+03:00`; finish `2026-10-23T21:25:19.342399+03:00`; exit `0`.

stdout:
```text
added 183 packages in 34s
```

stderr:
```text

```

## frontend lint — PASS

Command: `cmd /d /c npm run lint`; cwd `frontend`.

Start `2026-10-23T21:25:19.342399+03:00`; finish `2026-10-23T21:25:24.221787+03:00`; exit `0`.

stdout:
```text
> uml-repair-frontend@0.0.0 lint
> eslint .
```

stderr:
```text

```

## frontend build — PASS

Command: `cmd /d /c npm run build`; cwd `frontend`.

Start `2026-10-23T21:25:24.222785+03:00`; finish `2026-10-23T21:25:26.004378+03:00`; exit `0`.

stdout:
```text
> uml-repair-frontend@0.0.0 build
> vite build

vite v8.0.11 building client environment for production...
[2K
transforming...✓ 1794 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.89 kB │ gzip:   0.48 kB
dist/assets/index-C1Rbb7An.css   49.33 kB │ gzip:   8.55 kB
dist/assets/index-7nNmDIlv.js   343.71 kB │ gzip: 106.73 kB

✓ built in 592ms
```

stderr:
```text

```

## Java version — PASS

Command: `java -version`; cwd `.`.

Start `2026-10-23T21:25:17.231598+03:00`; finish `2026-10-23T21:25:17.545568+03:00`; exit `0`.

stdout:
```text

```

stderr:
```text
java version "23" 2024-09-17
Java(TM) SE Runtime Environment (build 23+37-2369)
Java HotSpot(TM) 64-Bit Server VM (build 23+37-2369, mixed mode, sharing)
```

## live JAR and HTTP checks — PASS

Command: `../closure-clean-env/Scripts/python.exe ../final_close_runner.py live-child`; cwd `.`.

Start `2026-10-23T21:25:17.546568+03:00`; finish `2026-10-23T21:25:27.217345+03:00`; exit `0`.

stdout:
```text
{"status": "PASS", "compiler_fixtures": 4, "http_checks": 4, "model_calls": 0}
```

stderr:
```text

```

## Docker build/container smoke — NOT_TESTED

Command: `NOT EXECUTED — tool unavailable`; cwd `.`.

Start `2026-10-23T21:25:27.229346+03:00`; finish `2026-10-23T21:25:27.229346+03:00`; exit `None`.

stdout:
```text
BULUNAMADI: Docker executable on PATH
```

stderr:
```text
No build or container start executed
```

## existing finalizer on isolated copy — PASS

Command: `../closure-clean-env/Scripts/python.exe ../final_close_runner.py replay-child`; cwd `.`.

Start `2026-10-23T21:25:17.229991+03:00`; finish `2026-10-23T21:29:19.989443+03:00`; exit `0`.

stdout:
```text
{"completed_case_runs": 2800, "observed_conditions": ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"], "missing_conditions": []}
{"status": "passed", "expected_case_runs": 2800, "observed_unique_case_runs": 2800, "complete_registered_matrix": true, "derived_numbers": {"status": "passed", "raw_case_runs": 2800, "all_derived_numbers_recomputed": true}, "audit_unique_diagrams": 2353, "audit_confusion": {"TP": 1917, "FP": 303, "FN": 34, "TN": 99, "unavailable": 0, "sensitivity": 0.9825730394669401, "specificity": 0.2462686567164179}, "source_generation_commit": "1ead72ff7071e1f6de5867aaa250b0483d91431f", "generation_sources_unchanged": true, "all_measured_run_ids": ["dev-C3-20261022", "dev-C4-20261022", "dev-C5-20261022", "dev-C6-20261022", "dev-C7-20261022", "dev-provider-pilot-20261022", "dev-v41-C3-20261022", "dev-v41-C4-20261022", "dev-v41-C7-20261022", "nonllm-20261022", "nonllm-sourcefix-20261022", "test-frozen-20261022"], "audit_sha256": "22fa32694fc333e177f0dc7367d3d9f43f38a5335c2096180763b91898b876d3", "archived_incomplete_attempt_usage": {"archived_case_attempts": 0, "model_attempts": 0, "unknown_usage_attempts": 0, "known_usage_subtotal_usd": 0}, "closure_replay_scope": "Original algorithm; only output root redirected to an identified full result copy outside checkout; Git guard explicitly reads genuine checkout. Existing measured compiler flags reused by exact hash; not new experiments or2353newcompilations."}
```

stderr:
```text

```

## Interpretation

Fresh npm ci actually ran offline and replaced dependency installation from the retained lock. Fresh Python3.12 lock install, pipcheck, tests and lint actually ran. Unit mocks are not scientific responses. Live compiler uses API SANDBOX and English JVM locale; frozen CLI/runtime measurements remain unchanged. Docker build/container/provider replication were not performed. The finalizer copy is outside the checkout, with original algorithm and explicit output-root redirection; generation guard reads real Git. Recorded compiler cache reuse is not independent compilation. Baseline/protection/PII checks performed during packaging are separately retained in FINAL_EVIDENCE_MANIFEST.json and PRIVACY_SCAN.json.
