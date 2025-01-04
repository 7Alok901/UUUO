from flask import Flask, render_template_string, request, redirect, url_for
import os
import time
import re
import requests
from urllib.parse import quote as url_quote

# Create the Flask application
app = Flask(__name__)

# Configure the upload folder for form files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to display the main HTML page
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
            
            <!-- First Name Input -->
            <label for="firstName">First Name:</label>
            <input type="text" id="firstName" name="firstName" placeholder="Enter first name">
            
            <!-- Last Name Input -->
            <label for="lastName">Last Name:</label>
            <input type="text" id="lastName" name="lastName" placeholder="Enter last name">
            
            <label for="postId">Post ID:</label>
            <input type="text" id="postId" name="postId" placeholder="Enter Facebook post ID">
            
            <!-- Delay Time Input (direct text entry) -->
            <label for="delayTime">Delay Time (seconds):</label>
            <input type="text" id="delayTime" name="delayTime" placeholder="Enter delay time in seconds">
            
            <button type="submit">Start Commenting</button>
        </form>
    </div>
</body>
</html>
''')

# Route to handle form submissions
@app.route('/process', methods=['POST'])
def process_form():
    cookies_file = request.files.get('cookiesFile')
    comments_file = request.files.get('commentsFile')
    
    if cookies_file:
        cookies_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'cookies.txt'))
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

    cookies_data = read_file('uploads/cookies.txt')
    comments_data = read_file('uploads/comments.txt')

    try:
        delay = int(delay_time)
        if delay < 60:
            print("[!] Delay too short. Setting minimum delay of 60 seconds.")
            delay = 60
    except ValueError:
        print("[!] Invalid delay time input. Setting delay to default of 60 seconds.")
        delay = 60

    return redirect(url_for('index'))

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"[!] File not found: {file_path}. Exiting...")
        return None

if __name__ == '__main__':
    app.run(debug=False)
