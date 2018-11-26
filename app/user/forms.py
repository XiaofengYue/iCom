from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(320))
    password = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'password': self.password}
