FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install uv (fast python package manager)
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (no dev deps)
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Hugging Face Spaces default port
EXPOSE 7860

# Run FastAPI app
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
