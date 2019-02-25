from flask_restful import reqparse, abort, Api, Resource
from data_base_control import *
from flask import *


app = Flask(__name__)
api = Api(app)
dbase = DB()

def abort_if_news_not_found(lvl_id):
    if not Levels(dbase.get_connection()).get(lvl_id):
        abort(404, message="Level {} not found".format(lvl_id))

class GetLevel(Resource):
    def get(self, lvl_id):
        abort_if_news_not_found(lvl_id)
        level = Levels(dbase.get_connection()).get(lvl_id)
        return level

lvl = GetLevel().get(lvl_id='45')
print(lvl)