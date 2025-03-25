SHELL := cmd
PYTHON_ENV := call .\env\Scripts\activate.bat
.ONESHELL:

help h:
	@echo Usage:
	@echo   help     h     Show help information
	@echo   serve    s     Start local server
	@echo   deploy   d     Push to remote repository
	@echo   upgrade        Upgrade mkdocs-material
	@echo   tiny           Compress images
	@echo   code           Open Visual Studio Code
	@echo   explorer       Open File Explorer
	@echo   install        Install dependencies
.PHONY: help h

serve s:
	$(PYTHON_ENV) && mkdocs --color serve
.PHONY: serve s

MSG := Upload via Makefile

deploy d:
	git add . && git commit -m "$(MSG)" && git push --porcelain
.PHONY: deploy d

upgrade:
	$(PYTHON_ENV)
	python -m pip install --upgrade pip
	pip install --upgrade --force-reinstall mkdocs-material
	pip freeze > requirements.txt
.PHONY: upgrade

install:
	py -3.12 -m venv env
	$(PYTHON_ENV)
	pip install -r requirements.txt
.PHONY: install

tiny:
	$(PYTHON_ENV)
	python .\scripts\tinify_image.py
.PHONY: tiny

code:
	code .
.PHONY: code

explorer:
	cmd /c start .
.PHONY: explorer
