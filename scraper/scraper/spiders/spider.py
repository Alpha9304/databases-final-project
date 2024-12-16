import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from ..items import ShootingPlace
import os
import time

script_directory = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(script_directory, 'zip_code.csv')
zip_zip = []
with open(zip_path, newline='') as csvfile:
    zipcodes_reader = csv.reader(csvfile)
    for row in zipcodes_reader:
        zip_zip.append(row[0])  


class SpidySpider(scrapy.Spider):
    name = 'spidy'
    start_urls = ['https://www.wheretoshoot.org/']
    zip_codes = zip_zip

    def __init__(self):
        self.driver = webdriver.Chrome()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        driver = self.driver
        driver.get(self.start_urls[0])

        for zip_code in self.zip_codes:
            try:
            
                search_bar = WebDriverWait(driver, 0.5).until(
                    EC.presence_of_element_located((By.ID, 'search'))
                )
                search_button = WebDriverWait(driver, 0.5).until(
                    EC.presence_of_element_located((By.ID, 'search-btn'))
                )

                search_bar.clear()
                search_bar.send_keys(zip_code)

                first_suggestion = WebDriverWait(driver, 0.5).until(
                    EC.visibility_of_element_located((By.XPATH, '(//div[@class="pac-item"])[1]'))
                )
                first_suggestion.click()
                search_button.click()

                WebDriverWait(driver, 0.5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.location-item'))
                )

                html = driver.page_source
                sel_response = HtmlResponse(url=driver.current_url, body=html, encoding='utf-8')
                locations = sel_response.css('#mCSB_1_container .location-item')

                for loc in locations:
                    item = ShootingPlace()
                    item["debug_zip"] = zip_code
                    item["id"] = loc.xpath('.//span[@class="id"]/text()').get()
                    item["name"] = loc.css(".name::text").get()
                    item["street_address"] = loc.css('.address::text').get()

                    big_address = loc.css('.address1::text').get()
                    if big_address:
                        address_parts = big_address.split(",")
                        item["city"] = address_parts[0].strip()
                        item["state"] = address_parts[1].strip()
                        item["zipcode"] = address_parts[2].strip()
                    else:
                        item["city"] = item["state"] = item["zipcode"] = None

                    item["phone_number"] = loc.css('.phone::text').get()
                    item["email"] = loc.css('.phoemail::text').get()
                    nssf_member = loc.css('.is-member::attr(style)').get()
                    item["nssf_member"] = "No" if nssf_member else "Yes"

                    item["facility_detail"] = ', '.join(loc.css('.facility-details-list li:not([class="hidden"])::text').extract()).strip()
                    item["service"] = ', '.join(loc.css('.services-list li:not([class="hidden"])::text').extract()).strip()
                    item["shooting_avaliable"] = ', '.join(loc.css('.shooting-av-list li:not([class="hidden"])::text').extract()).strip()
                    item["distance"] = ', '.join(loc.css('.distance-list li:not([class="hidden"])::text').extract()).strip()
                    item["competition"] = ', '.join(loc.css('.competitions-available-list li:not([class="hidden"])::text').extract()).strip()
                    item["website"] = loc.css('.btn-website::attr(href)').get()

                    yield item
                #change this
                time.sleep(0.5)

            except Exception as e:
                self.logger.error(f"Error occurred while processing zip code {zip_code}: {e}")
                continue


    def closed(self, reason):
        self.driver.quit()
