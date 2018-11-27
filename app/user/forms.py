from app import db


class User(db.Model):
    __tablename__ = 'users'
    user_num = db.Column(db.Integer, primary_key=True)
    user_pwd = db.Column(db.String(45))
    user_roleid = db.Column(db.Integer, db.ForeignKey('role_id'))
    user_name = db.Column(db.String(45), nullable=True)
    user_truename = db.Column(db.String(45), nullable=True)
    user_sex = db.Column(db.String(45), nullable=True)
    user_birthday = db.Column(db.String(45), nullable=True)
    user_interest = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.user_num

    def to_dict(self):
        # "user_num": self.user_num, "user_pwd": self.user_pwd,
        return {"user_roleid": self.user_roleid, "user_name": self.user_name, "user_truename": self.user_truename, "user_sex": self.user_sex, "user_birthday": self.user_birthday, "user_interest": self.user_interest}
