import flet as ft
from scanner_banco.core import buscar_acessos_banco

PADROES = [
    r'\.getConnection\(',
    r'\.createQuery\(',
    r'\.createNamedQuery\(',
    r'\.close\(',
    r'\bEntityManager\b',
]

def main(page: ft.Page):
    page.title = "Scanner Banco PRO"
    page.scroll = "auto"

    caminho_input = ft.TextField(label="Caminho do Projeto", width=500)
    resultados_tabela = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Arquivo")),
            ft.DataColumn(label=ft.Text("Linha")),
            ft.DataColumn(label=ft.Text("Padrão")),
            ft.DataColumn(label=ft.Text("Trecho")),
        ],
        rows=[]
    )

    def on_scan_click(e):
        caminho = caminho_input.value
        resultados = buscar_acessos_banco(caminho, PADROES)
        resultados_tabela.rows.clear()

        for r in resultados:
            resultados_tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(r["arquivo"])),
                        ft.DataCell(ft.Text(str(r["linha"]))),
                        ft.DataCell(ft.Text(r["padrao"])),
                        ft.DataCell(ft.Text(r["trecho"])),
                    ]
                )
            )
        page.update()

    page.add(
        ft.Column([
            ft.Text("🔍 Scanner Banco PRO", size=30, weight="bold"),
            caminho_input,
            ft.ElevatedButton("Scan", on_click=on_scan_click),
            resultados_tabela
        ])
    )

ft.app(target=main)
