from flask import Flask, render_template, request, make_response
import hashlib
import base64

app = Flask(__name__)
users = [
    {"username": "test", "password": "hardtocrack"},
    {"username": "demo", "password": "iloveyou"},
]

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    remember_me = request.form.get('remember_me')

    user = next((user for user in users if user['username'] == username), None)
    if user:
        password_md5 = hashlib.md5(password.encode()).hexdigest()
        if hashlib.md5(user['password'].encode()).hexdigest() == password_md5:
            response = make_response('Login success!')
            if remember_me:
                encoded_cookie = base64.b64encode(f"{username}:{password_md5}".encode()).decode()
                response.set_cookie('remember_me_cookie', value=encoded_cookie)
            return response
    return 'Login failed!'

if __name__ == '__main__':
    app.run(debug=True)
