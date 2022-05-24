FROM python:3.7-slim

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .
CMD ["python", "app.py"]

# command to run and publish port 5006
# docker run -d -p 5006:5005/tcp --name udaconnect-connections --env-file ../../local-env.list jstaley6/udaconnect-connections:v0.0