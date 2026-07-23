import src.tokens as token

class TokenObg:
    def __init__(self, type,value,line):
        self.type = type
        self.value = value
        self.line = line    
    
    def __repr__(self):
        return f"Token({self.type}), {self.value}, {self.line}"

class Lexer:
    def __init__(self,source_code:str):
        self.code = source_code
        self.position = 0


    def tokenizer(self):
        list_tokens =[]
        line = 1
        for match in token.TOKEN.finditer(self.code):
            tipo = match.lastgroup
            if tipo == "COMMENT":
                continue
            valor = match.group(tipo)
            if tipo == "ID_OR_KEYWORD":
                if token.PR_AS_FLO.fullmatch(valor):
                    tipo = "PR_AS_FLO"
                elif token.PR_AS_INT.fullmatch(valor):
                    tipo = "PR_AS_INT"
                elif token.PR.fullmatch(valor):
                    tipo = "PR"
                elif token.PR_D.fullmatch(valor):
                    tipo = "PR_D"
                elif token.PR_E.fullmatch(valor):
                    tipo = "PR_E"
                elif token.PR_V.fullmatch(valor):
                    tipo = "PR_V"
                elif token.PR_AS_STR.fullmatch(valor):
                    tipo = "PR_AS_STR"
                elif token.PR_L.fullmatch(valor):
                    tipo = "PR_L"
                elif token.OP_COMP.fullmatch(valor):
                    tipo = "OP_COMP"
                else:
                    tipo = "ID"
            real_line = self.code.count('\n', 0, match.start()) + 1
            list_tokens.append(TokenObg(tipo,valor,real_line))
            
        return list_tokens
            
