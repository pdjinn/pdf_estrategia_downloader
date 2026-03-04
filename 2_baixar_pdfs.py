from playwright.sync_api import sync_playwright
import time
import os
import re
import json

def obter_estado_sessao():
    """
    Tenta carregar a sessão do GitHub Secrets ou do arquivo local.
    """
    # 1. Verifica se existe um Secret do GitHub (Ambiente de Automação)
    secret_sessao = os.getenv("ESTRATEGIA_SESSION_JSON")
    if secret_sessao:
        print("🔐 Sessão carregada via GitHub Secrets.")
        with open("temp_session.json", "w") as f:
            f.write(secret_sessao)
        return "temp_session.json"
    
    # 2. Verifica se existe o arquivo local (Seu computador)
    if os.path.exists("sessao_estrategia.json"):
        print("🏠 Sessão carregada via arquivo local.")
        return "sessao_estrategia.json"
    
    return None

def baixar_disciplina(url_disciplina, nome_pasta):
    caminho_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    pasta_destino = os.path.join(caminho_downloads, nome_pasta)
    os.makedirs(pasta_destino, exist_ok=True)
    
    estado_sessao = obter_estado_sessao()
    if not estado_sessao:
        print("❌ ERRO: Nenhuma sessão encontrada!")
        print("Por favor, rode o script '1_login.py' primeiro para gerar o acesso.")
        return

    with sync_playwright() as p:
        # headless=False para você ver o robô trabalhando localmente
        browser = p.chromium.launch(headless=False)
        
        # Inicia o contexto com a sessão (local ou secret)
        context = browser.new_context(storage_state=estado_sessao)
        page = context.new_page()

        print("\nAcessando a página da matéria...")
        page.goto(url_disciplina, wait_until="domcontentloaded")
        time.sleep(4) 
        
        print(f"📂 Destino: {pasta_destino}")
        
        # Mapeia os títulos e links dos cards da página inicial
        dados_aulas = page.evaluate("""() => {
            const anchors = Array.from(document.querySelectorAll('a[href*="/aula"]'));
            const map = new Map();
            
            anchors.forEach(a => {
                let textNode = a.innerText.trim() ? a : a.closest('div, section, li');
                let linhas = (textNode ? textNode.innerText : "").split('\\n').map(l => l.trim()).filter(Boolean);
                
                let titulo = "Aula_Desconhecida";
                const idx = linhas.findIndex(l => l.toLowerCase().includes('aula'));
                
                if (idx !== -1) {
                    let aulaText = linhas[idx]; 
                    let subtitulo = "";
                    if (idx + 1 < linhas.length) {
                        const prox = linhas[idx + 1];
                        if (!prox.toLowerCase().match(/(estudei|baixad|questões|fórum|vídeo|%)/)) {
                            subtitulo = " - " + prox;
                        }
                    }
                    titulo = aulaText + subtitulo;
                }
                
                if (titulo !== "Aula_Desconhecida" || !map.has(a.href)) {
                    map.set(a.href, titulo);
                }
            });
            return Array.from(map.entries()).map(([url, titulo]) => ({ url, titulo }));
        }""")
        
        if not dados_aulas:
            print("⚠️ Não consegui encontrar os links das aulas.")
            browser.close()
            return

        dados_aulas.sort(key=lambda x: x['titulo'])
        print(f"✅ Encontrei {len(dados_aulas)} aulas! Iniciando...")

        for i, aula in enumerate(dados_aulas):
            titulo_limpo = re.sub(r'[\\/*?:"<>|]', "", aula['titulo']).strip()
            if "Aula_Desconhecida" in titulo_limpo:
                titulo_limpo = f"Aula {str(i).zfill(2)} - Título não identificado"
            
            print(f"\n[{i+1}/{len(dados_aulas)}] Acessando: '{titulo_limpo}'...")
            
            try:
                page.goto(aula['url'], wait_until="domcontentloaded")
                time.sleep(5) 

                btn_texto = page.locator("text='versão original'").first 

                if btn_texto.count() > 0:
                    tag_a = btn_texto.locator("xpath=ancestor-or-self::a").first
                    if tag_a.count() > 0:
                        link_direto = tag_a.evaluate("node => node.href")
                        
                        if "javascript" in link_direto:
                            print("⚠️ Link protegido por JS.")
                            continue
                            
                        resposta = page.context.request.get(link_direto, timeout=90000)
                        nome_final = f"{titulo_limpo}.pdf"
                        caminho_arquivo = os.path.join(pasta_destino, nome_final)
                        
                        with open(caminho_arquivo, "wb") as f:
                            f.write(resposta.body())
                        print(f"✅ Salvo: {nome_final}")
                else:
                    print("⚠️ PDF 'versão original' não disponível.")

            except Exception as e:
                print(f"❌ Erro na aula {i}: {e}")
            
            time.sleep(5)

        browser.close()
        # Limpa arquivo temporário se ele foi criado via Secret
        if estado_sessao == "temp_session.json" and os.path.exists("temp_session.json"):
            os.remove("temp_session.json")
            
        print("\n" + "="*50)
        print(f"🎉 TUDO PRONTO! Pasta: {pasta_destino}")
        print("="*50)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🦉 ROBÔ DE DOWNLOAD - ESTRATÉGIA CONCURSOS")
    print("="*50 + "\n")
    
    link = input("🔗 Cole o link da disciplina: ")
    pasta = input("📂 Nome da pasta (ex: legislação_transito): ")
    
    baixar_disciplina(link, pasta)