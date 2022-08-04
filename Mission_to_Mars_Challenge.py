#!/usr/bin/env python
# coding: utf-8

# # Deliverable 1
# 
# ## Scrape Full-Resolution Mars Hemisphere Images and Titles

# In[1]:


# 10.3.0 Scrape Mars Data


# In[2]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[3]:


executable_path = {'executable_path': ChromeDriverManager().install()}
# executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[5]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[6]:


slide_elem.find('div', class_='content_title')


# In[7]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# In[9]:


#  10.3.4 Scrape Mars Data: Featured Image


# ### JPL Space Images Featured Image

# In[10]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[12]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[13]:


#  use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image.
# Find the relative image url
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[14]:


# add the base URL to our code.
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[15]:


# 10.3.5 Scrape Mars Data: Mars Facts


# ## Mars Facts

# In[16]:


#  scrape the entire table with Pandas' .read_html() function.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[17]:


#  Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function. 
df.to_html


# In[18]:


#  Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function. 
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[19]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[20]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# In[21]:


# 3. Write code to retrieve the image urls and titles for each hemisphere
for hemis in range(4):
    # Browse through each article
    browser.links.find_by_partial_text('Hemisphere')[hemis].click()
    
    # Parse the HTML
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    # Scraping
    title = hemi_soup.find('h2', class_='title').text
    img_url = hemi_soup.find('li').a.get('href')
    
    # Store the finding into a dictionary and append the list
    hemispheres = {}
    hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)
    
    # Navigate back
    browser.back()


# In[22]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[23]:


# 5. Quit the browser
browser.quit()


# In[ ]:




