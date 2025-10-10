# Note Sharing Application

## High-Level Architecture
<img width="900" height="1093" alt="notes-sharing" src="https://github.com/user-attachments/assets/726617ae-dfe2-4807-afb1-559ec52c88c3" />

## Overview

This project is a unique web application that allows authenticated users to create and securely share an unlimited number of notes. Each note can be protected with an optional PIN, ensuring privacy. The core innovation lies in generating easy-to-remember and shareable URLs, making content accessible from any device across the internet. This application demonstrates a robust full-stack development approach, combining a powerful Flask backend with a dynamic Vue.js frontend, deployed on a Linux VM in Google Cloud.

## Key Features

* **Unlimited Note Creation:** Authenticated users can create an unrestricted number of personal notes.
* **PIN Protection:** Each note can be secured with an optional Personal Identification Number (PIN) for an added layer of privacy.
* **Memorable & Shareable URLs:** Notes are accessible via unique, easy-to-remember URLs, facilitating seamless sharing and access across different devices.
* **User Authentication:** Secure user registration and login system.
* **API-Driven Architecture:** A clear separation of concerns with a RESTful API backend serving data to the frontend.
* **Cross-Origin Resource Sharing (CORS):** Configured to allow secure communication between the frontend and backend.
* **Optimized for Larger Screens:** The user interface is primarily designed and optimized for viewing on larger displays.
* **Dockerized Application:** The entire stack is containerized using Docker for consistent and scalable deployment.
* **Production-Grade Stack:** Uses PostgreSQL as the production database and Redis for managing high user traffic efficiently.

## Technologies Used

This project leverages a modern tech stack to deliver a secure and great user experience:

### Backend (Flask)

* **Flask:** The micro web framework providing the core API structure.
* **Flask-Bcrypt:** For strong password hashing and verification, ensuring user data security.
* **Flask-Mail:** For handling email functionalities (e.g., account verification, password resets - if implemented).
* **Flask-CORS:** Manages Cross-Origin Resource Sharing, enabling secure communication with the Vue.js frontend.
* **JWT (JSON Web Tokens):** Employed for secure API authentication and authorization, enabling stateless user sessions.
* **SQLAlchemy:** ORM for interacting with the PostgreSQL database.
* **Redis:** Used as a caching and message broker system to handle high volumes of user requests efficiently.
* **Logging:** Configured Python’s built-in logging for structured error tracking and debugging.
* **Gunicorn:** WSGI HTTP server for running the Flask app in production.

### Project Structure - Flask (`flaskapp/`)

* `../run.py`: Main Flask application instance creation for development.
* `../wsgi.py`: Main Flask application instance creation for deployment.
* `config.py`: Centralized configuration management for the Flask app, database, and email settings.
* `users/`: Blueprint for user authentication and management (`/api-v1/users/`).
* `main/`: Blueprint for general application routes or public endpoints (`/api-v1/main/`).
* `notes/`: Blueprint for note creation, retrieval, updating, and deletion (`/api-v1/notes/`).

### Frontend (Vue.js)

* **Vue.js 3:** A progressive JavaScript framework for building the interactive user interface.
* **Vue Router:** For client-side routing, enabling single-page application (SPA) navigation.
* **Vue Reactive:** Simple and efficient state management for the application.
* **Axios:** A promise-based HTTP client for making API requests to the Flask backend.
* **CSS:** For custom styling.

### Project Structure - Vue.js (`src/`)

* `assets/`: Static assets like CSS.
* `views/`: Vue components representing different pages/views of the application.
* `main.js`: Vue.js application entry point, mounting the root component and configuring Axios, Vue Router, and the store.
* `components/`: Reusable Vue components. Different pages are separated into folders within this directory.
* `utils/`: JavaScript helper functions.
* `router/`: Routes definitions for client-side navigation.
* `store/`: Reactive object for simple state management.

### Database

* **PostgreSQL:** Used as the production-grade relational database for storing user accounts and notes securely.
* **SQLAlchemy:** Provides ORM-based interaction with the database.
* **Redis:** Used for caching, managing session data, and handling large volumes of user requests to improve performance.

### Testing

The backend API endpoints are tested using `Pytest` to ensure robust handling of various scenarios, particularly focusing on:

* **API Endpoint Validation:** Rigorously checking how endpoints respond to invalid or malformed inputs.
* **Access Control & Error Handling:** Verifying that specific endpoints correctly deny access to unauthorized users and provide appropriate error responses for invalid requests.
* **Edge Cases:** Explicitly testing scenarios like missing payloads or incorrect data formats/lengths.

### Deployment

* **Google Cloud Platform (GCP):** The cloud provider used for hosting the application on a Linux Virtual Machine.
* **Docker Compose:** Used to orchestrate multi-container deployment (Flask backend, Vue.js frontend, PostgreSQL, and Redis).
* **Nginx:** A high-performance web server and reverse proxy, used to serve the frontend and proxy requests to the backend.
* **Free SSL:** Implemented to secure all traffic with HTTPS, ensuring encrypted communication (e.g., using Let's Encrypt).
* **Gunicorn:** A Python WSGI HTTP Server for UNIX, used to run the Flask application in a production environment.


# Development
================================================

## Backend
### Export `.env` variables
```sh
SECRET_KEY=hola
AUTH_PREFIX=basic
SQLALCHEMY_DATABASE_URI=sqlite:///project.db
EMAIL_USER=
EMAIL_PASS=
JWT_TIMEOUT_MINUTES=120
REDIS_URI=redis://localhost:6379/0
ORIGIN=http://localhost:5173
```

### Create image & run container application layer
```sh
docker build -t backend-dev:latest .
docker run --name flask-app --env-file .env -p5000:5000 backend-dev

docker exec -it flask-app sh

# create db tables once
from wsgi import app
from flaskapp import db

with app.app_context():
  db.create_all()
```

## Frontend
### Export base `.env`
```sh
VITE_AUTH_PREFIX=basic
VITE_SERVER_ADDR=http://localhost:5000/api-v1
VITE_FRONTEND=http://localhost:5173
```

## run development environment, docker compose
```sh
docker compose -f dev-docker-compose.yml up

docker compose -f dev-docker-compose.yml down
```

# Production Service-based architecture
================================================

Run entire application using docker compose.
- build the vue app locally
- In one container nginx + vue build(/dist)

### export `.env.production` for override `.env` in build process
```sh
VITE_SERVER_ADDR=http://localhost:5000/api-v1
VITE_FRONTEND=http://localhost:8080
```

### build vue app locally
```sh
npm install
npm run build -- --mode production
```

### docker compose
```sh
docker compose up -d
docker compose down
```

### create database table in backend first time
```sh
docker exec -it <container_name> sh
python

from wsgi import app
from flaskapp import db

with app.app_context():
  db.create_all()
```

# Server Configuration on Linux
================================================

### Nginx configuration

```sh
sudo apt install nginx

sudo rm /etc/nginx/sites-enabled/default

nano /etc/nginx/nginx.conf
user username
```

### enable site without ssl

```sh
sudo nano /etc/nginx/sites-enabled/test

server {
  server_name 34.123.176.182;

  include /etc/nginx/proxy_params;

  location / {
    root /home/mahfuz/server/frontend/dist;
    try_files $uri /index.html;
  }

  location /api-v1 {
    proxy_pass http://localhost:8000;
  }
}
```

### install ssl

```sh
sudo apt install certbot
sudo apt install software-properties-common
sudo apt install python3-certbot-nginx

sudo certbot --nginx
sudo systemctl restart nginx
```

### after enable ssl nginx server config will look like

```sh
server {
  server_name domain.com www.domain.com;
  root /home/user/test/fontend/dist;
  location / {
    try_files $uri /index.html;
    include /etc/nginx/proxy_params;
    proxy_redirect off;
  }

  location /api {
    proxy_pass http://localhost:8000;
  }

    listen [::]:443 ssl ipv6only=on; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/domain.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/domain.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = www.domain.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = domain.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

  listen 80;
  listen [::]:80;
  server_name domain.com www.domain.com;
    return 404; # managed by Certbot
}
```

### firewall
on google cloud only allow https, ssh from firewall settings

```sh
sudo ufw reset
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow https
sudo ufw enable
```

### run flaskapp - Supervisor process manager

```sh
# install supervisor
sudo apt install supervisor

# create supervisor config file
sudo nano /etc/supervisor/conf.d/flaskapp.conf

[program:flaskapp]
directory=/home/username/test/backend
command=/home/username/test/backend/.env/bin/gunicorn -w 5 run:app
user=username
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/test/test.err.log
stdout_logfile=/var/log/test/test.out.log
```

### create logfile

```sh
sudo mkdir -p /var/log/test/
sudo touch /var/log/test/test.err.log
sudo touch /var/log/test/test.out.log
```

### Run flask server
```sh
sudo supervisorctl reload		# start running the application
sudo supervisorctl status		# check the status of supervisor
```

