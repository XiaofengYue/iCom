from app import db


class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(45))
    role_desc = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<ROLE>' + self.role_name

    def to_dict(self):
        return {'role_id': self.role_id, 'role_name': self.role_name, 'role_desc': self.role_desc}
