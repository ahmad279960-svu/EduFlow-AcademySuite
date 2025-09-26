#
# Dockerfile for EduFlow-AcademySuite v2.0
# This file describes the steps to create a production-ready Docker image
# for the Django application.
#

# --- Stage 1: Build Stage ---
# This stage installs Python dependencies into a separate directory.
# This leverages Docker's layer caching, so dependencies are only re-installed
# when requirements.txt changes.
FROM python:3.11-slim as builder

WORKDIR /opt/app

# Set environment variables to prevent generation of .pyc files and to ensure
# output is sent straight to the terminal without buffering.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for psycopg2 (PostgreSQL adapter) and WeasyPrint
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    pango1.0-tools \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /opt/app/wheels -r requirements.txt


# --- Stage 2: Final Stage ---
# This stage builds the final, lean image for the application.
FROM python:3.11-slim

WORKDIR /var/www/app

# Create a non-root user to run the application for security reasons
RUN addgroup --system django && adduser --system --ingroup django django

# Install system dependencies needed at runtime (WeasyPrint)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy pre-built Python wheels from the builder stage and install them
COPY --from=builder /opt/app/wheels /wheels
COPY --from=builder /opt/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy the application source code into the container
COPY . .

# Change ownership of the application directory to the non-root user
RUN chown -R django:django /var/www/app

# Switch to the non-root user
USER django

# Expose the port Gunicorn will run on
EXPOSE 8000

# Set the entrypoint to run Gunicorn
# Gunicorn is a production-ready WSGI server.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "academy_suite.wsgi:application"]