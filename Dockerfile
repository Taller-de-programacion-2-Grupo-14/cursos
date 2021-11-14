FROM python:3.8
WORKDIR /src

COPY . /src

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload", "-b", "0.0.0.0:8080"]