FROM python:3.7

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

RUN wget http://donnees.ville.montreal.qc.ca/dataset/1d785ef8-f883-47b5-bac5-dce1cdddb1b0/resource/e62322fb-3e14-4ee0-b724-a77190dac8e7/download/remorquages.csv && mv remorquages.csv data/

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
