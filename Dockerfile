FROM python:3.9-slim

# Create non-root user for security
RUN useradd -m -u 1000 appuser

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# Change ownership to non-root user
RUN chown -R appuser:appuser /code

# Switch to non-root user
USER appuser

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:80/').read()" || exit 1

CMD ["fastapi", "run", "app/main.py", "--port", "80"]