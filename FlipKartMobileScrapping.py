from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from urllib import parse as parse
import re
import http.client as http
import json

print('\n','========Scrapping Started=============','\n')
http.HTTPConnection._http_vsn = 10
http.HTTPConnection._http_vsn_str = 'HTTP/1.0'

base_url = "https://www.flipkart.com"

main_page = 'https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'

try:
    uMain = uReq(main_page)
except  http.IncompleteRead as e:
    uMain = e.partial

main_page_soup = soup(uMain.read(), "html.parser")
uMain.close()

mobile_item_details = {}
main_review_rating = {}
num_pages_div = main_page_soup.find("div", {"class": "_2zg3yZ"})
span = str(num_pages_div.find("span").text)
span = re.sub("[^\d\\s+]", "", span)
start, end = map(int, span.split())
UrlsProcessed=0
print('Start :', start, 'End:', end)
end = 1
for page_num in range(start, end + 1):
    #curr_url = main_page + '&page=' + str(page_num)
    curr_url='https://www.flipkart.com/search?q=mobiles&otracker=AS_Query_HistoryAutoSuggest_5_0&otracker1=AS_Query_HistoryAutoSuggest_5_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=5&as-type=HISTORY&p%5B%5D=facets.brand%255B%255D%3DApple'
    try:
        uCurrPage = uReq(curr_url)
    except http.IncompleteRead as e:
        uCurrPage = e.partial
        print('Partial')

    uCurrPageSoup = soup(uCurrPage.read(), "html.parser")
    uCurrPage.close()
    MainTopMostDivs = uCurrPageSoup.findAll("div", {"class": "_1HmYoV _35HD7C"})
    # MainTopMostDivs = uCurrPageSoup.find("div", {"class": "_1HmYoV _35HD7C"}) ##Remove
    #print(MainTopMostDivs)
    for MainTopMostDiv in MainTopMostDivs:
        AllItemsDivs = MainTopMostDiv.findAll("div", {"class": "bhgxx2 col-12-12"})
        for AllItemsDiv in AllItemsDivs:
            AllItemsMainDiv = AllItemsDiv.find("div", {"class": "_3O0U0u"})
            if AllItemsMainDiv is not None:
                AllItemDivId = AllItemsMainDiv.find("div", {"class": "_1UoZlX"})
                ObjId = AllItemsMainDiv.find("div")
                if ObjId is not None:
                    ObjIdText = ObjId['data-id']
                if AllItemDivId is not None:
                    IteamAClass = AllItemDivId.find("a", {"class": "_31qSD5"})
                    if IteamAClass is not None:
                        mobile_item_details[ObjIdText] = {'url': base_url + IteamAClass['href']}
                        ItemsURL = base_url + IteamAClass['href']
                        OutofStockAllTag=IteamAClass.find("div",{"class":'_1OCn9C'})
                        if OutofStockAllTag is not None:
                            OutOfStockFistDiv=OutofStockAllTag.find("div",{"class":"_3aV9Tq"})
                            if OutOfStockFistDiv is not None:
                                OutOfStockSpanTag=OutOfStockFistDiv.find("span",{"class":"_1GJ2ZM"})
                                if OutOfStockSpanTag is not None:
                                    mobile_item_details[ObjIdText]['InStock']=OutOfStockSpanTag.text
                        ItemAllTextDetails = IteamAClass.find("div", {"class": "_1-2Iqu row"})
                        if ItemAllTextDetails is not None:
                            ItemAllTextDetailsDefAmts = ItemAllTextDetails.findAll("div", {"class": "col col-7-12"})
                            for ItemAllTextDetailsDefAmt in ItemAllTextDetailsDefAmts:
                                ItemNameTag = ItemAllTextDetailsDefAmt.find("div", {"class": "_3wU53n"})
                                if ItemNameTag is not None:
                                    ItemName = ItemNameTag.text
                                    mobile_item_details[ObjIdText]['name'] = ItemName
                                ReviewRatingMainTag = ItemAllTextDetailsDefAmt.find("div", {"class": "niH0FQ"})
                                if ReviewRatingMainTag is not None:
                                    ReviewRatingMainTagSpan = ReviewRatingMainTag.find("span", {"class": "_38sUEc"})
                                    if ReviewRatingMainTagSpan is not None:
                                        main_review_rating = {}
                                        ReviewRatingMainSpan = ReviewRatingMainTagSpan.find("span")
                                        if ReviewRatingMainSpan is not None:
                                            ReviewRatingMainAllSpans = ReviewRatingMainSpan.findAll("span")
                                            for ReviewRatingMainAllSpan in ReviewRatingMainAllSpans:
                                                if 'Ratings' in ReviewRatingMainAllSpan.text:
                                                    main_review_rating['Ratings'] = re.sub("[^\\d+]", "",
                                                                                           ReviewRatingMainAllSpan.text)
                                                elif 'Reviews' in ReviewRatingMainAllSpan.text:
                                                    main_review_rating['Reviews'] = re.sub("[^\\d+]", "",
                                                                                           ReviewRatingMainAllSpan.text)
                                        mobile_item_details[ObjIdText]['MainReviewRating'] = main_review_rating
                                ItemDescpritionMainTag = ItemAllTextDetailsDefAmt.find("div", {"class": "_3ULzGw"})

                                ItemDescList = []
                                if ItemDescpritionMainTag is not None:
                                    UlItemDesc = ItemDescpritionMainTag.find("ul", {"class": "vFw0gD"})
                                    if UlItemDesc is not None:
                                        ListOfDescs = UlItemDesc.findAll("li", {"class": "tVe95H"})

                                        for ListOfDesc in ListOfDescs:
                                            ItemDescList.append(ListOfDesc.text)
                                    mobile_item_details[ObjIdText]['DescDetails'] = ItemDescList

                            PriceAndDiscountTagDetails = ItemAllTextDetails.find("div",
                                                                                 {"class": "col col-5-12 _2o7WAb"})
                            price_details_dict = {}
                            if PriceAndDiscountTagDetails is not None:
                                priceDetailsOffer = PriceAndDiscountTagDetails.find("div", {"class": "_6BWGkk"})
                                if priceDetailsOffer is not None:
                                    priceDetailsOff = priceDetailsOffer.find("div", {"class": "_1uv9Cb"})
                                    if priceDetailsOff is not None:
                                        FinalPriceTag = priceDetailsOff.find("div", {"class": "_1vC4OE _2rQ-NK"})
                                        if FinalPriceTag is not None:
                                            price_details_dict = {
                                                'FinalPrice': re.sub("[^\\d+]", "", FinalPriceTag.text)}

                                        ActualPriceTag = priceDetailsOff.find("div", {"class": "_3auQ3N _2GcJzG"})
                                        if ActualPriceTag is not None:
                                            price_details_dict['ActualPrice'] = re.sub("[^\\d+]", "",
                                                                                       ActualPriceTag.text)

                                        TotalDiscount = priceDetailsOff.find("div", {"class": "VGWI6T"})
                                        if TotalDiscount is not None:
                                            price_details_dict['TotalPercentageDiscount'] = re.sub("[^\\d+]", "",
                                                                                                   TotalDiscount.text)
                                        # print(price_details_dict)
                                        mobile_item_details[ObjIdText]['PriceAndDiscountOffers'] = price_details_dict

                                otherDiscountOffers = PriceAndDiscountTagDetails.findAll("div", {"class": "_2nE8_R"})
                                otherOffers = []
                                for otherDiscountOffer in otherDiscountOffers:
                                    emiDivs = otherDiscountOffer.findAll("div", {"class": "_3_G5Wj"})
                                    for emiDiv in emiDivs:
                                        otherOffers.append(str(emiDiv.text).replace('\u20b9','Rs '))
                                price_details_dict['otherOffers'] = otherOffers
                                mobile_item_details[ObjIdText]['PriceAndDiscountOffers'] = price_details_dict

                        ItemPage = uReq(ItemsURL)
                        ItemPageSoup = soup(ItemPage.read(), "html.parser")
                        ItemPage.close()
                        UrlsProcessed=UrlsProcessed+1
                        print('URLS Processed:',UrlsProcessed)
                        IndiItemsAllTextContaints = ItemPageSoup.find("div", {"class": "_1HmYoV _35HD7C col-8-12"})
                        if IndiItemsAllTextContaints is not None:
                            ItemsAllItemsTextDetails = IndiItemsAllTextContaints.findAll("div",
                                                                                         {"class": "bhgxx2 col-12-12"})
                            for ItemsAllItemsTextDetail in ItemsAllItemsTextDetails:
                                TextAndPricesMainDivTag = ItemsAllItemsTextDetail.find("div", {"class": "_29OxBi"})
                                if TextAndPricesMainDivTag is not None:
                                    TextAndPricesMainDivSubTagS = TextAndPricesMainDivTag.findAll("div")
                                    for TextAndPricesMainDivSubTag in TextAndPricesMainDivSubTagS:
                                        DeviceNameh1Tag = TextAndPricesMainDivSubTag.find("h1", {"class": "_9E25nV"})
                                        if DeviceNameh1Tag is not None:
                                            DeviceNameSpanTag = DeviceNameh1Tag.find("span", {"class": "_35KyD6"})
                                            if DeviceNameSpanTag is not None:
                                                mobile_item_details[ObjIdText][
                                                    'DeviceNameandDetails'] = DeviceNameSpanTag.text.replace(u'\xa0',
                                                                                                             ' ')

                                        ReviewRatingItemMainTag = TextAndPricesMainDivSubTag.find("div",
                                                                                                  {"class": "_3ors59"})
                                        reviewRatingMap = {}
                                        if ReviewRatingItemMainTag is not None:
                                            ReviewRatingItemInnerTag = ReviewRatingItemMainTag.find("div", {
                                                "class": "niH0FQ _2nc08B"})
                                            if ReviewRatingItemInnerTag is not None:
                                                StarsSpansTag = ReviewRatingItemInnerTag.find("span",
                                                                                              {"class": "_2_KrJI"})
                                                if StarsSpansTag is not None:
                                                    StarValueTag = StarsSpansTag.find("div", {"class": "hGSR34"})
                                                    if StarValueTag is not None:
                                                        reviewRatingMap['Stars'] = StarValueTag.text
                                                ReviewAndRatingMainTag = ReviewRatingItemInnerTag.find("span", {
                                                    "class": "_38sUEc"})
                                                if ReviewAndRatingMainTag is not None:
                                                    ReviewRatingMainSpanTag = ReviewAndRatingMainTag.find("span")
                                                    if ReviewRatingMainSpanTag is not None:
                                                        ReviewRatingMainSpanValTags = ReviewRatingMainSpanTag.findAll(
                                                            "span")
                                                        for ReviewRatingMainSpanValTag in ReviewRatingMainSpanValTags:
                                                            ReviewRatingMainSpanValText = ReviewRatingMainSpanValTag.text
                                                            if 'Ratings' in ReviewRatingMainSpanValText:
                                                                reviewRatingMap['Ratings'] = re.sub("[^\\d+]", "",
                                                                                                    ReviewRatingMainSpanValText)
                                                            elif 'Reviews' in ReviewRatingMainSpanValText:
                                                                reviewRatingMap['Reviews'] = re.sub("[^\\d+]", "",
                                                                                                    ReviewRatingMainSpanValText)
                                                    # print(reviewRatingMap)
                                                    mobile_item_details[ObjIdText][
                                                        'ReviewRatingStars'] = reviewRatingMap

                                    pricesAndDiscountMap = {}
                                    ExtraOffTag = TextAndPricesMainDivTag.find("div", "_2XDAh9")
                                    if ExtraOffTag is not None:
                                        ExtraOffTagSpan = ExtraOffTag.find("span")
                                        if ExtraOffTagSpan is not None:
                                            pricesAndDiscountMap['ExtraDiscount'] = re.sub("[^\\d+]", "",
                                                                                           ExtraOffTagSpan.text)

                                    PricesAndDiscountsMainTag = TextAndPricesMainDivTag.find("div", "_3iZgFn")
                                    if PricesAndDiscountsMainTag is not None:
                                        PriceAndDiscountSubTag = PricesAndDiscountsMainTag.find("div",
                                                                                                {"class": "_2i1QSc"})
                                        if PriceAndDiscountSubTag is not None:
                                            PriceAndDiscountInnerTag = PriceAndDiscountSubTag.find("div",
                                                                                                   {"class": "_1uv9Cb"})
                                            if PriceAndDiscountInnerTag is not None:
                                                ActPriceTag = PriceAndDiscountInnerTag.find("div", {
                                                    "class": "_1vC4OE _3qQ9m1"})
                                                if ActPriceTag is not None:
                                                    pricesAndDiscountMap['FinalPrice'] = re.sub("[^\\d+]", "",
                                                                                                ActPriceTag.text)
                                                ActuallyItemPriceTag = PriceAndDiscountInnerTag.find("div", {
                                                    "class": "_3auQ3N _1POkHg"})
                                                if ActuallyItemPriceTag is not None:
                                                    pricesAndDiscountMap['ActualPrice'] = re.sub("[^\\d+]", "",
                                                                                                 ActuallyItemPriceTag.text)
                                                PercentageDiscountTag = PriceAndDiscountInnerTag.find("div", {
                                                    "class": "VGWI6T _1iCvwn"})
                                                if PercentageDiscountTag is not None:
                                                    PercentageDiscountSpan = PercentageDiscountTag.find("span")
                                                    if PercentageDiscountSpan is not None:
                                                        pricesAndDiscountMap['PercentageDiscount'] = re.sub("[^\\d+]",
                                                                                                            "",
                                                                                                            PercentageDiscountSpan.text)

                                        mobile_item_details[ObjIdText]['PriceAndDiscount'] = pricesAndDiscountMap

                                allAvilaOffer = ''
                                allAvilaOfferList = []
                                AviableAllOffersMainTag = ItemsAllItemsTextDetail.find("div", {"class": "_3nSGUy"})
                                if AviableAllOffersMainTag is not None:
                                    AviableAllOffersNextTag = AviableAllOffersMainTag.find("div", {"class": "_2RzXYa"})
                                    if AviableAllOffersNextTag is not None:
                                        AviableAllOffersNextSubTag = AviableAllOffersNextTag.find("div",
                                                                                                  {"class": "_3D89xM"})
                                        if AviableAllOffersNextSubTag is not None:
                                            AviableAllOffersSpanLists = AviableAllOffersNextSubTag.findAll("span", {
                                                "class": "_7g_MLT row"})
                                            for AviableAllOffersSpanList in AviableAllOffersSpanLists:
                                                AvilableOffersAllLi = AviableAllOffersSpanList.find("li", {
                                                    "class": "_2-n-Lg col"})
                                                if AvilableOffersAllLi is not None:
                                                    AvilableOfferesAllSpans = AvilableOffersAllLi.findAll("span")
                                                    allAvilaOffer = ''
                                                    for AvilableOfferesAllSpan in AvilableOfferesAllSpans:
                                                        allAvilaOffer = allAvilaOffer + ' ' + str(
                                                            AvilableOfferesAllSpan.text).replace('<strong>',
                                                                                                 '').replace(
                                                            '</strong>', '').replace('\u20b9','Rs ')
                                                    allAvilaOfferList.append(allAvilaOffer)

                                    mobile_item_details[ObjIdText]['AvialbleOffers'] = allAvilaOfferList

                                WarrantyMainTag = ItemsAllItemsTextDetail.find("div", {"class": "_2sVT0Y"})
                                if WarrantyMainTag is not None:
                                    WarrantyNextTag = WarrantyMainTag.find("div", {"class": "_2b7gqe"})
                                    if WarrantyNextTag is not None:
                                        WarrantyTextTag = WarrantyNextTag.find("div", {"class": "_3h7IGd"})
                                        if WarrantyTextTag is not None:
                                            mobile_item_details[ObjIdText]['Warranty'] = WarrantyTextTag.text

                                ColorAndStroageMap = {}
                                ColorOrStroageLst = []
                                ColorAndStroageMainTag = ItemsAllItemsTextDetail.find("div", {"class": "rPoo01"})

                                if ColorAndStroageMainTag is not None:

                                    ColorAndStorageMainAllTags = ColorAndStroageMainTag.findAll("div", {
                                        "class": "_37KLG6 col col-6-12"})
                                    for ColorAndStorageMainAllTag in ColorAndStorageMainAllTags:
                                        ColorAndStorageMainDiv = ColorAndStorageMainAllTag.find("div",
                                                                                                {"class": "_2a2WU_"})
                                        if ColorAndStorageMainDiv is not None:
                                            ColorOrStorageTag = ColorAndStorageMainDiv.find("span",
                                                                                            {"class": "_1lwQLq"})
                                            if ColorOrStorageTag is not None:
                                                ColorOrStorageTagText = ColorOrStorageTag.text
                                            ColorOrStorageListTag = ColorAndStorageMainDiv.find("ul",
                                                                                                {"class": "fUBI-_"})
                                            if ColorOrStorageListTag is not None:
                                                ColorOrStroageLst = []
                                                ColorOrStorageListTagAllValvs = ColorOrStorageListTag.findAll("li", {
                                                    "class": "_3hSwtk"})
                                                for ColorOrStorageListTagAllValv in ColorOrStorageListTagAllValvs:
                                                    ColorOrStroageLowerTag = ColorOrStorageListTagAllValv.find("div", {
                                                        "class": "_11cw91 _1-fCbU E753YP DgCx9f"})
                                                    if ColorOrStroageLowerTag is not None:
                                                        ColorOrStroageTextTag = ColorOrStroageLowerTag.find("div", {
                                                            "class": "_2h52bo _15sV4W _3xOS0O"})
                                                        if ColorOrStroageTextTag is not None:
                                                            ColorOrStroageLst.append(ColorOrStroageTextTag.text)
                                                ColorAndStroageMap[ColorOrStorageTagText] = ColorOrStroageLst
                                                mobile_item_details[ObjIdText]['ColorAndStorage'] = ColorAndStroageMap

                            HighLitesAndPaymentMap = {}
                            HighLitesAndPaymentLst = []

                            HighLitesAndPaymentMainTags = IndiItemsAllTextContaints.findAll("div",
                                                                                            {"class": "_1HmYoV hCUpcT"})

                            for HighLitesAndPaymentMainTag in HighLitesAndPaymentMainTags:
                                HighLitesAndPaymentMainSubTags = HighLitesAndPaymentMainTag.findAll("div",
                                                                                                    "bhgxx2 col-6-12")
                                for HighLitesAndPaymentMainSubTag in HighLitesAndPaymentMainSubTags:
                                    HighLitsPaymentAllMainTag = HighLitesAndPaymentMainSubTag.find("div",
                                                                                                   {"class": "g2dDAR"})
                                    if HighLitsPaymentAllMainTag is not None:
                                        HighLitesAndPaymentTextTag = HighLitsPaymentAllMainTag.find("div", {
                                            "class": "_2hqjdd"})
                                        if HighLitesAndPaymentTextTag is not None:
                                            HighLitesAndPaymentTextTagText = HighLitesAndPaymentTextTag.text
                                        HighLitesAndPaymentValuesTag = HighLitsPaymentAllMainTag.find("div", {
                                            "class": "_3WHvuP"})
                                        if HighLitesAndPaymentValuesTag is not None:
                                            HighLitesAndPaymentValuesTagUl = HighLitesAndPaymentValuesTag.find("ul")
                                            if HighLitesAndPaymentValuesTagUl is not None:
                                                HighLitesAndPaymentLst = []
                                                HighLitesAndPaymentValuesTaglis = HighLitesAndPaymentValuesTagUl.findAll(
                                                    "li", {"class": "_2-riNZ"})
                                                for HighLitesAndPaymentValuesTagli in HighLitesAndPaymentValuesTaglis:
                                                    HighLitesAndPaymentLst.append(HighLitesAndPaymentValuesTagli.text)
                                                HighLitesAndPaymentMap[
                                                    HighLitesAndPaymentTextTagText] = HighLitesAndPaymentLst

                                    PaymentAllMainTag = HighLitesAndPaymentMainSubTag.find("div",
                                                                                           {"class": "qjOFxP flex"})
                                    if PaymentAllMainTag is not None:
                                        EasyPaymentTextTag = PaymentAllMainTag.find("div", {"class": "A6q-nB"})
                                        if EasyPaymentTextTag is not None:
                                            EasyPaymentTextTagText = EasyPaymentTextTag.text
                                        EasyPaymentTextTagValuesTag = PaymentAllMainTag.find("div",
                                                                                             {"class": "_1-V7IJ"})
                                        if EasyPaymentTextTagValuesTag is not None:
                                            EasyPaymentTextTagValuesUlTag = EasyPaymentTextTagValuesTag.find("ul")
                                            if EasyPaymentTextTagValuesUlTag is not None:
                                                HighLitesAndPaymentLst = []
                                                EasyPaymentTextTagValuesLiTags = EasyPaymentTextTagValuesUlTag.findAll(
                                                    "li", {"class": "_2ptBxu"})
                                                for EasyPaymentTextTagValuesLiTag in EasyPaymentTextTagValuesLiTags:
                                                    HighLitesAndPaymentLst.append(EasyPaymentTextTagValuesLiTag.text)
                                                HighLitesAndPaymentMap[EasyPaymentTextTagText] = HighLitesAndPaymentLst

                                    mobile_item_details[ObjIdText]['HighlitesAndPaymentOption'] = HighLitesAndPaymentMap

                            SellerDescriptionSpecsRatingReviewsMainTags = IndiItemsAllTextContaints.findAll("div", {
                                "class": "_1HmYoV _35HD7C"})

                            SellerInfoMap = {}
                            for SellerDescriptionSpecsRatingReviewsMainTag in SellerDescriptionSpecsRatingReviewsMainTags:
                                SellerDescriptionSpecsRatingReviewsSubTags = SellerDescriptionSpecsRatingReviewsMainTag.findAll(
                                    "div", {"class": "bhgxx2 col-12-12"})
                                for SellerDescriptionSpecsRatingReviewsSubTag in SellerDescriptionSpecsRatingReviewsSubTags:
                                    SellerDescriptionSpecsRatingReviewsInnerTag = SellerDescriptionSpecsRatingReviewsSubTag.find(
                                        "div", {"class": "_34wn58"})
                                    if SellerDescriptionSpecsRatingReviewsInnerTag is not None:
                                        SellerDivTag = SellerDescriptionSpecsRatingReviewsInnerTag.find("div", {
                                            "class": "_1pQ2tg"})
                                        if SellerDivTag is not None:
                                            SellerDivTagSpan = SellerDivTag.find("span")
                                            if SellerDivTagSpan is not None:
                                                SellerDivTagSpanText = SellerDivTagSpan.text
                                        SellerInfoDivs = SellerDescriptionSpecsRatingReviewsInnerTag.findAll("div")
                                        for SellerInfoDiv in SellerInfoDivs:
                                            SellerNameDiv = SellerInfoDiv.find("div", {"class": "_3HGjxn"})
                                            if SellerNameDiv is not None:
                                                SellerNameSpan = SellerNameDiv.find("span")
                                                if SellerNameSpan is not None:
                                                    SellerNameSpanText = SellerNameSpan.find("span")
                                                    if SellerNameSpanText is not None:
                                                        SellerInfoMap['Name'] = SellerNameSpanText.text
                                                SellerStarTag = SellerNameDiv.find("div", {"class": "hGSR34 YddkNl"})
                                                if SellerStarTag is not None:
                                                    SellerInfoMap['Star'] = SellerStarTag.text
                                                mobile_item_details[ObjIdText]['SellerInfo'] = SellerInfoMap

                                            PolicyMainTag = SellerInfoDiv.find("div", {"class": "_3aj0Jp"})
                                            if PolicyMainTag is not None:
                                                PolicyMainTagUl = PolicyMainTag.find("ul", {"class": "_2GIvqp"})
                                                if PolicyMainTagUl is not None:
                                                    PolicyMainTagli = PolicyMainTagUl.find("li", {"class": "_31u9b3"})
                                                    if PolicyMainTagli is not None:
                                                        PolicyMainTagNameTxt = PolicyMainTagli.find("div", {
                                                            "class": "_20PGcF"})
                                                        if PolicyMainTagNameTxt is not None:
                                                            SellerInfoMap['Policy'] = PolicyMainTagNameTxt.text
                                                            mobile_item_details[ObjIdText]['SellerInfo'] = SellerInfoMap
                                    ProductItemDescriptionTag = SellerDescriptionSpecsRatingReviewsSubTag.find("div", {
                                        "class": "_1y9a40"})
                                    if ProductItemDescriptionTag is not None:
                                        ProductItemDescriptionTagIn = ProductItemDescriptionTag.find("div", {
                                            "class": "_3cpW1u"})
                                        if ProductItemDescriptionTagIn is not None:
                                            ProductItemDescriptionTagNext = ProductItemDescriptionTagIn.find("div", {
                                                "class": "_3la3Fn _1zZOAc"})
                                            if ProductItemDescriptionTagNext is not None:
                                                ProductItemDescriptionTagText = ProductItemDescriptionTagNext.find("p")
                                                if ProductItemDescriptionTagText is not None:
                                                    mobile_item_details[ObjIdText][
                                                        'Description'] = ProductItemDescriptionTagText.text

                                    ProductDiscMap = {}
                                    ProductItemDescriptionDetailsMainTag = SellerDescriptionSpecsRatingReviewsSubTag.find(
                                        "div", {
                                            "class": "_1QrSNG"})
                                    if ProductItemDescriptionDetailsMainTag is not None:

                                        ValueTagText = ProductItemDescriptionDetailsMainTag.find("div",
                                                                                                 {"class": "_2HVvN7"})
                                        if ValueTagText is not None:
                                            ValueTagTextVal = ValueTagText.text

                                        ProdDescWordsTag = ProductItemDescriptionDetailsMainTag.find("div", {
                                            "class": "_3u-uqB"})

                                        if ProdDescWordsTag is not None:
                                            ProdDescWordsTagVal = ProdDescWordsTag.text
                                            ProductDiscMap[ValueTagTextVal] = ProdDescWordsTagVal
                                            mobile_item_details[ObjIdText]['ProductDescription'] = ProductDiscMap

                                    ProductItemFeaturesMainAlls = SellerDescriptionSpecsRatingReviewsSubTag.findAll(
                                        "div", {
                                            "class": "_38NXIU"})

                                    for ProductItemFeaturesMainAll in ProductItemFeaturesMainAlls:
                                        productFirstFeature = ProductItemFeaturesMainAll.find("div", {
                                            "class": "_3LyGPp _2briKY"})
                                        if productFirstFeature is not None:
                                            productFirstFeatureDiv = productFirstFeature.find("div")
                                            if productFirstFeatureDiv is not None:
                                                productFirstFeatureDivNext = productFirstFeatureDiv.find("div")
                                                if productFirstFeatureDivNext is not None:
                                                    HeadingTag = productFirstFeatureDivNext.find("div",
                                                                                                 {"class": "_2THx53"})
                                                    if HeadingTag is not None:
                                                        HeadingTagVal = HeadingTag.text
                                                    ParaTextTagDiv = productFirstFeatureDivNext.find("div",
                                                                                                     {
                                                                                                         "class": "_1aK10F"})
                                                    if ParaTextTagDiv is not None:
                                                        ParaTextTag = ParaTextTagDiv.find("p")
                                                        if ParaTextTag is not None:
                                                            ParaTextTagVal = ParaTextTag.text
                                                            ProductDiscMap[HeadingTagVal] = ParaTextTagVal
                                                            mobile_item_details[ObjIdText][
                                                                'ProductDescription'] = ProductDiscMap

                                    AllSpecMap = {}
                                    AllSpecMapInner = {}
                                    AllItemSpecificationsMainTag = SellerDescriptionSpecsRatingReviewsSubTag.find("div",
                                                                                                                  "MocXoX")
                                    if AllItemSpecificationsMainTag is not None:
                                        SpecMainHeadingTag = AllItemSpecificationsMainTag.find("div",
                                                                                               {"class": "_2GiuhO"})
                                        if SpecMainHeadingTag is not None:
                                            SpecMainHeadingTagVal = SpecMainHeadingTag.text
                                        AllSpecsMainDivs = AllItemSpecificationsMainTag.findAll("div")
                                        for AllSpecsMainDiv in AllSpecsMainDivs:
                                            AllSpecsMSubDiv = AllSpecsMainDiv.find("div", {"class": "_3Rrcbo"})
                                            if AllSpecsMSubDiv is not None:
                                                AllSubCatagoeryDivs = AllSpecsMSubDiv.findAll("div",
                                                                                              {"class": "_2RngUh"})
                                                for AllSubCatagoeryDiv in AllSubCatagoeryDivs:
                                                    SpecSubHeadDivTag = AllSubCatagoeryDiv.find("div", "_2lzn0o")
                                                    if SpecSubHeadDivTag is not None:
                                                        SpecSubHeadDivTagText = SpecSubHeadDivTag.text
                                                        # print(SpecSubHeadDivTagText) ###HashMainKey
                                                    SpecDetailsMainTable = AllSubCatagoeryDiv.find("table", "_3ENrHu")
                                                    if SpecDetailsMainTable is not None:
                                                        SpecDetailsMainTableTbody = SpecDetailsMainTable.find("tbody")
                                                        if SpecDetailsMainTableTbody is not None:
                                                            SpecDetailsMainTableAllTrs = SpecDetailsMainTableTbody.findAll(
                                                                "tr", {"class": "_3_6Uyw row"})
                                                            for SpecDetailsMainTableAllTr in SpecDetailsMainTableAllTrs:
                                                                DescNameTag = SpecDetailsMainTableAllTr.find("td", {
                                                                    "class": "_3-wDH3 col col-3-12"})
                                                                if DescNameTag is not None:
                                                                    DescNameTagVal = DescNameTag.text
                                                                DescValueTagTd = SpecDetailsMainTableAllTr.find("td", {
                                                                    "class": "_2k4JXJ col col-9-12"})
                                                                if DescValueTagTd is not None:
                                                                    DescValueTagUl = DescValueTagTd.find("ul")
                                                                    if DescValueTagUl is not None:
                                                                        DescValueTagLi = DescValueTagUl.find("li", {
                                                                            "class": "_3YhLQA"})
                                                                        if DescValueTagLi is not None:
                                                                            DescValueTagText = DescValueTagLi.text
                                                                            AllSpecMapInner[
                                                                                DescNameTagVal] = DescValueTagText
                                                    AllSpecMap[SpecSubHeadDivTagText] = DescValueTagText
                                                mobile_item_details[ObjIdText]['ItemSpecification'] = AllSpecMap

                                            ManufactureDivTag = AllSpecsMainDiv.find("div", {"class": "_39XK9P"})
                                            if ManufactureDivTag is not None:
                                                ManufactureDivTagVal = ManufactureDivTag.text
                                                print(ManufactureDivTagVal)

                                    AllReviewsAndRatingsStars = {}
                                    AllReviewsAndRatings = SellerDescriptionSpecsRatingReviewsSubTag.find("div", {
                                        "class": "col _39LH-M"})
                                    if AllReviewsAndRatings is not None:
                                        ReviewRatingHeadingMainTag = AllReviewsAndRatings.find("div",
                                                                                               {"class": "_1B7BXc"})
                                        if ReviewRatingHeadingMainTag is not None:
                                            ReviewRatingHeadingSubTag = ReviewRatingHeadingMainTag.find("div", {
                                                "class": "_3unCI7"})
                                            if ReviewRatingHeadingSubTag is not None:
                                                ReviewRatingHeadingSubTagVal = ReviewRatingHeadingSubTag.text
                                                # print(ReviewRatingHeadingSubTagVal)
                                        ReviewRatingRestOfTags = AllReviewsAndRatings.find("div", {
                                            "class": "row _1Ahy2t _2aFisS"})
                                        if ReviewRatingRestOfTags is not None:

                                            ReviewAndRatingInnerMainTag = ReviewRatingRestOfTags.find("div", {
                                                "class": "ebepc-"})
                                            if ReviewAndRatingInnerMainTag is not None:

                                                ReviewAndRatingInnerMainTagRow = ReviewAndRatingInnerMainTag.find("div",
                                                                                                                  {
                                                                                                                      "class": "row"})
                                                if ReviewAndRatingInnerMainTagRow is not None:

                                                    ReviewAndRatingInnerMainTagRowStarsNumbers = ReviewAndRatingInnerMainTagRow.find(
                                                        "div", {"class": "col-4-12"})
                                                    if ReviewAndRatingInnerMainTagRowStarsNumbers is not None:
                                                        ReviewAndRatingInnerMainTagRowStarsNumbersCol = ReviewAndRatingInnerMainTagRowStarsNumbers.find(
                                                            "div", {"class": "col"})
                                                        if ReviewAndRatingInnerMainTagRowStarsNumbersCol is not None:
                                                            ReviewAndRatingInnerMainTagRowStarsTags = ReviewAndRatingInnerMainTagRowStarsNumbersCol.findAll(
                                                                "div", {"class": "row"})
                                                            for ReviewAndRatingInnerMainTagRowStarsTag in ReviewAndRatingInnerMainTagRowStarsTags:
                                                                StarsValuesTags = ReviewAndRatingInnerMainTagRowStarsTag.find(
                                                                    "div", {"class": "col-12-12 _11EBw0"})
                                                                if StarsValuesTags is not None:
                                                                    StarsValuesTextTags = StarsValuesTags.find("div", {
                                                                        "class": "_1i0wk8"})
                                                                    if StarsValuesTextTags is not None:
                                                                        StarsValuesTextTagVal = StarsValuesTextTags.text
                                                                        AllReviewsAndRatingsStars[
                                                                            'Stars'] = StarsValuesTextTags.text

                                                            ReviewAndRatingInnerMainTagRowTextTags = ReviewAndRatingInnerMainTagRowStarsNumbersCol.findAll(
                                                                "div", {"class": "row _2yc1Qo"})
                                                            for ReviewAndRatingInnerMainTagRowTextTag in ReviewAndRatingInnerMainTagRowTextTags:
                                                                ReviewRatingTextMainTag = ReviewAndRatingInnerMainTagRowTextTag.find(
                                                                    "div", {"class": "col-12-12"})
                                                                if ReviewRatingTextMainTag is not None:
                                                                    ReviewRatingTextMainTagVal = ReviewRatingTextMainTag.text
                                                                    if 'Ratings' in ReviewRatingTextMainTagVal:
                                                                        RatingsVal = re.sub("[^\\d+]", "",
                                                                                            ReviewRatingTextMainTagVal)
                                                                        AllReviewsAndRatingsStars[
                                                                            'Ratings'] = RatingsVal
                                                                    elif 'Reviews' in ReviewRatingTextMainTagVal:
                                                                        ReviewsVal = re.sub("[^\\d+]", "",
                                                                                            ReviewRatingTextMainTagVal)
                                                                        AllReviewsAndRatingsStars[
                                                                            'Reviews'] = ReviewsVal
                                                            mobile_item_details[ObjIdText][
                                                                'ItmReviewRatingStars'] = AllReviewsAndRatingsStars
                                                    ReviewAndRatingInnerMainTagRowStarsAnsNumbers = ReviewAndRatingInnerMainTagRow.find(
                                                        "div", {"class": "col-8-12 _1S74qC TxMRTO"})
                                                    NumberOfStars = {}
                                                    starsList = []
                                                    starsValList = []
                                                    if ReviewAndRatingInnerMainTagRowStarsAnsNumbers is not None:
                                                        StarsImageMainTag = ReviewAndRatingInnerMainTagRowStarsAnsNumbers.find(
                                                            "div", {"class": "_1n1j36 DrZOea uD3lY9"})
                                                        if StarsImageMainTag is not None:
                                                            StarNumbersTagUl = StarsImageMainTag.find("ul", {
                                                                "class": "_2M5FGu"})
                                                            if StarNumbersTagUl is not None:
                                                                StarNumbersTagLis = StarNumbersTagUl.findAll("li", {
                                                                    "class": "_58ZIbs"})
                                                                for StarNumbersTagLi in StarNumbersTagLis:
                                                                    StarNumbersTagDiv = StarNumbersTagLi.find("div", {
                                                                        "class": "_1atKHO"})
                                                                    if StarNumbersTagDiv is not None:
                                                                        StarNumbersTagSpan = StarNumbersTagDiv.find(
                                                                            "span", {"class": "_3ApwOG"})
                                                                        if StarNumbersTagSpan is not None:
                                                                            starsList.append(StarNumbersTagSpan.text)
                                                            StarValuesTagUl = StarsImageMainTag.find("ul", {
                                                                "class": "_148m3I"})
                                                            if StarValuesTagUl is not None:
                                                                StarValuesTagLis = StarValuesTagUl.findAll("li", {
                                                                    "class": "_58ZIbs"})
                                                                for StarValuesTagLi in StarValuesTagLis:
                                                                    StarValuesTagDiv = StarValuesTagLi.find("div", {
                                                                        "class": "CamDho"})
                                                                    if StarValuesTagDiv is not None:
                                                                        starsValList.append(re.sub("[^\\d+]", "",
                                                                                                   StarValuesTagDiv.text))
                                                            for k, v in zip(starsList, starsValList):
                                                                NumberOfStars[k] = v
                                                        AllReviewsAndRatingsStars['Stars'] = NumberOfStars
                                                        mobile_item_details[ObjIdText][
                                                            'ItmReviewRatingStars'] = AllReviewsAndRatingsStars
                                            ImageReviewRating = {}
                                            ReviewAndRatingImageMainTag = ReviewRatingRestOfTags.find("div", {
                                                "class": "_251bNL"})
                                            if ReviewAndRatingImageMainTag is not None:
                                                ReviewAndRatingImageMainTagRow = ReviewAndRatingImageMainTag.find("div",
                                                                                                                  {
                                                                                                                      "class": "row"})
                                                if ReviewAndRatingImageMainTagRow is not None:
                                                    ReviewAndRatingImageMainTagRowClasses = ReviewAndRatingImageMainTagRow.findAll(
                                                        "a", {"class": "col-3-12 _2kDYyJ tsPZ29"})
                                                    for ReviewAndRatingImageMainTagRowClasse in ReviewAndRatingImageMainTagRowClasses:
                                                        Link = base_url + parse.quote(
                                                            ReviewAndRatingImageMainTagRowClasse['href'])
                                                        RawLink = base_url + ReviewAndRatingImageMainTagRowClasse[
                                                            'href'].replace(' ','%20')

                                                        ReviewImagesMainTopTag = ReviewAndRatingImageMainTagRowClasse.find(
                                                            "div", {"class": "_1nl9s1"})
                                                        if ReviewImagesMainTopTag is not None:
                                                            CreteriaNameTag = ReviewImagesMainTopTag.find("div", {
                                                                "class": "_3wUVEm"})
                                                            if CreteriaNameTag is not None:
                                                                CriteraText = CreteriaNameTag.text
                                                            CreteriaRatingTag = ReviewImagesMainTopTag.find("div", {
                                                                "class": "R3upVV"})
                                                            if CreteriaRatingTag is not None:
                                                                CreteriaRatingTagSvg = CreteriaRatingTag.find("svg", {
                                                                    "class": "_1jHJkZ"})
                                                                if CreteriaRatingTagSvg is not None:
                                                                    CreteriaRatingTagPath = CreteriaRatingTagSvg.find(
                                                                        "text", {"class": "PRNS4f"})
                                                                    if CreteriaRatingTagPath is not None:
                                                                        CreteriaRatingTagPathText = CreteriaRatingTagPath.text
                                                                        ImageReviewRating[CriteraText] = {
                                                                            'Link': RawLink,
                                                                            'StarRating': CreteriaRatingTagPathText}

                                                                        try:
                                                                            #print(Link)
                                                                            ReviewWisePage = uReq(RawLink)
                                                                        except http.IncompleteRead as e:
                                                                            ReviewWisePage = e.partial
                                                                        except http.InvalidURL:
                                                                            ReviewWisePage = uReq(Link)

                                                                        uReviewPageSoup = soup(ReviewWisePage.read(),
                                                                                               "html.parser")
                                                                        ReviewWisePage.close()
                                                                        MainFeedBackTag = uReviewPageSoup.find("div",
                                                                                                               {
                                                                                                                   "class": "_2m08jR"})

                                                                        if MainFeedBackTag is not None:
                                                                            NextMainFeedBackTag = MainFeedBackTag.find(
                                                                                "div", {"class": "_12iFZG _3PG6Wd"})
                                                                            if NextMainFeedBackTag is not None:
                                                                                NextMainFeedBackTagNx = NextMainFeedBackTag.find(
                                                                                    "div", {
                                                                                        "class": "ooJZfD _3FGKd2 col-12-12"})
                                                                                if NextMainFeedBackTagNx is not None:
                                                                                    LowerMainFeedBackTag = NextMainFeedBackTagNx.find(
                                                                                        'div', {
                                                                                            "class": "ooJZfD _2oZ8XT col-9-12"})
                                                                                    if LowerMainFeedBackTag is not None:
                                                                                        NextLowerMainFeedBackTagS = LowerMainFeedBackTag.findAll(
                                                                                            "div", {
                                                                                                "class": "_3gijNv col-12-12"})
                                                                                        for NextLowerMainFeedBackTag in NextLowerMainFeedBackTagS:

                                                                                            NextLowerMainFeedBackTagNx=NextLowerMainFeedBackTag.find("div",{"class":"_2xUvKq"})
                                                                                            if NextLowerMainFeedBackTagNx is not None:
                                                                                                PosNegFeedFackMainTag=NextLowerMainFeedBackTagNx.find("div",{"class":"NGnKYj"})
                                                                                                if PosNegFeedFackMainTag is not None:
                                                                                                    PosNegFeedFackMainTagDivs=PosNegFeedFackMainTag.findAll("div")
                                                                                                    FeedBackMap = {}
                                                                                                    for PosNegFeedFackMainTagDiv in PosNegFeedFackMainTagDivs:
                                                                                                        PosFeedBackTag=PosNegFeedFackMainTagDiv.find("span",{"class":"_1Iw1jf"})
                                                                                                        if PosFeedBackTag is not None:
                                                                                                            FeedBackMap['Positive']=re.sub("[^\\d+]","",PosFeedBackTag.text)
                                                                                                        NegFeedBackTag=PosNegFeedFackMainTagDiv.find("span",{"class":"_3MuE_5"})
                                                                                                        if NegFeedBackTag is not None:
                                                                                                            FeedBackMap['Negative']=re.sub("[^\\d+]","",NegFeedBackTag.text)
                                                                                                            ImageReviewRating[CriteraText]['FeedbackPercentage']=FeedBackMap
                                                        AllReviewsAndRatingsStars['CategoryReview'] = ImageReviewRating
                                                    mobile_item_details[ObjIdText][
                                                        'ItmReviewRatingStars'] = AllReviewsAndRatingsStars

'''
with open("C:\\Users\\Owner\\Documents\\datasets\\flipkark_Mobile.json",'w') as fp:
    json.dump(mobile_item_details,fp)
'''
for k,v in mobile_item_details.items():
    print(k,' ',v)
print('\n','========Scrapping Ended=============','\n')
