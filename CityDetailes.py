import urllib, json


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
    # print(data)
    # print city_details
    return city_details


def get_capitals_details():
    url = 'https://restcountries.eu/rest/v2/all?fields=name;capital;currencies;population'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    capitals_dict = {}
    for details in data:
        city_details = {}
        city_details["Country"] = details[u'name']
        city_details["Currency"] = str(details[u'currencies'])
        city_details["Population"] = str("%.2f" % (float(details[u'population']) / 1000000)) + 'M'
        # print details['capital']
        capitals_dict[details['capital']] = city_details
    return capitals_dict


def get_city_population(city):
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=worldcitiespop&q=" + city
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    print data

# get_city_details("Ashdod")
# get_capitals_details()
