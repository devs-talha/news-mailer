import scrapy
from scrapy.http import Response, Request
from lxml import etree
from image import ImageItem
from utils import download_images, split_str, invert_date, get_gmt_date, parse_date, second_last_occurrence_index, sanitize_name, verify_todays_date
from storage import upload_images
from mail import send_mail
import os
from dotenv import load_dotenv

# call load_dotenv() here since the crawlerprocess creates a separate process for the crawler
load_dotenv()

class DawnScraper(scrapy.Spider):
    name = 'Dawn'
    base_url = os.getenv('DAWN_SCRAPER_BASE_URL')
    sections_to_retrieve = split_str(os.getenv('DAWN_SCRAPER_SECTIONS_TO_RETRIEVE'))
    date = invert_date(get_gmt_date(int(os.getenv('GMT', '5'))), join_delimiter='_')
    retrieved_images = []

    def start_requests(self):
        self.retrieved_images.clear()
        start_url = f'{self.base_url}/?page={self.date}_001'
        return [Request(url=start_url, callback=self.parse_home_page)]

    def parse_home_page(self, response: Response):
        html_tree = etree.HTML(response.body)
        date = html_tree.xpath('//*[@id="epaper-date"]/option[1]')[0].text
        date = parse_date(date)
        if not verify_todays_date(date):
            return
        left_navbar_items = html_tree.xpath('/html/body/div[2]/div/div/ul/li')
        for item in left_navbar_items:
            navbar_item = item.getchildren()[0]
            if navbar_item.text.lower() in self.sections_to_retrieve:
                yield Request(url=f'{self.base_url}{navbar_item.get("href")}', 
                              callback=self.parse_page_iframe, 
                              meta={'section': sanitize_name(navbar_item.text)})

    def parse_page_iframe(self, response: Response):
        html_tree = etree.HTML(response.body)
        return Request(url=html_tree.xpath('//*[@id="DawnPaperFrame"]')[0].get('src'), 
                       callback=self.parse_page,
                       meta={'section': response.meta['section']})

    def parse_page(self, response: Response):
        html_tree = etree.HTML(response.body)
        page_image_url = f'''{response.url[:response.url.rindex('/')]}/{html_tree.xpath('//*[@id="imgmap"]/img')[0].get('src')}'''
        full_image = ImageItem(name=f"{response.meta['section']}{page_image_url[page_image_url.rindex('_'):]}", 
                               section=response.meta['section'],
                               newspaper_name=self.name,
                               url=page_image_url,
                               date=self.date)
        self.retrieved_images.append(full_image)
        yield full_image
        sections = html_tree.xpath('//*[@id="planetmap"]/area')
        for section in sections:
            href = section.get('href')
            href = href[href.rindex('/'):href.rindex("'")]
            section_url = self.base_url + href
            yield Request(url=section_url, 
                          callback=self.parse_section,
                          meta={'section': response.meta['section']})
    
    def parse_section(self, response: Response):
        html_tree = etree.HTML(response.body)
        section_image_url = html_tree.cssselect('body > div.px-4.font-merriweather > div.flex.w-full > table > tbody > tr.flex.sm\:table-cell > td > img')[0].get('src')
        section_image = ImageItem(name=f"{response.meta['section']}{section_image_url[second_last_occurrence_index(section_image_url, '_'):]}",
                                  section=response.meta['section'],
                                  newspaper_name=self.name,
                                  url=section_image_url,
                                  date=self.date)
        self.retrieved_images.append(section_image)
        yield section_image

    def closed(self, reason):
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------',
              'Images retrieved: ', len(self.retrieved_images),
                                        '----------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        download_images(self.retrieved_images)
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------',
              'Images downloaded: ', len(self.retrieved_images),
                                        '----------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        
        upload_images(self.retrieved_images)
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------',
              'Images uploaded: ', len(self.retrieved_images),
                                        '----------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        
        send_mail(self.retrieved_images)
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------------------',
              'Images sent in mail: ', len(self.retrieved_images),
                                        '----------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        
        