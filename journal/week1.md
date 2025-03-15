# Week 1 — App Containerization

## Docker
### Run Flask
```sh
cd backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
python3 -m flask run --host=0.0.0.0 --port=4567
cd ..
```
To set environment variables on Windows:
```sh
$env:FRONTEND_URL = "*"
$env:BACKEND_URL = "*"
```

### Installation
- Installed Docker extension for VSCode and [Docker for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)

### Build Container
```sh
docker build -t backend-flask ./backend-flask
```

### Run Container
Run:
```sh
docker run --rm -p 4567:4567 -it backend-flask
```
Run with implicitly set environment variables:
```sh
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
```
Run in background (**-d** flag):
```sh
docker container run --rm -p 4567:4567 -d backend-flask
```

### Stop Container
```sh
docker stop <container_id>
```

### Get Container Images or Running Container Ids
```sh
docker ps
docker images
```

### Delete an Image
```sh
docker image rm backend-flask --force
```

### Overriding Ports
```sh
FLASK_ENV= production PORT=8080 docker run -p 4567:4567 -it backend-flask
```

### Containerize Frontend
#### Install dependencies
```sh
cd frontend-react-js
npm install
```

#### Build Container
```sh
docker build -t frontend-react-js ./frontend-react-js
```

#### Run Container
```sh
docker run -p 3000:3000 -d frontend-react-js
```

### Docker Compose
#### docker-compose.yml
- To work locally without gitpod, convert to using localhost in the given docker-compose.yml file:
- To get CORS to work I had to use 127.0.0.1 instead of localhost
```yml
version: "3.8"
services:
  backend-flask:
    environment:
      #FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      #BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      FRONTEND_URL: "http://127.0.0.1:3000"
      BACKEND_URL: "http://127.0.0.1:4567"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
    networks:
      - internal-network

  frontend-react-js:
    environment:
      #REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      REACT_APP_BACKEND_URL: "http://127.0.0.1:4567"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js
    networks:
      - internal-network

networks: 
  internal-network:
    driver: bridge
    name: cruddur
```

#### Run
Run the command or right-click docker-compose.yml and select "Compose Up".
```sh
docker compose up
docker-compose up
```

#### Stop
Run the command or right-click docker-compose.yml and select "Compose Down".
```sh
docker compose down
docker-compose down
```
To stop the containers without removing them:
```sh
docker compose stop
docker-compose stop
```

#### Restart
```sh
docker compose restart
docker-compose restart
```
