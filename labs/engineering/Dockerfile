FROM python:3.12-slim
WORKDIR /course
COPY requirements-service.txt .
RUN pip install --no-cache-dir -r requirements-service.txt
COPY engineeringlab engineeringlab
COPY submission.py .
ENV COURSE_TICKET_DB=/data/tickets.sqlite
EXPOSE 8000
CMD ["uvicorn","engineeringlab.support:create_app","--factory","--host","0.0.0.0","--port","8000"]
