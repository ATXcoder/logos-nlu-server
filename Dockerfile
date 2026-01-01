# ========================
# Stage 1: Builder
# ========================
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system dependencies needed for ML builds
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

# Install CPU-only PyTorch compatible with sentence-transformers
RUN pip install --no-cache-dir \
    torch==2.2.2 \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Preload sentence-transformer model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Install spaCy English model
RUN pip install --no-cache-dir \
    https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# Copy app code (but we can exclude large unwanted files via .dockerignore)
COPY . .

# ========================
# Stage 2: Final / runtime image
# ========================
FROM python:3.10-slim

WORKDIR /app

# Copy all installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy only app code from builder
COPY --from=builder /app /app

# Expose port
EXPOSE 8001

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
