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
    fahrenheit = request.args.get('fahrenheit')
    if celsius and fahrenheit:
        return "Error: You can only provide one temperature"
    elif celsius:
        celsius = float(celsius)
        fahrenheit = (celsius * 1.8) + 32
        return {
            "celsius": celsius,
            "fahrenheit": fahrenheit
        }
    elif fahrenheit:
        fahrenheit = float(fahrenheit)
        celsius = (fahrenheit - 32) / 1.8
        return {
            "celsius": celsius,
            "fahrenheit": fahrenheit
        } 
    else:
        return "Error: No temperature provided"

if __name__ == "__main__":
    app.run(debug=True)