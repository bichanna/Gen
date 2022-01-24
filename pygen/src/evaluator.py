import src.gen_token as tk
import src.value as value
from src.error import RuntimeError

class RuntimeResult:
	def __init__(self):
		self.reset()
	
	def reset(self):
		self.value = None
		self.error = None
		self.func_return_value = None
		self.loop_continue = False
		self.loop_break = False
	
	def register(self, result):
		self.error = result.error
		self.func_return_value = result.func_return_value
		self.loop_continue = result.loop_continue
		self.loop_break = result.loop_break
		return result.value
	
	def success(self, value):
		self.reset()
		self.value = value
		return self
	
	def success_return(self, value):
		self.reset()
		self.func_return_value = value
		return self
	
	def success_continue(self):
		self.reset()
		self.loop_continue = True
		return self
	
	def success_break(self):
		self.reset()
		self.loop_break = True
		return self
	
	def should_return(self):
		return (self.error or self.func_return_value or self.loop_continue or self.loop_break)

	def failure(self, error):
		self.reset()
		self.error = error
		return self


class Evaluator:
	def visit(self, node, context, only_return_symtable=False):
		if isinstance(node, type(None)) is False:
			method_to_be_called = f"visit_{type(node).__name__}"
			method = getattr(self, method_to_be_called, self.no_visit_method)
			if only_return_symtable is False: return method(node, context)
			else:
				method(node, context)
				return context.symbol_table
		return None
	
	def no_visit_method(self, node, context):
		raise Exception(f"No visit_{type(node).__name__} method defined.")
	
	def visit_VarAccessNode(self, node, context):
		res = RuntimeResult()
		var_name = node.var_name_token.value
		value = context.symbol_table.get(var_name)
		if value is None: return res.failure(RuntimeError(
			node.pos_start, node.pos_end, f"'{var_name}' is not defined", context
		))
		value = value.copy().set_position(node.pos_start, node.pos_end)
		return res.success(value)
	
	def visit_VarAssignNode(self, node, context):
		res = RuntimeResult()
		var_name = node.var_name_token.value
		value = res.register(self.visit(node.value_node, context))
		if res.should_return(): return res
		context.symbol_table.set(var_name, value)
		return res.success(value)
	
	def visit_ReassignNode(self, node, context):
		res = RuntimeResult()
		if isinstance(node.var_name_token, list):
			return res.failure(RuntimeError(
				node.pos_start, node.pos_end, "Modifying an array directly is not allowed", context
			))
		elif isinstance(node.var_name_token, dict):
			return res.failure(RuntimeError(
				node.pos_start, node.pos_end, "Modifying a map directly is not allowed", context
			))
		else:
			var_name = node.var_name_token.value
			index_or_key = res.register(self.visit(node.index_or_key, context))
			if res.should_return(): return res
			new_value = res.register(self.visit(node.value_node, context))
			if res.should_return(): return res
			if isinstance(context.symbol_table.symbols[var_name], value.Array):
				if len(context.symbol_table.symbols[var_name].elements) > index_or_key.value:
					context.symbol_table.set_arr(var_name, index_or_key, new_value)
				else:
					return res.failure(RuntimeError(
						node.pos_start, node.pos_end, f"Element at index {index_or_key.value} does not exist", context
					))
			else:
				context.symbol_table.set_map(var_name, index_or_key, new_value)
		return res.success(new_value)
	
	def visit_IfNode(self, node, context):
		res = RuntimeResult()
		for condition, expression, should_return_null in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if res.should_return(): return res
			if condition_value.is_true():
				expr_value = res.register(self.visit(expression, context))
				if res.should_return(): return res
				return res.success(value.Number.null if should_return_null else expr_value)
		if node.else_case is not None:
			expr, should_return_null = node.else_case
			else_value = res.register(self.visit(expr, context))
			if res.should_return(): return res
			return res.success(value.Number.null if should_return_null else else_value)
		return res.success(value.Number.null)

	def visit_NumberNode(self, node, context):
		return RuntimeResult().success(value.Number(node.token.value).set_context(context).set_position(node.pos_start, node.pos_end))
	
	def visit_BinOpNode(self, node, context):
		res = RuntimeResult()
		left = res.register(self.visit(node.left_node, context))
		if res.should_return(): return res
		right = res.register(self.visit(node.right_node, context))
		if res.should_return(): return res
		# check the operator type
		if node.op_token.type == tk.TT_PLUS:
			result, err = left.added_to(right)
		elif node.op_token.type == tk.TT_MINUS:
			result, err = left.subtracted_by(right)
		elif node.op_token.type == tk.TT_AT:
			result, err = left.at(right)
		elif node.op_token.type == tk.TT_MULT:
			result, err = left.multiplied_by(right)
		elif node.op_token.type == tk.TT_DIV:
			result, err = left.divided_by(right)
		elif node.op_token.type == tk.TT_POWER:
			result, err = left.powered_by(right)
		elif node.op_token.type == tk.TT_MODULO:
			result, err = left.modulo(right)
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
		if res.should_return(): return res
		err = None
		if node.op_token.type == tk.TT_MINUS:
			num, err = num.multiplied_by(value.Number(-1))
		elif node.op_token.matches(tk.TT_KEYWORD, "not"):
			num, err = num.notted()

		return res.failure(err)	if err is not None else res.success(num.set_position(node.pos_start, node.pos_end))

	def visit_ForNode(self, node, context):
		res = RuntimeResult()
		elements = []
		start_value = res.register(self.visit(node.start_value_node, context))
		if res.should_return(): return res
		end_value = res.register(self.visit(node.end_value_node, context))
		if res.should_return(): return res
		if node.step_value_node:
			step_value = res.register(self.visit(node.step_value_node, context))
			if res.should_return(): return res
		else:
			step_value = value.Number(1)
		sv = start_value.value
		if step_value.value >= 0:
			condition = lambda: sv < end_value.value
		else:
			condition = lambda: sv > end_value.value
		while condition():
			context.symbol_table.set(node.var_name_token.value, value.Number(sv))
			sv += step_value.value
			val = res.register(self.visit(node.body_node, context))
			if res.should_return() and res.loop_continue is False and res.loop_break is False: return res
			if res.loop_continue is True:
				continue
			elif res.loop_break is True:
				break
			else:
				elements.append(val)
		return res.success(value.Number.null if node.should_return_null else value.Array(elements).set_context(context).set_position(node.pos_start, node.pos_end))
	
	def visit_ArrayNode(self, node, context):
		res = RuntimeResult()
		elements = []
		for element in node.element_nodes:
			elements.append(res.register(self.visit(element, context)))
			if res.should_return(): return res
		return res.success(value.Array(elements).set_context(context).set_position(node.pos_start, node.pos_end))
	
	def visit_MapNode(self, node, context):
		res = RuntimeResult()
		map = {}
		for key, v in node.map.items():
			map[key.token.value] = res.register(self.visit(v, context))
			if res.should_return(): return res
		return res.success(value.Map(map).set_context(context).set_position(node.pos_start, node.pos_end))
	
	def visit_WhileNode(self, node, context):
		res = RuntimeResult()
		elements = []
		while True:
			condition = res.register(self.visit(node.condition_node, context))
			if res.should_return(): return res
			if condition.is_true() is False: break
			val = res.register(self.visit(node.body_node, context))
			if res.should_return() and res.loop_continue is False and res.loop_break is False: return res
			if res.loop_continue is True:
				continue
			elif res.loop_break is True:
				break
			else:
				elements.append(val)
		return res.success(value.Number.null if node.should_return_null else value.Array(elements).set_context(context).set_position(node.pos_start, node.pos_end))
	
	def visit_FuncDefNode(self, node, context):
		res = RuntimeResult()
		func_name = node.var_name_token.value if node.var_name_token is not None else None
		body_node = node.body_node
		arg_names = [arg.value for arg in node.arg_name_tokens]
		func_value = value.Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_position(node.pos_start, node.pos_end)
		if node.var_name_token is not None:
			context.symbol_table.set(func_name, func_value)
		return res.success(func_value)

	def visit_CallNode(self, node, context):
		res = RuntimeResult()
		args = []
		called_value = res.register(self.visit(node.node_to_call, context))
		if res.should_return(): return res
		called_value = called_value.copy().set_position(node.pos_start, node.pos_end).set_context(context)
		for argnode in node.arg_nodes:
			args.append(res.register(self.visit(argnode, context)))
			if res.should_return(): return res
		
		return_value = res.register(called_value.execute(args))
		if res.should_return(): return res
		return_value = return_value.copy().set_position(node.pos_start, node.pos_end).set_context(context)
		return res.success(return_value)
	
	def visit_StringNode(self, node, context):
		return RuntimeResult().success(value.String(node.token.value).set_context(context).set_position(node.pos_start, node.pos_end))

	def visit_ReturnNode(self, node, context):
		res = RuntimeResult()
		if node.node_to_return:
			val = res.register(self.visit(node.node_to_return, context))
			if res.should_return(): return res
		else:
			val = value.Number.null
		return res.success_return(val)
	
	def visit_ContinueNode(self, node, context):
		return RuntimeResult().success_continue()
	
	def visit_BreakNode(self, node, context):
		return RuntimeResult().success_break()