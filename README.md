# Note Sharing Application

## High-Level Architecture
<img width="900" height="1093" alt="notes-sharing" src="https://github.com/user-attachments/assets/2d1001c7-d592-4f5b-a59e-bbe64d601042" />

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

## Technologies Used

This project leverages a modern tech stack to deliver a secure and great user experience:

### Backend (Flask)

* **Flask:** The micro web framework providing the core API structure.

* **Flask-Bcrypt:** For strong password hashing and verification, ensuring user data security.

* **Flask-Mail:** For handling email functionalities (e.g., account verification, password resets - if implemented).

* **Flask-CORS:** Manages Cross-Origin Resource Sharing, enabling secure communication with the Vue.js frontend.

* **JWT (JSON Web Tokens):** Employed for secure API authentication and authorization, enabling stateless user sessions.

* **Redis:** An in-memory data structure store, used for cahcing otp verification code.

### Project Structure - Flask (`flaskapp/`)

* `app.py`: Main Flask application instance creation and extension initialization.

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

* **SQLAlchemy:** Used as the ORM to interact with a relational database.

* **Relational Database:** `SQLite` file system database. Stores user accounts, notes information.

### Testing

The backend API endpoints are tested using `Pytest` to ensure robust handling of various scenarios, particularly focusing on:

* **API Endpoint Validation:** Rigorously checking how endpoints respond to invalid or malformed inputs.
* **Access Control & Error Handling:** Verifying that specific endpoints correctly deny access to unauthorized users and provide appropriate error responses for invalid requests.
* **Edge Cases:** Explicitly testing scenarios like missing payloads or incorrect data formats/lengths.

### Deployment

* **Google Cloud Platform (GCP):** The cloud provider used for hosting the application on a Linux Virtual Machine.

* **Nginx:** A high-performance web server and reverse proxy, used to serve the frontend and proxy requests to the backend.

* **Free SSL:** Implemented to secure all traffic with HTTPS, ensuring encrypted communication (e.g., using Let's Encrypt).

* **Gunicorn:** A Python WSGI HTTP Server for UNIX, used to run the Flask application in a production environment.


# Server Configuration
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
