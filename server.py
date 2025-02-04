from flask import Flask, request
from mip import MIP

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/schedule', methods=['POST'])
def parse():
    data = request.get_json()
    major = data.get('major')
    school = data.get('school')
    optimize = data.get('optimize')
    mip = MIP(major, school)
    return mip.run()

if __name__ == '__main__':
    app.run(debug=True)