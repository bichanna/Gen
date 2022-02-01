from src.error import RuntimeError
from src.context import Context
from src.symbol_table import SymbolTable
from src.evaluator import Evaluator, RuntimeResult

import math

class Value:
	def __init__(self):
		self.set_position()
		self.set_context()

	def set_context(self, context=None):
		self.context = context
		return self
	
	def set_position(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self
	
	def added_to(self, other):
		return None, self.invalid_operation(other)
	
	# make these invalid operations unless overriden by Number class
	def subtracted_by(self, other):
		return None, self.invalid_operation(other)
	
	def multiplied_by(self, other):
		return None, self.invalid_operation(other)
	
	def divided_by(self, other):
		return None, self.invalid_operation(other)

	def powered_by(self, other):
		return None, self.invalid_operation(other)
	
	def modulo(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_equal(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_not_equal(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_less_than(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_greater_than(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_lt_equals(self, other):
		return None, self.invalid_operation(other)
	
	def get_comparison_gt_equals(self, other):
		return None, self.invalid_operation(other)
	
	def and_by(self, other):
		return None, self.invalid_operation(other)
	
	def or_by(self, other):
		return None, self.invalid_operation(other)

	def at(self, other):
		return None, self.invalid_operation(other)
	
	def notted(self):
		return None, self.invalid_operation()
	
	def is_true(self):
		return False
	
	def invalid_operation(self, other=None):
		if other is None: other = self
		return RuntimeError(
			self.pos_start, other.pos_end, "Invalid operation", self.context
		)
	
	def copy(self):
		pass
		
	def __repr__(self):
		return f"{self.value}"
	
	def return_type(self):
		return String("value")


class Number(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value
	
	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	# make these invalid operations unless overriden
	def subtracted_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def multiplied_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def divided_by(self, other):
		if isinstance(other, Number):
			if other.value == 0: return None, RuntimeError(
				other.pos_start, other.pos_end, "Division by zero is not allowed", self.context
			)
			else:
				return Number(self.value / other.value), None
		else:
			return None, self.invalid_operation(other)

	def powered_by(self, other):
		if isinstance(other, Number):
			return Number(self.value ** other.value).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def modulo(self, other):
		if isinstance(other, Number):
			return Number(self.value % other.value).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def get_comparison_equal(self, other):
		if isinstance(other, Number):
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def get_comparison_not_equal(self, other):
		if isinstance(other, Number):
			return Number(int(self.value != other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def get_comparison_less_than(self, other):
		if isinstance(other, Number):
			return Number(int(self.value < other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def get_comparison_greater_than(self, other):
		if isinstance(other, Number):
			return Number(int(self.value > other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	def get_comparison_lt_equals(self, other):
		if isinstance(other, Number):
			return Number(int(self.value <= other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def get_comparison_gt_equals(self, other):
		if isinstance(other, Number):
			return Number(int(self.value >= other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def and_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value and other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def or_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value or other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def notted(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None
	
	def is_true(self):
		return self.value != 0
	
	def return_type(self):
		if isinstance(self.value, int):
			return String("integer")
		else:
			return String("float")
	
	def copy(self):
		copy = Number(self.value)
		copy.set_position(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

Number.null = Number(0)
Number.true = Number(1)
Number.false = Number(0)
Number.Pi = Number(math.pi)


class String(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value
	
	def added_to(self, other):
		if isinstance(other, String):
			return String(self.value + other.value).set_context(self.context), None
		elif isinstance(other, Number):
			return String(self.value + str(other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def multiplied_by(self, other): # allow "a" * 8
		if isinstance(other, Number):
			return String(self.value * other.value).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def get_comparison_equal(self, other):
		if isinstance(other, String):
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def get_comparison_not_equal(self, other):
		if isinstance(other, String):
			return Number(int(self.value != other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)

	def and_by(self, other):
		if isinstance(other, String):
			return Number(int(self.value and other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def or_by(self, other):
		if isinstance(other, String):
			return Number(int(self.value or other.value)).set_context(self.context), None
		else:
			return None, self.invalid_operation(other)
	
	def at(self, other):
		if isinstance(other, Number):
			try:
				value = str(self.value[int(other.value)])
				return String(value), None
			except:
				return None, RuntimeError(
					other.pos_start, other.pos_end, f"Element at index {other.value} does not exist", self.context
				)
		else:
			return Value.invalid_operation(self, other)
	
	def notted(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None
	
	def is_true(self):
		return len(self.value) > 0
	
	def copy(self):
		copy = String(self.value)
		copy.set_position(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy
	
	def __repr__(self):
		return f'"{self.value}"'
	
	def __str__(self):
		return str(self.value)
	
	def return_type(self):
		return String("string")


class Array(Value):
	def __init__(self, elements):
		super().__init__()
		self.elements = elements
	
	def added_to(self, other):
		new_array = self.copy()
		if isinstance(other, Array):
			new_array.elements.extend(other.elements)
		else:
			new_array.elements.append(other)
		return new_array, None
	
	def subtracted_by(self, other):
		if isinstance(other, Number):
			new_array = self.copy()
			try:
				new_array.elements.pop(other.value)
				return new_array, None
			except IndexError:
				return None, RuntimeError(
					other.pos_start, other.pos_end, f"Element at index {other.value} does not exist", self.context
				)
		else:
			return Value.invalid_operation(self, other)

	def at(self, other):
		if isinstance(other, Number):
			try:
				return self.elements[other.value], None
			except:
				return None, RuntimeError(
					other.pos_start, other.pos_end, f"Element at index {other.value} does not exist", self.context
				)
		else:
			return Value.invalid_operation(self, other)

	def copy(self):
		copy = Array(self.elements)
		copy.set_position(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy
	
	def __repr__(self):
		string = "[" + ', '.join([str(i) for i in self.elements]) + "]"
		return string
	
	def return_type(self):
		return String("array")


class Map(Value):
	def __init__(self, map):
		super().__init__()
		self.map = map

	def at(self, other):
		if isinstance(other, Number) or isinstance(other, String):
			try:
				return self.map[other.value], None
			except:
				return None, RuntimeError(
					other.pos_start, other.pos_end, f"Element at key '{other.value}' does not exist", self.context
				)
		else:
			return Value.invalid_operation(self, other)

	def copy(self):
		copy = Map(self.map)
		copy.set_position(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy
	
	def __repr__(self):
		string = "{"
		for key, value in self.map.items():
			string += f"{key}: {value}, "
		if string[-1] == " " and string[-2] == ",":
			string = string[:-2] + "}"
		else:
			string += "}"
		return string
	
	def return_type(self):
		return String("map")


class BaseFunction(Value):
	def __init__(self, name):
		super().__init__()
		self.name = name if name is not None else "<unnamed>"
	
	def generate_new_context(self):
		new_context = Context(self.name, self.context, self.pos_start)
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
		return new_context

	def check_arguments(self, argument_names, arguments):
		res = RuntimeResult()
		# check the number of args are correct or not
		if len(arguments) > len(argument_names):
			return res.failure(RuntimeError(
				self.pos_start, self.pos_end, f"Too many arguments are passed to {self.name}", self.context
			))
		elif len(arguments) < len(argument_names):
			return res.failure(RuntimeError(
				self.pos_start, self.pos_end, f"Too few arguments are passed to {self.name}", self.context
			))
		else:
			return res.success(None)
	
	def fill_args(self, argument_names, arguments, context):
		for i in range(len(arguments)):
			arg_name = argument_names[i]
			arg_value = arguments[i]
			arg_value.set_context(context)
			context.symbol_table.set(arg_name, arg_value)
	
	def check_and_fill_args(self, arg_names, args, context):
		res = RuntimeResult()
		res.register(self.check_arguments(arg_names, args))
		if res.should_return(): return res
		self.fill_args(arg_names, args, context)
		return res.success(None)


class Function(BaseFunction):
	def __init__(self, name, body_node, arg_names, should_auto_return):
		super().__init__(name)
		self.body_node = body_node
		self.arg_names = arg_names
		self.should_auto_return = should_auto_return
	
	def execute(self, args):
		res = RuntimeResult()
		evaluator = Evaluator()
		context = self.generate_new_context()
		res.register(self.check_and_fill_args(self.arg_names, args, context))
		if res.should_return(): return res
		value = res.register(evaluator.visit(self.body_node, context))
		if res.should_return() and res.func_return_value is None: return res
		return_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
		return res.success(return_value)
		
	def copy(self):
		copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
		copy.set_position(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy
	
	def __repr__(self):
		return f"<func {self.name}>"
	
	def return_type(self):
		return String("function")
	
