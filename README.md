# Web Scrapping VGC
This is a webscrapping project based on [ashaheedq vgchartzScrape](https://github.com/ashaheedq/vgchartzScrape). The purpose of this project was to learn the basics of using <b>BeautifulSoup4</b> and built upon on it another data analysis scripts in order to use the dataset offered by VGChartz to its fullest. 
 
 The first part of the project is dedicated to learn the basics of using proxies for scrapping purposes, with the aid of the <b>requests</b> class.

#Proxies / Scrapping Proxyscrape

There were little to no changes in the proxies_gen.py code and, if at any, all of them were variable name changes. You can review the original code at [ashaheedq vgchartzScrape](https://github.com/ashaheedq/vgchartzScrape). This add on is necessary for working with free proxies. 

#Scrapping VGChartz
The main body of the project. A lot of the code is based on [ashaheedq vgchartzScrape](https://github.com/ashaheedq/vgchartzScrape), but there were a couple more changes in this one. 
a) Disabled the multiprocessing part. 
b) Re-worked a lot of the syntaxis of the original code, manly to adjust to changes made in the HTML code of VGchart.
c) Added the another module to scrapping the release date of various games. 
d) Re-worked the saving and loading criteria for the dataframe once it is saved.
e) Added a save module in order to export the .csv file. 

All in all, this was a great first project in order to understand the BeautifulSoup4 web scrapping, and the criteria which need to be considered in order to make it work. The next part of this project is the visualization aspect of the data from VGChartz, in which I will intend to create dynamic_chartz using gganimate in R. 
