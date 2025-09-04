# topo do arquivo
import os, smtplib, ssl, traceback
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__, template_folder='.')
app.secret_key = "change-this"

SMTP_HOST = os.getenv("SMTP_HOST", "mail.privateemail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))  # SSL direto
SMTP_USER = os.getenv("SMTP_USER", "info@paristourtravel.com")
SMTP_PASS = os.getenv("SMTP_PASS", "paristourtravel2025")  # ideal: App Password

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name","").strip()
    email = request.form.get("email","").strip()
    phone = request.form.get("phone","").strip()
    message = request.form.get("message","").strip()

    if not name or not email or not message:
        flash("Please fill in Name, Email and Message.")
        return redirect(url_for("home") + "#contact")

    msg = EmailMessage()
    msg["Subject"] = f"[Paris Travel] New Contact from {name}"
    msg["From"]    = SMTP_USER               # TEM que ser o mesmo do login
    msg["To"]      = SMTP_USER               # vai para você
    msg["Reply-To"]= email                   # responder vai para o cliente
    msg.set_content(
        f"New lead:\n\nName: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}\n"
    )

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=30) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        flash("Your message was sent successfully! We'll contact you soon.")
    except smtplib.SMTPAuthenticationError as e:
        print("AUTH ERROR:", e)
        flash("Email auth failed. Check SMTP user/password (or App Password).")
    except Exception as e:
        print("=== EMAIL ERROR BEGIN ===")
        traceback.print_exc()
        print("=== EMAIL ERROR END ===")
        flash("Something went wrong while sending your message. Please try again later.")
    return redirect(url_for("home") + "#contact")

if __name__ == "__main__":
    app.run(debug=True)
