FROM python:3.12-slim
WORKDIR /course
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml models.lock.json ./
COPY raglab ./raglab
COPY data ./data
RUN pip install --no-deps .
ENV RAG_MODEL_DIR=/models
EXPOSE 8000
CMD ["uvicorn", "raglab.service:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
