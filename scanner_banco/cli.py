import argparse
from .core import buscar_acessos_banco

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
    <h2>Relatório de Acessos ao Banco de Dados</h2><table>
    <tr><th>Arquivo</th><th>Linha</th><th>Padrão</th><th>Trecho</th></tr>'''

    for r in resultados:
        html += f'''<tr>
            <td>{r["arquivo"]}</td>
            <td>{r["linha"]}</td>
            <td><code>{r["padrao"]}</code></td>
            <td><code>{r["trecho"]}</code></td></tr>'''
    html += "</table></body></html>"

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ Relatório gerado com sucesso: {caminho_saida}")

def main():
    parser = argparse.ArgumentParser(description="Scanner de acessos ao banco de dados em arquivos Java.")
    parser.add_argument("--caminho", type=str, required=True, help="Caminho base do projeto Java.")
    parser.add_argument("--saida", type=str, default="relatorio.html", help="Nome do arquivo HTML de saída.")
    args = parser.parse_args()

    PADROES = [
        r'\.getConnection\(',
        r'\.createQuery\(',
        r'\.createNamedQuery\(',
        r'\.close\(',
        r'\bEntityManager\b'
    ]

    resultados = buscar_acessos_banco(args.caminho, PADROES)
    gerar_html(resultados, args.saida)

if __name__ == "__main__":
    main()
