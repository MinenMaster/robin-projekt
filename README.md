# Robin’s Webprojekt

## Setup

### Entwicklungsumgebung

-   **VS Code** öffnen
-   Projektordner anlegen
-   Python & Git prüfen:

```bash
python --version
git --version
```

-   Virtuelle Umgebung einrichten:

```bash
python -m venv .venv
# Aktivieren (Windows)
.venv\Scripts\activate
# oder Linux/macOS
source .venv/bin/activate
```

-   Python Pakete für die API installieren:

```bash
pip install flask flask-cors
```

---

### Step 1: Eine kleine API mit Flask erstellen

Good to know:

-   Flask ist ein Framework, um sehr einfach REST APIs in Python zu erstellen.
-   REST steht für Representational State Transfer.
-   In REST Architekturen werden meistens die CRUD Operationen (Create, Read, Update, Delete) über HTTP Methoden (POST, GET, PUT, DELETE) abgebildet.

Grundgerüst der API:

```py
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.get("/api")
def index():
    return "API is running!"

if __name__ == "__main__":
    app.run(debug=True)
```

Starten: `python app.py` und testen: [http://127.0.0.1:5000/api](http://127.0.0.1:5000/api)

---

### Step 2: Eine Website zur API erstellen

Datei: `index.html`

```html
<!DOCTYPE html>
<html lang="de">
    <head>
        <meta charset="UTF-8" />
        <title>Robins Mini-Webseite</title>
        <style>
            button {
                background-color: #4caf50;
                color: white;
                border: none;
                padding: 4px 8px;
                cursor: pointer;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <h1>Robins Webseite</h1>
        <p>Hier kommunizieren wir mit unserer Python-API!</p>

        <form id="greetForm">
            <label>Name: <input name="name" /></label>
            <button type="submit">Grüssen</button>
        </form>
        <p id="output" class="muted"></p>

        <script>
            const API = "http://127.0.0.1:5000";
            const form = document.getElementById("greetForm");
            const out = document.getElementById("output");

            form.addEventListener("submit", async (e) => {
                e.preventDefault();
                const name = new FormData(form).get("name") || "Robin";
                const res = await fetch(
                    `${API}/api/greet?name=${encodeURIComponent(name)}`
                );
                const data = await res.json();
                out.textContent = data.message;
            });
        </script>
    </body>
</html>
```

---

### Step 4: Raspberry Pi Deployment

Auf dem Pi:

```bash
sudo apt update && sudo apt install -y python3 nginx git
git clone https://github.com/robinherger/robin-projekt.git
cd robin-projekt
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors gunicorn
gunicorn -b 0.0.0.0:8000 app:app
```

Test:  
[http://pi3.local:8000/api/greet](http://pi3.local:8000/api/greet)

---

### Step 5: Service & Reverse Proxy (für echten Webserver)

#### systemd-Service `/etc/systemd/system/robin-api.service`

```ini
[Unit]
Description=Robin Flask API
After=network.target

[Service]
User=robin
WorkingDirectory=/home/robin/robin-projekt
Environment="PATH=/home/robin/robin-projekt/.venv/bin"
ExecStart=/home/robin/robin-projekt/.venv/bin/python -m gunicorn -b 0.0.0.0:8000 app:app
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

#### nginx-Konfiguration `/etc/nginx/sites-available/robin`

```yml
server {
    listen 80;
    server_name _;

    root /home/robin/robin-projekt;
    index index.html;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
    }
}
```

Reload:

```bash
sudo systemctl enable --now robin-api

sudo ln -s /etc/nginx/sites-available/robin /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

sudo chmod 711 /home/robin
sudo find /home/robin/robin-projekt -type d -exec chmod 755 {} \;
sudo find /home/robin/robin-projekt -type f -exec chmod 644 {} \;

sudo nginx -t && sudo systemctl reload nginx

```

Dann:  
[http://pi3.local/](http://pi3.local/) → Website  
[http://pi3.local/api/greet](http://pi3.local/api/greet) → API

---
