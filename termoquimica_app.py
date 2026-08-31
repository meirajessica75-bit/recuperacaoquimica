import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import random
from datetime import datetime

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Recuperação de Química: Termoquímica Interativa",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminho para salvar os resultados
CSV_PATH = "resultados_estudantes.csv"

# Banco de 10 questões contextualizadas e grounded nas fontes
QUESTOES_BANCO = [
    {
        "id": 1,
        "pergunta": "De acordo com o texto sobre o Filtro de Barro (pág. 39), por que a água em seu interior se mantém sempre 'fresca'?",
        "opcoes": [
            "A cerâmica microporosa permite que uma pequena quantidade de água passe para o lado externo e evapore, absorvendo calor da água interna (um processo endotérmico).",
            "O filtro de barro possui um isolamento térmico de cerâmica que impede totalmente a entrada de calor externo, mantendo a água fria por condução térmica.",
            "A reação química entre a argila do filtro e os sais minerais da água libera energia em forma de frio, resfriando o sistema de forma espontânea.",
            "A água sofre uma reação de combustão lenta ao entrar em contato com os microporos do barro, resultando em uma reação exotérmica que estabiliza a temperatura."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 39"
    },
    {
        "id": 2,
        "pergunta": "Com base no texto sobre o Sistema de Arrefecimento de veículos (pág. 37 e 40), qual é a relação desse sistema com os conceitos da termoquímica?",
        "opcoes": [
            "A queima de combustíveis é uma reação exotérmica altamente energética que libera calor e aquece o motor; a água de arrefecimento deve absorver esse calor para evitar que as peças derretam.",
            "O motor do carro funciona por meio de uma reação endotérmica que resfria naturalmente as peças, e o sistema de arrefecimento serve para fornecer o calor necessário para a ignição acontecer.",
            "O sistema de arrefecimento utiliza a evaporação do combustível no motor para absorver calor, mimetizando perfeitamente o funcionamento de um filtro de barro de cerâmica.",
            "A queima de combustíveis é uma transformação física endotérmica, e a água do radiador serve para resfriar os gases de escape que saem a altas pressões."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 37, 40"
    },
    {
        "id": 3,
        "pergunta": "Os sacos de resfriamento instantâneo, usados em práticas esportivas para tratar lesões, utilizam a dissolução do nitrato de amônio (NH₄NO₃) em água (pág. 40). Esse processo é classificado como:",
        "opcoes": [
            "Endotérmico (ΔH ≈ 26 kJ/mol), pois a dissolução absorve calor do meio, resfriando o sistema e podendo atingir uma temperatura de cerca de -15 °C.",
            "Exotérmico (ΔH ≈ -26 kJ/mol), pois a quebra das ligações iônicas do sal libera energia térmica que gela a água instantaneamente.",
            "Isotérmico, pois a temperatura se mantém perfeitamente constante e o resfriamento é provocado apenas pela compressão física do saco plástico.",
            "Combustão controlada, na qual a água líquida atua como comburente e o nitrato de amônio sólido como combustível, absorvendo energia luminosa."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 40"
    },
    {
        "id": 4,
        "pergunta": "Segundo o texto explicativo da página 40 sobre as sensações térmicas nos experimentos, como se classifica a dissolução do cloreto de cálcio (CaCl₂) em água e por quê?",
        "opcoes": [
            "Endotérmico, pois nela observa-se um resfriamento do sistema decorrente da necessidade de ganho de energia para que ocorra a dissolução (ΔH > 0).",
            "Exotérmico, pois nela ocorre liberação ativa de calor, que é observada pelo aquecimento perceptível do béquer ao toque da mão (ΔH < 0).",
            "Endotérmico, porque a energia térmica 'sai do sistema' e se dissipa na atmosfera sob a forma de radiação infravermelha visível.",
            "Exotérmico, porque a reação consome a água do béquer para formar uma liga metálica sólida e liberar hidrogênio gasoso inflamável."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 40"
    },
    {
        "id": 5,
        "pergunta": "Analisando os gráficos de variação de entalpia (H) em relação ao caminho da reação (pág. 40), o que diferencia um gráfico de reação exotérmica de um gráfico de reação endotérmica?",
        "opcoes": [
            "Na reação exotérmica, a entalpia dos reagentes (H_R) é maior que a dos produtos (H_P), logo ΔH < 0; na endotérmica, a entalpia dos produtos (H_P) é maior que a dos reagentes (H_R), logo ΔH > 0.",
            "Na reação exotérmica, o gráfico é uma linha reta ascendente sem pico de energia; na endotérmica, o gráfico possui um pico correspondente ao complexo ativado.",
            "Na reação endotérmica, a entalpia final é nula pois toda a energia é consumida; na exotérmica, a entalpia final dobra devido à geração contínua de calor.",
            "Na reação exotérmica, o ΔH é positivo porque há ganho de energia pelo meio ambiente; na endotérmica, o ΔH é negativo porque o sistema perde energia interna."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 40"
    },
    {
        "id": 6,
        "pergunta": "Na página 41, são apresentadas equações termoquímicas. Sabendo que o calor pode ser representado dentro da equação, como identificamos se a reação é endotérmica ou exotérmica?",
        "opcoes": [
            "Se o calor estiver somado aos reagentes (ex: 2 NH3 + 22 kcal -> N2 + 3 H2), o processo é endotérmico; se estiver somado aos produtos (ex: C + 2 H2 -> CH4 + 18 kcal), é exotérmico.",
            "Se o calor estiver somado aos reagentes, a reação é exotérmica porque os reagentes liberam essa energia; se estiver nos produtos, é endotérmica porque foi absorvida.",
            "Toda equação que apresenta valores numéricos de energia em calorias (kcal) representa reações exotérmicas, enquanto as em quilojoules (kJ) são endotérmicas.",
            "Reações endotérmicas são representadas por sinais negativos ao lado do calor somado aos reagentes, demonstrando a ausência de entalpia nos produtos."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 41 & Vídeo"
    },
    {
        "id": 7,
        "pergunta": "Na videoaula do Brasil Escola, o professor Choven faz uma analogia divertida com compras de roupas em um shopping para explicar a Lei de Hess. O que essa analogia ilustra?",
        "opcoes": [
            "Que não importa o caminho ou as voltas que a reação dê (como a mulher andando pelo shopping e o homem indo direto), se o estado inicial e o final forem os mesmos, a variação de entalpia total será a mesma.",
            "Que as reações do tipo femininas gastam mais energia (entalpia) do que as reações masculinas devido ao número de etapas intermediárias necessárias.",
            "Que a Lei de Hess só é aplicável para processos que ocorrem em ambientes fechados e sob pressão constante de 1 ATM, semelhantes a um shopping center.",
            "Que o caminho mais curto sempre consome menos calor de reação, enquanto caminhos mais longos alteram irreversivelmente a entalpia final do sistema."
        ],
        "correta": 0,
        "referencia": "Videoaula Brasil Escola"
    },
    {
        "id": 8,
        "pergunta": "De acordo com as considerações importantes sobre equações termoquímicas (pág. 41), o que acontece com a variação de entalpia (ΔH) quando invertemos o sentido de uma reação química?",
        "opcoes": [
            "O valor numérico de ΔH permanece o mesmo, mas o sinal algébrico é invertido (por exemplo, se era negativo, passa a ser positivo).",
            "A reação deixa de possuir valor de entalpia e o ΔH torna-se nulo, pois os reagentes e produtos se cancelam mutuamente.",
            "O valor numérico de ΔH é duplicado devido ao esforço cinético necessário para forçar a reação a ocorrer no sentido contrário.",
            "O sinal permanece o mesmo, mas a unidade de medida muda de quilojoules (kJ) para quilocalorias (kcal) para diferenciar a reação inversa."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 41"
    },
    {
        "id": 9,
        "pergunta": "No início do vídeo do Brasil Escola, o professor Choven define o termo fundamental da termoquímica. Segundo ele, o que é entalpia (H)?",
        "opcoes": [
            "Entalpia é a quantidade de calor contida em um sistema.",
            "Entalpia é a velocidade com que uma reação química consome calor.",
            "Entalpia é a força eletromagnética gerada pela movimentação de elétrons nas ligações químicas.",
            "Entalpia é a temperatura absoluta de um gás ideal medida na escala Kelvin."
        ],
        "correta": 0,
        "referencia": "Videoaula Brasil Escola"
    },
    {
        "id": 10,
        "pergunta": "Na videoaula, o professor Choven destaca que o valor da variação de entalpia (ΔH) de uma reação pode ser alterado por alguns fatores importantes. Quais são eles?",
        "opcoes": [
            "Estado físico de reagente/produto, estado alotrópico, temperatura e concentração (quantidade de matéria).",
            "Pressão atmosférica, altitude geográfica, velocidade do vento e tipo de catalisador químico utilizado.",
            "Massa molar do soluto, volume do recipiente, pH da solução e condutividade elétrica do meio.",
            "Cor dos reagentes, presença de luz solar direta, umidade do ar e rotação da terra."
        ],
        "correta": 0,
        "referencia": "Videoaula Brasil Escola"
    }
]

# Inicializar estados da sessão do Streamlit
if "etapa" not in st.session_state:
    st.session_state.etapa = "Identificação"
if "nome" not in st.session_state:
    st.session_state.nome = ""
if "ano" not in st.session_state:
    st.session_state.ano = "2º Ano"
if "serie" not in st.session_state:
    st.session_state.serie = ""
if "questoes_sorteadas" not in st.session_state:
    st.session_state.questoes_sorteadas = []
if "respostas_estudante" not in st.session_state:
    st.session_state.respostas_estudante = {}
if "tentativas" not in st.session_state:
    st.session_state.tentativas = 0
if "aluno_submeteu" not in st.session_state:
    st.session_state.aluno_submeteu = False

# Função para sortear questões e embaralhar alternativas (evitando cópia)
def inicializar_quiz():
    # Sorteia 5 questões únicas das 10 disponíveis
    questoes = random.sample(QUESTOES_BANCO, 5)
    questoes_preparadas = []
    
    for q in questoes:
        # Copiar opções para não alterar a lista original
        opcoes_originais = list(q["opcoes"])
        correta_original = opcoes_originais[q["correta"]]
        
        # Embaralhar as alternativas
        opcoes_embaralhadas = list(opcoes_originais)
        random.shuffle(opcoes_embaralhadas)
        
        # Encontrar o novo índice da alternativa correta
        nova_correta = opcoes_embaralhadas.index(correta_original)
        
        questoes_preparadas.append({
            "id": q["id"],
            "pergunta": q["pergunta"],
            "opcoes": opcoes_embaralhadas,
            "correta": nova_correta,
            "referencia": q["referencia"]
        })
    st.session_state.questoes_sorteadas = questoes_preparadas
    st.session_state.respostas_estudante = {}
    st.session_state.aluno_submeteu = False

# Função para plotar o diagrama de entalpia dinamicamente
def plotar_diagrama(tipo_reacao, nome_reacao):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Definir coordenadas para desenhar a curva de entalpia
    # Reagentes -> Complexo Ativado (pico) -> Produtos
    if tipo_reacao == "Exotérmica":
        y_reag = 80
        y_pico = 120
        y_prod = 30
        cor_curva = "#d9534f"  # Vermelho para exotérmica
        cor_seta = "#c9302c"
    else:  # Endotérmica
        y_reag = 30
        y_pico = 100
        y_prod = 80
        cor_curva = "#0275d8"  # Azul para endotérmica
        cor_seta = "#025aa5"
        
    x = np.linspace(0, 10, 100)
    # Curva suave ligando Reagentes, Pico (Complexo Ativado) e Produtos
    # Usando polinômio simples para desenhar a curva
    y = np.zeros_like(x)
    for i, xi in enumerate(x):
        if xi < 3:
            y[i] = y_reag
        elif xi > 7:
            y[i] = y_prod
        else:
            # Curva de transição (senoidal suave) para o pico do complexo ativado
            t = (xi - 3) / 4  # Vai de 0 a 1
            # Forma de parábola invertida para o pico que começa em y_reag, vai a y_pico no meio, e termina em y_prod
            base = y_reag + (y_prod - y_reag) * t
            pico = 4 * (y_pico - max(y_reag, y_prod)) * t * (1 - t)
            y[i] = base + pico

    # Plotar a curva
    ax.plot(x, y, color=cor_curva, linewidth=3, label="Caminho da Reação")
    
    # Linhas pontilhadas horizontais para reagentes e produtos
    ax.axhline(y=y_reag, xmin=0.05, xmax=0.3, color="gray", linestyle="--")
    ax.axhline(y=y_prod, xmin=0.7, xmax=0.95, color="gray", linestyle="--")
    
    # Rótulos dos patamares
    ax.text(0.5, y_reag + 3, "Reagentes", fontsize=10, fontweight="bold", color="#333333")
    ax.text(7.5, y_prod + 3, "Produtos", fontsize=10, fontweight="bold", color="#333333")
    ax.text(5, y_pico + 3, "Complexo Ativado", fontsize=9, fontstyle="italic", color="#555555", ha="center")
    
    # Adicionar seta de Delta H (Variação de Entalpia)
    if tipo_reacao == "Exotérmica":
        # Seta apontando para baixo
        ax.annotate("", xy=(8.5, y_prod), xytext=(8.5, y_reag),
                    arrowprops=dict(facecolor=cor_seta, edgecolor=cor_seta, shrink=0.05, width=2, headwidth=8))
        ax.text(8.8, (y_reag + y_prod)/2, "ΔH < 0\n(Libera calor)", fontsize=10, fontweight="bold", color=cor_seta, va="center")
    else:
        # Seta apontando para cima
        ax.annotate("", xy=(8.5, y_prod), xytext=(8.5, y_reag),
                    arrowprops=dict(facecolor=cor_seta, edgecolor=cor_seta, shrink=0.05, width=2, headwidth=8))
        ax.text(8.8, (y_reag + y_prod)/2, "ΔH > 0\n(Absorve calor)", fontsize=10, fontweight="bold", color=cor_seta, va="center")
        
    # Seta da Energia de Ativação (Eat)
    ax.annotate("", xy=(5, y_pico), xytext=(5, y_reag),
                arrowprops=dict(arrowstyle="<->", color="purple", lw=1.5))
    ax.text(4.8, (y_pico + y_reag)/2, "Ea", color="purple", fontsize=10, fontweight="bold", ha="right")

    # Configurações do gráfico
    ax.set_title(f"Diagrama de Entalpia: {nome_reacao}", fontsize=12, fontweight="bold", pad=15)
    ax.set_xlabel("Caminho da Reação →", fontsize=10)
    ax.set_ylabel("Entalpia (H) →", fontsize=10)
    ax.set_ylim(0, y_pico + 20)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Remover bordas desnecessárias
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    
    plt.tight_layout()
    return fig

# --- BARRA LATERAL (Navegação & Status) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081971.png", width=70)
    st.title("Atividade de Recuperação")
    st.write("---")
    
    # Mostrar progresso do estudante se identificado
    if st.session_state.nome:
        st.subheader("👤 Estudante")
        st.write(f"**Nome:** {st.session_state.nome}")
        st.write(f"**Série/Ano:** {st.session_state.ano} - {st.session_state.serie}")
        st.write("---")
        
    st.subheader("🗺️ Etapas")
    etapas = ["Identificação", "Vídeo de Apoio", "Simulador Prático", "Quiz Preventivo", "Enviar Atividade"]
    
    for e in etapas:
        if st.session_state.etapa == e:
            st.markdown(f"👉 **<span style='color:#0275d8'>{e}</span>**", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:#777777'>{e}</span>", unsafe_allow_html=True)
            
    st.write("---")
    
    # --- ÁREA DO PROFESSOR (Senha Protegida) ---
    with st.expander("🔐 Área do Professor"):
        senha = st.text_input("Senha de Acesso", type="password")
        if senha == "quimica123":
            st.success("Acesso liberado!")
            st.subheader("Planilha de Notas")
            
            if os.path.exists(CSV_PATH):
                df = pd.read_csv(CSV_PATH)
                st.dataframe(df)
                
                # Botão de Download da planilha
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 Baixar Planilha Excel (CSV)",
                    data=csv,
                    file_name=f"notas_recuperacao_quimica_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
                
                # Botão de Reset
                if st.button("🗑️ Limpar Banco de Dados"):
                    os.remove(CSV_PATH)
                    st.warning("Banco de dados removido! Atualize a página.")
            else:
                st.info("Nenhuma resposta enviada ainda.")
        elif senha != "":
            st.error("Senha incorreta!")

# --- CORPO PRINCIPAL DO SITE ---

# --- ETAPA 1: IDENTIFICAÇÃO ---
if st.session_state.etapa == "Identificação":
    st.title("🧪 Atividade de Recuperação: Termoquímica")
    st.subheader("Processos Endotérmicos e Exotérmicos")
    st.write("""
    Olá, estudante! Esta é a sua atividade interativa de recuperação de Química.
    Siga atentamente as etapas da barra lateral:
    1. **Identifique-se** preenchendo os campos abaixo.
    2. **Assista ao vídeo** de resumo explicativo.
    3. **Interaja com o simulador** para fixar visualmente as reações.
    4. **Responda ao questionário** final. Suas respostas serão enviadas diretamente para a planilha do professor!
    """)
    
    st.info("⚠️ Cada aluno receberá perguntas aleatórias e alternativas embaralhadas. Faça a sua própria atividade!")

    st.markdown("### Preencha seus dados de identificação:")
    nome = st.text_input("Nome Completo do Estudante", value=st.session_state.nome)
    
    col1, col2 = st.columns(2)
    with col1:
        ano = st.selectbox("Ano de Ensino", ["2º Ano"], index=0)
    with col2:
        serie = st.text_input("Série / Turma (ex: 'A', 'B', 'C')", value=st.session_state.serie)
        
    if st.button("Avançar para o Vídeo ➡️"):
        if nome.strip() == "" or serie.strip() == "":
            st.error("Por favor, preencha o seu Nome Completo e a sua Série/Turma antes de avançar!")
        else:
            st.session_state.nome = nome
            st.session_state.ano = ano
            st.session_state.serie = serie
            # Inicializar o quiz sorteado exclusivamente para este aluno
            inicializar_quiz()
            st.session_state.etapa = "Vídeo de Apoio"
            st.rerun()

# --- ETAPA 2: VÍDEO DE APOIO ---
elif st.session_state.etapa == "Vídeo de Apoio":
    st.title("📺 Videoaula de Termoquímica")
    st.subheader("Resumo prático do Brasil Escola com Professor Choven")
    
    st.write("""
    Antes de ir para as atividades, assista ao vídeo abaixo para revisar os conceitos. 
    """)
    
    # Vídeo embutido
    st.video("https://www.youtube.com/watch?v=8mG5bJz82S0")
    st.markdown("🔗 **[CLIQUE AQUI PARA ASSISTIR DIRETAMENTE NO YOUTUBE](https://www.youtube.com/watch?v=8mG5bJz82S0)** (caso o player integrado esteja bloqueado ou indisponível na rede da escola).")
    
    # Alternativa de leitura caso o vídeo esteja bloqueado ou indisponível
    st.markdown("---")
    st.subheader("⚠️ Não consegue carregar o vídeo na rede da escola?")
    st.warning("Muitas redes escolares possuem filtros rígidos que bloqueiam o YouTube. Se esse for o seu caso, não se preocupe! Você pode ler o **Resumo Interativo da Aula** expandindo a seção abaixo para ter acesso a todo o conteúdo cobrado no quiz:")
    
    with st.expander("📖 Ler o Resumo Completo da Aula (Professor Choven)"):
        st.markdown("""
        ### 🧪 Resumo Geral da Termoquímica
        
        A **Termoquímica** é a parte da ciência (e da química) que estuda o **calor envolvido em processos e reações químicas**. 
        Como nem sempre temos aparelhos em laboratório para medir o calor de forma direta, os cientistas criaram tabelas e valores padrão de calor para cada reação. A partir disso, conseguimos calcular a energia térmica envolvida comparando o início e o fim do processo.
        
        ---
        
        ### 📊 1. O que é Entalpia (H) e Variação de Entalpia (ΔH)?
        *   **Entalpia (H):** É a quantidade de calor contida em um sistema químico.
        *   **Variação de Entalpia (ΔH):** É a diferença entre o calor final (produtos) e o calor inicial (reagentes):
            $$\\Delta H = H_{Produtos} - H_{Reagentes}$$
            
        #### Fatores que alteram o valor de ΔH:
        1.  **Estado físico** dos reagentes e produtos (por exemplo, a formação de água sólida tem $\\Delta H$ diferente da água gasosa).
        2.  **Estado alotrópico** das substâncias simples envolvidas.
        3.  **Temperatura** em que o processo ocorre.
        4.  **Concentração** (quantidade de reagentes e produtos consumidos/formados).
        
        ---
        
        ### 🔥 2. Classificação dos Processos Térmicos
        
        *   **Processos Exotérmicos (Liberam Calor):**
            *   "Solem" calor para fora do sistema (esquentam o frasco/meio ambiente).
            *   A entalpia final dos produtos é **menor** que a dos reagentes ($H_{Produtos} < H_{Reagentes}$).
            *   Portanto, a variação de entalpia é negativa: **$\\Delta H < 0$**.
            *   *Nas Equações Químicas:* O calor aparece somado aos **produtos** (ex: $A \\rightarrow B + \\text{Calor}$).
            
        *   **Processos Endotérmicos (Absorvem Calor):**
            *   "Puxam" calor do meio para dentro do sistema (esfriam o frasco/meio ambiente).
            *   A entalpia final dos produtos é **maior** que a dos reagentes ($H_{Produtos} > H_{Reagentes}$).
            *   Portanto, a variação de entalpia é positiva: **$\\Delta H > 0$**.
            *   *Nas Equações Químicas:* O calor aparece somado aos **reagentes** (ex: $A + \\text{Calor} \\rightarrow B$).
            
        #### 📈 Elementos de um Gráfico Termoquímico:
        *   **Energia de Ativação (Ea):** O "salto energético" inicial necessário para que a reação comece a acontecer.
        *   **Complexo Ativado:** O ponto máximo de energia (pico do gráfico) onde os reagentes começam a se transformar em produtos.
        
        ---
        
        ### 🔬 3. Os Três Principais Calores de Reação
        1.  **Calor de Formação:** Energia liberada ou absorvida na formação de 1 mol de uma substância a partir de substâncias simples no estado padrão (a 25 °C, 1 atm, e no estado alotrópico mais estável).
        2.  **Calor de Combustão:** Energia liberada na queima de 1 mol de substância a 25 °C e 1 atm. *Lembre-se: toda combustão libera energia (exotérmica)!*
        3.  **Calor de Ligação:** Energia envolvida para **romper** 1 mol de ligações químicas de uma substância no estado gasoso a 25 °C e 1 atm. Para quebrar uma ligação, o sistema precisa absorver energia (processo endotérmico).
        
        ---
        
        ### 🛍️ 4. A Lei de Hess e a Analogia do Shopping
        A **Lei de Hess** afirma que a variação de entalpia total de um processo depende apenas do **estado inicial** e do **estado final**, não importando o caminho que a reação faz.
        
        #### 👩‍❤️‍👨 A Divertida Analogia do Professor Choven:
        > Imagine que um homem e uma mulher recebem R$ 100 cada um na porta de um shopping para comprar exatamente a mesma calça na mesma loja.
        > *   **O Homem:** Vai direto à loja, compra a calça sem experimentar e sai do shopping. (Caminho curto e direto)
        > *   **A Mulher:** Sobe todos os andares, anda pelo shopping inteiro, olha todas as vitrines e finalmente vai à loja, compra a calça e sai. (Caminho longo com várias etapas intermediárias)
        > 
        > Ao final, ambos começaram com R$ 100 (Estado Inicial) e terminaram com a mesma calça comprada e R$ 0 no bolso (Estado Final). O gasto de dinheiro total foi exatamente o mesmo, independentemente se um foi direto ou se o outro deu voltas pelo shopping inteiro! 
        > 
        > Na química é igual: se os reagentes (início) e produtos (fim) forem os mesmos, o **$\\Delta H$ total gasto ou liberado será o mesmo**, seja a reação em uma única etapa ou em várias!
        
        #### 🔢 Regras para calcular a Lei de Hess:
        *   Se você **inverter** uma reação intermediária, deve **inverter o sinal do $\\Delta H$** (positivo vira negativo e vice-versa).
        *   Se você **multiplicar** ou dividir uma equação, deve **multiplicar** ou dividir o valor do $\\Delta H$ pelo mesmo número.
        """)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Voltar"):
            st.session_state.etapa = "Identificação"
            st.rerun()
    with col2:
        if st.button("Ir para o Simulador Prático ➡️"):
            st.session_state.etapa = "Simulador Prático"
            st.rerun()

# --- ETAPA 3: SIMULADOR PRÁTICO ---
elif st.session_state.etapa == "Simulador Prático":
    st.title("🌡️ Simulador Interativo de Reações")
    st.subheader("Explore o fluxo de calor e os diagramas de entalpia")
    
    st.write("""
    Escolha abaixo um processo termoquímico extraído diretamente dos seus materiais de estudo e clique em
    **Simular Processo** para ver o termômetro virtual se mover e o gráfico de entalpia correspondente ser desenhado!
    """)
    
    # Escolha do processo
    processo = st.selectbox(
        "Selecione um processo do livro para simular:",
        [
            "Sacos de Gelo de Nitrato de Amônio (Saco de Resfriamento)",
            "Combustão da Gasolina (Motor do Carro)",
            "Evaporação da Água no Filtro de Barro",
            "Dissolução do Cloreto de Cálcio (CaCl2) em Água"
        ]
    )
    
    if processo == "Sacos de Gelo de Nitrato de Amônio (Saco de Resfriamento)":
        nome_reacao = "Dissolução do Nitrato de Amônio (NH₄NO₃)"
        tipo_reacao = "Endotérmica"
        temp_inicial = 25
        temp_final = -15
        delta_h_val = "+26 kJ/mol"
        reacao_quimica = "NH₄NO₃(s) + energia → NH₄⁺(aq) + NO₃⁻(aq)"
        descricao = """
        ❄️ **Saco de Gelo Instantâneo (Pág. 40):** Quando o saco interno de água se rompe, o nitrato de amônio sólido 
        dissolve-se na água de forma endotérmica. Essa reação necessita absorver calor de forma tão rápida que retira o calor do meio circundante, 
        fazendo a temperatura despencar de 25°C para até -15°C! Excelente para tratar lesões musculares em esportes.
        """
    elif processo == "Combustão da Gasolina (Motor do Carro)":
        nome_reacao = "Combustão do Octano (Gasolina)"
        tipo_reacao = "Exotérmica"
        temp_inicial = 25
        temp_final = 90
        delta_h_val = "-5461 kJ/mol"
        reacao_quimica = "C₈H₁₈(l) + 25/2 O₂(g) → 8 CO₂(g) + 9 H₂O(l) + Calor"
        descricao = """
        🔥 **Motor do Carro e Combustão (Pág. 37, 40):** A queima do combustível libera uma imensa quantidade de calor para o sistema. 
        Como é uma reação fortemente exotérmica, o motor atinge temperaturas extremas. O sistema de arrefecimento (com água e aditivos) 
        serve especificamente para absorver esse calor liberado e evitar que as peças de metal do motor sofram fusão ou superaquecimento!
        """
    elif processo == "Evaporação da Água no Filtro de Barro":
        nome_reacao = "Evaporação de H₂O no Filtro de Barro"
        tipo_reacao = "Endotérmica"
        temp_inicial = 25
        temp_final = 18
        delta_h_val = "+44 kJ/mol"
        reacao_quimica = "H₂O(l) + calor do sistema → H₂O(g)"
        descricao = """
        🏺 **O Filtro de Barro (Pág. 39):** A cerâmica do filtro é microporosa. A água atravessa esses microporos e chega ao lado externo. 
        Ao passar para o estado gasoso (evaporação), ela necessita absorver calor. Essa energia térmica é retirada da própria água que ficou 
        no interior do filtro, resfriando-a e mantendo-a sempre fresca! É um processo de refrigeração natural e endotérmico.
        """
    else:  # CaCl2 em Água
        nome_reacao = "Dissolução do Cloreto de Cálcio (CaCl₂)"
        tipo_reacao = "Endotérmica"
        temp_inicial = 25
        temp_final = 10
        delta_h_val = "ΔH > 0"
        reacao_quimica = "CaCl₂(s) + energia → Ca²⁺(aq) + 2 Cl⁻(aq)"
        descricao = """
        🧪 **Dissolução de CaCl₂ (Pág. 38, 40):** Conforme registrado na página 40 do livro, o experimento laboratorial de dissolução 
        do cloreto de cálcio na água provoca uma absorção de energia (ganho de energia pelo sistema), caracterizando-se como um 
        processo endotérmico que causa um resfriamento perceptível ao toque no béquer.
        """

    # Layout de colunas para o simulador
    col1, col2 = st.columns([1.2, 1.8])
    
    with col1:
        st.markdown(f"### Reação Química:\n`{reacao_quimica}`")
        st.markdown(f"**Tipo de Processo:** `{tipo_reacao}`")
        st.markdown(f"**Variação de Entalpia:** `{delta_h_val}`")
        
        st.markdown("### Termômetro Virtual")
        # Visualizar temperatura mudando
        st.write(f"🌡️ **Temperatura Inicial:** {temp_inicial} °C")
        
        # Simular efeito dinâmico usando progress bar do Streamlit para representar a variação
        if tipo_reacao == "Exotérmica":
            progresso = st.slider("Acompanhar Progresso da Reação (Tempo)", 0, 100, 100)
            temp_atual = temp_inicial + (temp_final - temp_inicial) * (progresso / 100)
            st.metric("Temperatura do Sistema", f"{temp_atual:.1f} °C", f"+{temp_atual - temp_inicial:.1f} °C (AQUECEU)")
        else:
            progresso = st.slider("Acompanhar Progresso da Reação (Tempo)", 0, 100, 100)
            temp_atual = temp_inicial - (temp_inicial - temp_final) * (progresso / 100)
            st.metric("Temperatura do Sistema", f"{temp_atual:.1f} °C", f"-{temp_inicial - temp_atual:.1f} °C (RESFRIOU)", delta_color="inverse")
            
        st.markdown(descricao)
        
    with col2:
        # Gerar e mostrar o gráfico de entalpia com base na escolha
        fig_gr = plotar_diagrama(tipo_reacao, nome_reacao)
        st.pyplot(fig_gr)
        
    st.markdown("---")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        if st.button("⬅️ Voltar para o Vídeo"):
            st.session_state.etapa = "Vídeo de Apoio"
            st.rerun()
    with col_v2:
        if st.button("Avançar para o Quiz de Recuperação ➡️"):
            st.session_state.etapa = "Quiz Preventivo"
            st.rerun()

# --- ETAPA 4: QUIZ PREVENTIVO ---
elif st.session_state.etapa == "Quiz Preventivo":
    st.title("📝 Questionário de Recuperação")
    st.subheader("Responda com atenção para registrar sua nota")
    st.write(f"Estudante: **{st.session_state.nome}** | Série: **{st.session_state.serie}**")
    st.info("💡 As alternativas abaixo foram embaralhadas. Leia atentamente!")
    
    # Criar formulário para evitar múltiplos re-runs indesejados durante a seleção
    with st.form("quiz_form"):
        respostas_temporarias = {}
        
        for idx, q in enumerate(st.session_state.questoes_sorteadas):
            st.markdown(f"**Pergunta {idx + 1}:** {q['pergunta']}")
            # Mostrar a referência no livro/vídeo para ajudar o estudante na recuperação
            st.caption(f"📍 Dica de estudo: conteúdo localizado em {q['referencia']}")
            
            # Opções
            escolha = st.radio(
                f"Selecione uma resposta para a Pergunta {idx + 1}:",
                q["opcoes"],
                key=f"q_radio_{q['id']}",
                index=None
            )
            respostas_temporarias[q["id"]] = escolha
            st.markdown("<br>", unsafe_allow_html=True)
            
        botao_enviar = st.form_submit_button("Validar Respostas 💾")
        
        if botao_enviar:
            # Validar se todas foram respondidas
            todas_respondidas = True
            for q_id, resp in respostas_temporarias.items():
                if resp is None:
                    todas_respondidas = False
                    
            if not todas_respondidas:
                st.error("Por favor, responda todas as 5 questões antes de validar!")
            else:
                st.session_state.respostas_estudante = respostas_temporarias
                st.session_state.aluno_submeteu = True
                st.success("Respostas salvas! Clique no botão de avançar abaixo para enviar os resultados ao professor.")
                
    st.markdown("---")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        if st.button("⬅️ Voltar ao Simulador"):
            st.session_state.etapa = "Simulador Prático"
            st.rerun()
    with col_q2:
        if st.session_state.aluno_submeteu:
            if st.button("Avançar para Envio ➡️"):
                st.session_state.etapa = "Enviar Atividade"
                st.rerun()
        else:
            st.button("Avançar para Envio ➡️ (Responda o Quiz primeiro)", disabled=True)

# --- ETAPA 5: ENVIAR ATIVIDADE (Registro de Notas) ---
elif st.session_state.etapa == "Enviar Atividade":
    st.title("💾 Envio da Atividade")
    st.subheader("Confirme o envio dos seus dados para a planilha do professor")
    
    # Calcular acertos
    acertos = 0
    total_perguntas = len(st.session_state.questoes_sorteadas)
    detalhes_gabarito = []
    
    for idx, q in enumerate(st.session_state.questoes_sorteadas):
        resp_aluno = st.session_state.respostas_estudante.get(q["id"])
        idx_opcao_correta = q["correta"]
        texto_correto = q["opcoes"][idx_opcao_correta]
        
        foi_correto = (resp_aluno == texto_correto)
        if foi_correto:
            acertos += 1
            
        detalhes_gabarito.append({
            "num": idx + 1,
            "pergunta": q["pergunta"],
            "resposta_aluno": resp_aluno,
            "resposta_correta": texto_correto,
            "status": "✅ Correta" if foi_correto else "❌ Incorreta"
        })
        
    nota_final = (acertos / total_perguntas) * 10.0
    
    st.markdown("### Resumo da sua Atividade:")
    st.write(f"👤 **Nome:** {st.session_state.nome}")
    st.write(f"🏫 **Ano/Série:** {st.session_state.ano} - {st.session_state.serie}")
    st.write(f"🎯 **Nota Final:** `{nota_final:.1f} / 10.0` ({acertos} acertos de 5)")
    
    if nota_final >= 6.0:
        st.balloons()
        st.success("Parabéns! Você alcançou a nota mínima de recuperação! 🎉")
    else:
        st.warning("Estude um pouco mais o simulador e o vídeo para a próxima tentativa! 💪")
        
    st.info("👉 Clique no botão vermelho abaixo para salvar permanentemente a sua nota no banco de dados do professor.")
    
    # Botão para salvar na Planilha (CSV)
    if st.button("✅ ENVIAR RESPOSTAS AO PROFESSOR"):
        # Preparar dados para o DataFrame
        linha_resposta = {
            "Data_Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nome": st.session_state.nome,
            "Ano": st.session_state.ano,
            "Série": st.session_state.serie,
            "Nota": nota_final,
            "Acertos": acertos,
            "Q1": detalhes_gabarito[0]["status"],
            "Q2": detalhes_gabarito[1]["status"],
            "Q3": detalhes_gabarito[2]["status"],
            "Q4": detalhes_gabarito[3]["status"],
            "Q5": detalhes_gabarito[4]["status"],
        }
        
        # Salvar em CSV de forma segura (append se já existe)
        novo_registro = pd.DataFrame([linha_resposta])
        
        if os.path.exists(CSV_PATH):
            df_existente = pd.read_csv(CSV_PATH)
            df_final = pd.concat([df_existente, novo_registro], ignore_index=True)
        else:
            df_final = novo_registro
            
        df_final.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
        
        st.success("✨ Suas respostas foram salvas com sucesso na planilha do professor! Você já pode fechar esta aba.")
        
    st.markdown("### Histórico de Correção:")
    for dg in detalhes_gabarito:
        with st.expander(f"Questão {dg['num']}: {dg['status']}"):
            st.write(f"**Enunciado:** {dg['pergunta']}")
            st.write(f"**Sua Resposta:** {dg['resposta_aluno']}")
            if dg['status'] == "❌ Incorreta":
                st.write(f"**Resposta Correta:** {dg['resposta_correta']}")
                
    st.markdown("---")
    if st.button("🔄 Reiniciar Atividade (Outro Estudante)"):
        # Resetar sessão do estudante
        st.session_state.nome = ""
        st.session_state.serie = ""
        st.session_state.questoes_sorteadas = []
        st.session_state.respostas_estudante = {}
        st.session_state.aluno_submeteu = False
        st.session_state.etapa = "Identificação"
        st.rerun()
