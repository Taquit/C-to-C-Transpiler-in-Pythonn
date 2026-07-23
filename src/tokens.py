import re

#----------Identificadores----------
ID = re.compile(r"[a-zA-Z][a-zA-Z0-9_]*")

#----------Palabras reservadas----------

#PR generales
PR = re.compile(
    r"\b(break|continue|return|class|public|private|protected|"
    r"using|namespace|const|static|new|delete)\b"
)

#PR ciclos
PR_L = re.compile(r"\b(for|while|do)\b")

# PR decisiones
PR_D = re.compile(r"\b(if|else|switch|case|foreach|goto)\b")

# PR excepciones
PR_E = re.compile(r"\b(try|catch|finally|throw)\b")

# PR booleanos y nulos
PR_V = re.compile(r"\b(true|false|null|object)\b")

# PR tipos que producen float
PR_AS_FLO = re.compile(r"\b(float|double|void|decimal)\b")

# PR tipos que producen int
PR_AS_INT = re.compile(r"\b(int|byte|sbyte|short|long|uint|bool)\b")

# PR tipos que producen string / char
PR_AS_STR = re.compile(r"\b(char|string)\b")

#----------Literales y puntuacion----------

# Operador de asignacion
ASIG = re.compile(r"=")

# Literal punto flotante
FLOAT = re.compile(r"[0-9]+\.[0-9]+")

# Literal entero
INT = re.compile(r"[0-9]+")

# Fin de sentencia
END = re.compile(r";")

# Operadores
OP = re.compile(r"==|!=|<=|>=|[+\-*<>]")

# Compuestos
OP_COMP = re.compile(r"\+\+|--|\+=|-=|\*=|\/=")



# Parentesis
PAREN = re.compile(r"[()]")

#----------Comentarios----------
COMP_P = re.compile(r"//.*|/\*[\s\S]*?\*/")

#----------Tokenizador master----------
TOKEN = re.compile(
    r"(?P<FLOAT>[0-9]+\.[0-9]+)|"               # float literals
    r"(?P<INT>[0-9]+)|"                         # integer literals
    r"(?P<STRING>\"[^\"]*\")|"                  # string literals
    r"(?P<ID_OR_KEYWORD>[a-zA-Z_][a-zA-Z0-9_]*)|" # identificadores y keywords
    r"(?P<OP_DOUBLE>==|!=|<=|>=)|"      # two-character operators
    r"(?P<OP_COMP>\+\+|--|\+=|-=|\*=|\/=)|"     # two-character operators
    r"(?P<OP_SINGLE>[=;+\-*<>()\{\}\.,\[\]])|"  # single-character tokens
    r"(?P<COMMENT>//.*|/\*[\s\S]*?\*/)"         # comments
)
