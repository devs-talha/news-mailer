from scrapy.crawler import CrawlerProcess
from dawnscraper import DawnScraper
from dotenv import load_dotenv

load_dotenv()

process = CrawlerProcess()
process.crawl(DawnScraper)
process.start()
