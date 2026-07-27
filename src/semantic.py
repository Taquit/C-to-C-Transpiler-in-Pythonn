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
        
    def analyzer(self,nodo):
        nodo_type = type(nodo).__name__

        if nodo_type == "ProgramNodo":
            for statement in nodo.statement:
                self.analyzer(statement)
        elif nodo_type == "VarDeclarationNodo":
            self.sym_table.declare_variable(nodo.name,nodo.var_type)