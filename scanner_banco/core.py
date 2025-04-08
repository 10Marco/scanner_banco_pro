import os
import re

def buscar_acessos_banco(diretorio, padroes):
    resultados = []

    for root, _, arquivos in os.walk(diretorio):
        for nome_arquivo in arquivos:
            if nome_arquivo.endswith(".java"):
                caminho = os.path.join(root, nome_arquivo)
                with open(caminho, "r", encoding="utf-8") as arquivo:
                    linhas = arquivo.readlines()

                for num_linha, linha in enumerate(linhas, start=1):
                    for padrao, severidade in padroes.items():
                        if re.search(padrao, linha):
                            resultados.append({
                                "arquivo": caminho,
                                "linha": num_linha,
                                "padrao": padrao,
                                "trecho": linha.strip(),
                                "severidade": severidade
                            })

    return resultados
