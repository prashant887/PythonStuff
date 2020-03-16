from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import re
base_url = "https://www.flipkart.com"

main_page='https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
uMain = uReq(main_page)
main_page_soup = soup(uMain.read(), "html.parser")
uMain.close()

num_pages_div=main_page_soup.find("div", { "class": "_2zg3yZ"})
span=str(num_pages_div.find("span").text)
span=re.sub("[^\d\\s+]", "",span)
start,end=map(int,span.split())
for page_num in range(start,end+1):
    curr_url=main_page+'&page='+str(page_num)
    #print(curr_url)

page_url='https://www.flipkart.com/search?q=android+mobiles+4g&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_0_14_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_0_14_sc_na_na&as-pos=0&as-type=RECENT&suggestionId=android+mobiles+4g%7CMobiles&requestId=43d808ee-aac6-415c-9803-9b66d41a9c3d&as-searchtext=andrid%20mobiles'
page_url='https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(uClient.read(), "html.parser")
uClient.close()


containers = page_soup.findAll("div", { "class": "_3O0U0u"})

links = page_soup.findAll("a", {"class": "_31qSD5"})
link=containers[0].find("a", {"class": "_31qSD5"}).get('href')

#print(containers[0],'\n','link ',base_url+link)

descs=containers[0].findAll("li", {"class": "tVe95H"})

for desc in descs:
    print(desc.text,end=',')

emis=containers[0].findAll("div", {"class": "_3_G5Wj"})

print('\n')
for emi in emis:
    print(emi.text,end=' ')

name=containers[0].find("div", {"class": "_3wU53n"})

price=containers[0].find("div", {"class": "_1vC4OE _2rQ-NK"})

print('\n',name.text,' ',price.text)
'''
for link in links:
    print(link)


try:
    for container in containers:
        product_name = container.div.img["alt"]
        price_container = container.findAll("div", {"class": "col col-5-12 _2o7WAb"})
        price = price_container[0].text.strip()
        rating_container = container.findAll("div", {"class": "niH0FQ"})
        rating = rating_container[0].text
        trim_price=''.join(price.split(','))
        rm_rupee = trim_price.split('₹')
        add_rs_price = "Rs."+rm_rupee[1].replace("\\s+",'')
        split_price = add_rs_price.split('E')
        final_price = split_price[0]
        split_rating = rating.split(" ")
        final_rating = split_rating[0]
        print(product_name.replace("," ,"|") +"," + final_price +"," + final_rating + "\n")
except:
    pass

'''