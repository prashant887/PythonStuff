import urllib

import findspark

findspark.init()
findspark.find()

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from urllib.request import Request
from urllib import parse as parse
import re
import http.client as http
import json
import csv
import findspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.functions import lit

# print('\n', '========Scrapping Started=============', '\n')
http.HTTPConnection._http_vsn = 10
http.HTTPConnection._http_vsn_str = 'HTTP/1.0'

main_page = 'https://www.worldometers.info/coronavirus/'

try:
    req = Request(main_page, headers={'User-Agent': 'Mozilla/5.0'})
    # print(uReq(req).code)
    uMain = uReq(req)
except  http.IncompleteRead as e:
    uMain = e.partial

main_page_soup = soup(uMain.read(), "html.parser")
uMain.close()

corona_details_map = {}
left_right_map = {}
mid_panel_map = {}
cases_map = {}
table_headers_list = []
table_containts_all_list = []
table_containts_lst = []
MainContainers = main_page_soup.findAll("div", {"class": "container"})
for MainContainer in MainContainers:
    GetAllDivs = MainContainer.findAll("div", {"class": "row"})
    for GetAllDiv in GetAllDivs:
        MainClassContainer = GetAllDiv.find("div", {"class": "col-md-8"})
        if MainClassContainer is not None:
            NextMainClass = MainClassContainer.find("div", {"class": "content-inner"})
            if NextMainClass is not None:
                HeaderTag = NextMainClass.find("div", {"class": "label-counter"})
                if HeaderTag is not None:
                    corona_details_map['Topic'] = HeaderTag.text
                UpdatedTag = NextMainClass.find("div", {"style": "font-size:13px; color:#999; text-align:center"})
                if UpdatedTag is not None:
                    k, v = str(UpdatedTag.text).split(': ')
                    corona_details_map[k] = v
                MainCountWraps = NextMainClass.findAll("div", {"id": "maincounter-wrap"})
                for MainCountWrap in MainCountWraps:
                    MainH1Tag = MainCountWrap.find("h1")
                    if MainH1Tag is not None:
                        MainH1TagText = str(MainH1Tag.text)
                    MainCountNumTag = MainCountWrap.find("div", {"class": "maincounter-number"})
                    if MainCountNumTag is not None:
                        MainCountNumTagSpan = MainCountNumTag.find("span")
                        if MainCountNumTagSpan is not None:
                            MainCountText = MainCountNumTagSpan.text
                            corona_details_map[MainH1TagText] = re.sub("[^\\d+]", "", MainCountText)
                cases_details_map = {}
                MainPanelTags = NextMainClass.findAll("div", {"class": "col-md-6"})
                for MainPanelTag in MainPanelTags:
                    PanelDefaultTag = MainPanelTag.find("div", {"class": "panel panel-default"})
                    if PanelDefaultTag is not None:
                        PanelHeadingTag = PanelDefaultTag.find("div", {"class": "panel-heading"})
                        if PanelHeadingTag is not None:
                            PanelTitleTag = PanelHeadingTag.find("span", {"class": "panel-title"})
                            if PanelTitleTag is not None:
                                PanelTitleTagText = str(PanelTitleTag.text).replace('\n', '')
                                mid_panel_map[PanelTitleTagText] = {}
                        PanelBodyTag = PanelDefaultTag.find("div", {"class": "panel-body"})
                        if PanelBodyTag is not None:
                            PanelFlipTag = PanelBodyTag.find("div", {"class": "panel_flip"})
                            if PanelFlipTag is not None:
                                PanelFrontTag = PanelFlipTag.find("div", {"class": "panel_front"})
                                if PanelFrontTag is not None:
                                    NumTblMainTag = PanelFrontTag.find("div", {"class": "number-table-main"})
                                    if NumTblMainTag is not None:
                                        NumTblMainText = re.sub("[^\\d+]", "", NumTblMainTag.text)
                                    DivStyleHeaderTag = PanelFrontTag.find("div", {"style": "font-size:13.5px"})
                                    if DivStyleHeaderTag is not None:
                                        cases_map = {}
                                        DivStyleHeaderText = str(DivStyleHeaderTag.text)  ##Replace was removed
                                    cases_map[DivStyleHeaderText] = {"CaseCount": NumTblMainText}
                                    CasesMainCondtionTag = PanelFrontTag.find("div", {
                                        "style": "padding-top:20px;position:relative;text-align:center; "})
                                    if CasesMainCondtionTag is None:
                                        CasesMainCondtionTag = PanelFrontTag.find("div", {"style": "padding-top:20px "})
                                    if CasesMainCondtionTag is not None:
                                        left_right_map = {}
                                        RightCondtionTag = CasesMainCondtionTag.find("div", {
                                            "style": "float:right; text-align:center"})
                                        if RightCondtionTag is not None:
                                            TextRightTableTag = RightCondtionTag.find("div",
                                                                                      {"style": "font-size:13px"})
                                            if TextRightTableTag is not None:
                                                TextRightTableVal = TextRightTableTag.text
                                                left_right_map[TextRightTableVal] = {}

                                            NumberRightTableTag = RightCondtionTag.find("span",
                                                                                        {"class": "number-table"})
                                            if NumberRightTableTag is not None:
                                                NumberRightTableText = re.sub("[^\\d+]", "", NumberRightTableTag.text)
                                                left_right_map[TextRightTableVal]['Count'] = NumberRightTableText

                                            NumberRightPercentageTag = RightCondtionTag.find("strong")
                                            if NumberRightPercentageTag is not None:
                                                NumberRightPercentageText = NumberRightPercentageTag.text
                                                left_right_map[TextRightTableVal][
                                                    'Percentage'] = NumberRightPercentageText
                                        LeftCondtionTag = CasesMainCondtionTag.find("div", {
                                            "style": "float:left; text-align:center"})
                                        if LeftCondtionTag is not None:
                                            TextLeftTableTag = LeftCondtionTag.find("div",
                                                                                    {"style": "font-size:13px"})
                                            if TextLeftTableTag is not None:
                                                TextLeftTableVal = TextLeftTableTag.text
                                                left_right_map[TextLeftTableVal] = {}

                                            NumberLeftTableTag = LeftCondtionTag.find("span",
                                                                                      {"class": "number-table"})
                                            if NumberLeftTableTag is not None:
                                                NumberLeftTableText = re.sub("[^\\d+]", "", NumberLeftTableTag.text)
                                                left_right_map[TextLeftTableVal]['Count'] = NumberLeftTableText

                                            NumberLeftPercentageTag = LeftCondtionTag.find("strong")
                                            if NumberRightPercentageTag is not None:
                                                NumberLeftPercentageText = NumberLeftPercentageTag.text
                                                left_right_map[TextLeftTableVal][
                                                    'Percentage'] = NumberLeftPercentageText
                                            cases_map[DivStyleHeaderText]['Details'] = left_right_map
                                            mid_panel_map[PanelTitleTagText] = cases_map

            TableContaintsMainTag = MainClassContainer.find("div", {"class": "tab-content"})
            if TableContaintsMainTag is not None:
                TableContaintsMainIdTag = TableContaintsMainTag.find("div", {"class": "tab-pane active"})
                if TableContaintsMainIdTag is not None:
                    TableCountriesMainTagId = TableContaintsMainIdTag.find("div", {"class": "main_table_countries_div"})
                    if TableCountriesMainTagId is not None:
                        TableCountriesMainTabId = TableCountriesMainTagId.find("table",
                                                                               {"id": "main_table_countries_today"})
                        if TableCountriesMainTabId is not None:
                            TableColHeadersTh = TableCountriesMainTabId.find("thead")
                            if TableColHeadersTh is not None:
                                TableColHeadersAllTr = TableColHeadersTh.find("tr")
                                if TableColHeadersAllTr is not None:
                                    TableColHeadersAllThs = TableColHeadersAllTr.findAll("th")
                                    for TableColHeadersAllTh in TableColHeadersAllThs:
                                        table_headers_list.append(
                                            str(TableColHeadersAllTh.text).replace(",", "").replace("\xa0", ""))
                                    table_headers_list.append('Updated')
                                    # table_containts_all_list.append(table_headers_list)
                            TableContaintsAllBodys = TableCountriesMainTabId.findAll("tbody")
                            for TableContaintsAllBody in TableContaintsAllBodys:
                                TableWordTag = TableContaintsAllBody.find("tr", {"class": "total_row odd"})
                                if TableWordTag is not None:
                                    TableWordTagTds = TableWordTag.findAll("td")
                                    for TableWordTagTd in TableWordTagTds:
                                        pass
                                TableContainsAllTrs = TableContaintsAllBody.findAll("tr")

                                for TableContainsAllTr in TableContainsAllTrs:
                                    table_containts_lst = []
                                    TableContainsAllTds = TableContainsAllTr.findAll("td")

                                    for TableContainsAllTd in TableContainsAllTds:
                                        table_containts_lst.append(
                                            str(TableContainsAllTd.text).replace("\n", "").strip())
                                    table_containts_lst.append(corona_details_map['Last updated'])

                                    table_containts_all_list.append(table_containts_lst)

with open('C:\\Users\\Owner\\Documents\\datasets\\CoronaCases.csv', 'w', newline='\n', encoding='utf-8') as myfile:
    wr = csv.writer(myfile, delimiter='|', quoting=csv.QUOTE_NONE)
    wr.writerow(table_headers_list)
    for val in table_containts_all_list:
        wr.writerow(val)

corona_details_map['CaseDetails'] = mid_panel_map

for k, v in corona_details_map.items():
    if k == 'CaseDetails':
        for i, j in v.items():
            print(i, '===', j)
    else:
        print(k, '===', v)

# print('\n', '========Scrapping Ended=============', '\n')


spark = SparkSession.builder.appName("CornaCase").config("spark.sql.shuffle.partitions", "50").config(
    "spark.driver.maxResultSize", "5g").config("spark.sql.execution.arrow.enabled", "true").getOrCreate()

spark.sparkContext.setLogLevel("OFF")
'''
CoronaDataFrame = spark.read.format("csv").option("header", "true").option("delimiter","|").load(
    'C:\\Users\\Owner\\Documents\\datasets\\CoronaCases.csv')
CoronaDataFrame.withColumn('Updated',lit(corona_details_map['Last updated'])).show(10000, truncate=False)
#CoronaDataFrame.show(10000, truncate=False)
'''
CoronaDataFrame = spark.createDataFrame(table_containts_all_list, table_headers_list)
CoronaDataFrame.withColumn('Updated', lit(corona_details_map['Last updated'])).show(10000, truncate=False)
spark.stop
