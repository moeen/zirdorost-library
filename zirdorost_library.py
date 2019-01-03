import re
import sys


# Fix Function :
# fixes strings
# input : [self] self
# output : [string] fixed string
def fix(string):
    subtitle_fixer = SubtitleFixer()
    return subtitle_fixer.decode_string(string)

class SubtitleFixer:
	def __init__(self):
		self.time = '\d\d:\d\d:\d\d,\d\d\d'
		self.number = u'۰۱۲۳۴۵۶۷۸۹'
	
		self.string = ''

	def fix_encoding(self):
		assert isinstance(self.string, str), repr(self.string)
		#if isinstance(self.string, unicode):
			#return 'utf8'

		try:
			self.string.decode('utf8', 'strict')
			self.string = self.string.decode('utf8')
			return 'utf8'
		except UnicodeError:
			pass

		try:
			self.string.decode('utf16', 'strict')
			self.string = self.string.decode('utf16')
			return 'utf16'
		except UnicodeError:
			pass
	
		self.string = self.string.decode('windows-1256')
		return 'windows-1256'

	def fix_italic(self):
		self.string = self.string.replace('<i>' , '')
		self.string = self.string.replace('</i>', '')

	def fix_arabic(self):
		self.string = self.string.replace(u'ي', u'ی')
		self.string = self.string.replace(u'ك', u'ک')
	
	def fix_question_mark(self):
		# quistion mark in persina is ؟ not ?
		self.string = self.string.replace('?', u'؟')

	def fix_other(self):
		self.string = self.string.replace(u'\u202B', u'')

		lines  = self.string.split('\n')
		string = ''

		for line in lines:
			if re.match('^%s\s-->\s%s$' % (self.time, self.time), line):
				string += line
			elif re.match('^%s\s-->\s%s$' % (self.time, self.time), line[:-1]):
				string += line
			elif line.strip() == '':
				string += line
			elif re.match('^\d+$', line):
				string += line
			elif re.match('^\d+$', line[:-1]):
				string += line
			else:
				# this should be subtitle
				s = re.match('^([\.!?]*)', line)

				try:
					line = re.sub('^%s' % s.group(), '', line)
				except:
					pass

				# use persian numbers
				for i in range(0, 10):
					line = line.replace(str(i), self.number[i])

				# for ltr problems some peoples put '-' on EOL
				# it should be in start
				if len(line) != 0 and line[-1] == '-':
					line = '- %s' % line[:-1]
				line += s.group()

				# put rtl char in start of line (it forces some player to show that line rtl
				string += u'\u202B' + unicode(line)

			# noting to see here
			string += '\n'

			self.string = string


	def decode_string(self, string):
		self.string = string

		self.fix_encoding()

		self.fix_italic()
		self.fix_arabic()
		self.fix_question_mark()
		self.fix_other()

		return self.string
