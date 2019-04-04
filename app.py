import os
from flask import Flask

app = Flask(__name__)
# app.config["MONGO_DBNAME"] = 'online_cookbook'
# app.config["MONGO_URI"] = 'mongodb://admin:admin@ds123926.mlab.com:23926/task_manager'

# mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'Hello World'


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)