from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time
import re

# Create chrome wrapper object
def init_browser():
    executable_path ={"executable_path" :"chromedriver.exe"}
    return Browser("chrome",**executable_path, headless=False)

# Scrape mars astrogeology site
def scrape():

    # Get browser/chrome object
    browser = init_browser()

    # URLs to scrape
    url1 ="https://mars.nasa.gov/news/"
    url2 ="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url3 ="https://twitter.com/marswxreport?lang=en"
    url4 ="https://space-facts.com/mars/"
    url5= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Get site for Title and Para
    browser.visit(url1) 
    
    html_text = browser.html
    soup = bs(html_text,'lxml')

    # Get Title & paragraph text
    news_title = soup.select_one('.content_title').text.strip()
    news_p = soup.select_one('.rollover_description_inner').text.strip()

    # Get Image from 2nd URL
    browser.visit(url2)
    
    html_text = browser.html
    soup = bs(html_text,'lxml')

    # Get featured image
    featured_image_url = soup.select_one('.carousel_item')['style']
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url[23:-3]
    
    # Get page for tweet text
    browser.visit(url3)
    
    html_text = browser.html
    soup = bs(html_text,'lxml')
    
    # Get tweet text
    mars_weather_tweet =soup.select_one(".tweet-text").text.strip()

    # Get tables from Mars facts page
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['key', 'value']
    df = df.set_index('key')
    del df.index.name
    mars_facts_html = df.to_html(justify='left')

    #
    #  Get the Hemisphere Images
    #

    # Mars Title and Img
    browser.visit(url5)
    
    html_text = browser.html
    soup = bs(html_text,'lxml')

    # Extract all hemisphere names from page
    hemisphere_image_urls = []
    for div_tag in soup.find_all('div', "description"):
        # Get each hemisphere details
        link_tag = div_tag.find('a', 'itemLink')
        link_href = link_tag['href']
        hemi_text = link_tag.find("h3").text

        # Get the original size image from hemisphere page
        browser.visit("https://astrogeology.usgs.gov" + link_href)
        hemi_soup = bs(browser.html,'lxml')

        # Extract the tag for image with text 'Original' 
        image_tag = hemi_soup.find('a', text ='Sample')
        image_link = image_tag['href']

        hemisphere_image_urls.append( { 'title' : hemi_text, 'img_url' : image_link } ) 

    print(hemisphere_image_urls)


    # Save extracted data to dictionary
    mars_listings = {
        "title": news_title,
        "Paragraph": news_p,
        "image": featured_image_url,
        "weather_tweet": mars_weather_tweet,
        "facts": mars_facts_html,
        "hemispheres" : hemisphere_image_urls
    }

    # Return the mars_listings data
    return mars_listings
