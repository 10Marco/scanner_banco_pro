import os
import re

PADROES_MELHORIA = {
    r'\.getConnection\(': "Encapsular em try-with-resources para evitar vazamento de conexão",
    r'System\.exit\(': "Evitar encerramento abrupto da aplicação",
    r'Thread\.sleep\(': "Avaliar se o uso é realmente necessário – pode travar a thread principal"
}

def buscar_acessos_banco(caminho_base, padroes):
    resultados = []
    for raiz, _, arquivos in os.walk(caminho_base):
        for arquivo in arquivos:
            if arquivo.endswith(".java"):
                caminho_completo = os.path.join(raiz, arquivo)
                try:
                    with open(caminho_completo, "r", encoding="utf-8") as f:
                        linhas = f.readlines()
                        for numero_linha, linha in enumerate(linhas, start=1):
                            for padrao in padroes:
                                if re.search(padrao, linha):
                                    melhoria = PADROES_MELHORIA.get(padrao, "Nenhuma sugestão definida")
                                    resultados.append({
                                        "arquivo": caminho_completo,
                                        "linha": numero_linha,
                                        "trecho": linha.strip(),
                                        "padrao": padrao,
                                        "melhoria": melhoria
                                    })
                except Exception as e:
                    print(f"Erro ao ler {caminho_completo}: {e}")
    return resultados
