# **Web scraper for the Köchel catalogue using BeautifulSoup and pandas**

## Abstract

The following program scrapes data from the [All About Mozart](https://allaboutmozart.com/mozart-kochel-catalogue-works-compositions-koechel/) website dedicated to listing the Köchel catalogue, using the `BeautifulSoup` library as web scraping tool, the `requests` library for HTTP fetching and `pandas` to parse the results into CSV format. Additionally, the count of works per genre is included in the DataFrame.

As a music enthusiast, I take an interest in the historical record of musical works and their analysis. Mozart's catalogue, collected and studied a century later, during the 19th, by the musicologist Ludwig Ritter von Köchel, is specifically a vast one given the composer's prodigious ability at not only performing but also writing music, having in a short lifespan of 35 years almost 700 registered works, also starting to compose at age 5. With this simple analytical tool, we can observe Mozart mainly wrote arias, symphonies and piano pieces, and surprisingly more _lieder_ (i.e. short songs inspired by German poetry) than piano sonatas.