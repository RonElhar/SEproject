import urllib, json

"""
~~~~~~~~~~~~~~~~~~~~~~~~  Module Description ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This Module is used for getting info about cities 

    API Services:
        geobytes.com
        restcountries.eu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

"""
    Description :
        This method gets details of a city from geobytes API
    Args:
        param1 : city name

    Returns:
        information about the city From 
"""


def get_city_details(city):
    url = "http://getcitydetails.geobytes.com/GetCityDetails?fqcn=" + city
    response = urllib.urlopen(url)
    data = None
    try:
        data = json.loads(response.read())
    except UnicodeDecodeError:
        return None
    city_details = {}
    if data[u'geobytescountry'] == '':
        return ''
    city_details["Country"] = str(data[u'geobytescountry'])
    city_details["Currency"] = str(data[u'geobytescurrency'])
    city_details["Population"] = str(
        "%.2f" % (float(data[u'geobytespopulation']) / 1000000)) + 'M'  # in the task its 'M' first...
    return city_details

"""
    Description :
        This method gets relevant details of all of the capital cities in the world 
        from  RestCountries API
    Returns:
        information about the city From 
"""

def get_capitals_details():
    url = 'https://restcountries.eu/rest/v2/all?fields=name;capital;currencies;population'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    capitals_dict = {}
    city_details = {}
    for details in data:
        city_details["Country"] = details[u'name']
        city_details["Currency"] = str(details[u'currencies'])
        city_details["Population"] = str("%.2f" % (float(details[u'population']) / 1000000)) + 'M'
        capitals_dict[details['capital']] = city_details
    return capitals_dict
