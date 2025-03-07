FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Ensure pip is updated
RUN python -m pip install --upgrade pip

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:${PATH}"

# Expose port
EXPOSE 8000

# Run the FastAPI app using uvicorn explicitly from Python's bin
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
