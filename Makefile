build:
	@echo "Building weather data generator"
	@pip install -r requirements.txt

train:
	@echo "Training weather models"

run:
	@echo "Running weather data generator"
	@cd src && python run_simulation.py ${obs}

.PHONY: build train run

