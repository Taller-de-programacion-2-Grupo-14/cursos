FROM python:3.8
WORKDIR /src

COPY . /src

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]