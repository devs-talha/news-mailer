from scrapy import Item, Field

class ImageItem(Item):
    name = Field()
    newspaper_name = Field()
    section = Field()
    date = Field()
    url = Field()
    data = Field()
