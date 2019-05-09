## Installation

- Create virtualenv `virtual env -p python3` 
- Activate virtualenv `source env/bin/activate`
- Install dependencies `pip -r install requirements.txt`
- Install redis server `sudo apt-get install redis-server`
- Start redis server `redis-server`

*Note:-* If faced problem in installing `scrapy` refer [here](http://doc.scrapy.org/en/latest/intro/install.html)

## Load Data

- Navigate to `cd spider`
- To get data and save to redis run `python get_data.py`
	> script arguments: `--days`
	* days: Which implies number of days back from present days
	> Note:- As website doesnt't provide data for previous few days so passing `--days` args to get data of a specify day.
	Suppose today is: 09/May/19 we want data for 04/May/19 we can pass `--days=5` as script args
- Script will fetch data from website, extract zip and get cvs file. Zip and csv will be stored to there respective directories
- CSV will parsed and stored in redis DB

## Running Server

- To run server `python manage.py`
- Sever will start and navigate to `http://127.0.0.1:8080`  

## Git

Project covers both server side rendering as well as client side rendering (front-end rending) using ajax
#### Server Side-Rendering

- For **server side** rending using `jinja2` templating language.*Branch:* `git checkout master`
- For **client side** rending using `jQuery Datatable`.*Branch:* `git checkout api`.