import subprocess

scripts = ['scrapper.py', 'chrome.py', 'folders.py', 'template.py','pdf_extract_image.py','template2.py']

for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run(['python3', script], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error occurred while running {script}:")
        print(result.stderr)
        break
    print(f"{script} completed.\n")
