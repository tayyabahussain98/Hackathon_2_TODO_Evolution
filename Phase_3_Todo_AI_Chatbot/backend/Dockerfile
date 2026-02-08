# Use official Python 3.12 Alpine image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install uv and dependencies
RUN pip install uv

# Copy only dependency files first for caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy the rest of the backend code
COPY . .

# Expose port
EXPOSE 7860

# Command to run the app
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
