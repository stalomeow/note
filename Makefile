SHELL := cmd
PYTHON_ENV := .\env\Scripts\activate
.ONESHELL:

help h:
	@echo Usage:
	@echo   help     h     Show help information
	@echo   serve    s     Start local server
	@echo   deploy   d     Push to remote repository
	@echo   upgrade        Upgrade mkdocs-material
.PHONY: help h

serve s:
	$(PYTHON_ENV) && mkdocs --color serve
.PHONY: serve s

MSG := Update

deploy d:
	git add . && git commit -m "$(MSG)" && git push
.PHONY: deploy d

# https://github.com/urllib3/urllib3/issues/2168
upgrade:
	$(PYTHON_ENV)
	python -m pip install --upgrade pip
	pip install --upgrade --force-reinstall mkdocs-material
	pip install urllib3==1.26.18
	pip freeze > requirements.txt
.PHONY: upgrade
