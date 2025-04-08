import os
from scanner_banco.core import buscar_acessos_banco

def test_buscar_acessos_banco_tem_resultados():
    padroes = {
        r'\.getConnection\(': 'alta',
        r'\.createQuery\(': 'media'
    }
    caminho = "scanner_banco/exemplos_teste"
    resultados = buscar_acessos_banco(caminho, padroes)
    assert isinstance(resultados, list)
    if resultados:
        assert "arquivo" in resultados[0]
        assert "linha" in resultados[0]
        assert "padrao" in resultados[0]
        assert "trecho" in resultados[0]
        assert "severidade" in resultados[0]
        assert resultados[0]["severidade"] in ['alta', 'media']