build:
	@echo "Building random weather generator"
	@pip install -r requirements.txt

dockerbuild:
	@echo "Pulling weather-generator Docker image"
	docker pull federicociner/weather-generator:latest

run:
	@echo "Running random weather generator"
	@cd src && python run_simulation.py ${obs}

rundocker:
	@echo "Running random weather generator Docker container"
	docker run -it federicociner/weather-generator:latest bash

.PHONY: build train run

