from flask import Flask, render_template

app = Flask(__name__)

# Flask configuration parameters #
app.config['debug'] = True  # Testing only
app.secret_key = 'hella secret'


# TODO everything
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
