from app.funcao import funcao_teste

def test_funcao_teste():
    # Testa se a função retorna a string correta
    gabarito = "Hello, World!"
    assert funcao_teste() == gabarito