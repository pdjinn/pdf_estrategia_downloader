# 🦉 Estratégia PDF Downloader

Script automatizado em **Python** para facilitar a organização e o download de materiais (PDFs - Versão Original) da plataforma **Estratégia Concursos**.

## ✨ Funcionalidades

* **Login Persistente:** Salva sua sessão para evitar logins manuais repetitivos e barreiras de segurança.
* **Identificação Inteligente:** Captura automaticamente o título da aula e o tema (Ex: *Aula 00 - Princípios*).
* **Organização Automática:** Cria pastas específicas para cada matéria direto na sua pasta de **Downloads**.
* **Nomenclatura Sequencial:** Garante que os arquivos fiquem ordenados corretamente no seu computador.

---

## 🛠️ Pré-requisitos

Antes de começar, você precisará ter o Python instalado em sua máquina. Além disso, o robô utiliza a biblioteca **Playwright** para navegar no site.

---

## 🚀 Instalação e Configuração

1. **Clone o repositório:**
```bash
git clone https://github.com/pdjinn/pdf_estrategia_downloader.git
cd pdf_estrategia_downloader

```


2. **Crie e ative um ambiente virtual (recomendado):**
```bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate

```


3. **Instale as dependências:**
```bash
pip install -r requirements.txt
playwright install chromium

```



---

## 📖 Como Usar

O projeto é dividido em dois passos simples:

### Passo 1: Salvar seu Acesso (Login)

Execute o script de login para gerar o seu "crachá" de acesso digital:

```bash
python 1_login.py

```

* Uma janela do navegador será aberta.
* Faça seu login manualmente no site do Estratégia.
* Após entrar na sua área do aluno, volte ao terminal e aperte **ENTER**.
* Isso criará o arquivo `sessao_estrategia.json`. **Você só precisa fazer isso uma vez (ou quando seu acesso expirar).**

### Passo 2: Baixar os Materiais

Com a sessão salva, agora você pode baixar as matérias que desejar:

```bash
python 2_baixar_pdfs.py

```

* O robô solicitará o **link da página principal** da disciplina.
* Digite o **nome da pasta** onde deseja salvar os arquivos (ex: `Direito_Constitucional`).
* O robô fará o resto! Os arquivos aparecerão em: `Downloads/Nome_da_Materia`.

---

## 🛡️ Segurança e Privacidade

> [!IMPORTANT]
> O arquivo `sessao_estrategia.json` contém os tokens da sua conta e **não deve ser compartilhado**. Este projeto já vem configurado com um arquivo `.gitignore` para impedir que suas credenciais sejam enviadas para o GitHub por acidente.

---

## ⚖️ Aviso Legal

Este projeto tem fins estritamente **educacionais e de uso pessoal**. O autor não se responsabiliza pelo uso indevido da ferramenta. Certifique-se de respeitar os Termos de Uso da plataforma Estratégia Concursos.

---
