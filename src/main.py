from flask import Flask

from blueprints.executor import executor
from blueprints.user import user

app = Flask(__name__, static_url_path="")
app.register_blueprint(executor)
app.register_blueprint(user)

@app.route('/') 
def homepage():
    return app.send_static_file("index.html")

@app.route('/backdoor') 
def backdoor_page():
    return app.send_static_file("backdoor.html")

if __name__ == "__main__":
    app.run(debug=True)