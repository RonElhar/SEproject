from timeit import default_timer as timer
import string
import Stemmer
import re


def get_stop_words():
    stop_words_file = open("stopwords.txt")
    lines = stop_words_file.readlines()
    stop_words = set()
    for word in lines:
        word = word.replace('\n', '')
        stop_words.add(word)
    return stop_words


# def isFloat(token):
#     try:
#         float(token)
#         return True
#     except ValueError:
#         return False


def isFloat(token):
    i = 0
    decimal_point = False
    digit_exists = False
    while i < len(token):
        if not str.isdigit(token[i]) and not token[i] == '.':
            return False
        elif token[i] == '.':
            if decimal_point:
                return False
            decimal_point = True
        else:
            digit_exists = True
        i += 1
    if not digit_exists:
        return False
    return True


def isFraction(token):
    if token.find("/") == -1:
        return False

    nums = token.split("/")
    if not len(nums) == 2:
        return False
    if isFloat(nums[0]) and isFloat(nums[1]):
        return True

    return False


def isWord(token):
    for c in token:
        if not str.isalpha(c):
            return False
    return True


def isNumTerm(token):
    i = 0
    decimal_bool = False
    digit_exists = False
    while i < len(token):
        if not str.isdigit(token[i]):
            if i == 0 and token[i] == '$':
                i += 1
                continue
            if token[i] == '.' and decimal_bool:
                return False
            elif token[i] == '.':
                decimal_bool = True
            else:
                return False
        else:
            digit_exists = True
        i += 1
    if not digit_exists:
        return False
    return True


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
        self.num_dict = {'million': 1, 'm': 1, 'billion': 1000, 'bn': 1000, 'trillion': 1000000}
        self.num_word_dict = {'million': 'M', 'billion': 'B', 'thousand': 'K', 'trillion': '', "bn": 'B', "m": "M"}
        self.stop_words = get_stop_words()
        self.terms_dict = {}
        self.parsed_doc = object
        self.index = 0
        self.to_stem = False
        self.pystemmer = Stemmer.Stemmer('english')
        '''''
        self.get_terms_time = 0
        self.main_parser_time = 0
        self.number_terms_time = 0
        self.unite_dicts_time = 0
        self.range_term_time = 0
        '''''

    def set_stemming_bool(self, to_stem):
        self.to_stem = to_stem

    def main_parser(self, text):
        self.terms_dict = {}
        self.index = 0
        self.list_strings = self.get_terms(text)
        reg_number = re.compile(r'\$?\d+\.?\d*$')
        document_length = 0
        while self.index < len(self.list_strings):
            token = self.list_strings[self.index]
            if token in self.stop_words or token == '' or token == None or token.lower() in self.stop_words:
                document_length -= 1
            elif isWord(token) and not token == 'Between':
                self.add_word_term(token)
            elif reg_number.match(token):
                self.number_term(token)
            elif token.__contains__('-'):
                if isWord(token.replace('-','')):
                    tokens = token.split('-')
                    for t in tokens:
                        if not t == '':
                            if isWord(t):
                                self.add_word_term(t)
                if token.istitle():
                    self.add_to_dict(token.upper(), self.index)
                else:
                    self.add_to_dict(token.lower(), self.index)
            elif str.__contains__(token, '/'):
                if re.match(r'\$?[0-9]* ?[0-9]+/[0-9]+$', token):
                    if self.index + 1 < len(self.list_strings) and (
                                    self.list_strings[self.index + 1] == "Dollars" or token.startswith('$')):
                        self.add_to_dict('{} Dollars'.format(token.replace('$', '')), self.index)
                        self.index += 1
                    else:
                        self.add_to_dict(token, self.index)
                elif not token.__contains__('<'):
                    self.add_to_dict(token, self.index)
            elif self.index + 3 < len(self.list_strings) and token == "Between" and reg_number.match(
                    self.list_strings[self.index + 1]) and self.list_strings[
                        self.index + 2] == "and" and reg_number.match(self.list_strings[self.index + 3]):
                token = "between {} and {}".format(self.list_strings[self.index + 1],
                                                   self.list_strings[self.index + 3])
                self.add_to_dict(token, self.index)
                self.index += 3
            elif len(token) > 1 and not (token.__contains__('<') or token.__contains__('>')):
                self.add_to_dict(token, self.index)
            self.index += 1
            document_length += 1
        self.list_strings = ''
        self.parsed_doc.length = document_length
        self.parsed_doc.num_of_unique_words = len(self.terms_dict)
        return self.terms_dict

    def get_terms(self, text):
        SEPS = (' ', '--')
        allowed = "{}{}-$%/.<>".format(string.ascii_letters, string.digits)
        start = timer()
        rsplit = re.compile("|".join(SEPS)).split
        terms = [s.strip() for s in rsplit(text)]
        # terms = str.split(text, " ")
        for i in range(0, len(terms)):
            terms[i] = filter(allowed.__contains__, terms[i])
            if isFloat(terms[i]):
                if i + 1 < len(terms) and isFraction(terms[i + 1]):
                    terms[i] = "{} {}".format(terms[i], terms[i + 1])
                    terms[i + 1] = ''
            else:
                terms[i] = terms[i].replace('.', '')
            if terms[i].startswith("-"):
                terms[i] = terms[i][1:]
            if terms[i].endswith("-"):
                terms[i] = terms[i][:-1]
        end = timer()
        # self.get_terms_time += float(end - start)
        return terms

    def add_to_dict(self, term, index):

        if term in self.terms_dict:
            self.terms_dict[term][0] += 1
            self.terms_dict[term][1].append(index)
        else:
            self.terms_dict[term] = []
            self.terms_dict[term].append(1)
            self.terms_dict[term].append([index])
        if self.terms_dict[term][0] > self.parsed_doc.max_tf:
            self.parsed_doc.max_tf = self.terms_dict[term][0]

    def add_word_term(self, word):
        if self.to_stem:
            word = str(self.pystemmer.stemWord(word))
        lower = word.lower()
        upper = word.upper()
        if word[0].isupper():
            if lower in self.terms_dict:
                self.add_to_dict(lower, self.index)
            else:
                self.add_to_dict(upper, self.index)
        else:
            if upper in self.terms_dict:
                self.terms_dict[lower] = self.terms_dict.pop(upper)
                self.add_to_dict(lower, self.index)
            else:
                self.add_to_dict(lower, self.index)

    def number_term(self, num_word):
        def dollar_addons():
            if self.index + 3 < terms_len:
                return ' {} {} {}'.format(self.list_strings[self.index + 1], self.list_strings[self.index + 2],
                                          self.list_strings[self.index + 3])
            if self.index + 2 < terms_len:
                return ' {} {}'.format(self.list_strings[self.index + 1], self.list_strings[self.index + 2])
            if self.index + 1 < terms_len:
                return ' {}'.format(self.list_strings[self.index + 1])
            return ''

        orig_idx = self.index
        terms_len = len(self.list_strings)
        dollars_regex = re.compile("^\$?(\d+\.?\d*) ?(million|billion|trillion|m|bn)? ?(U\.S\.)? ?([Dd]ollars)?")
        dollar_expression = dollars_regex.match(num_word + dollar_addons())
        term = ''
        if self.index + 1 < terms_len and (self.list_strings[self.index + 1] == "percent"
                                           or self.list_strings[self.index + 1] == "percentage"):
            term = "{}%".format(num_word)
            self.index += 1
        elif self.index + 1 < terms_len and self.list_strings[self.index + 1] == "kgs":
            term = "{} Kilograms".format(num_word)
            self.index += 1
        elif self.index + 1 < terms_len and self.list_strings[self.index + 1] == "GMT" and self.list_strings[
            self.index] and len(self.list_strings[self.index]) is 4:
            term = "{}{}:{}{}".format(self.list_strings[self.index][0], self.list_strings[self.index][1],
                                      self.list_strings[self.index][2], self.list_strings[self.index][3])
        elif dollar_expression and (str.startswith(num_word, '$') or dollar_expression.group(4)):
            num = float(dollar_expression.group(1))
            if dollar_expression.group(2):
                num *= self.num_dict[str.lower(dollar_expression.group(2))]
                term = "{:.3f} M Dollars".format(num).replace('.000', '')
            elif num >= 1000000:
                num = num / 1000000.0
                term = "{:.3f} M Dollars".format(num).replace('.000', '')
            else:
                term = "{:.3f} Dollars".format(num).replace('.000', '')
            self.index += (1 if dollar_expression.group(4) else 0) + (1 if dollar_expression.group(3) else 0) + \
                          (1 if dollar_expression.group(2) else 0)
        elif self.index + 1 < terms_len and self.list_strings[self.index + 1] in self.date_dict:
            month = self.date_dict.get(self.list_strings[self.index + 1])
            self.index += 1
            num_word = num_word.replace('.', '')
            term = "{}-{}".format(month.zfill(2), num_word.zfill(2))
        elif self.index - 1 >= 0 and self.list_strings[self.index - 1] in self.date_dict:
            month = self.date_dict.get(self.list_strings[self.index - 1])
            num_word = num_word.replace('.', '')
            term = ("{}-{}".format(month.zfill(2), num_word.zfill(2))) if int(num_word) < 32 else \
                ("{}-{}".format(num_word.zfill(2), month.zfill(2)))
        elif self.index + 1 < terms_len and self.list_strings[self.index + 1].lower() in self.num_word_dict:
            if self.list_strings[self.index + 1] == "Trillion":
                term = "{}".format(float(num_word) * 100, 'B')
            else:
                term = "{}".format(num_word, self.num_word_dict[self.list_strings[self.index + 1].lower()])
            self.index += 1
        else:
            amounts = ['', 'K', 'M', 'B']
            counter = 0
            number = float(num_word)
            if number > 1000000000000:
                return num_word + amounts[counter]
            while number > 999:
                number = number / 1000.0
                counter += 1
            term = "{:.3f}{}".format(number, amounts[counter]).replace(".000", "")
        self.add_to_dict(term, orig_idx)
