from app import db


class Rest(db.Model):
    __tablename__ = 'REST'

    item_id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    star = db.Column(db.String(255), nullable=True)
    cost = db.Column(db.String(255), nullable=True)
    tast = db.Column(db.String(255), nullable=True)
    environment = db.Column(db.String(255), nullable=True)
    service = db.Column(db.String(255), nullable=True)
    review_count = db.Column(db.String(255), nullable=True)
    item_pic = db.Column(db.String(255), nullable=True)
    item_cat = db.Column(db.String(255), nullable=True)
    item_loc = db.Column(db.String(255), nullable=True)
    item_key_word = db.Column(db.String(255), nullable=True)
    lng = db.Column(db.String(255), nullable=True)
    lat = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<Rest>' + self.item_id

    def to_dict(self):
        return {'item_id': self.item_id,
                'name': self.name,
                'star': self.star,
                'cost': self.cost,
                'tast': self.tast,
                'environment': self.environment,
                'service': self.service,
                'review_count': self.review_count,
                'item_pic': self.item_pic,
                'item_cat': self.item_cat,
                'item_loc': self.item_loc,
                'item_key_word': self.item_key_word,
                'lng': self.lng,
                'lat': self.lat}


class Useritem(db.Model):
    __tablename__ = 'USERITEM'

    data_id = db.Column(db.String(45), primary_key=True)
    user_id = db.Column(db.String(255), nullable=True)
    item_id = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.String(255), nullable=True)
    tast = db.Column(db.String(255), nullable=True)
    environment = db.Column(db.String(255), nullable=True)
    service = db.Column(db.String(255), nullable=True)
    times = db.Column(db.String(255), nullable=True)
    month = db.Column(db.String(255), nullable=True)
    review = db.Column(db.String(255), nullable=True)
    user_pic = db.Column(db.String(255), nullable=True)
    recommend = db.Column(db.String(255), nullable=True)
    user_name = db.Column(db.String(255), nullable=True)
    user_rank = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<Useritem>' + self.data_id

    def to_dict(self):
        return {
            'data_id': self.data_id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'rating': self.rating,
            'tast': self.tast,
            'environment': self.environment,
            'service': self.service,
            'times': self.times,
            'month': self.month,
            'review': self.review,
            'user_pic': self.user_pic,
            'recommend': self.recommend,
            'user_name': self.user_name,
            'user_rank': self.user_rank}
