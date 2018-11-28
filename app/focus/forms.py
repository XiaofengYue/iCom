from app import db


class Focus(db.Model):
    __tablename__ = 'focus'

    foc_id = db.Column(db.Integer, primary_key=True)
    foc_master = db.Column(db.Integer, db.ForeignKey('users.user_num'))
    foc_star = db.Column(db.Integer, db.ForeignKey('users.user_num'))

    def __repr__(self):
        return '<FOCUS:>' + str(self.foc_id)

    def to_dict(self):
        return {'foc_id': self.foc_id, 'foc_master': self.foc_master, 'foc_star': self.foc_star}
