# LARD: A Redirect Daemon


```
Redirecting flows
LARD smoothly guides the way
URLs find a path
```

## Overview

LARD is a redirect daemon that can be used to redirect incoming HTTP requests to different URLs.

![user interface](https://raw.githubusercontent.com/diffra/Lard/master/Interface.png)

## Usage

To use LARD, it is strongly recommended to use docker-compose.

```
version: '3'
 services:
   lard:
     image: diffra/lard
     # other service configuration
     ports:
       - "8002:8000" # port mapping
     volumes:
       - "./data:/data" # config directory for LARD
```

## Configuration

The configuration for the application is stored in the file `./data/config.ini`. Create the folder 'data' and config.ini file within. The contents should look like this:

```
[General]
 baseurl  = https://l.yourdomain.com
 length   = 5

[Auth]
 password = lard
 #bcrypted admin:password
 #To generate a username:password string, see: https://hostingcanada.org/htpasswd-generator/ or run `htpasswd -nBC 10 admin`
 admin = admin:$2y$10$TGVz8YgPBXggJAf.BjOjHeMls59VXI7g7bGLLX9zF4uvHJcM8nKjG

```


The following sections and options are available:

### General
- `baseurl`: the base URL for the service.
- `length`: the length for shortened URL.

### Auth
- `password`: the password to create a new link. 

## Endpoints

### `GET /`

This endpoint returns a simple HTML page with a form.

### `GET /admin`

This password-protected HTML endpoint returns a list of links within the system with delete capability.

### `POST /create`

This endpoint allows you to create a new redirect. The following parameters are supported:

- `url`: The URL to redirect to.
- `key`: The password

### `DELETE /delete/{id}`

This endpoint deletes an existing link:

{id} is the database id of the link to be deleted.

Requires same auth as admin


HTML/CSS layout thanks to Smart Developers.
