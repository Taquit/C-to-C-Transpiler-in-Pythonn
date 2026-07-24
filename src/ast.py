class ASTNodo:
    pass

class ProgramNodo(ASTNodo):
    def __init__(self):
        self.statements = []
        
    def __repr__(self):
        return f"ProgramNodo({self.statements})"

class PrintNodo(ASTNodo):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"PrintNodo({self.value})"
    

class VarDeclarationNodo(ASTNodo):

    def __init__(self,var_type,var_name,value):
        self.var_type = var_type
        self.var_name = var_name
        self.value = value

    def __repr__(self):
        return f"VarDeclarationNodo({self.var_type},{self.var_name},{self.value})"


class AssignationNodo(ASTNodo):
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def __repr__(self):
        return f"AssignationNodo({self.var_name},{self.value})"



class ConditionNodo(ASTNodo):
    def __init__(self,left,operator,right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"ConditionNodo({self.left},{self.operator},{self.right})"

class IncrementoNodo(ASTNodo):
    def __init__(self,left_value,operator,right_value):
        self.left_value = left_value
        self.operator = operator
        self.right_value = right_value

    def __repr__(self):
        return f"IncrementoNodo({self.left_value},{self.operator},{self.right_value})"


class CaseNodo(ASTNodo):
    def __init__(self,value,statements):
        self.value = value
        self.statements = statements

    def __repr__(self):
        repr_str = f"CASE {self.value}:\n"
        for stmt in self.statements:
            repr_str += f"      {stmt}\n"
        return repr_str

class DecisionNodo(ASTNodo):
    def __init__(self,type_decision,condition,true_block,false_block=None):
        self.type_decision = type_decision
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def __repr__(self):
        repr_str = f"{self.type_decision.upper()} ( {self.condition} ){{\n"
        
        for instruccion in self.true_block:
            repr_str += f"    {instruccion}\n"
            
        repr_str += "  }"
        
        if self.false_block:
            repr_str += " ELSE {\n"
            for instruccion in self.false_block:
                repr_str += f"    {instruccion}\n"
            repr_str += "  }"
            
        return repr_str

class ForNodo(ASTNodo):
    def __init__(self, initialization, condition, increment, loop_block):
        self.initialization = initialization
        self.condition = condition
        self.increment = increment
        self.loop_block = loop_block

    def __repr__(self):
        repr_str = f"FOR ( {self.initialization} ; {self.condition} ; {self.increment} ){{\n"
        for instruccion in self.loop_block:
            repr_str += f"    {instruccion}\n"
        repr_str += "  }"
        return repr_str

class WhileNodo(ASTNodo):
    def __init__(self, condition, loop_block):
        self.condition = condition
        self.loop_block = loop_block

    def __repr__(self):
        repr_str = f"WHILE ( {self.condition} ){{\n"
        for instruccion in self.loop_block:
            repr_str += f"    {instruccion}\n"
        repr_str += "  }"
        return repr_str

class DoWhileNodo(ASTNodo):
    def __init__(self,condition,loop_block):
        self.condition = condition
        self.loop_block = loop_block

    def __repr__(self):
        repr_str = f"DO {{\n"
        for instruccion in self.loop_block:
            repr_str += f"    {instruccion}\n"
        repr_str += f"  }} WHILE({self.condition})"
        return repr_str

class SwitchNodo(ASTNodo):
    def __init__(self,variable,cases,default_block=None):
        self.variable = variable
        self.cases = cases
        self.default_block = default_block

    def __repr__(self):
        repr_str = f"SWITCH ({self.variable}) {{\n"
        for case in self.cases:
            repr_str += f"  {case}\n"
        if self.default_block:
            repr_str += f"  DEFAULT:\n"
            for stmt in self.default_block:
                repr_str += f"    {stmt}\n"
        repr_str += "}"
        return repr_str

class FunctionNodo(ASTNodo):
    def __init__(self, name, return_type, parameters, body):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        params_str = ", ".join([f"{p_type} {p_name}" for p_type, p_name in self.parameters])
        repr_str = f"FUNCTION {self.return_type} {self.name}({params_str}) {{\n"
        for stmt in self.body:
            repr_str += f"  {stmt}\n"
        repr_str += "}"
        return repr_str

class FunctionCallNodo(ASTNodo):
    def __init__(self, name, arguments, is_statement=False):
        self.name = name
        self.arguments = arguments
        self.is_statement = is_statement

    def __repr__(self):
        args_str = ", ".join(map(str, self.arguments))
        return f"CALL {self.name}({args_str})"

class ReturnNodo(ASTNodo):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"RETURN {self.value}"