from flask import Flask  
from flask_mail import Message  
from flask_mail import Mail  
  
app = Flask(__name__)  

app.config.update(dict(
    MAIL_SERVER = 'smtp.163.com',
    MAIL_PORT = 456,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_DEBUG = True,
    MAIL_USERNAME = 'liuyuhaoweb@163.com',
    MAIL_PASSWORD = 'ELCUNEUDEMBQXKRV',
    MAIL_DEFAULT_SENDER = 'liuyuhaoweb@163.com')
)
mail = Mail(app)  
@app.route('/')  
def home():  
    with app.app_context():
        msg = Message("Hello Email",  
                   recipients=["1944669201@qq.com"])  
        msg.body = "This is a test email sent from Flask-Mail"  
        mail.send(msg)  
    return 'Email sent!'  

if __name__ == '__main__':  
    app.run(debug=True)
