import re


ARGUMENT = re.compile(r"(?P<name>\w+): (?P<type>\w+)")
FUNCTION = re.compile(r"^fn ([a-z]\w+)\(")
CLASS = re.compile(r"^type ([A-Z]\w+)\(")
PROPERTY = re.compile(r"(this|self).([A-Z]\w+)\(")

