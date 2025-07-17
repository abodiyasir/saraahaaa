
from flask import Flask, render_template, request, redirect, url_for, session
import datetime
import socket
import requests

app = Flask(__name__)
app.secret_key = 'secretkey'

messages = []

def get_client_info(req):
    ip = req.remote_addr or req.environ.get('HTTP_X_FORWARDED_FOR', 'N/A')
    user_agent = req.headers.get('User-Agent', 'N/A')
    try:
        location = requests.get(f'https://ipapi.co/{ip}/json/').json()
        city = location.get('city', 'Unknown')
        country = location.get('country_name', 'Unknown')
    except:
        city, country = 'Unknown', 'Unknown'
    return ip, user_agent, f"{city}, {country}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        ip, user_agent, location = get_client_info(request)
        messages.append({
            'text': message,
            'ip': ip,
            'device': user_agent,
            'location': location,
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'abo12345':
            session['admin'] = True
        else:
            return render_template('admin_login.html', error="كلمة المرور غير صحيحة")
    if not session.get('admin'):
        return render_template('admin_login.html')
    return render_template('admin.html', messages=messages)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
