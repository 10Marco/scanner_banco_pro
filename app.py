import flet as ft
import re
import os
import json
import pandas as pd

PADROES = {
    r'\.getConnection\(': 'alta',
    r'\.createQuery\(': 'media',
    r'\.createNamedQuery\(': 'media',
    r'\.close\(': 'baixa',
    r'\bEntityManager\b': 'baixa'
}

resultados_cache = []

def buscar_acessos_banco(caminho_base, padroes):
    resultados = []
    for root, _, files in os.walk(caminho_base):
        for file in files:
            if file.endswith(".java"):
                caminho_arquivo = os.path.join(root, file)
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    linhas = f.readlines()
                for i, linha in enumerate(linhas, 1):
                    for padrao, severidade in padroes.items():
                        if re.search(padrao, linha):
                            resultados.append({
                                "arquivo": os.path.relpath(caminho_arquivo, caminho_base),
                                "linha": i,
                                "padrao": padrao,
                                "trecho": linha.strip(),
                                "severidade": severidade
                            })
    return resultados

def main(page: ft.Page):
    page.title = "Scanner Banco Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.CYAN))
    page.scroll = True

    caminho_input = ft.TextField(label="Caminho do projeto Java", width=500)
    resultado_texto = ft.Text()
    tabela = ft.DataTable(columns=[
        ft.DataColumn(label=ft.Text("Arquivo")),
        ft.DataColumn(label=ft.Text("Linha")),
        ft.DataColumn(label=ft.Text("Padrão")),
        ft.DataColumn(label=ft.Text("Trecho")),
        ft.DataColumn(label=ft.Text("Severidade"))
    ])

    def get_icone_severidade(nivel):
        cores = {
            "alta": ft.colors.RED,
            "media": ft.colors.AMBER,
            "baixa": ft.colors.GREEN
        }
        icones = {
            "alta": ft.Icons.WARNING,
            "media": ft.Icons.REPORT_GMAILERRORRED,
            "baixa": ft.Icons.CHECK_CIRCLE
        }
        return ft.Icon(name=icones[nivel], color=cores[nivel])

    def executar_scan(e):
        caminho = caminho_input.value.strip()
        if not caminho or not os.path.exists(caminho):
            resultado_texto.value = "❌ Caminho inválido."
            page.update()
            return

        tabela.rows.clear()
        resultados = buscar_acessos_banco(caminho, PADROES)
        resultados_cache.clear()
        resultados_cache.extend(resultados)

        for r in resultados:
            tabela.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(r["arquivo"])),
                ft.DataCell(ft.Text(str(r["linha"]))),
                ft.DataCell(ft.Text(r["padrao"])),
                ft.DataCell(ft.Text(r["trecho"])),
                ft.DataCell(get_icone_severidade(r["severidade"]))
            ]))

        resultado_texto.value = f"🔍 {len(resultados)} possíveis acessos encontrados."
        page.update()

    def salvar_com_dialogo(e, tipo):
        def handle_result(ev: ft.FilePickerResultEvent):
            if ev.path:
                if tipo == "csv":
                    pd.DataFrame(resultados_cache).to_csv(ev.path, index=False, encoding="utf-8")
                    resultado_texto.value = "📁 CSV exportado com sucesso."
                elif tipo == "json":
                    with open(ev.path, "w", encoding="utf-8") as f:
                        json.dump(resultados_cache, f, ensure_ascii=False, indent=4)
                    resultado_texto.value = "📁 JSON exportado com sucesso."
                elif tipo == "html":
                    html = '''<html>
                    <head><meta charset="utf-8"><style>
                    body { font-family: Arial; background: #121212; color: #eee; padding: 20px; }
                    table { width: 100%; border-collapse: collapse; }
                    th, td { padding: 8px; border: 1px solid #444; }
                    th { background: #222; }
                    tr:nth-child(even) { background: #1e1e1e; }
                    </style></head><body>
                    <h2>Relatório</h2><table><tr><th>Arquivo</th><th>Linha</th><th>Padrão</th><th>Trecho</th><th>Severidade</th></tr>'''
                    for r in resultados_cache:
                        html += f'''<tr><td>{r["arquivo"]}</td><td>{r["linha"]}</td><td>{r["padrao"]}</td><td>{r["trecho"]}</td><td>{r["severidade"]}</td></tr>'''
                    html += "</table></body></html>"
                    with open(ev.path, "w", encoding="utf-8") as f:
                        f.write(html)
                    resultado_texto.value = "📁 HTML exportado com sucesso."
                page.update()

        file_picker.save_file(file_name=f"relatorio.{tipo}")

    def alternar_tema(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.update()

    def resultado_dialogo(e: ft.FilePickerResultEvent):
        if e.path:
            caminho_input.value = e.path
            page.update()

    file_picker = ft.FilePicker(on_result=resultado_dialogo)
    page.overlay.append(file_picker)

    def selecionar_diretorio(e):
        file_picker.get_directory_path()

    # Interface
    page.add(
        ft.Column([
            ft.Row([
                ft.Text("🔍 Scanner Banco Pro", size=30, weight="bold"),
                ft.IconButton(ft.Icons.BRIGHTNESS_6, tooltip="Alternar tema", on_click=alternar_tema),
            ]),
            ft.Row([
                caminho_input,
                ft.IconButton(ft.Icons.FOLDER_OPEN, tooltip="Selecionar pasta", on_click=selecionar_diretorio),
            ]),
            ft.Row([
                ft.ElevatedButton("Executar Scan", on_click=executar_scan),
                ft.ElevatedButton("📥 Exportar CSV", on_click=lambda e: salvar_com_dialogo(e, "csv")),
                ft.ElevatedButton("📥 Exportar JSON", on_click=lambda e: salvar_com_dialogo(e, "json")),
                ft.ElevatedButton("📥 Exportar HTML", on_click=lambda e: salvar_com_dialogo(e, "html")),
            ]),
            resultado_texto,
            tabela
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)