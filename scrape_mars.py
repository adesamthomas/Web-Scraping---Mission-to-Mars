
# coding: utf-8

# # NASA Mars News
# 
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# In[21]:


from splinter import Browser
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import requests as req
import time

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[2]:


url = 'https://mars.nasa.gov/news/'

#BROWSER.VISIT BRINGS IN THE URL
browser.visit(url)


# In[3]:


#HTML OBJECT
html = browser.html
#PARSE HTML WITH BEAUTIFUL SOUP
soup = bs(html, 'html.parser')


# In[4]:


#EXTRACT TITLE TEXT
#title = soup.title.text

news_title = soup.find("div",class_="content_title").text
news_p = soup.find("div", class_="article_teaser_body").text
print(news_title)
print(news_p)


# # JPL Mars Space Images - Featured Image
# 
# Visit the url for JPL Featured Space Image here.
# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# Make sure to find the image url to the full size .jpg image.
# Make sure to save a complete url string for this image.

# In[5]:


image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(image_url)


# In[6]:


html = browser.html
soup = bs(html, 'html.parser')


# In[7]:


image = soup.find("img", class_="thumb")["src"]
featured_image_url = "https://www.jpl.nasa.gov" + image
print(featured_image_url)


# # Mars Weather
# 
# Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.

# In[8]:


weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)


# In[9]:


html = browser.html
soup = bs(html, 'html.parser')


# In[10]:


mars_weather = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
print(mars_weather[0].text)


# # Mars Facts
# 
# Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# Use Pandas to convert the data to a HTML table string.

# In[11]:


facts_url = 'https://space-facts.com/mars/'


# In[12]:


mars_tables = pd.read_html(facts_url)
mars_tables


# In[13]:


mars_df = mars_tables[0]
mars_df.columns = ['Stat Description', 'Stat Value']
mars_df


# In[14]:


#SETTING STAT DESCRIPTION COLUMN AS INDEX
mars_df.set_index('Stat Description', inplace=True)
mars_df


# In[15]:


html_table = mars_df.to_html()
html_table


# In[16]:


#STRIP UNWANTED NEW LINES TO CLEAN UP THE TABLE
html_table.replace('\n', '')


# In[17]:


mars_df.to_html('mars_table.html')


# # Mars Hemispheres
# 
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# In[37]:


hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemisphere_url)


# In[38]:


html = browser.html
soup = bs(html, "html.parser")


# In[39]:


mars_hemispheres_info = []

products = soup.find("div", class_ = "result-list" )
hemispheres = products.find_all("div", class_="item")

for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    #title = title.replace("Enhanced", "")
    end_link = hemisphere.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(image_link)
    html = browser.html
    soup=bs(html, "html.parser")
    download_files = soup.find("div", class_="downloads")
    image_url = download_files.find("a")["href"]
    mars_hemispheres_info.append({"title": title, "img_url": image_url})


# In[40]:


mars_hemispheres_info


# # Step 2 - MongoDB and Flask Application
# 
# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
# 
# Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
# 
# Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
# 
# Store the return value in Mongo as a Python dictionary.
# 
# Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
# 
# Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.
