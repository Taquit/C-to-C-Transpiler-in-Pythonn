#----Tabla de simbolos----#
import re

class SemanticError(Exception):
    pass

class SymbolTable:
    def __init__(self):
        self.scopes = [{}] #Lista de diccionarios

    def enter_scope(self):
        self.scopes.append({}) #Entrar a un bloqe
    
    def exit_scope(self):
        self.scopes.pop() #Salir de un bloque
    
    def declare_variable(self,name,var_type):
        current_scope = self.scopes[-1]

        if name in current_scope:
            raise SemanticError(f"Error Semantico: '{name}' ya esta declarada")
        
        current_scope[name] = var_type
    
    def get_type(self,name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise SemanticError(f"Error Semantico: '{name}' no declarada")


#----Analizador Semantico----#

class SemanticAnalyzer:
    def __init__(self):
        self.sym_table = SymbolTable()
        self.current_function_return = None # Para saber qué debería retornar el 'return'
        
    def analyzer(self, nodo):
        nodo_type = type(nodo).__name__

        if nodo_type == "ProgramNodo":
            for statement in nodo.statements: # Ojo, en tu ast.py se llama statements
                self.analyzer(statement)

        elif nodo_type == "FunctionNodo":
            # Registrar la función en la tabla global
            self.sym_table.declare_variable(nodo.name, {"type": "function", "return": nodo.return_type, "params": nodo.parameters})
            
            # Entrar al bloque de la función
            self.sym_table.enter_scope()
            self.current_function_return = nodo.return_type
            
            # Registrar los parámetros como variables locales
            for p_type, p_name in nodo.parameters:
                self.sym_table.declare_variable(p_name, p_type)
                
            # Analizar el cuerpo
            for stmt in nodo.body:
                self.analyzer(stmt)
                
            self.sym_table.exit_scope()
            self.current_function_return = None

        elif nodo_type == "FunctionCallNodo":
            # Verificar si la función existe
            func_info = self.sym_table.get_type(nodo.name)
            if type(func_info) is not dict or func_info.get("type") != "function":
                raise SemanticError(f"Error Semántico: '{nodo.name}' no es una función reconocida.")
            
            # Verificar cantidad de argumentos
            if len(nodo.arguments) != len(func_info["params"]):
                raise SemanticError(f"Error Semántico: '{nodo.name}' esperaba {len(func_info['params'])} argumentos, pero recibió {len(nodo.arguments)}.")
            
            # Analizar cada argumento (recursivo)
            for arg in nodo.arguments:
                self.analyzer(arg)
            
            return func_info["return"]

        elif nodo_type == "VarDeclarationNodo":
            if nodo.value is not None:
                val_type = self.analyzer(nodo.value)
                # Validación semántica: El tipo asignado debe coincidir (o ser compatible)
                # (Simplificado: asume que 'INT' es 'int', 'FLOAT' es 'float', 'STRING' es 'string')
                if val_type and val_type.lower() != nodo.var_type.lower() and val_type not in ["INT", "FLOAT", "STRING"]:
                    pass # En un compilador real aquí habría más reglas, lo dejamos flexible por ahora
            
            self.sym_table.declare_variable(nodo.var_name, nodo.var_type)

        elif nodo_type == "AssignationNodo":
            # Verificar que la variable exista
            var_type = self.sym_table.get_type(nodo.var_name)
            # Analizar el valor derecho
            self.analyzer(nodo.value)

        elif nodo_type == "ReturnNodo":
            ret_type = self.analyzer(nodo.value)
            # Validar que no haya return fuera de una función
            if self.current_function_return is None:
                raise SemanticError("Error Semántico: Sentencia 'return' fuera de una función.")

        elif nodo_type == "IdentifierNodo":
            # Si se usa una variable, debe existir
            return self.sym_table.get_type(nodo.name)

        elif nodo_type == "LiteralNodo":
            # Devuelve su tipo (INT, FLOAT, STRING)
            return nodo.val_type

        elif nodo_type == "BinOpNodo":
            left_type = self.analyzer(nodo.left)
            right_type = self.analyzer(nodo.right)
            # Si uno de los dos es STRING y se están sumando, el resultado es STRING (concatenación)
            if (left_type == "STRING" or right_type == "STRING") and nodo.operator == "+":
                return "STRING"
            # Si intentan restar o multiplicar strings, ¡Error!
            if (left_type == "STRING" or right_type == "STRING") and nodo.operator in ["-", "*", "/"]:
                raise SemanticError("Error Semántico: No se pueden realizar operaciones matemáticas con cadenas de texto.")
            return left_type # Simplificado: asume que devuelve el tipo izquierdo

        elif nodo_type == "PrintNodo":
            self.analyzer(nodo.value)
            
        elif nodo_type in ["DecisionNodo", "WhileNodo", "DoWhileNodo", "ForNodo"]:
            # Entrar a un nuevo scope (bloque) para variables locales
            self.sym_table.enter_scope()
            
            # Si es un FOR, analizar primero su inicialización (ej. int i = 0)
            if hasattr(nodo, 'initialization') and nodo.initialization:
                self.analyzer(nodo.initialization)
                
            # Analizar la condición (ej. i < 10)
            if hasattr(nodo, 'condition') and nodo.condition:
                self.analyzer(nodo.condition)
                
            # Si es un FOR, analizar su incremento (ej. i++)
            if hasattr(nodo, 'increment') and nodo.increment:
                self.analyzer(nodo.increment) # Aunque no lo definimos completo arriba, evita que se lo salte
                
            block = getattr(nodo, 'true_block', getattr(nodo, 'loop_block', []))
            for stmt in block:
                self.analyzer(stmt)
                
            self.sym_table.exit_scope()
