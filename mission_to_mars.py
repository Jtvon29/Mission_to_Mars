
# coding: utf-8

# In[1]:


import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import pandas as pd


# In[2]:


# Initialize browser
def init_Browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "Resources/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


# In[3]:


# Function to scrape the Nasa website
def scrape_mars():
    
    # Initialize the browser
    browser = init_Browser()
    # Visit the Nasa website
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(nasa_url)
    # Scrape the page into soup
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')
    # Find the most recent article title and paragraph text
    Article = nasa_soup.find("li", class_="slide")
    # Get the title of the article
    Article_title = Article.find("div", class_="content_title").text
    # Get the paragraph text
    Paragraph_text = Article.find("div", class_="article_teaser_body").text
    
    # Scrape mars image
    #Visit the website
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Navigate to the Full size image
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    #Scrape the page into soup
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'htm.parser')
    #Collect the path and paste to the new url
    image_path = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = 'https://www.jpl.nasa.gov' + image_path
    
    #Scrape weather from tweets
    #Visit the website
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    #Scrape the page using soup
    twitter_html = browser.html
    twitter_soup = BeautifulSoup(twitter_html,'html.parser')
    #Get the most recent tweet about the weather
    mars_weather = twitter_soup.find('p', class_='TweetTextSize TweetTextSize--normal.js-tweet-text.tweet-text').text
    
    # Scrape data table from website
    #Visit the website
    table_url = 'https://space-facts.com/mars/'
    #Read the table in using read_html
    table = pd.read_html(table_url)
    #Make it into a datframe
    df = table[0]
    #Convert it back into html
    html_table = df.to_html()
    html_table.replace('\n', '')
    #Save it as a file
    Data_table = df.to_html('Resources/table.html')
    
    # Scrape the hemisphere images of mars
    #Visit the website
    hemi_main_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_main_url)
    #Scrape the page into soup
    hemi_main_html = browser.html
    hemi_main_soup = BeautifulSoup(hemi_main_html, 'html.parser')
    #Find the path to the full size images
    first = hemi_main_soup.find('div', class_='collapsible results')
    second = first.find_all('div', class_='description')
    #Create an empty list to hold the images
    Hemisphere_images = []
    #create a loop to find the images of the hemispheres in each link
    for x in second:
        #go to the link
        title = x.a.h3.text
        link = 'https://astrogeology.usgs.gov' + x.a['href']
        browser.visit(link)
        #Scrape the page into soup
        hemi_html = browser.html
        hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
        #find the path of the fullsize image
        image_link = hemi_soup.find('div', class_='downloads').find('li').a['href']
        #Create dictioanry to hold the urls
        hemi_dict = {}
        hemi_dict['title'] = title
        hemi_dict['link'] = image_link
        Hemisphere_images.append(hemi_dict)
    

