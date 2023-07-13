from flask import Flask, render_template, url_for, flash, redirect
from flask_behind_proxy import FlaskBehindProxy

app = Flask(__name__)

@app.route('/create_password')
def create_password():
    return render_template('passwordCreator.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
