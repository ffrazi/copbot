from flask import Flask, render_template, url_for
from backend.routes.chat import chat_blueprint
app = Flask(__name__)
app.register_blueprint(chat_blueprint, url_prefix='/api')


# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Chat Page
@app.route('/chat')
def chat():
    return render_template('chat.html')

# Emergency Page
@app.route('/emergency')
def emergency():
    return render_template('emergency.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8000)