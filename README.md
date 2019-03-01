# flask-rest-api

Project that fetches towing data for the city of Montreal, processes it, and exposes 3 endpoints to access the data. These endpoints are:

* /data
* /boroughs-stats
* /weekdays-stats

## How to run
* Clone project:

  ```bash
  git clone git@github.com:ZakiChammaa/flask-rest-api.git
  ```
* Build Docker image:

  ```bash
  docker build --network=host -t flask-app:latest .
  ```
* Run Docker container:
  
  ```bash
  docker run --name flask-app -d -p 5000:5000 --rm flask-app:latest
  ```
