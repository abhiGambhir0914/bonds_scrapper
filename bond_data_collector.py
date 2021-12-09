from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import csv
import json
import codecs
import time
import datetime


url = "http://bondinfo.bnm.gov.my/portal/server.pt/gateway/PTARGS_0_22874_2750_313_0_43/http%3B/hqblkhub.w2k.bnm.gov.my%3B7070/BondInfoHub/InvestorTools/BondSearch/bondSearch.html?sp=S8&sp=S{ISIN_CODE}"

def selenium_parse(driver, ISIN_CODE, i):
    #     print(f'get:{url}')
    print(ISIN_CODE)
    csv_df = pd.DataFrame()

    driver.get(url.format(ISIN_CODE=ISIN_CODE))

#     bs_obj = BSoup(driver.page_source, 'lxml')

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'frmResult')))
        print ("Page is ready!")
    except TimeoutException as e:
        print('Already in frame!!')
        print(e)


    ISINCodeColumnValue = driver.find_element_by_xpath("//td[@class='ISINCodeColumnValue']").text
    stockCodeColumnValue = driver.find_element_by_xpath("//td[@class='stockCodeColumnValue']").text
    stockDescColumnValue = driver.find_element_by_xpath("//td[@class='stockDescColumnValue']").text
    issuerColumnValue = driver.find_element_by_xpath("//td[@class='issuerColumnValue']").text
    instrumentColumnValue = driver.find_element_by_xpath("//td[@class='instrumentColumnValue']").text
    issueDateColumnValue = driver.find_element_by_xpath("//td[@class='issueDateColumnValue']").text
    repo_maturityDateColumnValue = driver.find_element_by_xpath("//td[@class='repo_maturityDateColumnValue']").text
    ratingMARCColumnValue = driver.find_element_by_xpath("//td[@class='ratingMARCColumnValue']").text
    ratingRAMColumnValue = driver.find_element_by_xpath("//td[@class='ratingRAMColumnValue']").text
    bond_amountColumnValue = driver.find_element_by_xpath("//td[@class='bond_amountColumnValue']").text

    values = [
        [ISINCodeColumnValue, bond_amountColumnValue, stockCodeColumnValue, stockDescColumnValue, issuerColumnValue,
         instrumentColumnValue, issueDateColumnValue, repo_maturityDateColumnValue, ratingMARCColumnValue,
         ratingRAMColumnValue]]
    csv_df = csv_df.append(values)
    print(csv_df)

    if i == 1:
        csv_df.columns = [
            'ISIN Code',
            'Outstanding Amount',
            'Stock Code',
            'Stock Description',
            'Issuer',
            'Instrument',
            'Issue Date',
            'Maturity Date',
            'Rating MARC',
            'Rating RAM'
        ]
        csv_df.to_csv('bonds_data' + datetime.datetime.now().strftime("%Y-%m-%d.csv"), sep=',', encoding='utf-8', doublequote=False, index=False, mode="a",
                      quoting=csv.QUOTE_NONE, escapechar='\\')
    else:
        csv_df.to_csv('bonds_data' + datetime.datetime.now().strftime("%Y-%m-%d.csv"), sep=',', encoding='utf-8', doublequote=False, index=False, mode="a", header=False,
                      quoting=csv.QUOTE_NONE, escapechar='\\')

options = Options()
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver.maximize_window()
driver.implicitly_wait(30)

ISIN_CODES = []
i = 1
count = 0

data = json.load(codecs.open('codebeautify.json', 'r', 'utf-8-sig'))

for val in data["data"]:
    ISIN_CODES.append(val['isinCode'])

print(len(ISIN_CODES))


start_time = time.time()
for code in ISIN_CODES[0:700]:
    # print(i)
    if i == 1:
        selenium_parse(driver, code, i)
        i=0
        count += 1
    else:
        if float(count % 500) == 0:
            print()
            print('*'*50)
            print('Reached 500 limit, taking small break now !!! Will resume in 23 seconds.')
            time.sleep(23)
            print('*' * 50)
            print()
        selenium_parse(driver, code, i)
        count += 1

driver.quit()
print()
print()
print('*'*60)
print('Completed Successfully !!!')
print("--- %s seconds ---" % (time.time() - start_time))

