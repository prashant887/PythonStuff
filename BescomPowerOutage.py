import findspark

findspark.init()
findspark.find()
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import re
from pyspark.sql import SparkSession
import csv
from pyspark.sql import functions as f
import http.client as http

http.HTTPConnection._http_vsn = 10
http.HTTPConnection._http_vsn_str = 'HTTP/1.0'

main_page = 'https://www.bescom.org/upo/public.php'

try:
    uMain = uReq(main_page)
except  http.IncompleteRead as e:
    uMain = e.partial

main_page_soup = soup(uMain.read(), "html.parser")
uMain.close()

MainConentTag = main_page_soup.find("div", {"id": "dynamiccontent"})

trList = []
tdList = []
thList = []

if MainConentTag is not None:
    MainTableContent = MainConentTag.find("table")
    if MainTableContent is not None:
        AllTrs = MainTableContent.findAll("tr")
        for AlTr in AllTrs:
            AllThs = AlTr.findAll("th")
            for AlTh in AllThs:
                # print(AlTh.text)
                thList.append(AlTh.text)
            AllTds = AlTr.findAll("td")
            tdList = []
            for AlTd in AllTds:
                # print(AlTd.text)
                tdList.append(str(AlTd.text).replace('\"', '').replace("\n", "").strip())
            trList.append(tdList)

with open('C:\\Users\\Owner\\Documents\\datasets\\BesCom.csv', 'w', newline='\n', encoding='utf-8') as myfile:
    wr = csv.writer(myfile, delimiter='|')
    wr.writerow(thList)
    for val in trList:
        wr.writerow(val)

spark = SparkSession.builder.appName("BescomOutage").config("spark.sql.shuffle.partitions", "50").config(
    "spark.driver.maxResultSize", "5g").config("spark.sql.execution.arrow.enabled", "true").getOrCreate()

spark.sparkContext.setLogLevel("OFF")

dataframe = spark.read.format("csv").option("header", "True").option("delimiter", "|").load(
    'C:\\Users\\Owner\\Documents\\datasets\\BesCom.csv')
dataframe.show(100, truncate=False)


spark.stop
'''
OutageDataFrame=spark.createDataFrame(trList)#.toDF(thList)

OutageDataFrame.show(truncate=False)
'''
