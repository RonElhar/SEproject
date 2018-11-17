import StringIO
import re
from timeit import default_timer as timer


def get_stop_words():
    stop_words_file = open("stopwords.txt")
    lines = stop_words_file.readlines()
    stop_words = set()
    for word in lines:
        word = word.replace('\n', '')
        stop_words.add(word)
    return stop_words


def get_converted_number(number):
    amounts = ['', 'K', 'M', 'B']
    counter = 0
    if number > 1000000000000:
        return str(number) + amounts[counter]
    while number > 999:
        number = number / 1000
        counter += 1
    after_point = str.split(str(number), '.')[1]
    if after_point == '0':
        number = str(float.__int__(float(number)))
    return str(number) + amounts[counter]


class Parse:

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
        self.num_word = {'Million,Billion,Thousand,Trillion'}
        self.stop_words = get_stop_words()
        self.terms_dict = {}
        self.loc_dict = {}
        self.big_letters_dict = {}
        self.index = 0
        self.get_terms_time = 0
        self.main_parser_time = 0
        self.number_terms_time = 0
        self.unite_dicts_time = 0
        self.range_term_time = 0

    def main_parser(self, text):
        start = timer()
        self.terms_dict = {}
        self.loc_dict = {}
        self.big_letters_dict = {}
        self.index = 0
        list_strings = ["world", "6-7", "1000-2000", "Aviad", "Between", "6000", "and", "7000", "World", "May", "1994", "14",
                   "MAY", "JUNE", "4", "20.6bn", "Dollars", "32bn", "Dollars", "Aviad", "$100", "million", "40.5",
                   "Dollars", "100", "billion", "U.S.", "dollars", "NBA", "320", "million", "U.S.", "dollars", "1",
                   "trillion", "U.S.", "dollars", "Dollars", "NBA", "$100", "billion"]
        reg_number = re.compile(r'\$?[0-9]+')
        reg_word = re.compile(r'[a-zA-Z]')
        while self.index < list_strings.__len__():
            if self.stop_words.__contains__(list_strings[self.index]) or \
                    self.stop_words.__contains__(str.lower(list_strings[self.index])):
                pass
            elif reg_word.match(list_strings[self.index]):
                self.big_letter_term(list_strings[self.index])
            elif self.range_term(self.index, list_strings):
                pass
            elif reg_number.match(list_strings[self.index]):
                self.number_term(self.index, list_strings)
            self.index += 1
        self.add_big_letters_terms()
        end = timer()
        #  self.main_parser_time += float(end - start)
        return self.terms_dict

    def get_terms(self, text):
        start = timer()
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
        end = timer()
        # self.get_terms_time += float(end - start)
        return terms

    def add_to_dict(self, term, index):
        if self.terms_dict.__contains__(term):
            self.loc_dict[term] = index
            self.terms_dict[term] = self.terms_dict[term] + 1
        elif term != '':
            self.terms_dict[term] = 1

    def add_big_letters_terms(self):
        start = timer()
        for term in self.big_letters_dict.keys():
            lower = term.lower()
            upper = term.upper()
            if self.terms_dict.__contains__(lower):
                self.terms_dict[lower] = self.terms_dict[lower] + self.big_letters_dict[term]
            else:
                self.terms_dict[upper] = self.big_letters_dict[term]
        end = timer()
        self.unite_dicts_time += float(end - start)

    def big_letter_term(self, word):
        reg_big_letters = re.compile('([A-Z]+)')
        if reg_big_letters.match(word):
            if self.big_letters_dict.__contains__(word):
                self.big_letters_dict[word] = self.big_letters_dict[word] + 1
            else:
                self.big_letters_dict[word] = 1
        else:
            if self.terms_dict.__contains__(word):
                self.terms_dict[word] = self.terms_dict[word] + 1
            else:
                self.terms_dict[word] = 1

    def range_term(self, index, list_strings):
        start = timer()
        term = ''
        reg_number = re.compile(r'\$?[0-9]+')
        if index + 3 < list_strings.__len__() and list_strings[index] == "Between" and reg_number.match(
                list_strings[index + 1]) and list_strings[index + 2] == "and" and reg_number.match(
            list_strings[index + 3]):
            term = "Between {} and {}".format(self.number_term(0, list_strings[index + 1]), self.number_term(
                0, [list_strings[index + 3]]))
            self.index += 3
        elif str.__contains__(list_strings[index], '-') and reg_number.match(list_strings[index]):
            numbers = str.split(list_strings[index], '-')
            if reg_number.match(numbers[0]) and reg_number.match(numbers[1]):
                term = "{}-{}".format(self.number_term(0, [numbers[0]]), self.number_term(0, [numbers[1]]))
            else:
                term = list_strings[index]
            self.index += 1
        if term is not '':
            self.add_to_dict(term, index)
            end = timer()
            # self.range_term_time += end - start
            return True
        else:
            end = timer()
            # self.range_term_time += float(end - start)
            return False

    def number_term(self, index, list_strings):
        start = timer
        length = len(list_strings)
        reg_letters = re.compile('[a-zA-Z]')
        reg_num_with_letters = re.compile('([0-9]+[.,]?[0-9]+)([a-zA-Z]+)')
        m = reg_num_with_letters.match(list_strings[index])
        reg_num_with_dollar = re.compile('\$([0-9]+[.,]?[0-9]?)')
        m2 = reg_num_with_dollar.match(list_strings[index])
        term = ""
        if index + 1 < length:
            if list_strings[index + 1] == "percent" \
                    or list_strings[index + 1] == "percentage":
                term = "{}%".format(list_strings[index])
                self.index += 1
            elif index + 3 < length and list_strings[index + 2] == "U.S." and list_strings[
                index + 3] == "dollars":
                if list_strings[index + 1] == "million" or list_strings[index + 1] == 'm':
                    term = "{} M Dollars".format(list_strings[index])
                    self.index += 3
                elif list_strings[index + 1] == "billion" or list_strings[index + 1] == 'bn':
                    term = "{} M Dollars".format(int(list_strings[index]) * 1000)
                    self.index += 3
                elif list_strings[index + 1] == "trillion":
                    term = "{} M Dollars".format(int(list_strings[index]) * 1000000)
                    self.index += 3
            elif index + 1 < length and index + 2 < length and list_strings[index + 2] == "Dollars":
                if list_strings[index + 1] == "million" or list_strings[index + 1] == 'm':
                    term = "{} M Dollars".format(list_strings[index])
                    self.index += 3
                elif list_strings[index + 1] == "billion" or list_strings[index + 1] == 'bn':
                    term = "{} M Dollars".format(int(list_strings[index]) * 1000)
                    self.index += 3
                elif list_strings[index + 1] == "trillion":
                    term = "{} M Dollars".format(int(list_strings[index]) * 1000000)
                    self.index += 3
            elif m is None and list_strings[index + 1] == "Dollars":
                if list_strings[index].__contains__("/"):
                    term = "{} Dollars".format(list_strings[index])
                    num = float(list_strings[index])
                    if num >= 1000000:
                        term = "{} M Dollars".format(int(list_strings[index]) / 1000000)
                    else:
                        term = "{} Dollars".format(list_strings[index])
                self.index += 1            # Check if Date
            elif not re.search('[a-zA-Z]', list_strings[index]) and (self.date_dict.has_key(
                    list_strings[index + 1]) or (index - 1 >= 0 and self.date_dict.has_key(list_strings[index - 1]))):
                month = ""
                if self.date_dict.has_key(list_strings[index + 1]):
                    month = self.date_dict.get(list_strings[index + 1])
                    self.index += 1
                elif index - 1 >= 0 and self.date_dict.has_key(list_strings[index - 1]):
                    month = self.date_dict.get(list_strings[index - 1])
                if int(list_strings[index]) < 32:
                    if int(list_strings[index]) < 10:
                        term = "{}-0{}".format(month, list_strings[index])
                    else:
                        term = "{}-{}".format(month, list_strings[index])
                else:
                    term = "{}-{}".format(list_strings[index], month)
            elif self.num_word.__contains__(list_strings[index + 1]):
                term = ''
                if list_strings[index + 1] == "Thousand":
                    term = "{}".format(list_strings[index], 'K')
                elif list_strings[index + 1] == "Million":
                    term = "{}".format(list_strings[index], 'M')
                elif list_strings[index + 1] == "Billion":
                    term = "{}".format(list_strings[index], 'B')
                elif list_strings[index + 1] == "Trillion":
                    term = "{}".format(float(list_strings[index]) / 100, 'B')
            elif m is not None:
                term = ''
                if m.group(2) == "m" and index + 1 < len(list_strings) and list_strings[index + 1] == "Dollars":
                    term = "{} M Dollars".format(m.group(1))
                elif m.group(2) == "bn" and index + 1 < len(list_strings) and list_strings[index + 1] == "Dollars":
                    term = "{} M Dollars".format(int(float(m.group(1)) * 1000))
                self.index += 1
            elif m2 is not None:
                if index + 1 < length and (list_strings[index + 1] == "million" or list_strings[index + 1] == 'm'):
                    term = "{} M Dollars".format(m2.group(1))
                    self.index += 1
                elif index + 1 < length and (list_strings[index + 1] == "billion" or list_strings[index + 1] == 'bn'):
                    term = "{} M Dollars".format(int(float(m2.group(1)) * 1000))
                    self.index += 1
                elif index + 1 < length and list_strings[index + 1] == "trillion":
                    term = "{} M Dollars".format(int(float(m2.group(1)) * 1000000))
                    self.index += 1
                else:
                    if int(float(m2.group(1))) > 1000000:
                        term = "{} M Dollars".format(int(float(m2.group(1))) / 1000000)
                    else:
                        term = "{} Dollars".format(m2.group(1))
            else:
                term = str.replace(list_strings[index], ',', '')
                if not str.__contains__(term, '/') and str.isdigit(term):
                    term = get_converted_number(float(term))
                else:
                    term = ''
        else:
            if m is not None:
                term = ''
                if m.group(2) == "m" and index + 1 < len(list_strings) and list_strings[index + 1] == "Dollars":
                    term = "{} M Dollars".format(m.group(1))
                elif m.group(2) == "bn" and index + 1 < len(list_strings) and list_strings[index + 1] == "Dollars":
                    term = "{} M Dollars".format(int(float(m.group(1)) * 1000))
                self.index += 1
            elif reg_num_with_dollar.match(list_strings[index]):
                if index + 1 < length and (list_strings[index + 1] == "million" or list_strings[index + 1] == 'm'):
                    term = "{} M Dollars".format(m2.group(1))
                    self.index += 1
                elif index + 1 < length and (list_strings[index + 1] == "billion" or list_strings[index + 1] == 'bn'):
                    term = "{} M Dollars".format(int(float(m2.group(1)) * 1000))
                    self.index += 1
                elif index + 1 < length and list_strings[index + 1] == "trillion":
                    term = "{} M Dollars".format(int(float(m2.group(1)) * 1000000))
                    self.index += 1
                else:
                    if int(float(m2.group(1))) > 1000000:
                        term = "{} M Dollars".format(int(float(m2.group(1))) / 1000000)
                    else:
                        term = "{} Dollars".format(m2.group(1))
            else:
                term = str.replace(list_strings[index], ',', '')
                if not str.__contains__(term, '/') and str.isdigit(term):
                    term = get_converted_number(float(term))
                else:
                    term = ''
        if term == '':
            term = list_strings[index]
        self.add_to_dict(term, index)
        end = timer()
        # self.number_terms_time += float(end - start)
        return term

''''
    def number_with_percent(self, index, list_strings):
        term = ''
        term = "{}%".format(list_strings[index])
        self.index += 1
        return term

    def number_with_letter(self, m, index, list_strings):
        term = ''
        if m.group(2) == "m" and index + 1 < len(list_strings) and list_strings[index + 1] == "Dollars":
            term = "{} M Dollars".format(m.group(1))
        elif m.group(2) == "bn" and index + 1 < len(list_strings) and list_strings[index + 1] == "Dollars":
            term = "{} M Dollars".format(int(float(m.group(1)) * 1000))
        self.index += 1
        return term

    def number_with_dollar_sign(self, index, list_strings, length, m2):
        term = ''
        if index + 1 < length and (list_strings[index + 1] == "million" or list_strings[index + 1] == 'm'):
            term = "{} M Dollars".format(m2.group(1))
            self.index += 1
        elif index + 1 < length and (list_strings[index + 1] == "billion" or list_strings[index + 1] == 'bn'):
            term = "{} M Dollars".format(int(float(m2.group(1)) * 1000))
            self.index += 1
        elif index + 1 < length and list_strings[index + 1] == "trillion":
            term = "{} M Dollars".format(int(float(m2.group(1)) * 1000000))
            self.index += 1
        else:
            if int(float(m2.group(1))) > 1000000:
                term = "{} M Dollars".format(int(float(m2.group(1))) / 1000000)
            else:
                term = "{} Dollars".format(m2.group(1))
        return term

    def us_dollars_term(self, index, list_strings):
        term = ''
        if list_strings[index + 1] == "million" or list_strings[index + 1] == 'm':
            term = "{} M Dollars".format(list_strings[index])
            self.index += 3
        elif list_strings[index + 1] == "billion" or list_strings[index + 1] == 'bn':
            term = "{} M Dollars".format(int(list_strings[index]) * 1000)
            self.index += 3
        elif list_strings[index + 1] == "trillion":
            term = "{} M Dollars".format(int(list_strings[index]) * 1000000)
            self.index += 3
        return term

    def dollars_term(self, index, list_strings):
        term = ''
        if list_strings[index].__contains__("/"):
            term = "{} Dollars".format(list_strings[index])
            num = float(list_strings[index])
            if num >= 1000000:
                term = "{} M Dollars".format(int(list_strings[index]) / 1000000)
            else:
                term = "{} Dollars".format(list_strings[index])
        self.index += 1
        return term

    def number_letter_dollar_term(self, index, list_strings):
        term = ''
        if list_strings[index + 1] == "million" or list_strings[index + 1] == 'm':
            term = "{} M Dollars".format(list_strings[index])
            self.index += 3
        elif list_strings[index + 1] == "billion" or list_strings[index + 1] == 'bn':
            term = "{} M Dollars".format(int(list_strings[index]) * 1000)
            self.index += 3
        elif list_strings[index + 1] == "trillion":
            term = "{} M Dollars".format(int(list_strings[index]) * 1000000)
            self.index += 3
        return term

    def date_term(self, index, length, list_strings):
        term = ''
        month = ""
        if self.date_dict.has_key(list_strings[index + 1]):
            month = self.date_dict.get(list_strings[index + 1])
            self.index += 1
        elif index - 1 >= 0 and self.date_dict.has_key(list_strings[index - 1]):
            month = self.date_dict.get(list_strings[index - 1])
        if int(list_strings[index]) < 32:
            if int(list_strings[index]) < 10:
                term = "{}-0{}".format(month, list_strings[index])
            else:
                term = "{}-{}".format(month, list_strings[index])
        else:
            term = "{}-{}".format(list_strings[index], month)
        return term

    def number_with_word(self, index, length, list_strings):
        term = ''
        if list_strings[index + 1] == "Thousand":
            term = "{}".format(list_strings[index], 'K')
        elif list_strings[index + 1] == "Million":
            term = "{}".format(list_strings[index], 'M')
        elif list_strings[index + 1] == "Billion":
            term = "{}".format(list_strings[index], 'B')
        elif list_strings[index + 1] == "Trillion":
            term = "{}".format(float(list_strings[index]) / 100, 'B')
        return term

    def regular_number(self, index, length, list_strings):
        term = ''
        term = str.replace(list_strings[index], ',', '')
        if not str.__contains__(term, '/') and str.isdigit(term):
            term = get_converted_number(float(term))
        else:
            term = ''
        return term
'''

parse = Parse()

print parse.main_parser('')

