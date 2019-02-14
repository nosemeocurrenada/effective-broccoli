#!/usr/local/bin/python3

if __name__ != '__main__':
	raise Exception ('This is supposed to be a script')


def replaceFile (filepath, pattern, replacement):
	newtext = getReplacedFileText(filepath, pattern, replacement)
	with open(filepath, 'w') as file:
		file.write(newtext)

def getReplacedFileText (filepath, pattern, replacement):
	inputText = None
	with open(filepath) as file:
		lines = file.readlines()
		inputText = ''.join(lines)

	return replace(pattern, replacement, inputText)

def replace(pattern, replacement, inputText):
	import re
	magicWord = '__$MATCH$__'
	return re.sub(re.escape(pattern), magicWord, inputText).replace(magicWord, replacement)

def fillTemplate(template, filepath):
	name = camelCaseToSnakeCase(getFileName(filepath))
	return template.replace('$CLASSNAME', name)

def getFileName (filepath):
	from os import path
	return path.splitext(path.basename(filepath))[0]

def camelCaseToSnakeCase(name):
	import re
	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
	return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


from optparse import OptionParser
parser = OptionParser()
parser.add_option("-p", "--pattern", dest="pattern",
				help="Search pattern file", metavar="FILE")
parser.add_option("-t", "--template", dest="template",
				help="replacement template")

(options, args) = parser.parse_args()


pattern = None
with open(options.pattern) as file:
	pattern = file.readlines()
pattern = ''.join(pattern)

template = None
with open(options.template) as file:
	template = file.readlines()
template = ''.join(template)


for filepath in args:
	print ('Replacing ' + filepath)
	t = fillTemplate(template, filepath)
	replaceFile (filepath, pattern, t)