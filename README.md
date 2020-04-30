# uwcscoursescrape
Scraping the UWaterloo CS Course offerings into a CSV file through *Python*. This uses *requests* to get the HTML, and *BeautifulSoup4* to parse it.\
This skips courses not available to CS students, and was made based on the 2020-21 Undergraduate Calendar

This scrapes the following data:\
*Title (eg, 'CS135')\
Course ID\
Name (eg, 'Designing Functional Programs)\
Credits\
Terms Offered (eg, FW)\
Prerequisites\
Corequisites\
Antirequisites\
Course Description\*

This skips the following data:\
*Course notes\
Department consent requirement\
Cross-listings*
