from pathlib import Path
from src.lexer import Lexer
from src.parse import Parse
from src.generator import Generator
from src.semantic import SemanticAnalyzer, SemanticError

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

    # --- NUEVO: Análisis Semántico ---
    print("\n[Iniciando Análisis Semántico]")
    analyzer = SemanticAnalyzer()
    try:
        analyzer.analyzer(ast)
        print("✅ Análisis Semántico Completado: 0 Errores.")
    except SemanticError as e:
        print(f" {e}")
        return # Detenemos la compilación si hay errores de lógica
    # ---------------------------------
    generator = Generator()
    code_cpp = generator.generate(ast)
    print("\n[Código C++ Generado]")
    print(code_cpp)

    output_file = Path(__file__).parent/"data"/"c++_code.txt"
    output_file.write_text(code_cpp, encoding="utf-8")


if __name__ == "__main__":
    main()