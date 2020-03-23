import requests
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import lxml
import re

base_url = "https://www.flipkart.com"

cromecastlink = 'https://www.flipkart.com/search?q=google%20cromecast&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'

uClient = uReq(cromecastlink)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

items_lst = []
item_dict = {}
device_details = {}
containers = page_soup.findAll("div", {"class": "_3O0U0u"})
for container in containers:
    conitems = container.findAll("div", {"class": "_3liAhj"})

    for conitem in conitems:

        bestsellerMainTag = conitem.find("a", {"class": "Zhf2z-"})
        title_tag = conitem.find("a", {"class": "_2cLu-l"})

        bestsellerMainTag = conitem.find("a", {"class": "Zhf2z-"})
        # print('BestTag',bestsellerMainTag['href'])
        if 'BestsellerId' in bestsellerMainTag['href']:
            bestSeller = 'Yes'
        else:
            bestSeller = 'No'

        color = conitem.find("div", {"class": "_1rcHFq"})
        rating = conitem.find("div", {"class": "niH0FQ _36Fcw_"}).find("span", {"class": "_38sUEc"}).text
        price = conitem.find("a", {"class": "_1Vfi6u"}).find("div", {"class": "_1uv9Cb"}).find("div", {
            "class": "_1vC4OE"}).text

        item_dict[title_tag.text] = {"name": title_tag["title"], "BestSeller": bestSeller,
                                     "url": base_url + title_tag["href"]
            , "color": color.text, "ratings": re.sub("[^\d\\s+]", "", rating),
                                     "price": re.sub("[^\d\\s+]", "", price)
                                     }

        uClientItems = uReq(base_url + title_tag["href"])

        # parses html into a soup data structure to traverse html
        # as if it were a json data type.
        pageSoupItems = soup(uClientItems.read(), "html.parser")
        uClientItems.close()
        ItemDiv = pageSoupItems.find("div", {"class": "t-0M7P _3GgMx1 _2doH3V"}).find("div", {"class": "_3e7xtJ"}).find(
            "div", {"class": "_1HmYoV hCUpcT"})
        ItemImageDivBest = ItemDiv.find("div", {"class": "_1HmYoV _35HD7C col-5-12 _3KsTU0"}).find("div", {
            "class": "_2qOAoY _1P8T3k"})
        if ItemImageDivBest is not None:
            # print(ItemImageDivBest.text)
            IsBestSeller = 'Y'
        else:
            IsBestSeller = 'N'

        ItemDetailsDiv = ItemDiv.find("div", {"class": "_1HmYoV _35HD7C col-8-12"})
        ItemTextDetails = ItemDetailsDiv.findAll("div", {"class": "bhgxx2 col-12-12"})
        for divs in ItemTextDetails:
            deviceNameDiv = divs.find("div", {"class": "_29OxBi"})
            if deviceNameDiv is not None:
                deviceName = deviceNameDiv.find("div").find("h1", {"class": "_9E25nV"}).find("span",
                                                                                             {"class": "_35KyD6"})

                devicePrice = deviceNameDiv.find("div", {"class": "_3iZgFn"}).find("div", {"class": "_2i1QSc"}).find(
                    "div", {"class": "_1uv9Cb"}).find("div", {"class": "_1vC4OE _3qQ9m1"})
                # print('=====', deviceName.text, ':', devicePrice.text, '=============')
                device_details[title_tag.text] = {"name": re.sub(r'[^A-Za-z0-9 ]+', ' ', str(deviceName.text)),
                                                  "price": re.sub("[^\d\\s+]", "", str(devicePrice.text)),
                                                  "BestSeller": IsBestSeller
                                                  }

                specialPriceTag = deviceNameDiv.find("div", {"class": "_2XDAh9"})
                if specialPriceTag is not None:
                    specialPriceSpan = specialPriceTag.find("span")
                    if specialPriceSpan is not None:
                        device_details[title_tag.text]['SpecialPrice'] = specialPriceSpan.text

            SoldOutTag = divs.find("div", {"class": "_9-sL7L"})

            if SoldOutTag is not None:
                device_details[title_tag.text]['StockSts'] = SoldOutTag.text
            else:
                if device_details.get(title_tag.text, {}).get('StockSts') is None:
                    device_details[title_tag.text]['StockSts'] = 'Avilable'

            StockAvilComments = divs.find("div", {"class": "_1mzTZn"})
            if StockAvilComments is not None:
                device_details[title_tag.text]['StockAvilComment'] = StockAvilComments.text
            else:

                device_details[title_tag.text]['StockAvilComment'] = device_details.get(title_tag.text, {}).get(
                    'StockAvilComment', 'Item is currently avilable')
            deviceRatingAndReviewsDivs = divs.find("div")
            if deviceRatingAndReviewsDivs is not None:
                deviceRatingAndReviewsInnerDiv = deviceRatingAndReviewsDivs.find("div", {"class": "_3ors59"})
                if deviceRatingAndReviewsInnerDiv is not None:
                    deviceRatingAndReviewsFinal = deviceRatingAndReviewsInnerDiv.find("div",
                                                                                      {"class": "niH0FQ _2nc08B"})
                    if deviceRatingAndReviewsFinal is not None:
                        RatingFinal = deviceRatingAndReviewsFinal.find("div", {"class": "hGSR34"})
                        if RatingFinal is not None:
                            Rating = RatingFinal.text
                            # print(Rating)
                            device_details[title_tag.text]["stars"] = Rating
                        ReviewSpan = deviceRatingAndReviewsFinal.find("span", {"class": "_38sUEc"})
                        if ReviewSpan is not None:
                            InnerReviewSpan = ReviewSpan.find("span")
                            if InnerReviewSpan is not None:
                                ReviewRatingText = ''
                                FinalReviewSpans = InnerReviewSpan.findAll("span")
                                if FinalReviewSpans is not None:
                                    for FinalReviewSpan in FinalReviewSpans:
                                        ReviewRatingText = ReviewRatingText + FinalReviewSpan.text
                                        if 'Ratings' in FinalReviewSpan.text:
                                            device_details[title_tag.text]["Ratings"] = re.sub("[^\d]", "",
                                                                                               str(
                                                                                                   FinalReviewSpan.text))
                                        if 'Reviews' in FinalReviewSpan.text:
                                            device_details[title_tag.text]["Reviews"] = re.sub("[^\d]", "",
                                                                                               str(
                                                                                                   FinalReviewSpan.text))
                                    # print(ReviewRatingText)
            offer_lst = []
            avilableOffersNameTag = divs.find("div", {"class": "_1wg1IU"})
            if avilableOffersNameTag is not None:
                avilableOffersName = avilableOffersNameTag.find("div", {"class": "edKlv2"})
                if avilableOffersName is not None:
                    device_details[title_tag.text]['OfferStatus'] = avilableOffersName.text
            lisOfOffersTag = divs.find("div", {"class": "_3nSGUy"})
            if lisOfOffersTag is not None:
                lisOfInnerOffersTag = lisOfOffersTag.find("div", {"class": "_2RzXYa"})
                if lisOfInnerOffersTag is not None:
                    lisOfInnerOffersTagSubTag = lisOfInnerOffersTag.find("div", {"class": "_3D89xM"})
                    if lisOfInnerOffersTagSubTag is not None:
                        lisOfInnerOffersTagSubSpans = lisOfInnerOffersTagSubTag.findAll("span", "_7g_MLT row")
                        for spanList in lisOfInnerOffersTagSubSpans:
                            li = spanList.find("li", {"class": "_2-n-Lg col"})
                            if li is not None:
                                SpanAll = li.findAll("span")
                                spanTxt = ''

                                for span in SpanAll:
                                    spanTxt = spanTxt + ' ' + span.text
                                # print('spanTxt:',spanTxt)
                                offer_lst.append(spanTxt)
                            device_details[title_tag.text]['Offers'] = offer_lst

        highLiteLst = []
        serviceLst = []
        HighLighteTopTags = ItemDetailsDiv.findAll("div", {"class": "_1HmYoV hCUpcT"})
        for HighLighteTopTag in HighLighteTopTags:
            HighLighteTopTagNextTags = HighLighteTopTag.findAll("div", {"class": "bhgxx2 col-6-12"})

            for HighLighteTopTagNextTag in HighLighteTopTagNextTags:
                HighLiteTextTopTag = HighLighteTopTagNextTag.find("div", {"class": "g2dDAR"})
                if HighLiteTextTopTag is not None:
                    HighLiteText = HighLiteTextTopTag.find("div", {"class": "_2hqjdd"})
                    if HighLiteText is not None:
                        HighLiteTextVal = HighLiteText.text
                    HighLiteTextLineTag = HighLiteTextTopTag.find("div", {"class": "_3WHvuP"})
                    if HighLiteTextLineTag is not None:
                        HighLiteTextLinesUl = HighLiteTextLineTag.find("ul")
                        if HighLiteTextLinesUl is not None:
                            HighLiteTextLines = HighLiteTextLinesUl.findAll("li", {"class": "_2-riNZ"})
                            for HighLiteTextLine in HighLiteTextLines:
                                highLiteLst.append(HighLiteTextLine.text)
                    device_details[title_tag.text][HighLiteTextVal] = highLiteLst
                ServicesTextTopTag = HighLighteTopTagNextTag.find("div", {"class": "_3aj0Jp flex"})
                if ServicesTextTopTag is not None:
                    ServiceTexTag = ServicesTextTopTag.find("div", {"class": "_3KRH50"})
                    if ServiceTexTag is not None:
                        ServiceText = ServiceTexTag.text
                    ServiceTagLinesUl = ServicesTextTopTag.find("ul", {"class": "_77jr7B"})
                    if ServiceTagLinesUl is not None:
                        ServiceTagLines = ServiceTagLinesUl.findAll("li", {"class": "_3tB8QY"})
                        for ServiceTagLine in ServiceTagLines:
                            ServiceTag = ServiceTagLine.find("div", {"class": "_20PGcF"})
                            if ServiceTag is not None:
                                serviceLst.append(re.sub(r'[^A-Za-z0-9 ]+', '', ServiceTag.text))
                    device_details[title_tag.text][ServiceText] = serviceLst

        SpecsAndDescTopTags = ItemDetailsDiv.findAll("div", {"class": "_1HmYoV _35HD7C"})

        for SpecsAndDescTopTag in SpecsAndDescTopTags:
            SpecsAndDescNextTags = SpecsAndDescTopTag.findAll("div", {"class": "bhgxx2 col-12-12"})
            for SpecsAndDescNextTag in SpecsAndDescNextTags:
                SellerMainTag = SpecsAndDescNextTag.find("div", {"class": "_34wn58"})
                if SellerMainTag is not None:
                    SellersDivs = SellerMainTag.findAll("div")
                    for SellersDiv in SellersDivs:
                        sellerNameDiv = SellersDiv.find("div", {"id": "sellerName"})
                        if sellerNameDiv is not None:
                            sellerNameSpan = sellerNameDiv.find("span")
                            if sellerNameSpan is not None:
                                finalSpan = sellerNameSpan.find("span")
                                if finalSpan is not None:
                                    device_details[title_tag.text]['SellerName'] = finalSpan.text
                                sellerStarTag = sellerNameSpan.find("div", {"class": "hGSR34 YddkNl"})
                                if sellerStarTag is not None:
                                    device_details[title_tag.text]['SellerStar'] = sellerStarTag.text

                descriptionMainTags = SpecsAndDescNextTag.find("div", {"class": "_1y9a40"})
                if descriptionMainTags is not None:
                    descTextTag = descriptionMainTags.find("div", {"class": "_1oCqc9"})
                    if descTextTag is not None:
                        descText = descTextTag.text
                    descLinesTag = descriptionMainTags.find("div", {"class": "_3cpW1u"})
                    if descLinesTag is not None:
                        descLines = descLinesTag.find("div", {"class": "_3la3Fn _1zZOAc"})
                        if descLines is not None:
                            descLineText = descLines.text
                            device_details[title_tag.text]['Divdesc'] = descLineText

                spec_details_dict = {}
                spec_details_dict_inner = {}
                MainHeaderText = ''
                specificationMainTags = SpecsAndDescNextTag.find("div", {"class": "MocXoX"})
                if specificationMainTags is not None:
                    specTextTag = specificationMainTags.find("div", {"class": "_2GiuhO"})
                    if specTextTag is not None:
                        specText = specTextTag.text
                    specAllDivs = specificationMainTags.findAll("div")
                    for specAllDiv in specAllDivs:
                        specNexAllDivs = specAllDiv.find("div", {"class": "_3Rrcbo"})
                        if specNexAllDivs is not None:
                            specNextAllDivs = specNexAllDivs.findAll("div", {"class": "_2RngUh"})
                            for specNextAllDiv in specNextAllDivs:
                                MainHeaderTag = specNextAllDiv.find("div", {"class": "_2lzn0o"})
                                if MainHeaderTag is not None:
                                    MainHeaderText = MainHeaderTag.text
                                tableMainTag = specNextAllDiv.find("table", {"class": "_3ENrHu"})
                                if tableMainTag is not None:
                                    tbodyTag = tableMainTag.find("tbody")
                                    if tbodyTag is not None:
                                        trTag = tbodyTag.find("tr", {"class": "_3_6Uyw row"})
                                        if trTag is not None:
                                            specNameTag = trTag.find("td", {"class": "_3-wDH3 col col-3-12"})
                                            if specNameTag is not None:
                                                specNameTagList = specNameTag.text
                                                # print('Sub Tag',specNameTagList)
                                            tdListTag = trTag.find("td", {"class": "_2k4JXJ col col-9-12"})
                                            if tdListTag is not None:
                                                ulListSpec = tdListTag.find("ul")
                                                if ulListSpec is not None:
                                                    liListSpec = ulListSpec.find("li", {"class": "_3YhLQA"})
                                                    if liListSpec is not None:
                                                        liListSpecText = liListSpec.text
                                                        # print('Main:',MainHeaderText,'SubTag:',specNameTagList,'Value:',liListSpecText)
                                                        spec_details_dict_inner[specNameTagList] = liListSpecText
                                                        spec_details_dict[MainHeaderText] = spec_details_dict_inner
                                                        device_details[title_tag.text]['SpecDesc'] = spec_details_dict

                total_reviews = {}
                total_sub_reviews = {}
                starVals = []
                starName = []
                ReviewAndRatingMainTag = SpecsAndDescNextTag.find("div", {"class": "col _39LH-M"})

                if ReviewAndRatingMainTag is not None:
                    ReviewAndRatingSecTag = ReviewAndRatingMainTag.find("div", {"class": "row _1Ahy2t _2aFisS"})
                    if ReviewAndRatingSecTag is not None:
                        ReviewAndRatingNexSecTag = ReviewAndRatingSecTag.find("div", {"class": "ebepc- _2eB0mV"})
                        if ReviewAndRatingNexSecTag is not None:
                            RevRatRow = ReviewAndRatingNexSecTag.find("div", {"class": "row"})
                            if RevRatRow is not None:
                                RevRatStarTag = RevRatRow.find("div", {"class": "col-3-12"})
                                if RevRatStarTag is not None:
                                    colRevRatStar = RevRatStarTag.find("div", {"class": "col"})
                                    if colRevRatStar is not None:
                                        rowRevRatStar = colRevRatStar.find("div", {"class": "row"})
                                        if rowRevRatStar is not None:
                                            rowRevRatStarDiv = rowRevRatStar.find("div", {"class": "col-12-12 _11EBw0"})
                                            if rowRevRatStar is not None:
                                                StartTag = rowRevRatStar.find("div", {"class": "_1i0wk8"})
                                                if StartTag is not None:
                                                    StartTagVal = StartTag.text
                                                    total_reviews['Stars'] = StartTagVal
                                        rowRevRatTags = colRevRatStar.findAll("div", {"class": "row _2yc1Qo"})
                                        for rowRevRatTag in rowRevRatTags:
                                            finalRavRatTag = rowRevRatTag.find("div", {"class": "col-12-12"})
                                            if finalRavRatTag is not None:
                                                spanRavRatTag = finalRavRatTag.find("span")
                                                if spanRavRatTag is not None:
                                                    if 'Ratings' in spanRavRatTag.text:
                                                        total_reviews['Ratings'] = re.sub("[^\\d+]", "",
                                                                                          spanRavRatTag.text)
                                                    elif 'Reviews' in spanRavRatTag.text:
                                                        total_reviews['Reviews'] = re.sub("[^\\d+]", "",
                                                                                          spanRavRatTag.text)

                                AllStrarsMainTag = RevRatRow.find("div", {"class": "col-9-12 _1S74qC"})
                                if AllStrarsMainTag is not None:
                                    AllStrarsNextTag = AllStrarsMainTag.find("div", {"class": "_1n1j36 DrZOea uD3lY9"})
                                    if AllStrarsNextTag is not None:
                                        StartsValTag = AllStrarsNextTag.find("ul", {"class": "_2ZGksR"})
                                        if StartsValTag is not None:
                                            listStartsVals = StartsValTag.findAll("li", {"class": "_58ZIbs"})
                                            for listStartsVal in listStartsVals:
                                                divSaratsVal = listStartsVal.find("div", {"class": "_1atKHO"})
                                                if divSaratsVal is not None:
                                                    spanSartVal = divSaratsVal.find("span", {"class": "_3ApwOG"})
                                                    if spanSartVal is not None:
                                                        SartValTxt = spanSartVal.text
                                                        starName.append(SartValTxt)
                                                        # print('SartValTxt:', SartValTxt)
                                        StartsRatingTags = AllStrarsNextTag.find("ul", {"class": "_2M5FGu"})
                                        if StartsRatingTags is not None:
                                            listStarsNumbers = StartsRatingTags.findAll("li", {"class": "_58ZIbs"})
                                            for listStarsNumber in listStarsNumbers:
                                                listStarsNumberValTag = listStarsNumber.find("div", {"class": "CamDho"})
                                                if listStarsNumberValTag is not None:
                                                    listStarsNumberVal = listStarsNumberValTag.text
                                                    starVals.append(listStarsNumberVal)
                                                    # print('listStarsNumberValTag:', listStarsNumberVal)

                    for vals in zip(starName, starVals):
                        total_sub_reviews[vals[0]] = re.sub("[^\d+]", "", vals[1])

                    total_reviews['ReviewStars'] = total_sub_reviews
                    device_details[title_tag.text]['ReviewRatingStars'] = total_reviews
                    # print(total_reviews)

for k, v in device_details.items():
    print(k, ' ', v['ReviewRatingStars'])
