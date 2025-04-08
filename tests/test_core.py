import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scanner_banco.core import buscar_acessos_banco

def test_busca_padrao_getConnection():
    caminho = "scanner_banco/exemplos_teste"
    padroes = [r'\.getConnection\(']
    resultados = buscar_acessos_banco(caminho, padroes)
    assert any(".getConnection(" in r["trecho"] for r in resultados), f"Nenhum resultado encontrado! Retorno: {resultados}"
