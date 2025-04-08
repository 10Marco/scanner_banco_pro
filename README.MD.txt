# 🔍 scanner_banco_pro

![Python CI](https://github.com/10Marco/scanner_banco_pro/actions/workflows/python-ci.yml/badge.svg)

Scanner de arquivos Java para identificar possíveis acessos inseguros ao banco de dados e más práticas de programação.

---

## Propósito do projeto

- Busca por padrões de acesso ao banco em arquivos `.java`
- Geração de relatório em HTML
- Interface gráfica com Flet para análise visual dos dados
- CLI simples e funcional
- Possíveis expansões futuras - adaptação para a linguagem PHP 

---

## Formatos de saída do relatório
- 'HTML'
- 'CSV'
- 'JSON'

---

## Instalação

```bash
python -m scanner_banco.cli --caminho scanner_banco/exemplos_teste --formato csv --saida resultado.csv
git clone https://github.com/10Marco/scanner_banco_pro.git
cd scanner_banco_pro
pip install .
