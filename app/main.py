import configparser
import os
import random
import re
import sqlite3
import string
from datetime import datetime

from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import RedirectResponse


def get_config():
    config = configparser.ConfigParser()
    config.read("/data/config.ini")
    return config

def get_password():
    config = get_config()
    return config.get('Auth', 'password')

def get_baseurl():
    config = get_config()
    return config["General"]["baseurl"]

def get_length():
    config = get_config()
    return int(config["General"]["length"])

def is_valid_key(key):
    print(key)
    return bool(key and len(key) == 20 and isbase64(key))

def is_valid_url(url):
    pattern = re.compile(r"^(?:http|ftp)s?://[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
    return bool(pattern.match(url))

def database_exists(db_file):
    return os.path.exists(db_file)

def isbase64(value):
    b64pattern = re.compile(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$')
    return bool(b64pattern.match(value))

def generate_shorturl():
    with sqlite3.connect('/data/lard.db') as conn:
        cursor = conn.cursor()
        url_length = get_length()
        short = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=url_length))
        cursor.execute("select * from links where short=?", (short,))
        if cursor.fetchone():
            return generate_shorturl()
        return short

def update_link_on_view(conn, short_url):
    # Connect to the database
    cur = conn.cursor()
    
    # Get the current time
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Update the views and last fields
    cur.execute("UPDATE links SET views = views + 1, last = ? WHERE short = ?", (timestamp, short_url))
    conn.commit()


# Create schema if not exists
if not database_exists('/data/lard.db'):
    try:
        with sqlite3.connect('/data/lard.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    short TEXT, 
                    long TEXT, 
                    views INTEGER, 
                    last TEXT
                )
            ''')
            cursor.execute("CREATE INDEX idx_short ON links (short)")
            cursor.execute("CREATE INDEX idx_last ON links (last)")
            conn.commit()
    except Exception as e:
        print("Error creating database:", e)

app = FastAPI()
security = HTTPBasic()


@app.post("/create")
async def createlink(data: dict):
    url = data.get("url")
    key = data.get("key")
    # Sanity checks
    if not is_valid_url(url):
        return JSONResponse(content={"message": "Invalid URL format"},status_code=400)
    elif key != get_password():
        return JSONResponse(content={"message": "Unauthorized"},status_code=401)
    else:
        with sqlite3.connect('/data/lard.db') as conn:
            cursor = conn.cursor()
            baseurl = get_baseurl()
            safe_url = url.replace("'", "''")  # escape single quotes
            short = generate_shorturl()
            cursor.execute("INSERT INTO links (short, long, views, last) VALUES (?, ?, 0, NULL)", (short, safe_url))
            conn.commit()
        return f"{baseurl}/{short}"

@app.get("/")
async def read_root():
    with open("/app/templates/index.html") as f:
        html = f.read()
    return HTMLResponse(html)

@app.get("/admin")
def admin(request: Request):
    with sqlite3.connect('data/lard.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM links")
        entries = cursor.fetchall()
    return templates.TemplateResponse("admin.html", {"request": request, "entries": entries})

@app.get("/{path}")
async def redirect(path = None):
    conn = sqlite3.connect('/data/lard.db')

    # Create a cursor
    cursor = conn.cursor()
    # Create links table
    cursor.execute("SELECT long FROM links WHERE short = ?", (path,))
    rows = cursor.fetchall()
    
    if len(rows) == 1:
        update_link_on_view(conn, path)
        conn.close()
        return RedirectResponse(url=rows[0][0], status_code=301)
    else:
        conn.close()
        return RedirectResponse(url=get_baseurl(), status_code=301)
