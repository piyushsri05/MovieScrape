# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 14:11:47 2017

@author: piyus
"""


from bs4 import BeautifulSoup
import re
import time #to wait for some time
import requests


def getCritic(review):
    critic='NA' 
    criticChunk=review.find('a',{'href':re.compile('/critic/')})
    if criticChunk: 
       critic=criticChunk.text    
    return critic

def getTextLen(review):
    text='NA'
    textChunk=review.find('div',{'class':'the_review'})
    if textChunk: 
        text=textChunk.text       
    return len(text)


def getDate(review):
    date='NA'
    dateChunk=review.find('div',{'class':re.compile('review_date')})
    if dateChunk:    
        date=dateChunk.text
    return date
    
def getSource(review):
    source='NA'
    sourceChunk=review.find('em',{'class':re.compile('subtle')})
    if source:
        source=sourceChunk.text
    return source
        
def getRating(review):
    rating='NA'
    ratingChunk=review.find('div',{'class':re.compile('review_icon')})
    if "fresh" in str(ratingChunk).lower():
        ratingChunk="Fresh"
    elif 'rotten' in str(ratingChunk).lower():
         ratingChunk='Rotten'
    else:
        ratingChunk='NA'
    return ratingChunk


def run(url):

    pageNum=2 # number of pages to collect

    fw=open('reviews.txt','w') # output file
	
    for p in range(1,pageNum+1): # for each page 

        print ('page',p)
        html=None # used to store page source

        if p==1: pageLink=url # url for page 1
        else: pageLink=url+'?page='+str(p)+'&sort=' # make the page url
		
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 secs
		
        if not html:continue # couldnt get the page, ignore
        
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 

        reviews=soup.findAll('div', {'class':re.compile('review_table_row')}) # get all the review divs # re.compile it does flexible search and will return exact search
        
        for review in reviews:

            critic=str(getCritic(review))                
            textLength=str(getTextLen(review))
            date=str(getDate(review))
            source=str(getSource(review))
            rating=str(getRating(review))  
            
            print(critic,textLength,date,source,rating)

            fw.write(critic+'\t'+textLength+'\t'+date+'\t'+source+'\t'+rating+'\n') # write to file 
		
            time.sleep(2)	# wait 2 secs 

    fw.close()

if __name__=='__main__':
    url='https://www.rottentomatoes.com/m/space_jam/reviews/'
    run(url)