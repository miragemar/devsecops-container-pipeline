
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY app/ ./app/

RUN useradd --system --no-create-home --shell /usr/sbin/nologin appuser

USER appuser

EXPOSE 8000

CMD ["python", "app/main.py"]
