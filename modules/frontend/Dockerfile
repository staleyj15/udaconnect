FROM node:14.8.0-alpine3.12

WORKDIR .

COPY package.json ./
COPY package-lock.json ./

RUN npm install
RUN npm install react-scripts@3.4.3 -g

CMD ["pwd"]

COPY . ./

EXPOSE 3000

CMD ["npm", "start"]

# run and publish to local port 3000
# docker run -d -p 3000:3000/tcp --name udaconnect-frontend jstaley6/udaconnect-frontend:v2.0


