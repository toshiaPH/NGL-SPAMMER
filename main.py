import random
import time
import json
import urllib.request
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.37 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
]

for _ in range(293):  
    user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500, 600)}.{random.randint(1, 99)} (KHTML, like Gecko) Chrome/{random.randint(80, 95)}.0.{random.randint(4000, 5000)}.{random.randint(100, 999)} Safari/{random.randint(500, 600)}.{random.randint(1, 99)}"
    USER_AGENTS.append(user_agent)


console_logs = []

def neon_print(message):
    return message

def send_message_to_user(username, message):
    url = 'https://ngl.link/api/submit'
    data = {
        'username': username,
        'question': message,
        'deviceId': "" 
    }
    headers = {'Content-Type': 'application/json'}
    headers['User-Agent'] = random.choice(USER_AGENTS)
    try:
        req = urllib.request.Request(url, method='POST', headers=headers)
        with urllib.request.urlopen(req, json.dumps(data).encode('utf-8')) as response:
            status_code = response.getcode()
            if status_code == 200:
                return 200, None
            else:
                return status_code, f"HTTP Error: {status_code}"
    except Exception as err:
        return 500, str(err)

def handle_message_sending(username, message, attempts):
    for attempt in range(1, int(attempts) + 1):
        status_code, error_msg = send_message_to_user(username, message)
        status_msg = "COMPLETE" if status_code == 200 else "error"

        if status_msg == "error":
            console_logs.append(f"[{attempt}] [{status_msg}]: SENDED TO  {username} - Error: {error_msg}")
        else:
            console_logs.append(f"[{attempt}] [{status_msg}]: SENDED TO {username}")
        time.sleep(2)

@app.route('/')
def index():
    return render_template('home.html', console_logs=console_logs)

@app.route('/ngl', methods=['POST'])
def send_spam_message():
    user_link = request.form.get('link')
    message = request.form.get('message')
    amount = request.form.get('amount')

    if not user_link or not message or not amount:
        return jsonify({"error_msg": "Please provide all inputs"}), 400
    if not user_link.startswith("https://ngl.link/"):
        return jsonify({"error_msg": "Invalid link"}), 400

    username = user_link.split('/')[-1]
    handle_message_sending(username, message, amount)
    return jsonify({"msg": "Successful spam message"}), 200

@app.route('/console_logs')
def get_console_logs():
    return jsonify({"logs": console_logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
