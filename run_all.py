import subprocess

# Absolute path to virtual env python
python_path = r"F:\LLM-Mysql-DB-agent\myenv\Scripts\python.exe"

processes = [
    ["uvicorn", "server:app", "--reload"],
    [python_path, "mcp_client.py"],
    [python_path, "rag/update_rag.py"],
    ["streamlit", "run", "app.py"]
]

for cmd in processes:
    subprocess.Popen(cmd)

print("All processes started.")
