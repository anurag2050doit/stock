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

    @staticmethod
    def get_filter_result(search):
        search = search + '*'
        keys = db.keys(search.upper())
        stocks = [get_json_data(db.get(key)) for key in keys]
        return stocks

    @staticmethod
    def get_stocks():
        stocks = db.get(constant.REDIS_DB_KEY)
        return get_json_data(stocks)[:constant.DATA_LIMIT]


if __name__ == '__main__':
    cherrypy.quickstart(Index(), '/', conf)
