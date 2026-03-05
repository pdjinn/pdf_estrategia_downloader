# 🦉 Estratégia PDF Downloader

Script em Python para automatizar o download de materiais (PDFs - Versão Original) do Estratégia Concursos.

## 🛠️ Como usar este robô:

1. **Instalação:** Clone o repositório e instale as dependências:
   ```bash
   pip install -r requirements.txt
   playwright install
Primeiro Passo (Login): Rode o arquivo 1_login.py. Uma janela de navegador vai abrir. Faça seu login normalmente e aperte ENTER no terminal quando terminar. Isso criará o arquivo sessao_estrategia.json (seu acesso salvo).

Segundo Passo (Download): Rode o arquivo 2_baixar_pdfs.py. O robô pedirá o link da disciplina e o nome da pasta. Ele usará o acesso salvo anteriormente para baixar tudo automaticamente.
