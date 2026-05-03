FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN python -m compileall -q .
CMD ["python", "make_campaign_002.py", "--skip-repro"]
