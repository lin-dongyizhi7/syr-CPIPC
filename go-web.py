from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

def upload_file():
    if request.method == 'POST':
        file = request.files['the_file']
        print(file)

if __name__ == '__main__':
    app.run()