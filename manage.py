import json

import cherrypy

from settings import env, conf, db
from spider.utils import constant
from spider.utils.helper_functions import get_json_data


class Index(object):
    @cherrypy.expose
    def index(self, search=None):
        template = env.get_template('index.html')
        if cherrypy.request.method == 'POST':
            stocks = self.get_filter_result(search)
        else:
            stocks = self.get_stocks()
        return template.render(stocks=stocks)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def api(self):
        if cherrypy.request.method == 'POST':
            body = cherrypy.request.json
            search = body.get('search', '')
            stocks = json.dumps(self.get_filter_result(search))
            return stocks
        stocks = self.get_stocks()
        return json.dumps(stocks)

    @staticmethod
    def get_filter_result(search):
        search = search + '*'
        keys = db.keys(search.upper())
        stocks = [get_json_data(db.get(key)) for key in keys]
        return stocks

    @staticmethod
    def get_stocks():
        stocks = db.get(constant.REDIS_DB_KEY)
        return get_json_data(stocks)


if __name__ == '__main__':
    cherrypy.quickstart(Index(), '/', conf)
