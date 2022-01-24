from src.lexer import Lexer
from src.parser import Parser
from src.value import *
from src.evaluator import RuntimeResult, RuntimeError

class BuiltinFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)
	
	def execute(self, args):
		res = RuntimeResult()
		context = self.generate_new_context()
		method = getattr(self, f"execute_{self.name}", self.no_visit_method)
		res.register(self.check_and_fill_args(method.arg_names, args, context))
		if res.error: return res
		return_value = res.register(method(context))
		if res.error: return res
		return res.success(return_value)

	def no_visit_method(self, node, context):
		raise Exception(f"execute_{self.name} is not defined")

	def copy(self):
		copy = BuiltinFunction(self.name)
		copy.set_context(self.context)
		copy.set_position(self.pos_start, self.pos_end)
		return copy
	
	def __repr__(self):
		return f"<built-in func {self.name}>"
	
	######################################
	######### BUILT-IN FUNCTIONS #########
	######################################

	def execute_println(self, context):
		"""
			print the value passed in with a new line at the end
			example: println("Hello World")
		"""
		print(str(context.symbol_table.get("value")))
		return RuntimeResult().success(Number.null)
	execute_println.arg_names = ["value"]

	def execute_print(self, context):
		"""
			print the value passed in without a new line at the end
			example: print("Hello World!")
		"""
		print(str(context.symbol_table.get("value")), end="")
		return RuntimeResult().success(Number.null)
	execute_print.arg_names = ["value"]

	def execute_input(self, context):
		"""
			read a line from input, convert it to String, and return it
			example: value = input("Enter your name: ")
		"""
		text = ""
		try:
			text = str(context.symbol_table.get("text"))
		except:
			pass
		input_value = input(text)
		return RuntimeResult().success(String(input_value))
	execute_input.arg_names = ["text"]

	def execute_int_input(self, context):
		"""
			read a line from input, try to convert it to Number, and return it
			example 1: value = int_input("Enter a value: ")
		"""
		text = str(context.symbol_table.get("text"))
		error_text = "Input value must be an integer."
		while True:
			input_value = input(text)
			try:
				input_value = int(input_value)
				break
			except ValueError:
				print(error_text)
		return RuntimeResult().success(Number(input_value))
	execute_int_input.arg_names = ["text"]

	def execute_absolute_number_of(self, context):
		"""
			try to return the absolute number of the value passed in
			example: abs_num = absolute_number_of(-9)
		"""
		value = context.symbol_table.get("value")
		try:
			value = int(context.symbol_table.get("value").value)
		except ValueError:
			return RuntimeResult().failure(RuntimeError(
				self.pos_start, self.pos_end, f"{value} does not have an absolute number", context
			))
		return RuntimeResult().success(Number(abs(value)))
	execute_absolute_number_of.arg_names = ["value"]

	def execute_is_number(self, context):
		"""
			check if the value passed in is a number
			example: is_number(3)
		"""
		value = context.symbol_table.get("value")
		is_number = isinstance(value, Number)
		return RuntimeResult().success(Number.true if is_number is True else Number.false)
	execute_is_number.arg_names = ["value"]

	def execute_is_string(self, context):
		"""
			check if the value passed in is a string
			example: is_string("Hello World")
		"""
		value = context.symbol_table.get("value")
		is_string = isinstance(value, String)
		return RuntimeResult().success(Number.true if is_string is True else Number.false)
	execute_is_string.arg_names = ["value"]

	def execute_is_array(self, context):
		"""
			check if the value passed in is an array
			example: is_array([1, 2, 3])
		"""
		value = context.symbol_table.get("value")
		is_array = isinstance(value, Array)
		return RuntimeResult().success(Number.true if is_array is True else Number.false)
	execute_is_array.arg_names = ["value"]

	def execute_is_function(self, context):
		"""
			check if the value passed in is a function
			example: is_function(some_func)
		"""
		value = context.symbol_table.get("value")
		is_function = isinstance(value, BaseFunction)
		return RuntimeResult().success(Number.true if is_function is True else Number.false)
	execute_is_function.arg_names = ["value"]

	def execute_is_map(self, context):
		"""
			check if the given value is a map or not
		"""
		value = context.symbol_table.get("value")
		is_map = isinstance(value, Map)
		return RuntimeResult().success(Number.true if is_map is True else Number.false)

	def execute_exit_program(self, context):
		"""
			exit the program
			example: exit_program()
		"""
		print("Bye bye!")
		exit()
	execute_exit_program.arg_names = []

	def execute_size(self, context):
		"""
			return the size of the value
			example: size([1, 2, 3])
		"""
		value = context.symbol_table.get("value")
		if isinstance(value, Number):
			return RuntimeResult().failure(RuntimeError(
				self.pos_start, self.pos_end, "The argument should be string or array", context
			))
		else:
			return RuntimeResult().success(Number(len(value.elements) if isinstance(value, Array) else len(value.value)))
	execute_size.arg_names = ["value"]

	def execute_typeof(self, context):
		"""
			return the type of the given value
			example: typeof("string")
		"""
		value = context.symbol_table.get("value")
		if isinstance(value, Number):
			if isinstance(value.value, int):
				return RuntimeResult().success(String("integer"))
			elif isinstance(value.value, float):
				return RuntimeResult().success(String("float"))
		elif isinstance(value, String):
			return RuntimeResult().success(String("string"))
		elif isinstance(value, Array):
			return RuntimeResult().success(String("array"))
		elif isinstance(value, Map):
			return RuntimeResult().success(String("map"))
		else:
			return RuntimeResult().failure(RuntimeError(
				self.pos_start, self.pos_end, f"{value} has no type", context
			))
	execute_typeof.arg_names = ["value"]
	
	def execute_int(self, context):
		"""
			convert the given value to integer type
			example: int("3")
		"""
		value = context.symbol_table.get("value")
		try:
			int_value = int(value.value)
		except:
			return RuntimeResult().failure(RuntimeError(
				self.pos_start, self.pos_end, f"{value.value} cannot be converted to integer", context
			))
		return RuntimeResult().success(Number(int_value))
	execute_int.arg_names = ["value"]

	def execute_float(self, context):
		"""
			convert the given value to float
			example: float(4)
		"""
		value = context.symbol_table.get("value")
		try:
			float_value = float(value.value)
		except:
			return RuntimeResult().failure(RuntimeError(
				self.pos_start, self.pos_end, f"{value.value} cannot be converted to float", context
			))
		return RuntimeResult().success(Number(float_value))
	execute_float.arg_names = ["value"]

	def execute_string(self, context):
		"""
			convert the given value to string
			example: string(344.3)
		"""
		value = context.symbol_table.get("value")
		new_value = str(value.value)
		return RuntimeResult().success(String(new_value))
	execute_string.arg_names = ["value"]

	def execute_chars(self, context):
		"""
			convert the given value to array
			example 1: chars("some string")
			example 2: chars(123)
		"""
		value = context.symbol_table.get("value")
		lst = []
		for i in str(value.value):
			lst.append(String(i))
		return RuntimeResult().success(Array(lst))
	execute_chars.arg_names = ["value"]

	def execute_split(self, context):
		"""
			split the given string
			example: split("Bob,Sue,John", ",")
		"""
		value = context.symbol_table.get("value").value
		delimiter = context.symbol_table.get("delimiter").value
		lst = value.split(delimiter)
		return RuntimeResult().success(Array(lst))
	execute_split.arg_names = ["value", "delimiter"]

	def execute_import(self, context):
		"""
			import the specified file
			example: import("some_file.gen")
					 some_function()
		"""
		filename = context.symbol_table.get("filename").value
		try:
			with open(filename, "r") as fobj:
				code = fobj.read()
		except Exception:
			return RuntimeResult().failure(RuntimeError(
				self.pos_start, self.pos_end, f"Could not open file'{filename}'", context
			))

		# generate tokens
		lexer = Lexer(filename, code)
		tokens, err = lexer.make_tokens()
		if err is not None: return None, err

		# generate AST
		parser = Parser(tokens)
		ast = parser.parse()
		if ast.error: return None, ast.error
		
		evaluator = Evaluator()
		new_symbol_table = evaluator.visit(ast.node, context, only_return_symtable=True)
		
		for k, v in new_symbol_table.symbols.items():
			self.context.symbol_table.set(k, v)
		return RuntimeResult().success(Number.null)
	execute_import.arg_names = ["filename"]


BuiltinFunction.println 			= BuiltinFunction("println")
BuiltinFunction.print	 			= BuiltinFunction("print")
BuiltinFunction.input	 			= BuiltinFunction("input")
BuiltinFunction.int_input			= BuiltinFunction("int_input")
BuiltinFunction.absolute_number_of	= BuiltinFunction("absolute_number_of")
BuiltinFunction.is_number			= BuiltinFunction("is_number")
BuiltinFunction.Pi					= BuiltinFunction("Pi")
BuiltinFunction.is_string			= BuiltinFunction("is_string")
BuiltinFunction.is_array			= BuiltinFunction("is_array")
BuiltinFunction.is_function			= BuiltinFunction("is_function")
BuiltinFunction.exit_program		= BuiltinFunction("exit_program")
BuiltinFunction.size				= BuiltinFunction("size")
BuiltinFunction.typeof				= BuiltinFunction("typeof")
BuiltinFunction.int					= BuiltinFunction("int")
BuiltinFunction.float				= BuiltinFunction("float")
BuiltinFunction.string				= BuiltinFunction("string")
BuiltinFunction.chars				= BuiltinFunction("chars")
BuiltinFunction.split				= BuiltinFunction("split")
BuiltinFunction.import_				= BuiltinFunction("import")