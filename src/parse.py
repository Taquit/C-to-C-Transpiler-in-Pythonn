from src.ast import ProgramNodo, VarDeclarationNodo, AssignationNodo, DecisionNodo, ConditionNodo, IncrementoNodo, ForNodo, PrintNodo, WhileNodo, DoWhileNodo, CaseNodo, SwitchNodo, FunctionNodo, FunctionCallNodo, ReturnNodo
class Parse:
    #-------BASICOS-------#
    def __init__(self,tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def next_token(self):
        self.pos += 1

    def expected (self,expected_type):
        token_actual = self.current_token()
        if token_actual is None:
            raise SyntaxError(f"Se esperaba {expected_type} pero el archivo termino.")
        
        if token_actual.type == expected_type or token_actual.value == expected_type:
            self.next_token()
            return token_actual

        raise SyntaxError(
            f"Error de Sintaxis en la línea {token_actual.line}: "
            f"Se esperaba '{expected_type}', pero se encontró '{token_actual.value}'"
        )

    
    def parse(self):
        #Consume "using sapece"
        while self.current_token() and self.current_token().value == "using":
            self.expected("using")
            self.expected("ID")
            while self.current_token() and self.current_token().value ==".":
                self.expected(".")
                self.expected("ID")
            self.expected(";")
        
        #consume "nmaespace ..."
        has_namespace = False
        if self.current_token() and self.current_token().value == "namespace":
            has_namespace = True
            self.expected("namespace")
            self.expected("ID")
            self.expected("{")
            
        #Consume "class program {...}"
        has_class = False
        while self.current_token() and self.current_token().value in ["public","private"]:
            self.next_token()
        if self.current_token() and self.current_token().value == "class":
            has_class = True
            self.expected("class")
            self.expected("ID")
            self.expected("{")
        
        #Programa dentro de clase
        program = ProgramNodo()
        
        if has_class:
            while self.current_token() is not None and self.current_token().value != "}":
                method = self.parse_method()
                if method is not None:
                    program.statements.append(method)
            self.expected("}")
        else:
            while self.current_token() is not None:
                stament = self.parse_stament()
                if stament is not None:
                    program.statements.append(stament)
                    
        if has_namespace:
            self.expected("}")
            
        return program

    def parse_method(self):
        # Modifiers
        while self.current_token() and self.current_token().value in ["public", "private", "static"]:
            self.next_token()
            
        # Return type
        token_type = self.current_token()
        if token_type.type not in ["PR_AS_FLO", "PR_AS_INT", "PR_AS_STR"] and token_type.value != "void":
            raise SyntaxError(f"Error línea {token_type.line}: Se esperaba un tipo de retorno")
        return_type = token_type.value
        self.next_token()
        
        # Name
        name = self.expected("ID").value
        
        self.expected("(")
        parameters = []
        if self.current_token() and self.current_token().value != ")":
            if name == "Main" and self.current_token().value == "string":
                self.expected("string")
                self.expected("[")
                self.expected("]")
                p_name = self.expected("ID").value
                parameters.append(("string[]", p_name))
            else:
                while True:
                    p_type = self.current_token().value
                    self.next_token()
                    p_name = self.expected("ID").value
                    parameters.append((p_type, p_name))
                    if self.current_token() and self.current_token().value == ",":
                        self.expected(",")
                    else:
                        break
        self.expected(")")
        self.expected("{")
        
        body = []
        while self.current_token() and self.current_token().value != "}":
            stmt = self.parse_stament()
            if stmt is not None:
                body.append(stmt)
        self.expected("}")
        
        return FunctionNodo(name, return_type, parameters, body)

    def parse_stament(self):
        token = self.current_token()
        if token is None:
            return None
        
        if token.value == "return":
            self.next_token()
            ret_val = ""
            while self.current_token() and self.current_token().value != ";":
                ret_val += str(self.current_token().value) + " "
                self.next_token()
            self.expected(";")
            return ReturnNodo(ret_val.strip())
        
        if token.type in {"PR_AS_FLO","PR_AS_INT","PR_AS_STR"}:
            return self.parse_var_declaration()
        
        if token.type == "PR_D":
            return self.parse_decision()

        if token.type == "PR_L":
            return self.parse_loop()
            
        if token.type == "ID":
            return self.parse_id_statement()
        
        raise SyntaxError(
            f"Error de Sintaxis en la línea {token.line}: "
            f"Instrucción no reconocida '{token.value}'"
        )

    def parse_id_statement(self):
        token_id = self.current_token()
        var_name = token_id.value
        self.next_token()

        if var_name == "Console":
            self.expected(".")
            func_name = self.expected("ID")
            if func_name.value != "WriteLine":
                raise SyntaxError(f"Error línea {func_name.line}: Método no soportado '{func_name.value}'")
            self.expected("(")
            
            token_val = self.current_token()
            if token_val is not None and token_val.type in ["STRING", "ID"]:
                value = token_val.value
                self.next_token()
            else:
                raise SyntaxError(f"Error línea {token_val.line if token_val else '?'}: Se esperaba un string o identificador")
            
            self.expected(")")
            self.expected(";")
            return PrintNodo(value)

        token_next = self.current_token()
        if token_next is None:
            raise SyntaxError(f"Error línea {token_id.line}: Sentencia incompleta después de '{var_name}'")

        if token_next.value == "(":
            self.next_token()
            args = []
            if self.current_token() and self.current_token().value != ")":
                while True:
                    args.append(self.current_token().value)
                    self.next_token()
                    if self.current_token() and self.current_token().value == ",":
                        self.expected(",")
                    else:
                        break
            self.expected(")")
            self.expected(";")
            return FunctionCallNodo(var_name, args, is_statement=True)

        if token_next.value == "=":
            self.next_token()
            token_val = self.current_token()
            if token_val is not None:
                value = token_val.value
                self.next_token()
            else:
                raise SyntaxError(f"Error línea {token_next.line}: Se esperaba un valor después de '='")
            self.expected(";")
            return AssignationNodo(var_name, value)
            
        elif token_next.type in ["OP_COMP", "OP_SINGLE"]:
            operator = token_next.value
            self.next_token()
            
            right_value = None
            if operator in ["+=", "-=", "*=", "/="]:
                token_right = self.current_token()
                if token_right is not None and token_right.type in ["ID", "INT", "FLOAT", "STRING"]:
                    right_value = token_right.value
                    self.next_token()
                else:
                    raise SyntaxError(f"Error línea {token_next.line}: Se esperaba un valor para el operador '{operator}'")
            
            self.expected(";")
            return IncrementoNodo(var_name, operator, right_value)
        else:
            raise SyntaxError(f"Error línea {token_next.line}: Sentencia no reconocida después del identificador '{var_name}'")

    #-------HELPERS-------#
    def parse_condition(self):
        
        #Verificamos token left
        token_left = self.current_token()
        if token_left is not None and token_left.type in ["ID","INT","FLOAT","STRING","PR_V"]:
            left_value = token_left.value
            self.next_token()
        else:
            raise SyntaxError(
                f"Error línea {token_left.line if token_left else '?'}: Se esperaba un operador ID, INT, FLOAT, STRING o booleano"
            )

        #Verificamos operador
        token_op = self.current_token()
        if token_op is not None and token_op.type in ["OP_DOUBLE","OP_SINGLE"]:
            operator = token_op.value
            self.next_token()
        else:
            raise SyntaxError(
                f"Error línea {token_op.line if token_op else '?'}: Se esperaba un operador (==, <, >, etc.)"
            )
        # Verificamos token right
        token_right = self.current_token()
        if token_right is not None and token_right.type in ["ID","INT","FLOAT","STRING","PR_V"]:
            right_value = token_right.value
            self.next_token()
        else:
            raise SyntaxError(
                f"Error línea {token_right.line if token_right else '?'}: Se esperaba un operador ID, INT, FLOAT, STRING o booleano"
            )
        return ConditionNodo(left_value,operator,right_value)

    def parse_incremento(self):
        # 1. Identificador
        token_left = self.current_token()
        if token_left is not None and token_left.type == "ID":
            left_value = token_left.value
            self.next_token()
        else:
            raise SyntaxError(
                f"Error línea {token_left.line if token_left else '?'}: Se esperaba un identificador para el incremento"
            )

        # 2. Operador
        token_op = self.current_token()
        if token_op is not None and token_op.type in ["OP_COMP", "OP_SINGLE"]:
            operator = token_op.value
            self.next_token()
        else:
            raise SyntaxError(
                f"Error línea {token_op.line if token_op else '?'}: Se esperaba un operador de incremento o asignación compuesta"
            )

        # 3. Valor derecho (si aplica)
        right_value = None
        if operator in ["+=", "-=", "*=", "/="]:
            token_right = self.current_token()
            if token_right is not None and token_right.type in ["ID", "INT", "FLOAT", "STRING"]:
                right_value = token_right.value
                self.next_token()
            else:
                raise SyntaxError(
                    f"Error línea {token_right.line if token_right else '?'}: Se esperaba un valor para el incremento compuesto"
                )

        return IncrementoNodo(left_value, operator, right_value)

    def parse_case(self):
        self.expected("case")
        value = self.current_token().value
        self.next_token()
        self.expected(":")
        token_actual = self.current_token()
        statements = []
        while token_actual is not None and token_actual.value != "break":
            staments = self.parse_stament()
            statements.append(staments)
            token_actual = self.current_token()
        self.expected("break")
        self.expected(";")
        return CaseNodo(value,statements)
        
        
    #-------EXPRESIONES-------#

    def parse_var_declaration(self):
        
        #Tipo
        token_type = self.current_token()
        var_type = token_type.value
        self.next_token()
        
        # Nombre 
        token_name = self.expected("ID")
        var_name = token_name.value
        
        # Regla
        value = None
        token_actual = self.current_token()
        if token_actual is not None and token_actual.value != ";":
            self.expected("=")
            val_token = self.current_token()
            self.next_token()
            if self.current_token() and self.current_token().value == "(":
                self.next_token()
                args = []
                if self.current_token() and self.current_token().value != ")":
                    while True:
                        args.append(self.current_token().value)
                        self.next_token()
                        if self.current_token() and self.current_token().value == ",":
                            self.expected(",")
                        else:
                            break
                self.expected(")")
                value = FunctionCallNodo(val_token.value, args)
            else:
                value = val_token.value
            
        self.expected(";")
        return VarDeclarationNodo(var_type,var_name,value)
    


    def parse_decision(self):
        
        # Vemos que tipo de condicional es
        keyword = self.current_token().value
        self.next_token()

        # si es if
        if keyword == "if":
            self.expected("(")
            condition = self.parse_condition()
            self.expected(")")
            self.expected("{")
            true_bloque = []    
            token_actual = self.current_token()
            while token_actual is not None and token_actual.value != "}":
                stament = self.parse_stament()
                if stament is not None:
                    true_bloque.append(stament)
                token_actual = self.current_token()
            self.expected("}")
            
            false_bloque = None
            token_actual = self.current_token()
            if token_actual is not None and token_actual.value == "else":
                self.next_token() 
                self.expected("{")
                false_bloque = []
                token_actual = self.current_token()
                while token_actual is not None and token_actual.value != "}":
                    stament = self.parse_stament()
                    if stament is not None:
                        false_bloque.append(stament)
                    token_actual = self.current_token()
                self.expected("}")

            return DecisionNodo(keyword,condition,true_bloque, false_bloque)

        if keyword == "switch":
            self.expected("(")
            token_var = self.expected("ID")
            variable = token_var.value
            self.expected(")")
            self.expected("{")
            cases = []
            default_block = None
            token_actual = self.current_token()
            while token_actual is not None and token_actual.value != "}":
                if token_actual.value == "case":
                    case = self.parse_case()
                    if case is not None:
                        cases.append(case)
                elif token_actual.value == "default":
                    self.expected("default")
                    self.expected(":")
                    default_block = []
                    token_act = self.current_token()
                    while token_act is not None and token_act.value not in ["}", "break"]:
                        stament = self.parse_stament()
                        if stament is not None:
                            default_block.append(stament)
                        token_act = self.current_token()
                    if self.current_token().value == "break":
                        self.expected("break")
                        self.expected(";")
                else:
                    raise SyntaxError(f"Error línea {token_actual.line}: Se esperaba 'case' o 'default', pero se encontró '{token_actual.value}'")
                token_actual = self.current_token()
            self.expected("}")
            return SwitchNodo(variable, cases, default_block)
        


    def parse_loop(self):
        keyword = self.current_token().value
        self.next_token()
        
        #Si es for
        if keyword == "for":
            self.expected("(")

            # inicializacion
            token_actual = self.current_token()
            if token_actual is not None and token_actual.type in ["PR_AS_INT"]:
                initialization = self.parse_var_declaration()
            elif token_actual is not None and token_actual.type in ["ID"]:
                var_name = token_actual.value
                self.next_token()
                self.expected("=")
                value = self.current_token().value
                self.next_token()
                self.expected(";")
                initialization = AssignationNodo(var_name, value)
            else:
                raise SyntaxError(
                    f"Error línea {token_actual.line if token_actual else '?'}: Se esperaba una declaracion o inicializacion para el for"
                )
            
            #condicion
            condition = self.parse_condition()
            self.expected(";")
            
            #incremento
            incremento = self.parse_incremento()
            self.expected(")")
            self.expected("{")
            loop_block = []
             
            token_actual = self.current_token()
            while token_actual is not None and token_actual.value != "}":
                stament = self.parse_stament()
                if stament is not None:
                    loop_block.append(stament)
                token_actual = self.current_token()
                
            self.expected("}")
            return ForNodo(initialization, condition, incremento, loop_block)
        
            
        # Si es while 
        if keyword == "while":
            self.expected("(")
            condition = self.parse_condition()
            self.expected(")")
            self.expected("{")
            loop_block = []

            token_actual = self.current_token()
            while token_actual is not None and token_actual.value != "}":
                stament = self.parse_stament()
                if stament is not None:
                    loop_block.append(stament)
                token_actual = self.current_token()
            self.expected("}")
            return WhileNodo(condition,loop_block)

        # Si es do-while
        if keyword == "do":
            self.expected("{")
            loop_block =[]
            token_actual = self.current_token()
            while token_actual is not None and token_actual.value != "}":
                stament = self.parse_stament()
                if stament is not None:
                    loop_block.append(stament)
                token_actual = self.current_token()
            self.expected("}")
            self.expected("while")
            self.expected("(")
            condition = self.parse_condition()
            self.expected(")")
            self.expected(";")
            return DoWhileNodo(condition,loop_block)
        
            