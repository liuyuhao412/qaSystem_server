#这是配置文件
import os
from datetime import timedelta

class Config:
    #flask密钥和session等相关配置
    SECRET_KEY = os.environ.get ('SECRET_KEY') or "Liu412"  #配置环境变量
    PERMANENT_SESSION_LIFETIME = timedelta (days=7)

class DevelopmengConfig(Config):
    DEBUG = True
    #数据库的配置信息
    USERNAME = 'root'
    PASSWORD = '123456'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'qa_system'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOST, PORT,DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS=False #动态追踪修改设置，没有设置会有警告
    SQLALCHEMY_ECHO = False #   #查询时显示原始SQL语句
    
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = 'liuyuhaoweb@163.com'
    MAIL_PASSWORD = 'ELCUNEUDEMBQXKRV'
    MAIL_DEFAULT_SENDER = 'liuyuhaoweb@163.com'



class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development':DevelopmengConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmengConfig
}