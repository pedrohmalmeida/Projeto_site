import streamlit as st
import requests
import os # <--- Importante para resolver o problema de caminhos
from io import BytesIO
from PIL import Image, ImageOps

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Meu Portfólio de Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNÇÃO AUXILIAR PARA IMAGENS ---
def carregar_e_cortar_imagem(caminho_ou_url, tamanho=(400, 250), borda=0, cor_borda="black"):
    """
    Carrega uma imagem, ajusta para tamanho fixo e opcionalmente adiciona uma borda.
    Resolve problemas de caminho (Windows vs Linux/Web).
    """
    try:
        # 1. Verifica se é URL
        if caminho_ou_url.startswith("http"):
            response = requests.get(caminho_ou_url)
            img = Image.open(BytesIO(response.content))
        else:
            # --- SOLUÇÃO DO PROBLEMA DE CAMINHO ---
            # Pega o diretório onde ESTE arquivo (portfolio.py) está localizado
            diretorio_script = os.path.dirname(os.path.abspath(__file__))
            
            # Limpa o caminho que veio do dicionário (remove barras extras ou invertidas)
            # Isso permite que 'Imagens/foto.png' funcione tanto no Windows quanto Linux
            caminho_limpo = os.path.normpath(caminho_ou_url)
            
            # Junta o diretório do script com o caminho da imagem
            caminho_final = os.path.join(diretorio_script, caminho_limpo)
            
            img = Image.open(caminho_final)
        
        # 2. Aplica o corte inteligente (ImageOps.fit)
        img_processada = ImageOps.fit(img, tamanho, Image.Resampling.LANCZOS)
        
        # 3. Adiciona borda se solicitado
        if borda > 0:
            img_processada = ImageOps.expand(img_processada, border=borda, fill=cor_borda)
            
        return img_processada
    except Exception as e:
        # Dica de debug: imprime o caminho que ele tentou acessar se der erro
        print(f"Erro ao carregar imagem. Caminho tentado: {caminho_ou_url} | Erro: {e}")
        return None

# --- DADOS ---
INFO_PESSOAL = {
    "nome": "Seu Nome Completo",
    "titulo": "Cientista de Dados | Desenvolvedor Python",
    "resumo": """
    Olá! Sou apaixonado por transformar dados em soluções. 
    Aqui você encontra uma coleção dos meus projetos desenvolvidos 
    em Python e Streamlit, focados em análise de dados, machine learning e automação.
    """,
    "linkedin": "https://www.linkedin.com/in/seu-perfil",
    "github": "https://github.com/seu-usuario",
    "email": "seu.email@exemplo.com"
}

PROJETOS = [
    {
        "titulo": "Análise de Crescimento Microbiano",
        "tags": ["Streamlit", "Pandas", "Visualização", "Análise Experimental"],
        "descricao": "Um dashboard interativo que fornece ferramentas para remover ruídos de dados experimentais e calcular dados relacionados ao crescimento microbriano.",
        "link": "https://crescimento-celular-aj-dados.streamlit.app/",
        # Use sempre o caminho relativo à pasta do script (Imagens/...)
        "imagem": "Imagens/Intro_cresc_experimental.png" 
    },
    {
        "titulo": "S.Pr.E.M.E.",
        "tags": ["TCC", "Python", "EME", "TCC Engenharia"],
        "descricao": "Uma poderosa ferramenta didática que permite realizar o projeto de um evaporador de múltiplos efeitos (até 5 efeitos), com apresentação da teoria e cada etapa de cálculo.",
        "link": "https://evaporador-me.streamlit.app/",
        # Mesmo se no Windows você usava contrabarra, aqui use barra normal ou deixe o código tratar
        "imagem": "Imagens/EME.png" 
    },
    {
        "titulo": "Simulação de Biorreatores Contínuos",
        "tags": ["Python", "Excel", "Automação"],
        "descricao": "Simulação e análise de biorreatores em regime contínuo para otimização de processos fermentativos.",
        "link": "https://link-para-seu-github.com",
        "imagem": "Imagens/Dia_p_continuo.png"
    },
    {
        "titulo": "Análise de Sentimentos",
        "tags": ["NLP", "Streamlit", "API"],
        "descricao": "Aplicação que consome reviews de clientes e classifica o sentimento (Positivo/Negativo) usando NLP.",
        "link": "#",
        "imagem": "https://via.placeholder.com/400x200?text=NLP+Analysis"
    }
]

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    .project-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
    }
    h1, h2, h3 {
        font-family: 'Helvetica', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (PERFIL) ---
with st.sidebar:
    st.write("### 👤 Perfil")
    st.title(INFO_PESSOAL["nome"])
    st.markdown(f"**{INFO_PESSOAL['titulo']}**")
    st.info(INFO_PESSOAL["resumo"])
    
    st.markdown("---")
    st.write("### 📬 Contato & Redes")
    
    st.markdown(f"""
    - [👔 LinkedIn]({INFO_PESSOAL['linkedin']})
    - [💻 GitHub]({INFO_PESSOAL['github']})
    - [✉️ Email](mailto:{INFO_PESSOAL['email']})
    """)
    
    st.markdown("---")
    st.caption("Desenvolvido com Streamlit 🚀")

# --- CORPO PRINCIPAL ---

st.title("🚀 Meus Projetos")
st.markdown("Bem-vindo ao meu portfólio. Abaixo você encontra as aplicações que desenvolvi.")
st.markdown("---")

# Lógica para criar o Grid de Projetos
col1, col2 = st.columns(2, border=True)

for index, projeto in enumerate(PROJETOS):
    coluna_atual = col1 if index % 2 == 0 else col2
    
    with coluna_atual:
        with st.container():
            st.subheader(projeto["titulo"])
            
            # --- PROCESSAMENTO DE IMAGEM COM BORDA ---
            img_processada = carregar_e_cortar_imagem(
                projeto["imagem"], 
                tamanho=(400, 200), 
                borda=4, 
                cor_borda="#d3d3d3"
            )
            
            if img_processada:
                st.image(img_processada, use_container_width=True)
            else:
                st.warning(f"Imagem não encontrada: {projeto['imagem']}")
            # -------------------------------
            
            st.write(f"**Tecnologias:** {', '.join(projeto['tags'])}")
            st.write(projeto["descricao"])
            st.link_button(f"Acessar {projeto['titulo']}", projeto["link"])
            
            st.markdown("---")

# --- SEÇÃO EXTRA ---
st.header("📈 Minha Jornada")
with st.expander("Ver linha do tempo profissional"):
    st.write("""
    - **2024:** Focando em projetos de Generative AI e LLMs.
    - **2023:** Atuação como Analista de Dados Sênior.
    - **2021:** Início dos estudos em Python e Data Science.
    """)