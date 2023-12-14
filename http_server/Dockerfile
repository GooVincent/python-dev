FROM python:3

WORKDIR /workspace

COPY ./requirements.txt /workspace/requirements.txt

RUN pip install -r /workspace/requirements.txt

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
