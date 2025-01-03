import requests
import json
import brotli
from prettytable import PrettyTable
from lxml import html
import traceback
import csv
from datetime import datetime

from seleniumbase import Driver
from time import sleep
import json

def ParsePage(driver:Driver, url,tokens):
    res = driver.get(url)
    


    tree = html.fromstring(driver.page_source)

    query = '//a[@class="ds-dex-table-row ds-dex-table-row-top"]'
    dex_rows = tree.xpath(query)
    for i in dex_rows:
        try:
            name = i.xpath('./div')[0]
            token_sumbol = name.xpath('.//span[@class="ds-dex-table-row-base-token-symbol" or @class="chakra-text ds-dex-table-row-base-token-symbol custom-1hn6cw4"]/text()')[0]
            second_token = name.xpath('.//span[@class="ds-dex-table-row-quote-token-symbol"]/text()')[0]
            tok_pair = token_sumbol+'/'+second_token
            tok_name = name.xpath('.//span[@class="ds-dex-table-row-base-token-name-text"]/text()')[0]

            name =  tok_pair + ' ' + tok_name
            price = i.xpath('./div[@class="ds-table-data-cell ds-dex-table-row-col-price" or @class="ds-table-data-cell ds-dex-table-row-col-price ds-dex-table-row-col-price-long"]')[0].text_content()
            age = i.xpath('./div[@class="ds-table-data-cell ds-dex-table-row-col-pair-age"]')[0].text_content()
            txns = i.xpath('./div[@class="ds-table-data-cell ds-dex-table-row-col-txns"]')[0].text_content()
            volume = i.xpath('./div[@class="ds-table-data-cell ds-dex-table-row-col-txns"]')[0].text_content()
            makers = i.xpath('./div[@class="ds-table-data-cell ds-dex-table-row-col-txns"]')[0].text_content()
            _5m = i.xpath('./div[@class="ds-table-data-cell ds-dex-table-row-col-price-change-m5"]')[0].text_content()
            _1h = i.xpath('./div[@class="ds-table-data-cell ds-dex-table-row-col-price-change-h1"]')[0].text_content()
            _6h = i.xpath('./div[@class="ds-table-data-cell ds-dex-table-row-col-price-change-h6"]')[0].text_content()
            _24h = i.xpath('./div[@class="ds-table-data-cell ds-dex-table-row-col-price-change-h24"]')[0].text_content()
            liquidity = i.xpath('./div[@class="ds-table-data-cell ds-dex-table-row-col-liquidity"]')[0].text_content()
            mcap = i.xpath('./div[@class="ds-table-data-cell ds-dex-table-row-col-market-cap"]')[0].text_content()

            tokens.append({
                'Name':name,
                'Price':price,
                'Age':age,
                'TXNS':txns,
                'Volume':volume,
                'Makers':makers,
                '5m':_5m,
                '1h':_1h,
                '6h':_6h,
                '24h':_24h,
                'Liquidity':liquidity,
                'MCAP':mcap
            })
        except:
            traceback.print_exc()


def SaveResultAsTable(tokens:list):
    tab = PrettyTable(['Name','Price','Age','TXNS','Volume','Makers','5m','1h','6h','24h','Liquidity','MCAP'])
    for token in tokens:
        tab.add_row(token.values())
    
    formatted_datetime = datetime.now().strftime("%H-%M-%d-%m-%Y")
    f = open(f'results_{formatted_datetime}.md','w',encoding='utf-8',newline='')   
    f.write(tab.get_string())

def SaveAsCSV(tokens:list):
    now = datetime.now()
    formatted_datetime = now.strftime("%H-%M-%d-%m-%Y")

    f = open(f'results_{formatted_datetime}.csv','w',encoding='utf-8',newline='')    
    headers = ['Name','Price','Age','TXNS','Volume','Makers','5m','1h','6h','24h','Liquidity','MCAP']
    writer = csv.DictWriter(f,delimiter=',',fieldnames=headers)
    writer.writeheader()

    for tok in tokens:
        writer.writerow(tok)
    
def main():
    driver = Driver(uc=True)
    url = 'https://dexscreener.com/'

    driver.uc_open_with_reconnect(url,4)
    driver.uc_gui_click_captcha()

    tokens = []
    

    ParsePage(driver,'https://dexscreener.com/',tokens)
    for i in range(2,21):
        print('curr url',f'https://dexscreener.com/page-{i}')
        ParsePage(driver,f'https://dexscreener.com/page-{i}',tokens)

    SaveAsCSV(tokens)
    SaveResultAsTable(tokens)

    driver.quit()

if __name__ == '__main__':
    main()
