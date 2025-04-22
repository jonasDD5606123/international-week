from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    # print('')  # This will print in the terminal/console
    return 'test'

if __name__ == '__main__':
    app.run(debug=True)
