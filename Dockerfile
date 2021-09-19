FROM python:3.8

WORKDIR /TESTTASK

COPY requirements.txt   .

RUN pip install -r requirements.txt

COPY  ./tests ./tests

COPY  mkad_coordinates.py .

COPY  app.py .

COPY  app.log .

COPY test_app.py .

COPY  ./templates ./templates

COPY ./middleware ./middleware 

CMD ["python", "app.py"]
