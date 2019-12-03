from bs4 import BeautifulSoup
import urllib.request as urlreq
import re
from requests import get
import json
url='https://www.cermati.com/karir'

url=input("Enter the URL: ")
json_out=input("Enter Output Json File: ")
try:
    page=urlreq.urlopen(url)
    soup=BeautifulSoup(page,'html.parser')
    content = soup.find('div', {"class": "tab-content"})
    joblist={}
    #print(content)
    div=content.findAll('div',{"role":"tabpanel"})
    for elem in div:
        title=elem.find('h4',{"class":"tab-title"})
        desc=elem.find('p',{"class":"description-group"})
        #print(elem.get('id'),':',title.text,':',desc.text.strip())
        avil_jobs=elem.find('div',{"class":"container-fluid"})
        for jobs in avil_jobs.findAll('div',{"clickable-row row"}):
            job=jobs.find('div',{"class":"dept-label col-sm-7"})
            loc=jobs.find('div',{"class":"col-sm-4"})
            link=jobs.find('a',href=True)['href']
            decs_dict={'title':job.text.strip().replace('&apos;',"'"),'location':loc.text.strip()}
            #print(elem.get('id'),':',title.text.replace('&apos;',"'"),':',desc.text.strip().replace('&apos;',"'"),job.text.replace('&apos;',"'"),link.strip())
            try:
                #print('Opening ',title.text.replace('&apos;',"'"),':',link.strip())
                subpage=urlreq.urlopen(link.strip().replace(' ','%20'))
                subsoup=BeautifulSoup(subpage,'html.parser')
                jd=subsoup.find('meta',{"property":"og:description"})
                jd_arys=jd.get('content').strip().split('\n')
                for jd_ary in jd_arys:
                    if ':' in jd_ary:
                        #print(jd_ary)
                        spl=jd_ary.split(':')
                        desc=spl[0]
                        wrds=spl[-1]
                        wrds=wrds.replace(u'\xa0', u' ')

                        if wrds.strip().startswith('*'):
                            dtls=wrds.strip().split('*')
                            dtls=list(filter(bool,dtls))
                        if wrds.strip().startswith('.'):
                            dtls=wrds.strip().split('.')
                            dtls=list(filter(bool,dtls))
                        if desc=="Job Description":
                            decs_dict['description']=dtls
                        elif desc=="Qualifications":
                            decs_dict['qualification']=dtls

                postedtag=subsoup.find('h3',{"class":"details-title"})

                if postedtag is not None:
                    posted=postedtag.text
                    decs_dict['posted by']=posted
            except Exception as e:
                print('Error in ',link,str(e))
            #print(subsoup)

            #print('decs_dict:',title.text.replace('&apos;',"'"),':',decs_dict)

            if title.text.strip().replace('&apos;',"'") in joblist:
                val=joblist.get(title.text.strip().replace('&apos;',"'"))
                #print('VAL:',title.text.strip().replace('&apos;',"'"),';',val)
                val.append(decs_dict)
                joblist[title.text.strip().replace('&apos;',"'")]=val
            else:
                joblist[title.text.strip().replace('&apos;',"'")]=[decs_dict]

        #print(elem.get('id'),':',title.text,':',desc.text.strip(),':',avil_jobs.strip())
        #print(avil_jobs)
    #divcont=soup.select('#section-vacancies')
    #print(divcont)
except Exception as ex:
    print('Could Not Open URL %s'%url)
    print(str(ex))
finally:
    #print(joblist)
    with open(json_out,'w') as fp:
        json.dump(joblist,fp)
    print("Done Json",joblist,"created")

