from pathlib import Path
from src.lexer import Lexer
from src.parse import Parse
from src.generator import Generator

def main():
    input_file = Path(__file__).parent/"data"/"c#_code.txt"
    if not input_file.exists():
        print(f"Error: {input_file} no existe.")
        return
    
    source_code = input_file.read_text(encoding="utf-8")
    lex = Lexer(source_code)
    tokens = lex.tokenizer()
    parser = Parse(tokens)
    ast = parser.parse()
    for token in tokens:
        print(token)

    print(ast)

    generator = Generator()
    code_cpp = generator.generate(ast)
    print(code_cpp)




if __name__ == "__main__":
    main()