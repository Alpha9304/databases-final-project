# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShootingPlace(scrapy.Item):
    debug_zip = scrapy.Field(default=None) 
    id = scrapy.Field(default=None) 
    name  = scrapy.Field(default=None) 
    street_address= scrapy.Field(default=None) 
    #big_address = scrapy.Field(default= "N/A") spli tit
    city = scrapy.Field(default="N/A") 
    state = scrapy.Field(default="N/A") 
    zipcode = scrapy.Field(default="N/A") 
    email= scrapy.Field(default="N/A") 
    phone_number= scrapy.Field(default="N/A") 
    nssf_member= scrapy.Field(default="N/A") 
    facility_detail= scrapy.Field(default="N/A") 
    service= scrapy.Field(default="N/A") 
    shooting_avaliable= scrapy.Field(default="N/A") 
    distance= scrapy.Field(default="N/A") 
    competition= scrapy.Field(default="N/A") 
    website= scrapy.Field(default=None)

