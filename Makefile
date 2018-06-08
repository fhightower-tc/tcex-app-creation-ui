clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log* && rm -fr .cache && rm -rf ./tcex_app_creator/static/apps/*.zip && rm -rf ./tcex_app_creator/static/apps/*/ && rm -rf .pytest_cache/

venv:
	virtualenv -p python3 ~/.virtualenvs/tcex_app_creator && . ~/.virtualenvs/tcex_app_creator/bin/activate && pip3 install -r requirements.txt

run:
	~/.virtualenvs/tcex_app_creator/bin/python tcex_app_creator/tcex_app_creator.py

test: clean
	~/.virtualenvs/tcex_app_creator/bin/python -m pytest
