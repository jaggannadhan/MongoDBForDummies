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

docker-build:
	docker build -t mongodbfordummies:latest .    

# shell runs shell script command
# -n checks if the resposne of the shell command is not empty; -a includes all containers including the ones not running; 
# -q return only the container id; --filter filters the containers using name
docker-start:
	@if [ -n "$(shell docker ps -a --filter "name=$(container_name)" -q)" ]; then \
        docker start $(container_name); \
    else \
        docker run -d -p 8000:8000 --name $(container_name) mongodbfordummies:latest; \
    fi

docker-stop:
	echo "Stopping docker container: $(container_name)"
	docker stop $(container_name)