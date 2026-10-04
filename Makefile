.PHONY: install test run bench live fetch figures video preview clean docker-build docker-run

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=src pytest -v tests/

run:
	PYTHONPATH=src python experiments/run_all.py

bench:
	PYTHONPATH=src python benchmarks/benchmark_all.py

live:
	PYTHONPATH=src python scripts/fetch_live_data.py
	PYTHONPATH=src python experiments/exp_live_market.py

fetch:
	PYTHONPATH=src python scripts/fetch_live_data.py

figures:
	PYTHONPATH=src python scripts/make_figures.py

video:
	PYTHONPATH=src python scripts/make_video.py

preview:
	@echo "Open preview.html directly (no server needed)."

clean:
	rm -rf results/tables/* results/figures/* data/processed/* data/live_cache/* .pytest_cache __pycache__

docker-build:
	docker compose build

docker-run:
	docker compose up research
