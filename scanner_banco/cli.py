import argparse
import json
import pandas as pd
from .core import buscar_acessos_banco

# Dicionário de padrões com nível de severidade
PADROES = {
    r'\.getConnection\(': 'alta',
    r'\.createQuery\(': 'media',
    r'\.createNamedQuery\(': 'media',
    r'\.close\(': 'baixa',
    r'\bEntityManager\b': 'baixa'
}

def salvar_csv(resultados, caminho="relatorio.csv"):
    df = pd.DataFrame(resultados)
    df.to_csv(caminho, index=False, encoding="utf-8")
    print(f"\n✅ Relatório CSV gerado com sucesso: {caminho}")

def gerar_html(resultados, caminho_saida="relatorio.html"):
    html = '''<html>
    <head><meta charset="utf-8"><style>
    body { font-family: Arial; padding: 20px; background-color: #f4f4f4; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 8px; }
    th { background-color: #333; color: white; }
    tr:nth-child(even) { background-color: #eee; }
    code { background-color: #e0e0e0; padding: 2px 4px; border-radius: 4px; }
    </style></head><body>
    <h2>Relatório de Acessos ao Banco de Dados</h2>
    <table><tr><th>Arquivo</th><th>Linha</th><th>Padrão</th><th>Trecho</th><th>Severidade</th></tr>'''

    for r in resultados:
        html += f'''<tr>
            <td>{r["arquivo"]}</td>
            <td>{r["linha"]}</td>
            <td><code>{r["padrao"]}</code></td>
            <td><code>{r["trecho"]}</code></td>
            <td>{r["severidade"]}</td></tr>'''

    html += "</table></body></html>"

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ Relatório HTML gerado com sucesso: {caminho_saida}")

def salvar_json(resultados, caminho="relatorio.json"):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)
    print(f"\n✅ Relatório JSON gerado com sucesso: {caminho}")

def main():
    parser = argparse.ArgumentParser(description="Scanner de acessos ao banco de dados em arquivos Java.")
    parser.add_argument("--caminho", type=str, required=True, help="Caminho base do projeto Java.")
    parser.add_argument("--formato", choices=["html", "csv", "json"], default="html", help="Formato do relatório.")
    parser.add_argument("--saida", type=str, default="relatorio.html", help="Caminho do arquivo de saída.")
    args = parser.parse_args()

    resultados = buscar_acessos_banco(args.caminho, PADROES)

    # Geração do relatório no formato escolhido
    if args.formato == "html":
        gerar_html(resultados, args.saida)
    elif args.formato == "csv":
        salvar_csv(resultados, args.saida)
    elif args.formato == "json":
        salvar_json(resultados, args.saida)

if __name__ == "__main__":
    main()
