from passlib.apps import custom_app_context as pwd_context
from app import db


class User(db.Model):
    __tablename__ = 'users'
    user_num = db.Column(db.Integer, primary_key=True)
    user_roleid = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    user_name = db.Column(db.String(45), nullable=True)
    user_headimage = db.Column(db.String(255), nullable=True)
    user_sex = db.Column(db.String(45), nullable=True)
    user_birthday = db.Column(db.String(45), nullable=True)
    user_interest = db.Column(db.String(255), nullable=True)
    user_pwd_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.user_pwd_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.user_pwd_hash)

    def __repr__(self):
        return '<User %r>' % self.user_num

    def to_dict(self):
        # "user_num": self.user_num, "user_pwd": self.user_pwd,
        return {"user_num": self.user_num, "user_roleid": self.user_roleid, "user_name": self.user_name, "user_headimage": self.user_headimage, "user_sex": self.user_sex, "user_birthday": self.user_birthday, "user_interest": self.user_interest}
