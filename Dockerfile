FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

# Create entrypoint script
RUN echo '#!/bin/bash\n\
python init_db.py\n\
exec gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 120 app:app' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
