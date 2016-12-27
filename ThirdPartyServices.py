from flask import Flask

app = Flask(__name__)


@app.route('/v1/')
def status():
    return 'Status: Online'



if __name__ == '__main__':
    app.run()
