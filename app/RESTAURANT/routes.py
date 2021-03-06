from flask import Blueprint, jsonify, request
from app.RESTAURANT.forms import Rest, Useritem, Msg
import jieba
from wordcloud import WordCloud
from sqlalchemy import func

rests = Blueprint('rests', __name__)


def return_json(code=200, msg='成功', data=None):
    return jsonify({'code': code, 'msg': msg, 'data': data})


@rests.route('/rest/allrest', methods=['POST'])
def get_all():
    rests = Rest.query.all()
    return return_json(data=[rest.to_dict() for rest in rests])


@rests.route('/rest/byid', methods=['POST'])
def get_id():
    try:
        p_id = request.json.get("id")
        rest = Rest.query.filter(Rest.item_id == p_id).first()
        return return_json(data=rest.to_dict())
    except Exception as e:
        raise e
        return return_json(code=0, msg='失败')


@rests.route('/rest/picbyid', methods=['POST'])
def get_pic_id():
    try:
        p_id = request.json.get("id")
        items = Useritem.query.filter(Useritem.item_id == p_id).all()
        books = ''
        for item in items:
            books += item.review
        print(books)
        if books == '':
            return return_json(code=1,msg='无评论')
        if get_pic(books, p_id):
            return return_json(data='http://www.pipicat.top/static/iCom_images/'+str(p_id)+'ciyun.jpg')

    except Exception as e:
        raise e
        return return_json(code=0, msg='失败')


def get_pic(books, p_id):
    words = jieba.lcut(books)
    excludes = {'团购', '点评', '这么', '就是', '只是', '有点', '今天', '这么', '为啥', '下次', '里面'}
    counts = {}
    for word in words:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    for word in excludes:
        if word in counts:
            del(counts[word])

    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)

    list_name = []
    max_sum = min(len(items), 30)
    for i in range(max_sum):
        word, count = items[i]
        list_name.append(word)
    string = ' '.join(list_name)

    font = r'SimSun.ttf'
    wc = WordCloud(font_path=font, background_color='white', width=1000, height=800,).generate(string)
    wc.to_file('/home/yxf/myproject/flask_demo/flaskblog/static/iCom_images/'+str(p_id)+'ciyun.jpg')

    return True


@rests.route('/rest/combyid', methods=['POST'])
def get_com_id():
    try:
        p_id = request.json.get("id")
        items = Useritem.query.filter(Useritem.item_id == p_id).all()
        return return_json(data=[item.to_dict() for item in items])
    except Exception:
        return return_json(code=0, msg='失败')


@rests.route('/rest/msg', methods=['POST'])
def get_msg():
    try:
        msgs = Msg.query.all()
        tasts = Rest.query.order_by(Rest.tast.desc()).limit(5)
        environments = Rest.query.order_by(Rest.environment.desc()).limit(5)
        services = Rest.query.order_by(Rest.service.desc()).limit(5)
        return return_json(data={"type":[msg.to_dict() for msg in msgs], "tasts": [tast.to_dict() for tast in tasts], "environments": [tast.to_dict() for tast in environments], "services": [tast.to_dict() for tast in services]})
    except Exception as e:
        raise e
        return return_json(code=0, msg='失败')

@rests.route('/rest/allcom', methods = ['POST'])
def get_all_com_date():
    try:
        items = Useritem.query.all()
        return return_json(data=[item.times for item in items])
    except Exception:
        return return_json(code=0,msg='失败')
