init-db:
	flask initdb

install:
	pip install -r requirements.txt
	pip install -r requirements_test.txt

installer:
	pyinstaller --clean pardal.spec

reload-db:
	rm pardal.db && flask initdb

run:
	sudo python pardal/run.py

run-server:
	flask run

stop-server:
	sudo fuser -k 6001/tcp  # or MacOS lsof -ti:3000 | xargs kill

test:
	pytest tests
