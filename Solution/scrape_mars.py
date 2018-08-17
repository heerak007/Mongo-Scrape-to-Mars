# function to scrape the websites and collect the information to be posted on webpage

# import necessary libraries
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import re, time

def scrape():
    # switch executable_path depending on windows or mac users, set to windows currently
    executable_path = {'executable_path': 'chromedriver.exe'}
    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')
    newsinfo = soup.find('div', class_='list_text')
    news_title = newsinfo.find('div', class_='content_title').text
    news_p = newsinfo.find('div', class_='article_teaser_body').text
    # return news_title, news_p
    print("Latest News Info Collected")

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    featured_image_url = soup2.find('article', class_='carousel_item').footer.a.get("data-fancybox-href")
    featured_image_url =f'https://www.jpl.nasa.gov{featured_image_url}'
    print("Featured Image collected")
    # return featured_image_url

    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')
    mars_weather = soup3.find('p', text=re.compile(' hPa, daylight ')).text
    print("Mars current weather collected")
    # return mars_weather

    url4 = 'https://space-facts.com/mars/'
    table = pd.read_html(url4)[0].rename(columns={0:"Description",1:"Value"})

    html_table = table.to_html(index=False, border=0, classes="table table-hover")
    # return html_table
    print("HTML table collected")

    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    html5 = browser.html
    soup5 = bs(html5, 'html.parser')
    imagelist = soup5.find_all('div', class_="description")
    hemisphere_image_urls=[]
    for x in imagelist:
        titlex= x.h3.text
        urlx = f"https://astrogeology.usgs.gov{x.a['href']}"
        
        browser.visit(urlx)
        soupx = bs(browser.html, 'html.parser')
        
        imagex = soupx.find('img', class_='wide-image')['src']
        imagex = f"https://astrogeology.usgs.gov{imagex}"
        print("Image url collected")
        
        imgdict = {"title":titlex, "img_url":imagex}
        hemisphere_image_urls.append(imgdict)
    # return hemisphere_image_urls

    MarsInfo = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "mars_weather":mars_weather,
        "html_table":html_table,
        "hemisphere_image_urls":hemisphere_image_urls
    }
    print("Information Collection Complete")
    return MarsInfo
    