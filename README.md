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
     build: .
     # other service configuration
     ports:
       - "8002:8000" # port mapping
     volumes:
       - "./data:/data" # config directory for LARD
```

## Configuration

The configuration for the application is stored in the file `./data/config.ini`. The following sections and options are available:

### General
- `baseurl`: the base URL for the service.
- `length`: the length for shortened URL.

### Auth
- `key`: the API key to access the service, with a maximum length of 100 characters and encoded in base64 format. 

To generate a new API Key: 

**Mac or linux:** `head /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 20 | head -n 1 | base64`

**Windows Powershell:** `[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes([System.Guid]::NewGuid().ToString().Substring(0, 20)))`

## Bookmarklet

Use the following bookmarklet to create a short URL for the current page:

```
javascript:(function() {
  const baseUrl = "https://your-lard-application.com/create";
  const apiKey = "your-api-key";
  const currentUrl = encodeURIComponent(window.location.href);
  fetch(`${baseUrl}?key=${apiKey}&url=${currentUrl}`)
    .then(response => response.json())
    .then(data => {
      const shortUrl = data.shortUrl;
      navigator.clipboard.writeText(shortUrl).then(() => {
        alert("The short URL has been copied to your clipboard.");
      });
    });
})();
```

## Endpoints

### `GET /`

This endpoint returns a simple HTML page with a message indicating that LARD is running.

### `POST /create`

This endpoint allows you to create a new redirect. The following parameters are supported:

- `url`: The URL to redirect to.
- `key`: The api key.