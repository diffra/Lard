# LARD: A Redirect Daemon


```
Redirecting flows
LARD smoothly guides the way
URLs find a path
```

## Overview

LARD is a redirect daemon that can be used to redirect incoming HTTP requests to different URLs.

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

### `POST /create`

This endpoint allows you to create a new redirect. The following parameters are supported:

- `url`: The URL to redirect to.
- `key`: The password

HTML/CSS layout thanks to Smart Developers.
