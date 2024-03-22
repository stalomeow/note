help h:
	@echo.                                              \
	&& @echo Usage:                                     \
	&& @echo   help     h     Show help information     \
	&& @echo   serve    s     Start local server        \
	&& @echo   edit     e     Open VSCode               \
	&& @echo   blog     b     New blog post             \
	&& @echo   deploy   d     Push to remote repository \
	&& @echo   upgrade        Upgrade mkdocs-material
.PHONY: help h

serve s:
	.\env\Scripts\activate && mkdocs --color serve
.PHONY: serve s

edit e:
	code .
.PHONY: edit e

blog b:
	.\env\Scripts\activate && python .\scripts\new_blog.py
.PHONY: blog b

MSG := Update

deploy d:
	git add . && git commit -m "$(MSG)" && git push
.PHONY: deploy d

# https://github.com/urllib3/urllib3/issues/2168
upgrade:
	.\env\Scripts\activate                                     \
	&& python -m pip install --upgrade pip                     \
	&& pip install --upgrade --force-reinstall mkdocs-material \
	&& pip install urllib3==1.26.18                            \
	&& pip freeze > requirements.txt
.PHONY: upgrade
