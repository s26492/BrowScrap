import os
import json
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from browarscrap.spiders.homebrewing import HomebrewingSpider


def run_spider():
    if os.path.exists('ScrapperData.json'):
        os.remove('ScrapperData.json')
    process = CrawlerProcess(get_project_settings())
    process.crawl(HomebrewingSpider)
    process.start()  # Czekamy aż spider zakończy scrapować


def analyze_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    df['price'] = df['price'].str.replace(' ', '').str.replace(',', '.')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    category_analysis = df.groupby('category').agg(
        product_count=pd.NamedAgg(column='name', aggfunc='count'),
        average_price=pd.NamedAgg(column='price', aggfunc='mean')
    ).reset_index()

    print(category_analysis)


if __name__ == '__main__':
    output_file = 'ScrapperData.json'
    run_spider()
    analyze_data(output_file)
