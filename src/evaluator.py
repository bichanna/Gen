import src.gen_token as tk
from src.error import RuntimeError
from value import *

class RuntimeResult:
	def __init__(self):
		self.value = None
		self.error = None
	
	def register(self, result):
		if result.error: self.error = result.error
		return result.value
	
	def success(self, value):
		self.value = value
		return self

	def failure(self, error):
		self.error = error
		return self


class Evaluator:
	def visit(self, node, context):
		method_to_be_called = f"visit_{type(node).__name__}"
		method = getattr(self, method_to_be_called, self.no_visit_method)
		return method(node, context)
	
	def no_visit_method(self, node, context):
		raise Exception(f"No visit_{type(node).__name__} method defined.")
	
	def visit_VarAccessNode(self, node, context):
		res = RuntimeResult()
		var_name = node.var_name_token.value
		value = context.symbol_table.get(var_name)
		if value is None: return res.failure(RuntimeError(
			node.pos_start, node.pos_end, f"var '{var_name}' is not defined", context
		))
		value = value.copy().set_position(node.pos_start, node.pos_end)
		return res.success(value)
	
	def visit_VarAssignNode(self, node, context):
		res = RuntimeResult()
		var_name = node.var_name_token.value
		value = res.register(self.visit(node.value_node, context))
		if res.error: return res
		context.symbol_table.set(var_name, value)
		return res.success(value)
	
	def visit_IfNode(self, node, context):
		res = RuntimeResult()
		for condition, expression in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if res.error: return res
			if condition_value.is_true():
				expr_value = res.register(self.visit(expression, context))
				if res.error: return res
				return res.success(expr_value)
		if node.else_case is not None:
			else_value = res.register(self.visit(node.else_case, context))
			if res.error: return res
			return res.success(else_value)
		return res.success(None)

	def visit_NumberNode(self, node, context):
		return RuntimeResult().success(Number(node.token.value).set_context(context).set_position(node.pos_start, node.pos_end))
	
	def visit_BinOpNode(self, node, context):
		res = RuntimeResult()
		left = res.register(self.visit(node.left_node, context))
		if res.error: return res
		right = res.register(self.visit(node.right_node, context))
		if res.error: return res
		# check the operator type
		if node.op_token.type == tk.TT_PLUS:
			result, err = left.added_to(right)
		elif node.op_token.type == tk.TT_MINUS:
			result, err = left.subtracted_by(right)
		elif node.op_token.type == tk.TT_MULT:
			result, err = left.multiplied_by(right)
		elif node.op_token.type == tk.TT_DIV:
			result, err = left.divided_by(right)
		elif node.op_token.type == tk.TT_POWER:
			result, err = left.powered_by(right)
		elif node.op_token.type == tk.TT_DEQUALS:
			result, err = left.get_comparison_equal(right)
		elif node.op_token.type == tk.TT_NEQUALS:
			result, err = left.get_comparison_not_equal(right)
		elif node.op_token.type == tk.TT_LTHAN:
			result, err = left.get_comparison_less_than(right)
		elif node.op_token.type == tk.TT_GTHAN:
			result, err = left.get_comparison_greater_than(right)
		elif node.op_token.type == tk.TT_LTEQUALS:
			result, err = left.get_comparison_lt_equals(right)
		elif node.op_token.type == tk.TT_GTEQUALS:
			result, err = left.get_comparison_gt_equals(right)
		elif node.op_token.matches(tk.TT_KEYWORD, "and"):
			result, err = left.and_by(right)
		elif node.op_token.matches(tk.TT_KEYWORD, "or"):
			result, err = left.or_by(right)
		
		return res.failure(err) if err is not None else res.success(result.set_position(node.pos_start, node.pos_end))
	
	def visit_UnaryOpNode(self, node, context):
		res = RuntimeResult()
		num = res.register(self.visit(node.node, context))
		if res.error: return res
		err = None
		if node.op_token.type == tk.TT_MINUS:
			num, err = num.multiplied_by(Number(-1))
		elif node.op_token.matches(tk.TT_KEYWORD, "not"):
			num, err = num.notted()

		return res.failure(err)	if err is not None else res.success(num.set_position(node.pos_start, node.pos_end))

	def visit_ForNode(self, node, context):
		res = RuntimeResult()
		start_value = res.register(self.visit(node.start_value_node, context))
		if res.error: return res
		end_value = res.register(self.visit(node.end_value_node, context))
		if res.error: return res
		if node.step_value_node:
			step_value = res.register(self.visit(node.step_value_node, context))
			if res.error: return res
		else:
			step_value = Number(1)
		sv = start_value.value
		if step_value.value >= 0:
			condition = lambda: sv < end_value.value
		else:
			condition = lambda: sv > end_value.value
		while condition():
			context.symbol_table.set(node.var_name_token.value, Number(sv))
			sv += step_value.value
			res.register(self.visit(node.body_node, context))
			if res.error: return res
		return res.success(None)
	
	def visit_WhileNode(self, node, context):
		res = RuntimeResult()
		while True:
			condition = res.register(self.visit(node.condition_node, context))
			if res.error: return res
			if condition.is_true() is False: break
			res.register(self.visit(node.body_node, context))
			if res.error: return res
		return res.success(None)
