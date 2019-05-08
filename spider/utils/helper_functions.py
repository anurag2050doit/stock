import json


def get_hidden_inputs(response):
    """ Get hidden inputs. """
    formdata = {}
    for hid in response.xpath('//input[@type="hidden" and @name and @value]'):
        formdata[hid.xpath('@name').extract()[0]] = hid.xpath('@value').extract()[0]

    return formdata


def get_headers(response):
    """
    Return page headers
    :param response: page response
    :return:
    """
    return {
        'content-type': 'application/x-www-form-urlencoded',
        'upgrade-insecure-requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'origin': 'https://www.bseindia.com',
        'referer': response.url
    }


def get_json_data(data):
    try:
        return json.loads(data.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return []
