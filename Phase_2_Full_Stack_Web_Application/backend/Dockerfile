# Base image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install uv package
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies in frozen mode
RUN uv sync --frozen --no-dev

# Copy all backend source code
COPY . .

# Expose backend port
EXPOSE 7860

# Run backend app
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
