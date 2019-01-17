from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Página inciial')


if __name__ == '__main__':
    #app.run()
    app.run(host='localhost', port=8000, debug=True)


