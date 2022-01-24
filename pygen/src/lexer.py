import src.gen_token as tk
import string
from src.error import InvalidSyntaxError, TypeCharError
from src.position import Position

# for checking if a character is a digit or not
DIGITS = "0123456789"
LETTERS = string.ascii_letters
LETTERS_AND_DIGITS = DIGITS + LETTERS

class Lexer:
	def __init__(self, filename, text):
		self.filename = filename
		self.text = text
		self.position = Position(-1, 0, -1, self.filename, self.text)
		self.current_char = None
		self.advance()
	
	def advance(self):
		self.position.advance(self.current_char)
		self.current_char = self.text[self.position.index] if self.position.index < len(self.text) else None
	
	def make_tokens(self):
		tokens = []

		while self.current_char is not None:
			if self.current_char in " \t": # ignore tabs and spaces
				self.advance()
			elif self.current_char in DIGITS:
				tokens.append(self.make_number())
			elif self.current_char == "#": # comment
				self.skip_comment()
			elif self.current_char == "\"": # string
				tokens.append(self.make_string()) # check for new line or ;
			elif self.current_char in ";\n":
				tokens.append(tk.Token(tk.TT_NL, pos_start=self.position))
				self.advance()
			elif self.current_char == "+":
				tokens.append(tk.Token(tk.TT_PLUS, pos_start=self.position))
				self.advance()
			elif self.current_char == "-":
				tokens.append(self.make_minus_or_arrow())
			elif self.current_char == "*":
				tokens.append(tk.Token(tk.TT_MULT, pos_start=self.position))
				self.advance()
			elif self.current_char == "/":
				tokens.append(tk.Token(tk.TT_DIV, pos_start=self.position))
				self.advance()
			elif self.current_char == "^":
				tokens.append(tk.Token(tk.TT_POWER, pos_start=self.position))
				self.advance()
			elif self.current_char == "%":
				tokens.append(tk.Token(tk.TT_MODULO, pos_start=self.position))
				self.advance()
			elif self.current_char == "(":
				tokens.append(tk.Token(tk.TT_L_PAREN, pos_start=self.position))
				self.advance()
			elif self.current_char == ")":
				tokens.append(tk.Token(tk.TT_R_PAREN, pos_start=self.position))
				self.advance()
			elif self.current_char == "[":
				tokens.append(tk.Token(tk.TT_L_SQ, pos_start=self.position))
				self.advance()
			elif self.current_char == "]":
				tokens.append(tk.Token(tk.TT_R_SQ, pos_start=self.position))
				self.advance()
			elif self.current_char == "{":
				tokens.append(tk.Token(tk.TT_L_BRACE, pos_start=self.position))
				self.advance()
			elif self.current_char == "}":
				tokens.append(tk.Token(tk.TT_R_BRACE, pos_start=self.position))
				self.advance()
			elif self.current_char == ":":
				tokens.append(tk.Token(tk.TT_MAP_COLON, pos_start=self.position))
				self.advance()
			elif self.current_char == ",":
				tokens.append(tk.Token(tk.TT_COMMA, pos_start=self.position))
				self.advance()
			elif self.current_char == "@":
				tokens.append(tk.Token(tk.TT_AT, pos_start=self.position))
				self.advance()
			elif self.current_char == "!":
				token, error = self.make_not_equals()
				if error: return [], error
				tokens.append(token)
			elif self.current_char == "=":
				tokens.append(self.make_equals())
			elif self.current_char == "<":
				tokens.append(self.make_less_than())
			elif self.current_char == ">":
				tokens.append(self.make_greater_than())
			elif self.current_char in LETTERS:
				tokens.append(self.make_identifier())
			else:
				# return TypeCharError
				pos_start = self.position.copy()
				char = self.current_char
				self.advance()
				return [], TypeCharError(pos_start, self.position, f"'{char}'")
		tokens.append(tk.Token(tk.TT_EOF, pos_start=self.position))
		return tokens, None
	
	def make_number(self):
		number_str = ""
		dot = False
		pos_start = self.position.copy()
		while self.current_char is not None and self.current_char in DIGITS + ".":
			if self.current_char == ".":
				if dot is True: break
				dot = True
				number_str += self.current_char
			else:
				number_str += self.current_char
			self.advance()
		
		return tk.Token(tk.TT_INT, int(number_str), pos_start, self.position) if dot is False else tk.Token(tk.TT_FLOAT, float(number_str), pos_start, self.position)

	def make_string(self):
		pos_start = self.position.copy()
		escape_character = False
		string_to_return = ""
		self.advance()
		while self.current_char != None and (self.current_char != "\"" or escape_character is not False):
			if escape_character is True:
				if self.current_char == "n": # new line
					string_to_return += "\n"
				elif self.current_char == "t": # tab
					string_to_return += "\t"
				else:
					string_to_return += self.current_char
			if self.current_char == "\\":
				escape_character = True
			else:
				string_to_return += self.current_char
			self.advance()
			escape_character = False
		self.advance()
		return tk.Token(tk.TT_STRING, string_to_return, pos_start, self.position)
	
	def make_identifier(self):
		string = ""
		pos_start = self.position.copy()
		while self.current_char is not None and self.current_char in LETTERS_AND_DIGITS+"_":
			string += self.current_char
			self.advance()
		token_type = tk.TT_KEYWORD if string in tk.KEYWORDS else tk.TT_IDENTIFIER
		return tk.Token(token_type, string, pos_start, self.position)
	
	def make_minus_or_arrow(self):
		token_type = tk.TT_MINUS
		pos_start = self.position.copy()
		self.advance()
		if self.current_char == ">":
			token_type = tk.TT_ARROW
			self.advance()
		return tk.Token(token_type, pos_start=pos_start, pos_end=self.position)

	
	def make_not_equals(self):
		pos_start = self.position.copy()
		self.advance()
		if self.current_char == "=":
			self.advance()
			return tk.Token(tk.TT_NEQUALS, pos_start=pos_start, pos_end=self.position), None
		else:
			self.advance()
			return None, InvalidSyntaxError(
				pos_start, self.position, "Expected '=' after '!'"
			)
	
	def make_equals(self):
		pos_start = self.position.copy()
		token_type = tk.TT_EQUALS
		self.advance()
		if self.current_char == "=":
			self.advance()
			token_type = tk.TT_DEQUALS
		return tk.Token(token_type, pos_start=pos_start, pos_end=self.position)
	
	def make_less_than(self):
		pos_start = self.position.copy()
		token_type = tk.TT_LTHAN
		self.advance()
		if self.current_char == "=":
			self.advance()
			token_type = tk.TT_LTEQUALS
		return tk.Token(token_type, pos_start=pos_start, pos_end=self.position)
	
	def make_greater_than(self):
		pos_start = self.position.copy()
		token_type = tk.TT_GTHAN
		self.advance()
		if self.current_char == "=":
			self.advance()
			token_type = tk.TT_GTEQUALS
		return tk.Token(token_type, pos_start=pos_start, pos_end=self.position)
	
	def skip_comment(self): # for commenting
		self.advance()
		while self.current_char != "\n" and self.current_char is not None:
			self.advance()
		self.advance()

		
