from os import getenv


class Config:
    # Database config
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email config
    SMTP_SERVER = getenv("SMTP_SERVER")
    SMTP_PORT = getenv("SMTP_PORT")
    EMAIL = getenv("EMAIL")
    PASSWORD = getenv("PASSWORD")
    SENDER = getenv("SENDER")
    DESTINATION = getenv("DESTINATION")
