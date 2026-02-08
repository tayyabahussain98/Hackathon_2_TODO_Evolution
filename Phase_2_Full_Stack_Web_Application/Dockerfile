FROM python:3.12-alpine

WORKDIR /app

# Install uv
RUN pip install uv

# Copy pyproject.toml and uv.lock from backend folder
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev

# Copy all backend source code
COPY backend/ ./

# Expose port
EXPOSE 7860

# Run backend
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
