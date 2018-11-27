from app import db


class Competition(db.Model):
    __tablename__ = 'competitions'
    com_id = db.Column(db.Integer, primary_key=True)
    com_url = db.Column(db.String(45), nullable=True)
    com_signurl = db.Column(db.String(45), nullable=True)
    com_title = db.Column(db.String(45))
    com_registrationstart = db.Column(db.String(45), nullable=True)
    com_registrationdeadline = db.Column(db.String(45), nullable=True)
    com_starttime = db.Column(db.String(45), nullable=True)
    com_endtime = db.Column(db.String(45), nullable=True)
    com_sponsor = db.Column(db.String(45))
    com_level = db.Column(db.String(45), nullable=True)
    com_districtrestriction = db.Column(db.String(45), nullable=True)
    com_publisher = db.Column(db.String(45))
    com_picture = db.Column(db.String(45), nullable=True)

    def __repr__(self):
        return '<ROLE>' + self.com_id

    def to_dict(self):
        return {"com_id": com_id, "com_url": com_url, "com_signurl": com_signurl, "com_title": com_title, "com_registrationstart": com_registrationstart, "com_registrationdeadline": com_registrationdeadline, "com_starttime": com_starttime, "com_endtime": com_endtime, "com_sponsor": com_sponsor, "com_level": com_level, "com_districtrestriction": com_districtrestriction, "com_publisher": com_publisher, "com_picture": com_picture}
