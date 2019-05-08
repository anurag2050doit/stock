import os
from jinja2 import Environment, FileSystemLoader
from spider.utils import constant
import redis

# Jinja template config
TEMPLATE_DIR = 'templates'
CUR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), TEMPLATE_DIR)
env = Environment(loader=FileSystemLoader(CUR_DIR), trim_blocks=True)


# Static Files config
conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './static'
    }
}

# Redis config
db = redis.StrictRedis(host=constant.REDIS_HOST, port=constant.REDIS_PORT, db=constant.REDIS_DB)