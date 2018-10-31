import StringIO
import ReadFile
import re


def getStopWords():
    file = open("C:\\Users\\ronel\\Desktop\\Search Engine\\SEproject\\stopwords.txt")
    lines = file.readlines()
    stop_words = []
    for word in lines:
        word = word.replace('\n', '')
        stop_words.append(word)
    return stop_words


class Parse:
    def __init__(self):
        #   self.docs = ReadFile.seperateDocsInDir("D:\Studies\BGU\semesterE\IR\partA\corpus")
        self.date_dict = {'JANUARY': '01', 'January': '01', 'JAN': '01', 'Jan': '01', 'FEBRUARY': '02',
                          'February': '02',
                          'FEB': '02', 'Feb': '02', 'MARCH': '03', 'March': '03', 'MAR': '03', 'Mar': '03',
                          'APRIL': '04',
                          'April': '04', 'APR': '04', 'Apr': '04', 'MAY': '05', 'May': '05', 'JUNE': '06', 'June': '06',
                          'JUN': '06', 'Jun': '06', 'JULY': '07', 'July': '07', 'JUL': '07', 'Jul': '07',
                          'AUGUST': '08',
                          'August': '08', 'AUG': '08', 'Aug': '08', 'SEPTEMBER': '09', 'September': '09', 'SEP': '09',
                          'Sep': '09', 'OCTOBER': '10', 'October': '10', 'OCT': '10', 'Oct': '10', 'NOVEMBER': '11',
                          'November': '11', 'NOV': '11', 'Nov': '11', 'DECEMBER': '12', 'December': '12', 'DEC': '12',
                          'Dec': '12'}
        self.num_dict = {'Million': 1000000, 'million': 1000000, 'm': 1000000, 'Thousand': 1000}
        self.stop_words = getStopWords()

    def main_parser(self, list_strings):
        length = len(list_strings)
        reg_number = re.compile(r'\d+(?:,\d*)?')
        for index, word in enumerate(list_strings):
            if self.stop_words.__contains__(word):
                pass
            if reg_number.match(word):
                self.number_term(index, list_strings)

    def getConvertedNumber(self, number):
        amounts = ['', 'K', 'M', 'B']
        counter = 0
        devider = 1
        if number > 1000000000000:
            (number) + amounts[counter]
        while number > 999:
            number = number / 1000
            counter += 1
        return str(number) + amounts[counter]

    def number_term(self, index, list_strings):
        reg_num_with_letters = re.compile('([0-9]+[.,]?[0-9]+)([a-zA-Z]+)')
        m = reg_num_with_letters.match(list_strings[index])
        reg_num_with_dollar = re.compile('([0-9]+[.,]?[0-9]+)\$')
        m2 = reg_num_with_dollar.match(list_strings[index])
        # check if percent
        term = ""
        if list_strings[index + 1] == "percent" or list_strings[index + 1] == "percentage":
            term = "{}%".format(list_strings[index])
        # check if money
        elif m != None:
            if m.group(2) == "m" and list_strings[index + 1] == "Dollars":
                term = "{} M Dollars".format(m.group(1))
            elif m.group(2) == "bn" and list_strings[index + 1] == "Dollars":
                term = "{} M Dollars".format(int(float(m.group(1)) * 1000))
        elif reg_num_with_dollar.match(list_strings[index]):
            if list_strings[index + 1] == "million":
                term = "{} M Dollars".format(m2.group(1))
            elif list_strings[index + 1] == "billion":
                term = "{} M Dollars".format(int(float(m2.group(1)) * 1000))
            else:
                if int(float(m2.group(1))) > 1000000:
                    term = "{} M Dollars".format(int(float(m2.group(1))) / 1000000)
                else:
                    term = "{} Dollars".format(m2.group(1))
        elif list_strings[index + 2] == "U.S." and list_strings[index + 3] == "Dollars":
            if list_strings[index + 1] == "million":
                term = "{} M Dollars".format(list_strings[index])
            elif list_strings[index + 1] == "billion":
                term = "{} M Dollars".format(int(list_strings[index]) * 1000)
            elif list_strings[index + 1] == "trillion":
                term = "{} M Dollars".format(int(list_strings[index]) * 1000000)
        elif list_strings[index + 1] == "Dollars":
            num = float(list_strings[index])
            if num >= 1000000:
                term = "{} M Dollars".format(int(list_strings[index]) / 1000000)
            else:
                term = "{} Dollars".format(list_strings[index])
        # check if Date
        elif self.date_dict.has_key(list_strings[index + 1]) or self.date_dict.has_key(list_strings[index - 1]):
            month = ""
            if self.date_dict.has_key(list_strings[index + 1]):
                month = self.date_dict.get(list_strings[index + 1])
            elif self.date_dict.has_key(list_strings[index - 1]):
                month = self.date_dict.get(list_strings[index - 1])
            if int(list_strings[index]) < 32:
                if int(list_strings[index]) < 10:
                    term = "{}-0{}".format(month, list_strings[index])
                else:
                    term = "{}-{}".format(month, list_strings[index])
            else:
                term = "{}-{}".format(list_strings[index], month)
        else:
            if list_strings[index + 1] == "Thousand":
                term = "{}".format(list_strings[index], 'K')
            elif list_strings[index + 1] == "Million":
                term = "{}".format(list_strings[index], 'M')
            elif list_strings[index + 1] == "Billion":
                term = "{}".format(list_strings[index], 'B')
            elif list_strings[index + 1] == "Trillion":
                term = "{}".format(float(list_strings[index]) / 100, 'B')
            else:
                if list_strings[index].__contains__('.'):
                    term = self.getConvertedNumber(float(list_strings[index]))
                else:
                    term = self.getConvertedNumber(int(list_strings[index]))

        # index(term) or self.terms.append(term) ?
        print term


parse = Parse()
parse.main_parser(
    ["6-7", "May", "1994", "14", "MAY", "JUNE", "4", "20.6bn", "Dollars", "32bn", "Dollars", "1000", "Dollars",
     "40.5", "Dollars", "100", "billion", "U.S.", "Dollars", "320", "million", "U.S.", "Dollars", "1000.23", "1",
     "trillion", "U.S.", "Dollars"])
