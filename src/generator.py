class Generator:
    def generate(self,nodo):
        if type(nodo).__name__=="ProgramNode":
            code_cpp = "#include <iostream>\n\n"
            code_cpp += "int main() {\n"
            for statment in nodo.statements:
                code_cpp += self.generate(statment) + "\n"
            code_cpp += "return 0;\n}\n"
            return code_cpp
            
        elif type(nodo).__name__=="VarDeclarationNode":
            if nodo.value is None:
                return f"{nodo.var_type} {nodo.var_name};"
            else:
                return f"{nodo.var_type} {nodo.var_name} = {nodo.value};"

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
            return f"{nodo.var_name} = {nodo.value};"

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



            
        
            