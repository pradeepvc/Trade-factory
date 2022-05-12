from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String())
    name = db.Column(db.String())
    password = db.Column(db.String())
    api_key = db.Column(db.String())
    api_secret_key = db.Column(db.String())
    totp_key = db.Column(db.String())
    access_key = db.Column(db.String())
    access_key_time = db.Column(db.String())
    autologin_status = db.Column(db.String(80))
    autologin1 = db.Column(db.String(80))
    autologin_verify = db.Column(db.String(80))
    sp_buy_n = db.Column(db.String())
    sp_sell_n = db.Column(db.String())
    sp_buy_bn = db.Column(db.String())
    sp_sell_bn = db.Column(db.String())
    q_n = db.Column(db.String())
    q_bn = db.Column(db.String())

    def __init__(self, user_id, name, password, api_key, api_secret_key, totp_key, access_key,
                 access_key_time, autologin_status, autologin1, autologin_verify, sp_buy_n, sp_sell_n, sp_buy_bn,
                 sp_sell_bn, q_n, q_bn):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.totp_key = totp_key
        self.access_key = access_key
        self.access_key_time = access_key_time
        self.autologin_status = autologin_status
        self.autologin1 = autologin1
        self.autologin_verify = autologin_verify
        self.sp_buy_n = sp_buy_n
        self.sp_sell_n = sp_sell_n
        self.sp_buy_bn = sp_buy_bn
        self.sp_sell_bn = sp_sell_bn
        self.q_n = q_n
        self.q_bn = q_bn

    def __repr__(self):
        return f"{self.user_id}:{self.name}"
