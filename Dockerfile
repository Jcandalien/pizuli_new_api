# Use Python 3.11
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgres://postgres:postgres@localhost:5432/pizuli

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Copy project files
COPY . /app/

# Make start.sh executable
RUN chmod +x /app/start.sh

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start PostgreSQL and run the application
CMD ["/app/start.sh"]