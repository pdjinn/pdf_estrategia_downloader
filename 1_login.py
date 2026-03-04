from playwright.sync_api import sync_playwright

def salvar_sessao():
    with sync_playwright() as p:
        # Abre o navegador visível para você fazer login
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Vai para a página do Estratégia
        page.goto("https://www.estrategiaconcursos.com.br/app/login")

        print("⚠️ ATENÇÃO: Faça o login manualmente no navegador que abriu.")
        print("Quando terminar de logar e a sua área do aluno carregar, volte aqui no terminal e aperte ENTER.")
        input() # O script pausa aqui esperando você apertar Enter

        # Salva a sessão no seu computador
        context.storage_state(path="sessao_estrategia.json")
        print("✅ Sessão salva com sucesso no arquivo 'sessao_estrategia.json'!")
        
        browser.close()

if __name__ == "__main__":
    salvar_sessao()
    