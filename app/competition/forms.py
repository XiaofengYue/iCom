from app import db


class Competition(db.Model):
    __tablename__ = 'competitions'
    com_id = db.Column(db.Integer, primary_key=True)
    com_url = db.Column(db.String(255), nullable=True)
    com_squrl = db.Column(db.String(255), nullable=True)
    com_picture = db.Column(db.String(255), nullable=True)
    com_title = db.Column(db.String(255))
    com_signupstart = db.Column(db.String(45), nullable=True)
    com_signupend = db.Column(db.String(45), nullable=True)
    com_starttime = db.Column(db.String(45), nullable=True)
    com_endtime = db.Column(db.String(45), nullable=True)
    com_sponsor = db.Column(db.String(255))
    com_publisher = db.Column(db.Integer, db.ForeignKey('users.user_num'), default=15681953321)
    com_level = db.Column(db.String(45), nullable=True)
    com_type = db.Column(db.String(255), nullable=True)
    com_mode = db.Column(db.String(45), nullable=True)
    com_object = db.Column(db.String(255), nullable=True)
    com_browse = db.Column(db.Integer)

    def __repr__(self):
        return '<COMPETITION:>' + self.com_id

    def to_dict(self):
        return {"com_id": self.com_id, "com_url": self.com_url, "com_squrl": self.com_squrl, "com_picture": self.com_picture, "com_title": self.com_title, "com_signupstart": self.com_signupstart, "com_signupend": self.com_signupend, "com_starttime": self.com_starttime, "com_endtime": self.com_endtime, "com_sponsor": self.com_sponsor, "com_publisher": self.com_publisher, "com_level": self.com_level, "com_type": self.com_type, "com_mode": self.com_mode, "com_object": self.com_object, "com_browse": self.com_browse}
