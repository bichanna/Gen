import readline # this is necessary: DO NOT REMOVE
import sys
import signal
from src.value import Number
from src.builtin_func import BuiltinFunction
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import Evaluator
from src.context import Context
from src.symbol_table import SymbolTable

def set_default_symbol_table(symbol_table):
	symbol_table.set("null", Number.null)
	symbol_table.set("true", Number.true)
	symbol_table.set("false", Number.false)
	symbol_table.set("Pi", Number.Pi)
	# built-in functions
	symbol_table.set("println", BuiltinFunction.println)
	symbol_table.set("print", BuiltinFunction.print)
	symbol_table.set("input", BuiltinFunction.input)
	symbol_table.set("int_input", BuiltinFunction.int_input)
	symbol_table.set("absolute_number_of", BuiltinFunction.absolute_number_of)
	symbol_table.set("is_number", BuiltinFunction.is_number)
	symbol_table.set("is_string", BuiltinFunction.is_string)
	symbol_table.set("is_array", BuiltinFunction.is_array)
	symbol_table.set("is_function", BuiltinFunction.is_function)
	symbol_table.set("exit_program", BuiltinFunction.exit_program)
	symbol_table.set("size", BuiltinFunction.size)
	symbol_table.set("typeof", BuiltinFunction.typeof)
	symbol_table.set("int", BuiltinFunction.int)
	symbol_table.set("float", BuiltinFunction.float)
	symbol_table.set("string", BuiltinFunction.string)
	symbol_table.set("chars", BuiltinFunction.chars)
	symbol_table.set("split", BuiltinFunction.split)
	symbol_table.set("import", BuiltinFunction.import_)
	symbol_table.set("clear", BuiltinFunction.clear)
	return symbol_table

global_symbol_table = SymbolTable()
global_symbol_table = set_default_symbol_table(global_symbol_table)

def run(filename, text, show_tokens=False):
	# generate tokens
	lexer = Lexer(filename, text)
	tokens, err = lexer.make_tokens()
	if err is not None: return None, err
	if show_tokens: print(tokens)

	# generate AST
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error
	# print(ast.node.element_nodes)

	# call evaluator
	evaluator = Evaluator()
	context = Context("<module>")
	context.symbol_table = global_symbol_table
	result = evaluator.visit(ast.node, context)
	if result is None:
		exit()
	return result.value, result.error

def shell():
	while True:
		t = input("gen>> ")
		if t.strip() == "": continue
		result, err = run("<stdin>", t)
		if err is not None:
			print(err)
		elif result:
			if len(result.elements) == 1:
				print(result.elements[0])
			else:
				print(result.__repr__())

def file(filename, show_tokens):
	try:
		with open(filename, "r") as fobj:
			code = fobj.read()
	except Exception:
		print(f"Could not open file '{filename}'.")
		sys.exit()
	_, error = run(filename, code, show_tokens)
	if error is not None: print(error)

def ctrl_c_handler(*_):
	print("\nBye bye!")
	sys.exit()

if __name__ == "__main__":
	# for catching Ctrl-C
	signal.signal(signal.SIGINT, ctrl_c_handler)

	if len(sys.argv) < 2 or sys.argv[-1].endswith(".py"):
		shell()
	else:
		show_tokens = False
		if "--show-tokens" in sys.argv:
			show_tokens = True
		filename = sys.argv[-1]
		if filename.endswith(".gen"):
			file(filename, show_tokens)
		else:
			print("Specify a file with .gen extension.")
