import urllib, json


def get_city_details(city):
    url = "http://getcitydetails.geobytes.com/GetCityDetails?fqcn=" + city
    response = urllib.urlopen(url)
    data = None
    data = json.loads(response.read())
    city_details = {}
    if data[u'geobytescountry'] == '':
        return ''
    city_details["City"] = city
    city_details["Country"] = str(data[u'geobytescountry'])
    city_details["Currency"] = str(data[u'geobytescurrency'])
    city_details["Population"] = str(
        "%.2f" % (float(data[u'geobytespopulation']) / 1000000)) + 'M'  # in the task its 'M' first...
    city_details["Capital"] = str(data[u'geobytescapital'])
    # print(data)
    # print city_details
    return city_details


def get_capital_details(city):
    url = "https://restcountries.eu/rest/v2/capital/" + city
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    print data


def get_city_population(city):
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=worldcitiespop&q=" + city
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    print data

# get_city_details("Ashdod")
