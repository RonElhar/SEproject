from ReadFile import ReadFile
from Parse import Parse

reader = ReadFile()
terms = reader.getTerms(reader.get_text())
parser = Parse()
parser.main_parser(terms)
