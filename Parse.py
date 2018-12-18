from timeit import default_timer as timer
import string
import Stemmer
import re
import heapq

"""
~~~~~~~~~~~~~~~~~~~~~~~~  Module Description ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This Module Contains Parse class , its part is to parse texts given from corpus

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

"""
      Description : getting stop words list from stopwords.txt
"""


def get_stop_words(main_path):
    stop_words_file = open(main_path + "\\stopwords.txt")
    lines = stop_words_file.readlines()
    stop_words = set()
    for word in lines:
        word = word.replace('\n', '')
        stop_words.add(word)
    stop_words.add('TYPEBFN')
    return stop_words


"""
      Description : checking if token is float
"""


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


"""
      Description : checking if token is a fraction
"""


def isFraction(token):
    if token.find("/") == -1:
        return False

    nums = token.split("/")
    if not len(nums) == 2:
        return False
    if isFloat(nums[0]) and isFloat(nums[1]):
        return True

    return False


"""
      Description : checking if token is a word
"""


def isWord(token):
    for c in token:
        if not str.isalpha(c):
            return False
    return True


"""
      Description : checking if token is a number term
"""


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
    """
       Class Description :
           This Class is used for tokenizing text of a doc and saving the occurrences and its location of the tokens
    """
    """
       Description :
           initialize properties of Parse object
    """

    def __init__(self, main_path):
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
        self.stop_words = get_stop_words(main_path)
        self.terms_dict = {}
        self.parsed_doc = object
        self.tokens_list = ''
        self.index = 0
        self.to_stem = False
        self.pystemmer = Stemmer.Stemmer('english')
        self.entities = []

    """
       Description :
           set stem bool of the clas
    """

    def set_stemming_bool(self, to_stem):
        self.to_stem = to_stem

    """
       Description :
           This method gets a text of a doc, tokenizing it, perform parse rules on the tokens list
           and saves details about the terms in the specific doc, 
       Args:
           param1: text
        Return:
            Dictionary of occurrences and its location of the terms 
    """

    def main_parser(self, text):
        self.entities = []
        self.terms_dict = {}
        self.index = 0
        self.tokens_list = self.get_terms(text)
        reg_number = re.compile(r'\$?\d+\.?\d*$')
        document_length = 0
        while self.index < len(self.tokens_list):
            token = self.tokens_list[self.index]
            if token in self.stop_words or token == '' or token == None or token.lower() in self.stop_words:
                document_length -= 1
            elif isWord(token) and not token == 'Between':
                self.word_term(token)
            elif reg_number.match(token):
                self.number_term(token)
            elif token.__contains__('-'):
                if isWord(token.replace('-', '')):
                    tokens = token.split('-')
                    for t in tokens:
                        if not t == '':
                            if isWord(t):
                                self.word_term(t)
                if token.istitle():
                    self.add_to_dict(token.upper(), self.index)
                else:
                    self.add_to_dict(token.lower(), self.index)
            elif str.__contains__(token, '/'):
                if re.match(r'\$?[0-9]* ?[0-9]+/[0-9]+$', token):
                    if self.index + 1 < len(self.tokens_list) and (
                                    self.tokens_list[self.index + 1] == "Dollars" or token.startswith('$')):
                        self.add_to_dict('{} Dollars'.format(token.replace('$', '')), self.index)
                        self.index += 1
                    else:
                        self.add_to_dict(token, self.index)
                elif not token.__contains__('<'):
                    self.add_to_dict(token, self.index)
            elif self.index + 3 < len(self.tokens_list) and token == "Between" and reg_number.match(
                    self.tokens_list[self.index + 1]) and self.tokens_list[
                        self.index + 2] == "and" and reg_number.match(self.tokens_list[self.index + 3]):
                token = "between {} and {}".format(self.tokens_list[self.index + 1],
                                                   self.tokens_list[self.index + 3])
                self.add_to_dict(token, self.index)
                self.index += 3
            elif len(token) > 1 and not (token.__contains__('<') or token.__contains__('>')):
                self.add_to_dict(token, self.index)
            self.index += 1
            document_length += 1
        self.tokens_list = ''
        if not self.parsed_doc is None:
            self.parsed_doc.length = document_length
            self.parsed_doc.num_of_unique_words = len(self.terms_dict)
            self.add_to_entities()
            five_entities = heapq.nlargest(5,self.entities)
            for entity in five_entities:
                self.parsed_doc.five_entities.append(entity[1])
        return self.terms_dict

    """
       Description :
           This method gets a text of a doc, tokenizing it, and cleaning it
           from irrelevant delimiters and chars 
       Args:
           param1: text
        Return:
            list of "cleaned" tokens
    """

    def get_terms(self, text):
        SEPS = (' ', '--')
        allowed = "{}{}-$%/.<>".format(string.ascii_letters, string.digits)
        start = timer()
        rsplit = re.compile("|".join(SEPS)).split
        tokens = [s.strip() for s in rsplit(text)]
        # terms = str.split(text, " ")
        for i in range(0, len(tokens)):
            tokens[i] = filter(allowed.__contains__, tokens[i])
            if isFloat(tokens[i]):
                if i + 1 < len(tokens) and isFraction(tokens[i + 1]):
                    tokens[i] = "{} {}".format(tokens[i], tokens[i + 1])
                    tokens[i + 1] = ''
            else:
                tokens[i] = tokens[i].replace('.', '')
            if tokens[i].startswith("-"):
                tokens[i] = tokens[i][1:]
            if tokens[i].endswith("-"):
                tokens[i] = tokens[i][:-1]
        end = timer()
        # self.get_terms_time += float(end - start)
        return tokens

    """
       Description :
           This method adds a term to the terms dictionary and updating its 
           occurrences and location in the dictionary
       Args:
           param1: token
    """

    def add_to_dict(self, term, index):
        if term in self.terms_dict:
            self.terms_dict[term][0] += 1
            self.terms_dict[term][1].append(index)
        else:
            self.terms_dict[term] = []
            self.terms_dict[term].append(1)
            self.terms_dict[term].append([index])

        if not self.parsed_doc is None and self.terms_dict[term][0] > self.parsed_doc.max_tf:
            self.parsed_doc.max_tf = self.terms_dict[term][0]

    def add_to_entities(self):
        for term in self.terms_dict:
            if term.isupper():
                tf = self.terms_dict[term][0]
                dominance = float(tf) / float(self.parsed_doc.length)
                if term in self.parsed_doc.title :
                    dominance = dominance*1.3
                if self.terms_dict[term][1][0] < self.parsed_doc.length/10:
                    dominance = dominance*1.1
                heapq.heappush(self.entities, (dominance, term))

    """
           Description :
               This method takes care of the word terms
               and the "Big letters - Small letters" rule and adding 
               those to the terms dictionary
           Args:
               param1: word term
    """

    def word_term(self, word):
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

    """
            Description :
                This method takes care of the number terms rules
                and adding those to the terms dictionary
            Args:
                param1: number term
     """

    def number_term(self, num_word):
        def dollar_addons():
            if self.index + 3 < terms_len:
                return ' {} {} {}'.format(self.tokens_list[self.index + 1], self.tokens_list[self.index + 2],
                                          self.tokens_list[self.index + 3])
            if self.index + 2 < terms_len:
                return ' {} {}'.format(self.tokens_list[self.index + 1], self.tokens_list[self.index + 2])
            if self.index + 1 < terms_len:
                return ' {}'.format(self.tokens_list[self.index + 1])
            return ''

        orig_idx = self.index
        terms_len = len(self.tokens_list)
        dollars_regex = re.compile("^\$?(\d+\.?\d*) ?(million|billion|trillion|m|bn)? ?(U\.S\.)? ?([Dd]ollars)?")
        dollar_expression = dollars_regex.match(num_word + dollar_addons())
        term = ''
        if self.index + 1 < terms_len and (self.tokens_list[self.index + 1] == "percent"
                                           or self.tokens_list[self.index + 1] == "percentage"):
            term = "{}%".format(num_word)
            self.index += 1
        elif self.index + 1 < terms_len and self.tokens_list[self.index + 1] == "kgs":
            term = "{} Kilograms".format(num_word)
            self.index += 1
        elif self.index + 1 < terms_len and self.tokens_list[self.index + 1] == "GMT" and self.tokens_list[
            self.index] and len(self.tokens_list[self.index]) is 4:
            term = "{}{}:{}{}".format(self.tokens_list[self.index][0], self.tokens_list[self.index][1],
                                      self.tokens_list[self.index][2], self.tokens_list[self.index][3])
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
        elif self.index + 1 < terms_len and self.tokens_list[self.index + 1] in self.date_dict:
            month = self.date_dict.get(self.tokens_list[self.index + 1])
            self.index += 1
            num_word = num_word.replace('.', '')
            term = "{}-{}".format(month.zfill(2), num_word.zfill(2))
        elif self.index - 1 >= 0 and self.tokens_list[self.index - 1] in self.date_dict:
            month = self.date_dict.get(self.tokens_list[self.index - 1])
            num_word = num_word.replace('.', '')
            term = ("{}-{}".format(month.zfill(2), num_word.zfill(2))) if int(num_word) < 32 else \
                ("{}-{}".format(num_word.zfill(2), month.zfill(2)))
        elif self.index + 1 < terms_len and self.tokens_list[self.index + 1].lower() in self.num_word_dict:
            if self.tokens_list[self.index + 1] == "Trillion":
                term = "{}".format(float(num_word) * 100, 'B')
            else:
                term = "{}".format(num_word, self.num_word_dict[self.tokens_list[self.index + 1].lower()])
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
