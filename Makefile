build:
	@echo "Building random weather generator"
	@pip install -r requirements.txt

run:
	@echo "Running random weather generator"
	@-cd src && python run_simulation.py ${obs}

rundocker:
	@echo "Running random weather generator with Docker"
	@obs=${obs} docker-compose up