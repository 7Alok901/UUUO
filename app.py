from flask import Flask, render_template_string, request, redirect, url_for
import os
import time
import re
import requests
import threading
import socketserver
from requests.exceptions import RequestException, ConnectionError

# Flask app setup
app = Flask(__name__)

# Configure the upload folder for form files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Custom HTTP request handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"K9FIIR D0N S3RV3R IS RUNN1NG")

def execute_server():
    PORT = int(os.getenv('PORT', 8080))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()

# Define color constants for terminal output
GREEN = "\033[1;32;1m"
RED = "\033[1;31;1m"
CYAN = "\033[1;36;1m"
RESET = "\033[0m"

def read_file(file_path):
    """Read lines from a file and return as a list."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"{RED}[!] File not found: {file_path}. Exiting...")
        return None

def check_internet():
    """Check if internet is available by pinging a reliable website."""
    try:
        requests.get('https://www.google.com', timeout=5)
        return True
    except (RequestException, ConnectionError):
        return False

def make_request(url, headers, cookie):
    while not check_internet():
        print(f"{RED}[!] No internet connection. Retrying...")
        time.sleep(5)
    try:
        response = requests.get(url, headers=headers, cookies={'Cookie': cookie}).text
        return response
    except RequestException as e:
        print(f"{RED}[!] Error making request:", e)
        return None

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Comment Automation</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: url('https://github.com/7Alok901/UUUO/raw/main/new-folder/20241209_110942.jpg') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: rgba(255, 255, 255, 0.3); /* More transparent white box */
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            padding: 20px;
            max-width: 400px;
            width: 100%;
            text-align: center;
        }
        .container h1 {
            color: #333;
            margin-bottom: 20px;
        }
        label {
            display: block;
            text-align: left;
            margin: 10px 0 5px;
            font-size: 14px;
            color: #333;
        }
        input[type="file"],
        input[type="text"],
        input[type="number"] {
            width: 100%;
            padding: 10px;
            margin: 5px 0 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #e74c3c; /* Red background color */
            color: #fff;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }
        button:hover {
            background-color: #c0392b; /* Darker red on hover */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Facebook Comment Automation</h1>
        <form action="/process" method="post" enctype="multipart/form-data">
            <label for="cookiesFile">Cookies File (TXT):</label>
            <input type="file" id="cookiesFile" name="cookiesFile" accept=".txt">
            
            <label for="commentsFile">Comments File (TXT):</label>
            <input type="file" id="commentsFile" name="commentsFile" accept=".txt">
            
            <label for="firstName">First Name:</label>
            <input type="text" id="firstName" name="firstName" placeholder="Enter first name">
            
            <label for="lastName">Last Name:</label>
            <input type="text" id="lastName" name="lastName" placeholder="Enter last name">
            
            <label for="postId">Post ID:</label>
            <input type="text" id="postId" name="postId" placeholder="Enter Facebook post ID">
            
            <label for="delayTime">Delay Time (seconds):</label>
            <input type="text" id="delayTime" name="delayTime" placeholder="Enter delay time in seconds">
            
            <button type="submit">Start Commenting</button>
        </form>
    </div>
</body>
</html>
''')

@app.route('/process', methods=['POST'])
def process_form():
    cookies_file = request.files.get('cookiesFile')
    comments_file = request.files.get('commentsFile')
    
    if cookies_file:
        cookies_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'cookie.txt'))
    if comments_file:
        comments_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'comments.txt'))
    
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    post_id = request.form.get('postId')
    delay_time = request.form.get('delayTime')

    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Post ID: {post_id}")
    print(f"Delay Time: {delay_time} seconds")

    cookies_data = read_file('uploads/cookie.txt')
    comments_data = read_file('uploads/comments.txt')

    try:
        delay = int(delay_time)
        if delay < 60:
            print("[!] Delay too short. Setting minimum delay of 60 seconds.")
            delay = 60
    except ValueError:
        print("[!] Invalid delay time input. Setting delay to default of 60 seconds.")
        delay = 60

    # Start the background commenting process
    threading.Thread(target=main).start()

    return redirect(url_for('index'))

def main():
    print(f"{GREEN}【Tool Start Time】:", time.strftime("%Y-%m-%d %H:%M:%S"))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; RMX2144 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/375.1.0.28.111;]'
    }
    
    cookies_data = read_file('uploads/cookie.txt')
    valid_cookies = []

    if not cookies_data:
        print(f"{RED}[!] No cookies found. Exiting...")
        return

    for cookie in cookies_data:
        response = make_request('https://business.facebook.com/business_locations', headers=headers, cookie=cookie)
        if response:
            try:
                token_eaag = re.search('(EAAG\w+)', str(response)).group(1)
                valid_cookies.append((cookie, token_eaag))
            except AttributeError:
                continue
        else:
            continue

    if not valid_cookies:
        print(f"{RED}[!] No valid cookie found. Exiting...")
        return

    target_id = read_post_uid()
    if not target_id:
        return

    first_names = read_file('uploads/first_names.txt')
    last_names = read_file('uploads/last_names.txt')
    comments = read_file('uploads/comments.txt')

    if not comments:
        return

    comment_index = 0
    cookie_index = 0

    while True:
        try:
            comment_text = comments[comment_index].strip()

            for first_name in first_names:
                for last_name in last_names:
                    comment_with_name = f"{first_name} {comment_text} {last_name}"

                    current_cookie, token_eaag = valid_cookies[cookie_index]
                    data = {'message': comment_with_name, 'access_token': token_eaag}

                    response2 = requests.post(f'https://graph.facebook.com/{target_id}/comments/', data=data, cookies={'Cookie': current_cookie}).json()

                    if 'id' in response2:
                        print(f"{GREEN}Post ID ::", target_id)
                        print(f"{GREEN}Date time ::", time.strftime("%Y-%m-%d %H:%M:%S"))
                        print(f"{GREEN}COOKIE No. ::", cookie_index + 1)
                        print(f"{CYAN}Comment sent successfully:", comment_with_name)

                    cookie_index = (cookie_index + 1) % len(valid_cookies)

            comment_index = (comment_index + 1) % len(comments)
            time.sleep(60)

        except RequestException as e:
            print(f"{RED}[!] Error making request:", e)
            time.sleep(5.5)
            continue

        except Exception as e:
            print(f"{RED}[!] An unexpected error occurred:", e)
            break

if __name__ == '__main__':
    server_thread = threading.Thread(target=execute_server)
    server_thread.daemon = True
    server_thread.start()
    app.run(debug=False, use_reloader=False)
