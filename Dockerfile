FROM python:3.13-slim

# Create non-root user
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Switch to non-root user
USER user

# Set environment path
ENV PATH="/home/user/.local/bin:$PATH"

# Expose port
EXPOSE 7860

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]