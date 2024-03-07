import scrapy
import os
import csv
import sys
from src.logger import logging
from src.exception import CustomException

base_url = "https://www.magicbricks.com/mbsrp/propertySearch.html?editSearch=Y&category=S&propertyType=10002,10003,10021,10022,10001,10017&city=2624&page={}&groupstart={}&offset=0&maxOffset=399&sortBy=premiumRecent&postedSince=-1&pType=10002,10003,10021,10022,10001,10017&isNRI=N&multiLang=en"

try:
    class DatacollectorSpider(scrapy.Spider):
        name = "dataCollector"
        allowed_domains = ["www.magicbricks.com"]
        cities = {
        'Hyderabad':2060,
        'New Delhi':2624,
        'Bangalore':3327,
        'Kolkata':6903,
        'Chennai':5196
        }
        max_pages  = 1000
        
        def start_requests(self) :
            logging.info("Scraping Started")
            for city,code in self.cities.items():
                for page in range(1,self.max_pages+1):
                    groupstart = (page-1)*30
                    url = f'https://www.magicbricks.com/mbsrp/propertySearch.html?editSearch=Y&category=S&propertyType=10002,10003,10021,10022,10001,10017&city={code}&page={page}&groupstart={groupstart}&offset=0&maxOffset=399&sortBy=premiumRecent&postedSince=-1&pType=10002,10003,10021,10022,10001,10017&isNRI=N&multiLang=en'
                    yield scrapy.Request(url,callback=self.parse,meta={'city':city})
                    
            logging.info("Scraping Finised")

        def parse(self, response):
            
            data = response.json()
            city = response.meta['city']
            resultlist = data.get('resultList',[])
            for item in resultlist:
                price = item.get('price')
                coordinates = item.get('ltcoordGeo')
                luxury = item.get('isLuxury')
                projctprop = item.get('isProjProp')
                power_status = item.get('powerStatusD')
                furnished = item.get('furnishedD')
                bath = item.get('bathD')
                bedroom = item.get('bedroomD')
                property_type = item.get('propTypeD')
                water_status = item.get('waterStatus')
                os = item.get('operatingSinceYear')
                prefered_tenants = item.get('tenantsPreference')
                luxury_service = item.get('isLuxuryServiceAvailable')
                locality_name = item.get('lmtDName')
                sqft_price = item.get('sqFtPrice')
                parking = item.get('parkingD')
                yield{
                    'City':city,
                    'Locality_name':locality_name,
                    'Coordinates':coordinates,
                    'Luxury':luxury,
                    'Project_Property':projctprop,
                    'Power_Status':power_status,
                    'Furnished':furnished,
                    'Bathrooms':bath,
                    'Bedrooms':bedroom,
                    'Property_type':property_type,
                    'Water_Status':water_status,
                    'Operating_Since': os,
                    'Tenants_prefered':prefered_tenants,
                    'Luxury_service':luxury_service,
                    'Parking':parking,
                    'Sqft_price':sqft_price,
                    'Price': price
                }
                
                '''data_row = [
                    city, locality_name, coordinates, luxury, projctprop, power_status, furnished,
                    bath, bedroom, property_type, water_status, os, prefered_tenants, luxury_service,
                    parking, sqft_price, price
                ]
                self.save_to_csv(data_row)'''
                
            logging.info("Data saved successfully to raw_data.csv")
                
        '''def save_to_csv(self, data_row):
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            CSV_FILE = os.path.join(BASE_DIR, '..', '..','..','..', 'data', 'raw_data.csv')

            # Check if the data directory exists, if not, create it
            if not os.path.exists(os.path.dirname(CSV_FILE)):
                os.makedirs(os.path.dirname(CSV_FILE))

            # Write data to CSV file
            with open(CSV_FILE, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data_row)'''
            
    
except Exception as e:
    logging.info("Error Occured While Extracting the data from Website")
    raise CustomException(e,sys)
