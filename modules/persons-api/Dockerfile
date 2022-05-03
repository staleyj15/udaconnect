FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# command to run and publish port 5003
# docker run -d -p 5003:5000/tcp --name udaconnect-persons --env-file ../../local-env.list jstaley6/udaconnect-persons:v0.0