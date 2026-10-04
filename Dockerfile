FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

# System deps (pinned base image above; no apt version drift for core run)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY experiments/ ./experiments/
COPY benchmarks/ ./benchmarks/
COPY tests/ ./tests/
COPY scripts/ ./scripts/
COPY docs/ ./docs/
COPY preview.html README.md PAPER.md METHODOLOGY.md ./
COPY data/ ./data/
COPY Makefile ./Makefile

ENV PYTHONPATH=/workspace/src:$PYTHONPATH \
    MH_SEED=12345

# Default: verify everything, then run full benchmark suite
CMD ["bash", "-c", "pytest -v tests/ && python experiments/run_all.py && python benchmarks/benchmark_all.py"]
