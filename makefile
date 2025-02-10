setup:
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install -r requirements.txt

start-mongo:
	brew services start mongodb-community

run: 
	uvicorn main:app --reload --port 8000

stop-mongo:
	brew services stop mongodb-community
