class NumberNode:
	def __init__(self, token):
		self.token = token
		self.pos_start = self.token.pos_start
		self.pos_end = self.token.pos_end

	def __repr__(self):
		return f"{self.token}"


class StringNode:
	def __init__(self, token):
		self.token = token
		self.pos_start = self.token.pos_start
		self.pos_end = self.token.pos_end
	
	def __repr__(self):
		return str(self.token)


class ArrayNode:
	def __init__(self, elements, pos_start, pos_end):
		self.element_nodes = elements
		self.pos_start = pos_start
		self.pos_end = pos_end


class MapNode:
	def __init__(self, map, pos_start, pos_end):
		self.map = map
		self.pos_start = pos_start
		self.pos_end = pos_end


class BinOpNode:
	def __init__(self, left_node, op_token, right_node):
		self.left_node = left_node
		self.op_token = op_token
		self.right_node = right_node
		
		self.pos_start = self.left_node.pos_start
		self.pos_end = self.right_node.pos_end
	
	def __repr__(self):
		return f"({self.left_node}, {self.op_token}, {self.right_node})"


class UnaryOpNode:
	def __init__(self, op_token, node):
		self.op_token = op_token
		self.node = node
		self.pos_start = self.op_token.pos_start
		self.pos_end = self.node.pos_end
	
	def __repr__(self):
		return f"({self.op_token}, {self.node})"


class VarAccessNode:
	def __init__(self, var_name_token):
		self.var_name_token = var_name_token
		self.pos_start = self.var_name_token.pos_start
		self.pos_end = self.var_name_token.pos_end


class VarAssignNode:
	def __init__(self, var_name_token, value_node):
		self.var_name_token = var_name_token
		self.value_node = value_node
		self.pos_start = self.var_name_token.pos_start
		self.pos_end = self.value_node.pos_end


class ReassignNode:
	def __init__(self, var_name_token, index_or_key, value_node, is_direct):
		# var_name_token is either an IDENTIFIER or a Python list
		self.var_name_token = var_name_token
		self.index_or_key = index_or_key
		self.value_node = value_node
		self.is_direct = is_direct
		from src.gen_token import Token
		if isinstance(self.var_name_token, list):
			self.pos_start = self.var_name_token[0].pos_start
		elif isinstance(self.var_name_token, Token):
			self.pos_start = self.var_name_token.pos_start
		else:
			key = list(self.var_name_token.keys())[0]
			self.pos_start = self.var_name_token[key].pos_start
		self.pos_end = self.value_node.pos_end

class IfNode:
	def __init__(self, cases, else_case):
		self.cases = cases
		self.else_case = else_case
		self.pos_start = self.cases[0][0].pos_start
		self.pos_end = (self.else_case or self.cases[len(self.cases)-1])[0].pos_end


class ReturnNode:
	def __init__(self, node_to_return, pos_start, pos_end):
		self.node_to_return = node_to_return
		self.pos_start = pos_start
		self.pos_end = pos_end


class ContinueNode:
	def __init__(self, pos_start, pos_end):
		self.pos_start = pos_start
		self.pos_end = pos_end


class BreakNode:
	def __init__(self, pos_start, pos_end):
		self.pos_start = pos_start
		self.pos_end = pos_end


class ForNode:
	def __init__(self, var_name_token, start_value_node, end_value_node, step_value_node, body_node, should_return_null):
		self.var_name_token = var_name_token
		self.start_value_node = start_value_node
		self.end_value_node = end_value_node
		self.step_value_node = step_value_node
		self.body_node = body_node
		self.pos_start = self.var_name_token.pos_start
		self.pos_end = self.body_node.pos_end
		self.should_return_null = should_return_null


class ForInNode:
	def __init__(self, var_name_token, array_elements, body_node):
		self.var_name_token = var_name_token
		self.array_elements = array_elements
		self.body_node = body_node
		self.pos_start = self.var_name_token.pos_start
		self.pos_end = self.body_node.pos_end
	
	def __repr__(self):
		return f"{self.var_name_token}\n{self.array_elements}"


class WhileNode:
	def __init__(self, condition, body_node, should_return_null):
		self.condition_node = condition
		self.body_node = body_node
		self.pos_start = self.condition_node.pos_start
		self.pos_end = self.body_node.pos_end
		self.should_return_null = should_return_null


class FuncDefNode:
	def __init__(self, var_name_token, arg_name_tokens, body_node, should_auto_return):
		self.var_name_token = var_name_token
		self.arg_name_tokens = arg_name_tokens
		self.body_node = body_node
		self.should_auto_return = should_auto_return
		if self.var_name_token:
			self.pos_start = self.var_name_token.pos_start
		elif len(self.arg_name_tokens) > 0:
			self.pos_start = self.arg_name_tokens[0].pos_start
		else:
			self.pos_start = self.body_node.pos_start
		self.pos_end = self.body_node.pos_end


class CallNode:
	def __init__(self, node_to_call, arg_nodes):
		self.node_to_call = node_to_call
		self.arg_nodes = arg_nodes
		self.pos_start = self.node_to_call.pos_start
		if len(self.arg_nodes) > 0:
			self.pos_end = self.arg_nodes[len(self.arg_nodes)-1].pos_end
		else:
			self.pos_end = self.node_to_call.pos_end