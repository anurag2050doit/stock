import datetime
import logging

from scrapy import Request, FormRequest
from scrapy import Spider
from scrapy.crawler import CrawlerProcess

from utils import constant
from utils.helper_functions import get_hidden_inputs, get_headers
from utils.parse_data import extract_zip_file, parse_csv_file
from argparse import ArgumentParser


class BseIndia(Spider):
    start_urls = constant.start_urls
    name = 'bse_india'

    def parse(self, response):
        prev_days = args.days if isinstance(args.days, int) else int(args.days)
        date = datetime.datetime.now() - datetime.timedelta(days=prev_days)
        form_data = get_hidden_inputs(response)
        form_data.update({
            'ctl00$ContentPlaceHolder1$Debt': 'rbteqty',
            'ctl00$ContentPlaceHolder1$fdate1': '%s' % date.day,
            'ctl00$ContentPlaceHolder1$fmonth1': '%s' % date.month,
            'ctl00$ContentPlaceHolder1$fyear1': '%s' % date.year,
            'ctl00$ContentPlaceHolder1$btnSubmit': 'Submit',
            'ctl00$ContentPlaceHolder1$DDate': '%s-%s-%s' % (
                date.year, date.month, date.day)
        })
        headers = get_headers(response)

        yield FormRequest(
            response.url,
            formdata=form_data,
            callback=self.parse_data,
            headers=headers
        )

    def parse_data(self, response):
        file_path = response.xpath('//a[@id="ContentPlaceHolder1_btnHylSearBhav"]/@href').extract_first()
        if file_path:
            file_name = file_path.split('/')[-1]
            logging.info('Getting File %s' % file_path)
            yield Request(
                url=file_path,
                callback=self.parse_file,
                meta={'file_name': file_name}

            )
        logging.error('Unable to get file')
        error = response.xpath('//span[@id="ContentPlaceHolder1_lblCurZip"]/text()').extract_first()
        logging.error('Error message: %s' % error)

    def parse_file(self, response):
        file_name = response.meta['file_name']
        if file_name:
            with open('%s/%s' % (constant.ZIP_FILE_DIR, response.meta['file_name']), 'wb') as zip_file:
                zip_file.write(response.body)
            csv_files = extract_zip_file(file_name)
            parse_csv_file(csv_files)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--days", default=10,
                        help="Number of days back for getting data", metavar="FILE")
    args = parser.parse_args()
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(BseIndia)
    process.start()
