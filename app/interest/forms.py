from app import db


class Interest(db.Model):
    __tablename__ = 'interests'

    int_id = db.Column(db.Integer, primary_key=True)
    int_usernum = db.Column(db.Integer, db.ForeignKey('users.user_num'))
    int_typename = db.Column(db.String(45))

    def __repr__(self):
        return '<INTERESTS:>' + str(self.int_id)

    def to_dict(self):
        return {"int_id": self.int_id, "int_usernum": self.int_usernum, "int_typename": self.int_typename}
