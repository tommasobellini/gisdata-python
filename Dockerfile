FROM python:3.8
RUN apt-get update && apt-get install curl -y
WORKDIR /gisdata-python
ENV PYTHONPATH ${PYTHONPATH}:/gisdata-python
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN ls -l
CMD [ "python", "main.py" ]