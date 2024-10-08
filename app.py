from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    # Fetch data from the API
    api_url = "https://mocki.io/v1/a0f82128-4e3b-4091-8f8e-99f6192b18b3"
    response = requests.get(api_url)
    expenses = response.json()
    return render_template('home.html', expenses=expenses)

@app.route('/login', methods=['POST'])
def login_post():
    # Here you would normally check the credentials
    # For now, we'll just redirect to the home page
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)