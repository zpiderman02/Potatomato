from flask import Flask, render_template, request, redirect, url_for
import random
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Send verification email (example with an SMTP provider like Gmail or Elastic Email)
        verification_code = random.randint(100000, 999999)  # Simple 6-digit code

        # Send the code via email (Elastic Email or another service)
        send_verification_email(email, verification_code)

        # Store the verification code temporarily (can be stored in a session or database)
        return redirect(url_for('verify', email=email))  # Redirect to verify page

    return render_template('signup.html')


def send_verification_email(email, code):
    subject = "Your Verification Code"
    body = f"Your verification code is: {code}"

    # Using Elastic Email or any other SMTP provider
    sender_email = "youremail@example.com"
    receiver_email = email
    password = "yourpassword"  # Use app password for Gmail or appropriate SMTP password

    # Compose the email
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP('smtp.elasticemail.com', 2525) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        code_entered = request.form['code']
        # Here, check the verification code entered by the user
        # If it's correct, finalize the sign-up process
        # Otherwise, show an error message
        return "Verification Successful!"  # Or redirect to login page

    return render_template('verify.html')


if __name__ == '__main__':
    app.run(debug=True)
