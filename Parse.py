import StringIO
import re


def get_stop_words():
    stop_words_file = open("C:\\Users\\ronel\\Desktop\\Search Engine\\SEproject\\stopwords.txt")
    lines = stop_words_file.readlines()
    stop_words = []
    for word in lines:
        word = word.replace('\n', '')
        stop_words.append(word)
    return stop_words


def get_converted_number(number):
    amounts = ['', 'K', 'M', 'B']
    counter = 0
    if number > 1000000000000:
        number + amounts[counter]
    while number > 999:
        number = number / 1000
        counter += 1
    after_point = str.split(str(number), '.')[1]
    if after_point == '0':
        number = str(float.__int__(float(number)))
    return str(number) + amounts[counter]


class Parse:
    index = 0
    def __init__(self):
        self.date_dict = {'JANUARY': '01', 'January': '01', 'JAN': '01', 'Jan': '01', 'FEBRUARY': '02',
                          'February': '02', 'FEB': '02', 'Feb': '02', 'MARCH': '03', 'March': '03', 'MAR': '03',
                          'Mar': '03', 'APRIL': '04', 'April': '04', 'APR': '04', 'Apr': '04', 'MAY': '05', 'May': '05',
                          'JUNE': '06', 'June': '06', 'JUN': '06', 'Jun': '06', 'JULY': '07', 'July': '07',
                          'JUL': '07', 'Jul': '07', 'AUGUST': '08', 'August': '08', 'AUG': '08', 'Aug': '08',
                          'SEPTEMBER': '09', 'September': '09', 'SEP': '09', 'Sep': '09', 'OCTOBER': '10',
                          'October': '10', 'OCT': '10', 'Oct': '10', 'NOVEMBER': '11', 'November': '11', 'NOV': '11',
                          'Nov': '11', 'DECEMBER': '12', 'December': '12', 'DEC': '12', 'Dec': '12'}
        self.num_dict = {'Million': 1000000, 'million': 1000000, 'm': 1000000, 'Thousand': 1000}
        self.stop_words = get_stop_words()
        self.doc_dict = {}
        self.big_letters_dict = {}

    def main_parser(self, text):
        list_strings = self.get_terms(text)
        reg_number = re.compile(r'\$?[0-9]+')
        while Parse.index < list_strings.__len__():
            if self.range_term(Parse.index, list_strings):
                pass
            elif self.stop_words.__contains__(list_strings[Parse.index]):
                pass
            elif reg_number.match(list_strings[Parse.index]):
                self.number_term(Parse.index, list_strings)
            else:
                self.big_letter_term(list_strings[Parse.index])
            Parse.index += 1

        self.add_big_letters_terms()
        print self.doc_dict

    def get_terms(self, text):
        terms = str.split(text, " ")
        terms = filter(None, terms)
        tCount = 0
        for term in terms:
            terms[tCount] = re.sub('[^A-Za-z0-9\-$%/.]+', '', term)
            if not re.match("^\d+?\.\d+?$", terms[tCount]) and not re.match(r'^\d+/\d+$', terms[tCount]):
                terms[tCount] = re.sub('[^A-Za-z0-9\-$%]+', '', terms[tCount])
            if re.match(r'^\d+\d+$', terms[tCount]) and tCount + 1 < terms.__len__() and re.match(r'^\d+/\d+$',
                                                                                                  terms[tCount + 1]):
                terms[tCount] += ' ' + terms[tCount + 1]
                terms[tCount + 1] = ''
            if term.__contains__('-') and not re.search('[a-zA-Z]', term) and not re.search('[0-9]', term):
                terms.__delitem__(tCount)
            elif term.__contains__('-'):
                words = str.split(term, '-')
                if words[words.__len__() - 1] == '':
                    terms[tCount] = terms[tCount].replace('-', '')
            terms[tCount] = terms[tCount].replace('\n', '')
            tCount += 1
        terms = filter(None, terms)
        return terms

    def add_big_letters_terms(self):
        for term in self.big_letters_dict.keys():
            lower = term.lower()
            upper = term.upper()
            if self.doc_dict.__contains__(lower):
                self.doc_dict[lower] = self.doc_dict[lower] + self.big_letters_dict[term]
            else:
                self.doc_dict[upper] = self.big_letters_dict[term]

    def big_letter_term(self, word):
        reg_big_letters = re.compile('([A-Z]+)')
        if reg_big_letters.match(word):
            if self.big_letters_dict.__contains__(word):
                self.big_letters_dict[word] = self.big_letters_dict[word] + 1
            else:
                self.big_letters_dict[word] = 1
        else:
            if self.doc_dict.__contains__(word):
                self.doc_dict[word] = self.doc_dict[word] + 1
            else:
                self.doc_dict[word] = 1

    def range_term(self, index, list_strings):
        term = ''
        reg_number = re.compile(r'\$?[0-9]+')
        if index + 3 < list_strings.__len__() and list_strings[index] == "Between" and reg_number.match(
                list_strings[index + 1]) and list_strings[index + 2] == "and" and reg_number.match(
                list_strings[index + 3]):
            term = "Between {} and {}".format(self.number_term(index + 1, list_strings), self.number_term(
                0, [list_strings[index + 3], ""]))
        elif str.__contains__(list_strings[index], '-') and reg_number.match(list_strings[index]):
            numbers = str.split(list_strings[index], '-')
            if reg_number.match(numbers[0]) and reg_number.match(numbers[1]):
                term = "{}-{}".format(self.number_term(0, [numbers[0], ""]), self.number_term(0, [numbers[1], ""]))
            else:
                term = list_strings[index]
        if term is not '':
            if self.doc_dict.__contains__(term):
                self.doc_dict[term] = self.doc_dict[term] + 1
            else:
                self.doc_dict[term] = 1
            return True
        else:
            return False

    def number_term(self, index, list_strings):
        length = len(list_strings)
        reg_letters = re.compile('[a-z]+')
        reg_num_with_letters = re.compile('([0-9]+[.,]?[0-9]+)([a-zA-Z]+)')
        m = reg_num_with_letters.match(list_strings[index])
        reg_num_with_dollar = re.compile('\$([0-9]+[.,]?[0-9]+)')
        m2 = reg_num_with_dollar.match(list_strings[index])
        # Check if percent
        term = ""
        if index + 1 < length and list_strings[index + 1] == "percent"\
                or list_strings[index + 1] == "percentage":
            term = "{}%".format(list_strings[index])
            Parse.index += 1
        # Check if money
        elif m is not None:
            # 100bn or 100m cases
            if m.group(2) == "m" and index + 1 < length and list_strings[index + 1] == "Dollars":
                term = "{} M Dollars".format(m.group(1))
            elif m.group(2) == "bn" and index + 1 < length and list_strings[index + 1] == "Dollars":
                term = "{} M Dollars".format(int(float(m.group(1)) * 1000))
            Parse.index += 1
        # $100 cases
        elif reg_num_with_dollar.match(list_strings[index]):
            if index + 1 < length and list_strings[index + 1] == "million":
                term = "{} M Dollars".format(m2.group(1))
                Parse.index += 1
            elif index + 1 < length and list_strings[index + 1] == "billion":
                term = "{} M Dollars".format(int(float(m2.group(1)) * 1000))
                Parse.index += 1
            elif index + 1 < length and list_strings[index + 1] == "trillion":
                term = "{} M Dollars".format(int(float(m2.group(1)) * 1000000))
                Parse.index += 1
            else:
                if int(float(m2.group(1))) > 1000000:
                    term = "{} M Dollars".format(int(float(m2.group(1))) / 1000000)
                else:
                    term = "{} Dollars".format(m2.group(1))
        elif index + 3 < length and list_strings[index + 2] == "U.S." and list_strings[index + 3] == "dollars":
            print list_strings[index]
            if list_strings[index + 1] == "million":
                term = "{} M Dollars".format(list_strings[index])
            elif list_strings[index + 1] == "billion":
                term = "{} M Dollars".format(int(list_strings[index]) * 1000)
            elif list_strings[index + 1] == "trillion":
                term = "{} M Dollars".format(int(list_strings[index]) * 1000000)
            Parse.index += 3
        elif index + 1 < length and list_strings[index + 1] == "Dollars":
            if list_strings[index].__contains__("/"):
                term = "{} Dollars".format(list_strings[index])
            else:
                num = float(list_strings[index])
                if num >= 1000000:
                    term = "{} M Dollars".format(int(list_strings[index]) / 1000000)
                else:
                    term = "{} Dollars".format(list_strings[index])
            list_strings.__delitem__(index + 1)
        # Check if Date
        elif index + 1 < length and self.date_dict.has_key(list_strings[index + 1]) or index - 1 >= 0 and self.date_dict.has_key(list_strings[index - 1]):
            month = ""
            if index + 1 < length and self.date_dict.has_key(list_strings[index + 1]):
                month = self.date_dict.get(list_strings[index + 1])
                Parse.index += 1
            elif index - 1 >= 0 and self.date_dict.has_key(list_strings[index - 1]):
                month = self.date_dict.get(list_strings[index - 1])
            if int(list_strings[index]) < 32:
                if int(list_strings[index]) < 10:
                    term = "{}-0{}".format(month, list_strings[index])
                else:
                    term = "{}-{}".format(month, list_strings[index])
            else:
                term = "{}-{}".format(list_strings[index], month)
        else:
            if index + 1 < length and list_strings[index + 1] == "Thousand":
                term = "{}".format(list_strings[index], 'K')
                Parse.index += 1
            elif index + 1 < length and list_strings[index + 1] == "Million":
                term = "{}".format(list_strings[index], 'M')
                Parse.index += 1
            elif index + 1 < length and list_strings[index + 1] == "Billion":
                term = "{}".format(list_strings[index], 'B')
                Parse.index += 1
            elif index + 1 < length and list_strings[index + 1] == "Trillion":
                term = "{}".format(float(list_strings[index]) / 100, 'B')
                Parse.index += 1
            elif not str.__contains__(list_strings[index], '/') and not re.search('[a-zA-Z]', list_strings[index]):
                term = get_converted_number(float(list_strings[index]))
            else:
                term = str(list_strings[index])
        if self.doc_dict.__contains__(term):
            self.doc_dict[term] = self.doc_dict[term] + 1
        else:
            self.doc_dict[term] = 1
        return term

##################important: to check that we are not missing words because of "range_term!!!!!!
# choose = nltk.choose(12, 6)