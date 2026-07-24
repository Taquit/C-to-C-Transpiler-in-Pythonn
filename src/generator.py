class Generator:
    def generate(self,nodo):
        if type(nodo).__name__=="ProgramNode":
            body_code = ""
            for statment in nodo.statements:
                body_code += self.generate(statment) + "\n"
            
            code_cpp = "#include <iostream>\n"
            if "std::string" in body_code:
                code_cpp += "#include <string>\n"
            code_cpp += "\n"
            code_cpp += body_code
            return code_cpp
            
        elif type(nodo).__name__=="VarDeclarationNode":
            var_type = nodo.var_type
            if var_type == "string":
                var_type = "std::string"
            if nodo.value is None:
                return f"{var_type} {nodo.var_name};"
            else:
                val_gen = self.generate(nodo.value) if hasattr(nodo.value, "__class__") and "Node" in type(nodo.value).__name__ else nodo.value
                return f"{var_type} {nodo.var_name} = {val_gen};"

        elif type(nodo).__name__=="DecisionNode":
            if nodo.type_decision == "if":
                code_cpp = f"if ({nodo.condition.left}{nodo.condition.operator}{nodo.condition.right}){{\n"
                for statment in nodo.true_block:
                    code_cpp += self.generate(statment) + "\n"
                code_cpp += "}\n"
                if nodo.false_block is not None:
                    code_cpp += "else {\n"
                    for statment in nodo.false_block:
                        code_cpp += self.generate(statment) + "\n"
                    code_cpp += "}\n"
                return code_cpp

        elif type(nodo).__name__=="AssignationNode":
            val_gen = self.generate(nodo.value) if hasattr(nodo.value, "__class__") and "Node" in type(nodo.value).__name__ else nodo.value
            return f"{nodo.var_name} = {val_gen};"

        elif type(nodo).__name__=="IncrementoNodo":
            if nodo.right_value is not None:
                return f"{nodo.left_value} {nodo.operator} {nodo.right_value};"
            else:
                return f"{nodo.left_value}{nodo.operator};"

        elif type(nodo).__name__=="PrintNode":
            return f"std::cout << {nodo.value} << std::endl;"

        elif type(nodo).__name__=="ForNode":
            init_code = self.generate(nodo.initialization)
            cond_code = f"{nodo.condition.left}{nodo.condition.operator}{nodo.condition.right}"
            inc_code = self.generate(nodo.increment).rstrip(';')
            
            code_cpp = f"for ({init_code} {cond_code}; {inc_code}){{\n"
            for statment in nodo.loop_block:
                code_cpp += self.generate(statment) + "\n"
            code_cpp += "}\n"
            return code_cpp

        elif type(nodo).__name__=="WhileNode":
            cond_code = f"{nodo.condition.left}{nodo.condition.operator}{nodo.condition.right}"
            
            code_cpp = f"while ({cond_code}){{\n"
            
            for statment in nodo.loop_block:
                code_cpp += self.generate(statment) + "\n"
            code_cpp += "}\n"
            return code_cpp

        elif type(nodo).__name__=="DoWhileNode":
            code_cpp = f"do {{\n"
            for statment in nodo.loop_block:
                code_cpp += self.generate(statment) + "\n"
            code_cpp += f"}} while({nodo.condition.left}{nodo.condition.operator}{nodo.condition.right})\n"
            return code_cpp

        elif type(nodo).__name__=="CaseNodo":
            code_cpp = f"case {nodo.value}:\n"
            for statment in nodo.statements:
                code_cpp += self.generate(statment) + "\n"
            code_cpp += "break;\n"
            return code_cpp

        elif type(nodo).__name__=="SwitchNode":
            code_cpp = f"switch ({nodo.variable}) {{\n"
            for case_node in nodo.cases:
                code_cpp += self.generate(case_node) + "\n"
            if getattr(nodo, "default_block", None):
                code_cpp += "default:\n"
                for statment in nodo.default_block:
                    code_cpp += self.generate(statment) + "\n"
                code_cpp += "break;\n"
            code_cpp += "}\n"
            return code_cpp

        elif type(nodo).__name__=="FunctionNode":
            if nodo.name == "Main":
                code_cpp = "int main() {\n"
                for stmt in nodo.body:
                    code_cpp += self.generate(stmt) + "\n"
                code_cpp += "return 0;\n}\n"
                return code_cpp
            else:
                ret_type = nodo.return_type
                if ret_type == "string":
                    ret_type = "std::string"
                params = []
                for p_type, p_name in nodo.parameters:
                    if p_type == "string":
                        p_type = "std::string"
                    params.append(f"{p_type} {p_name}")
                params_str = ", ".join(params)
                code_cpp = f"{ret_type} {nodo.name}({params_str}) {{\n"
                for stmt in nodo.body:
                    code_cpp += self.generate(stmt) + "\n"
                code_cpp += "}\n"
                return code_cpp

        elif type(nodo).__name__=="FunctionCallNode":
            args_str = ", ".join([str(arg) if not hasattr(arg, "generate") else self.generate(arg) for arg in nodo.arguments])
            call_str = f"{nodo.name}({args_str})"
            if getattr(nodo, "is_statement", False):
                return call_str + ";"
            return call_str

        elif type(nodo).__name__=="ReturnNode":
            return f"return {nodo.value};"