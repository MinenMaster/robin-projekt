from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.get("/api")
def index():
    return "API is running!"

@app.get("/api/greet")
def greet():
    name = request.args.get("name")
    return f"Hallo {name}!"

@app.post("/api/greet")
def greet_post():
    data = request.get_json()
    name = data.get("name")
    return {"message": f"Hallo {name}!"}

@app.get('/api/temp')
def temp():
    celsius = request.args.get('celsius')
    kelvin = request.args.get('kelvin')
    if celsius and kelvin:
        return "Error: You can only provide one temperature"
    elif celsius:
        celsius = float(celsius)
        kelvin = celsius + 273.15
        return {
            "celsius": celsius,
            "kelvin": kelvin
        }
    elif kelvin:
        kelvin = float(kelvin)
        celsius = kelvin - 273.15
        return {
            "celsius": celsius,
            "kelvin": kelvin
        } 
    else:
        return "Error: No temperature provided"

if __name__ == "__main__":
    app.run(debug=True)