import requests
from parsel import Selector
from models import BusinessRow, Database

db_instant = Database()
business = 'amici-s-east-coast-pizzeria-at-cloudkitchens-soma-san-francisco'
url = "https://www.yelp.com/biz/{}".format(business)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'
}


def get_selector():
    response = requests.request("GET", url, headers=HEADERS)
    content = response.text
    selector = Selector(text=content)
    return selector


def get_business_title(selector: Selector):
    business_title = selector.xpath('//*[@class="css-11q1g5y"]/text()').get()
    return business_title


def get_business_site(selector: Selector):
    business_site = selector.xpath('//p[text()="Business website"]/..//a/text()').get()
    return business_site


def get_business_phone(selector: Selector):
    business_phone = selector.xpath('//p[text()="Phone number"]/../p[2]/text()').get()
    return business_phone


def get_business_work_hours(selector: Selector):
    day_list = selector.xpath('//*[@id="wrap"]//table/tbody/tr/th/p/text()').getall()
    hour_list = selector.xpath('//*[@id="wrap"]//table/tbody/tr/td/ul/li/p/text()').getall()
    working_hours_dict = dict(zip(day_list, hour_list))
    return str(working_hours_dict)


def get_business_address(selector: Selector):
    business_address = selector.xpath('//a[text()="Get Directions"]/../../p[2]/text()').get()
    return business_address


def get_business_data():
    selector = get_selector()
    business_data = dict()
    business_data['business_title'] = get_business_title(selector)
    business_data['business_site'] = get_business_site(selector)
    business_data['business_phone'] = get_business_phone(selector)
    business_data['business_work_hours'] = get_business_work_hours(selector)
    business_data['business_address'] = get_business_address(selector)
    return business_data


def transform_business_data(business_dict: dict):
    business_row = BusinessRow(
        title=business_dict['business_title'],
        site=business_dict['business_site'],
        phone=business_dict['business_phone'],
        work_hours=business_dict['business_work_hours'],
        address=business_dict['business_address'])
    db_instant.save_business_data(business_row)


def run():
    business_data = get_business_data()
    transform_business_data(business_data)


if __name__ == '__main__':
    run()
