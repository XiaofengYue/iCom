from app import db


class Collection(db.Model):
    __tablename__ = 'collections'

    col_id = db.Column(db.Integer, primary_key=True)
    col_usernum = db.Column(db.Integer, db.ForeignKey('users.user_num'))
    col_comid = db.Column(db.Integer, db.ForeignKey('competitions.com_id'))
    col_album = db.Column(db.String(45), nullable=True)

    def __repr__(self):
        return '<COLLECTION:>' + str(self.col_id)

    def to_dict(self):
        return {"col_id": self.col_id, "col_usernum": self.col_usernum, "col_comid": self.col_comid, "col_album": self.col_album}
