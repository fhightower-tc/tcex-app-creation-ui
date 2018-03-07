clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log* && rm -fr .cache && rm -rf ./playbook_app_creator/static/apps/*.zip && rm -rf ./playbook_app_creator/static/apps/*/

venv:
	virtualenv -p python3 ~/.virtualenvs/playbook_app_creator && . ~/.virtualenvs/playbook_app_creator/bin/activate && pip3 install -r requirements.txt

run:
	~/.virtualenvs/playbook_app_creator/bin/python playbook_app_creator/playbook_app_creator.py

test:
	~/.virtualenvs/playbook_app_creator/bin/python -m unittest
