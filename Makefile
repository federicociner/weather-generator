build:
	@echo "Building random weather generator"
	@pip install -r requirements.txt

run:
	@echo "Running random weather generator"
	@-cd src && python run_simulation.py ${obs}

dockerpull:
	@echo "Pulling Docker image from DockerHub"
	@docker pull federicociner/weather-generator:latest

dockerbuild:
	@echo "Building Docker image locally"
	@docker build . --tag federicociner/weather-generator:latest

rundocker:
	@echo "Running random weather generator from Docker"
	@obs=${obs} docker-compose up