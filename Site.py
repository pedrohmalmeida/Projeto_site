import streamlit as st
import requests
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
    """
    try:
        # 1. Abre a imagem dependendo se é URL ou arquivo local
        if caminho_ou_url.startswith("http"):
            response = requests.get(caminho_ou_url)
            img = Image.open(BytesIO(response.content))
        else:
            # Para arquivos locais
            img = Image.open(caminho_ou_url)
        
        # 2. Aplica o corte inteligente (ImageOps.fit)
        img_processada = ImageOps.fit(img, tamanho, Image.Resampling.LANCZOS)
        
        # 3. Adiciona borda se solicitado (Novo passo)
        if borda > 0:
            img_processada = ImageOps.expand(img_processada, border=borda, fill=cor_borda)
            
        return img_processada
    except Exception as e:
        print(f"Erro ao carregar imagem {caminho_ou_url}: {e}")
        return None

# --- DADOS (FUTURAMENTE VOCÊ VAI EDITAR AQUI) ---
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
        "imagem": "Projeto_site\Imagens/Intro_cresc_experimental.png" 
    },
    {
        "titulo": "S.Pr.E.M.E.",
        "tags": ["TCC", "Python", "EME", "TCC Engenharia"],
        "descricao": "Uma poderosa ferramenta didática que permite realizar o projeto de um evaporador de múltiplos efeitos (até 5 efeitos), com apresentação da teoria e cada etapa de cálculo.",
        "link": "https://evaporador-me.streamlit.app/",
        "imagem": "Projeto_site\Imagens\EME.png"
    },
    {
        "titulo": "Simulação de Biorreatores Contínuos",
        "tags": ["Python", "Excel", "Automação"],
        "descricao": "Simulação e análise de biorreatores em regime contínuo para otimização de processos fermentativos.",
        "link": "https://link-para-seu-github.com",
        "imagem": "Projeto_site/Imagens/Dia_p_continuo.png"
    },
    {
        "titulo": "Análise ",
        "tags": [],
        "descricao": "",
        "link": "#",
        "imagem": ""
    }
]

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    /* Estilização para os cards de projetos */
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
    /* Ajuste de fontes */
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

# Lógica para criar o Grid de Projetos (2 por linha)
col1, col2 = st.columns(2, border=True)

for index, projeto in enumerate(PROJETOS):
    coluna_atual = col1 if index % 2 == 0 else col2
    
    with coluna_atual:
        with st.container():
            st.subheader(projeto["titulo"])
            
            # --- PROCESSAMENTO DE IMAGEM COM BORDA ---
            # Ajustei a altura de volta para 200px para ficar mais proporcional com a borda
            # borda=4 adiciona 4 pixels de cada lado
            # cor_borda="#d3d3d3" é um cinza claro elegante
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

# --- SEÇÃO EXTRA (OPCIONAL) ---
st.header("📈 Minha Jornada")
with st.expander("Ver linha do tempo profissional"):
    st.write("""
    - **2024:** Focando em projetos de Generative AI e LLMs.
    - **2023:** Atuação como Analista de Dados Sênior.
    - **2021:** Início dos estudos em Python e Data Science.
    """)