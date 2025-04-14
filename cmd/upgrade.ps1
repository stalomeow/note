$python = "./env/Scripts/python.exe"

& $python -m pip install --upgrade pip
& $python -m pip install --upgrade --force-reinstall mkdocs-material
& $python -m pip freeze > requirements.txt