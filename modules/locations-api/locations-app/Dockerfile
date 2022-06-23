FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# command to run and publish port 30002
# docker run -d -p 30002:5000/tcp --name udaconnect-locations --env-file ../../local-env.list jstaley6/udaconnect-locations:v1.0