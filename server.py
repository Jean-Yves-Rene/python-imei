from flask import Flask, render_template,redirect, url_for, flash
from waitress import serve
import logging
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
app.logger.info('Application started')
# Home route
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
