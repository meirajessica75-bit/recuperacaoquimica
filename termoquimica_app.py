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
if "finalizado" not in st.session_state:
    st.session_state.finalizado = False
if "nota_final" not in st.session_state:
    st.session_state.nota_final = 0.0
if "acertos" not in st.session_state:
    st.session_state.acertos = 0
if "detalhes_gabarito" not in st.session_state:
    st.session_state.detalhes_gabarito = []

# Se o estudante já finalizou a prova, ele fica permanentemente travado na tela do Quiz Corrigido
if st.session_state.finalizado:
    st.session_state.etapa = "Quiz Corrigido"

# Função para sortear questões e embaralhar alternativas (evitando cópia)
def inicializar_quiz():
    questoes = random.sample(QUESTOES_BANCO, 5)
    questoes_preparadas = []
    
    for q in questoes:
        opcoes_originais = list(q["opcoes"])
        correta_original = opcoes_originais[q["correta"]]
        
        opcoes_embaralhadas = list(opcoes_originais)
        random.shuffle(opcoes_embaralhadas)
        
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
    st.session_state.finalizado = False

# Função para plotar o diagrama de entalpia dinamicamente
def plotar_diagrama(tipo_reacao, nome_reacao):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    if tipo_reacao == "Exotérmica":
        y_reag = 80
        y_pico = 120
        y_prod = 30
        cor_curva = "#d9534f"  # Vermelho
        cor_seta = "#c9302c"
    else:  # Endotérmica
        y_reag = 30
        y_pico = 100
        y_prod = 80
        cor_curva = "#0275d8"  # Azul
        cor_seta = "#025aa5"
        
    x = np.linspace(0, 10, 100)
    y = np.zeros_like(x)
    for i, xi in enumerate(x):
        if xi < 3:
            y[i] = y_reag
        elif xi > 7:
            y[i] = y_prod
        else:
            t = (xi - 3) / 4
            base = y_reag + (y_prod - y_reag) * t
            pico = 4 * (y_pico - max(y_reag, y_prod)) * t * (1 - t)
            y[i] = base + pico

    ax.plot(x, y, color=cor_curva, linewidth=3, label="Caminho da Reação")
    ax.axhline(y=y_reag, xmin=0.05, xmax=0.3, color="gray", linestyle="--")
    ax.axhline(y=y_prod, xmin=0.7, xmax=0.95, color="gray", linestyle="--")
    
    ax.text(0.5, y_reag + 3, "Reagentes", fontsize=10, fontweight="bold", color="#333333")
    ax.text(7.5, y_prod + 3, "Produtos", fontsize=10, fontweight="bold", color="#333333")
    ax.text(5, y_pico + 3, "Complexo Ativado", fontsize=9, fontstyle="italic", color="#555555", ha="center")
    
    if tipo_reacao == "Exotérmica":
        ax.annotate("", xy=(8.5, y_prod), xytext=(8.5, y_reag),
                    arrowprops=dict(facecolor=cor_seta, edgecolor=cor_seta, shrink=0.05, width=2, headwidth=8))
        ax.text(8.8, (y_reag + y_prod)/2, "ΔH < 0\n(Libera calor)", fontsize=10, fontweight="bold", color=cor_seta, va="center")
    else:
        ax.annotate("", xy=(8.5, y_prod), xytext=(8.5, y_reag),
                    arrowprops=dict(facecolor=cor_seta, edgecolor=cor_seta, shrink=0.05, width=2, headwidth=8))
        ax.text(8.8, (y_reag + y_prod)/2, "ΔH > 0\n(Absorve calor)", fontsize=10, fontweight="bold", color=cor_seta, va="center")
        
    ax.annotate("", xy=(5, y_pico), xytext=(5, y_reag),
                arrowprops=dict(arrowstyle="<->", color="purple", lw=1.5))
    ax.text(4.8, (y_pico + y_reag)/2, "Ea", color="purple", fontsize=10, fontweight="bold", ha="right")

    ax.set_title(f"Diagrama de Entalpia: {nome_reacao}", fontsize=12, fontweight="bold", pad=15)
    ax.set_xlabel("Caminho da Reação →", fontsize=10)
    ax.set_ylabel("Entalpia (H) →", fontsize=10)
    ax.set_ylim(0, y_pico + 20)
    ax.set_xticks([])
    ax.set_yticks([])
    
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
        
    # Desabilitar navegação se o aluno já finalizou para evitar fraudes
    if not st.session_state.finalizado:
        st.subheader("🗺️ Etapas")
        etapas = ["Identificação", "Vídeo de Apoio", "Simulador Prático", "Quiz Interativo"]
        
        for e in etapas:
            if st.session_state.etapa == e:
                st.markdown(f"👉 **<span style='color:#0275d8'>{e}</span>**", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:#777777'>{e}</span>", unsafe_allow_html=True)
    else:
        st.subheader("🏁 Status da Prova")
        st.success("✅ Respostas Enviadas!")
        st.info("Você já concluiu sua tentativa e suas respostas foram salvas na planilha do professor.")
            
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
                
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 Baixar Planilha Excel (CSV)",
                    data=csv,
                    file_name=f"notas_recuperacao_quimica_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
                
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
    1. **Identifique-se** preenchendo os seus dados abaixo.
    2. **Assista ao vídeo** de apoio ou leia o resumo interativo.
    3. **Interaja com o simulador** prático para fixar os conceitos.
    4. **Responda ao quiz de 5 questões**. Suas respostas serão avaliadas e enviadas diretamente para o professor!
    """)
    
    st.info("⚠️ Atenção: Você só poderá responder ao questionário uma única vez. Certifique-se de colocar seu nome correto!")

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
            # Validação anti-duplicação: verificar se este estudante já enviou respostas antes
            nome_limpo = nome.strip().lower()
            serie_limpo = serie.strip().lower()
            ja_respondeu = False
            nota_existente = 0.0
            
            if os.path.exists(CSV_PATH):
                try:
                    df_check = pd.read_csv(CSV_PATH)
                    filtro = (df_check["Nome"].astype(str).str.strip().str.lower() == nome_limpo) & \
                             (df_check["Série"].astype(str).str.strip().str.lower() == serie_limpo)
                    duplicados = df_check[filtro]
                    if not duplicados.empty:
                        ja_respondeu = True
                        nota_existente = duplicados.iloc[0]["Nota"]
                except Exception:
                    pass
            
            if ja_respondeu:
                st.error(f"❌ Acesso Negado: O estudante **{nome}** da série **{serie}** já realizou esta atividade! Sua nota ({nota_existente:.1f}) já foi registrada anteriormente na planilha do professor.")
            else:
                st.session_state.nome = nome
                st.session_state.ano = ano
                st.session_state.serie = serie
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
    
    with st.expander("📖 Ler o Resumo Completo da Aula (Preparação para o Quiz)"):
        st.markdown("""
        ### 1. O que é Termoquímica?
        A **termoquímica** é a parte da ciência química que estuda as trocas de calor (energia térmica) que acompanham as reações químicas e as transformações físicas. [22]
        Como não é possível medir a quantidade absoluta de calor dentro de um corpo, nós medimos a **Variação de Entalpia (ΔH)**, que é a diferença de energia térmica entre o estado final (produtos) e o estado inicial (reagentes). [23, 24]
        
        **Fórmula da Variação de Entalpia:**
        $$ \\Delta H = H_{Produtos} - H_{Reagentes} $$ [24]
        
        ---
        
        ### 2. Processos Exotérmicos vs. Endotérmicos
        As transformações químicas e físicas podem ser classificadas em dois grupos quanto à energia térmica: [25]
        
        *   **Processos Exotérmicos (ΔH < 0):** São transformações que **liberam calor** para o ambiente externo. [25, 27]
            *   *Gráfico:* A energia dos produtos é **menor** que a dos reagentes (linha cai). [26, 27]
            *   *Sinal:* O ΔH é sempre **negativo**. [27]
            *   *Sensação:* O recipiente esquenta.
            *   *Exemplos:* Queima da gasolina nos motores de automóveis. [37, 40]
        *   **Processos Endotérmicos (ΔH > 0):** São transformações que **absorvem calor** do ambiente externo. [25, 28]
            *   *Gráfico:* A energia dos produtos é **maior** que a dos reagentes (linha sobe). [28]
            *   *Sinal:* O ΔH é sempre **positivo**. [28]
            *   *Sensação:* O recipiente esfria (sensação de frio). [40]
            *   *Exemplos:* Resfriamento do Saco de Gelo Instantâneo de Nitrato de Amônio (NH₄NO₃) e evaporação da água no filtro de barro. [39, 40]
            
        ---
        
        ### 3. Fatores que Alteram a Variação de Entalpia (ΔH)
        A variação de energia de uma reação pode mudar de acordo com quatro fatores fundamentais destacados pelo professor: [24, 25]
        1.  **Estado Físico:** A água sólida, líquida e gasosa possuem entalpias de formação diferentes. [25]
        2.  **Estado Alotrópico:** Formas alotrópicas diferentes (como carbono grafite e diamante) afetam o calor envolvido. [25]
        3.  **Temperatura:** Deve ser avaliada dentro de uma faixa ideal controlada. [25]
        4.  **Concentração / Quantidade de Matéria:** A energia é uma propriedade extensiva (depende da quantidade de moléculas que reagem). [25, 54]
        
        ---
        
        ### 4. A Lei de Hess e a divertida analogia do Shopping
        A **Lei de Hess** afirma que a variação de entalpia (ΔH) de um processo depende apenas do **estado inicial** e do **estado final** da reação, não importando os caminhos intermediários que a reação faz para chegar até lá! [31, 33]
        
        *   **Analogia do Professor:** Imagine que um homem e uma mulher entram em um shopping para comprar a mesma calça na mesma loja, cada um com R$ 100. [32]
            *   A **mulher** entra, anda por todos os andares do shopping, olha todas as lojas de roupas possíveis antes de finalmente comprar a calça. [32, 33]
            *   O **homem** entra direto pelo caminho mais rápido, compra a calça sem experimentar e sai logo em seguida. [32, 33]
            *   *Resultado:* Ambos começaram com R$ 100 (estado inicial) e terminaram com a calça comprada e sem dinheiro (estado final). O caminho de cada um foi diferente, mas a **variação de energia e dinheiro final foi exatamente a mesma!** [33]
            
        *   **Regras da Lei de Hess:** [34]
            *   Se você **inverter** uma reação química, você deve **inverter o sinal** do seu ΔH (ex: de negativo para positivo). [34]
            *   Se você **multiplicar ou dividir** os coeficientes de uma reação, você deve **multiplicar ou dividir** o valor de ΔH pelo mesmo número. [34]
        """)
        
    st.markdown("---")
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
        🔥 **Motor do Carro e Combustão (Pág. 37, 40):** A queima do combustível libera uma imensa quantidade de calor para o sistema. \n        Como é uma reação fortemente exotérmica, o motor atinge temperaturas extremas. O sistema de arrefecimento (com água e aditivos) \n        serve especificamente para absorver esse calor liberado e evitar que as peças de metal do motor sofram fusão ou superaquecimento!\n        """
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
    else: # CaCl2 em Água
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

    col1, col2 = st.columns([1.2, 1.8])
    
    with col1:
        st.markdown(f"### Reação Química:\n`{reacao_quimica}`")
        st.markdown(f"**Tipo de Processo:** `{tipo_reacao}`")
        st.markdown(f"**Variação de Entalpia:** `{delta_h_val}`")
        
        st.markdown("### Termômetro Virtual")
        st.write(f"🌡️ **Temperatura Inicial:** {temp_inicial} °C")
        
        progresso = st.slider("Acompanhar Progresso da Reação (Tempo)", 0, 100, 100)
        
        if tipo_reacao == "Exotérmica":
            temp_atual = temp_inicial + (temp_final - temp_inicial) * (progresso / 100)
            st.metric("Temperatura do Sistema", f"{temp_atual:.1f} °C", f"+{temp_atual - temp_inicial:.1f} °C (AQUECEU)")
        else:
            temp_atual = temp_inicial - (temp_inicial - temp_final) * (progresso / 100)
            st.metric("Temperatura do Sistema", f"{temp_atual:.1f} °C", f"-{temp_inicial - temp_atual:.1f} °C (RESFRIOU)", delta_color="inverse")
            
        st.markdown(descricao)
        
    with col2:
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
            st.session_state.etapa = "Quiz Interativo"
            st.rerun()

# --- ETAPA 4: QUIZ INTERATIVO (AGORA INTEGRADO COM ENVIO AUTOMÁTICO E TRAVA) ---
elif st.session_state.etapa == "Quiz Interativo":
    st.title("📝 Questionário de Recuperação")
    st.subheader("Responda com atenção e envie diretamente")
    st.write(f"Estudante: **{st.session_state.nome}** | Série: **{st.session_state.serie}**")
    st.info("💡 As alternativas abaixo foram embaralhadas pelo sistema para evitar cópias. Leia com atenção e responda. Ao clicar no botão abaixo, suas respostas serão validadas e enviadas de forma definitiva.")
    
    # Criar formulário para o Quiz
    with st.form("quiz_form"):
        respostas_temporarias = {}
        
        for idx, q in enumerate(st.session_state.questoes_sorteadas):
            st.markdown(f"**Pergunta {idx + 1}:** {q['pergunta']}")
            st.caption(f"📍 Dica de estudo: conteúdo localizado em {q['referencia']}")
            
            escolha = st.radio(
                f"Selecione uma resposta para a Pergunta {idx + 1}:",
                q["opcoes"],
                key=f"q_radio_{q['id']}",
                index=None
            )
            respostas_temporarias[q["id"]] = escolha
            st.markdown("<br>", unsafe_allow_html=True)
            
        botao_validar_e_enviar = st.form_submit_button("Validar e Enviar Respostas ao Professor 🚀")
        
        if botao_validar_e_enviar:
            # Validar se todas foram respondidas
            todas_respondidas = True
            for q_id, resp in respostas_temporarias.items():
                if resp is None:
                    todas_respondidas = False
                    
            if not todas_respondidas:
                st.error("⚠️ Você precisa responder TODAS as 5 questões antes de enviar!")
            else:
                # 1. Processar notas e acertos imediatamente
                acertos = 0
                total_perguntas = len(st.session_state.questoes_sorteadas)
                detalhes_gabarito = []
                
                for idx, q in enumerate(st.session_state.questoes_sorteadas):
                    resp_aluno = respostas_temporarias.get(q["id"])
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
                
                # 2. Salvar na planilha imediatamente (Envio automático sem etapa extra)
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
                
                novo_registro = pd.DataFrame([linha_resposta])
                
                if os.path.exists(CSV_PATH):
                    try:
                        df_existente = pd.read_csv(CSV_PATH)
                        df_final = pd.concat([df_existente, novo_registro], ignore_index=True)
                    except Exception:
                        df_final = novo_registro
                else:
                    df_final = novo_registro
                    
                df_final.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
                
                # 3. Salvar no Estado da Sessão para bloquear alterações adicionais
                st.session_state.respostas_estudante = respostas_temporarias
                st.session_state.nota_final = nota_final
                st.session_state.acertos = acertos
                st.session_state.detalhes_gabarito = detalhes_gabarito
                st.session_state.finalizado = True
                st.session_state.etapa = "Quiz Corrigido"
                st.rerun()

# --- TELA FINAL: APENAS VISUALIZAÇÃO DA NOTA E CORREÇÃO (BLOQUEADO) ---
elif st.session_state.etapa == "Quiz Corrigido":
    st.title("🏆 Resultado da Avaliação")
    st.subheader("Sua atividade de recuperação foi finalizada!")
    st.write(f"Estudante: **{st.session_state.nome}** | Série: **{st.session_state.serie}**")
    
    st.success("✨ Respostas registradas e enviadas diretamente para a planilha do professor com sucesso!")
    
    st.markdown("### Seu Desempenho:")
    st.write(f"🎯 **Nota Final:** `{st.session_state.nota_final:.1f} / 10.0` ({st.session_state.acertos} acertos de 5)")
    
    if st.session_state.nota_final >= 6.0:
        st.balloons()
        st.success("Excelente! Você obteve a nota mínima para aprovação na recuperação! 🎉")
    else:
        st.warning("Estude um pouco mais os diagramas de entalpia e os tipos de reações termoquímicas! 💪")
        
    st.markdown("### Correção Detalhada da sua Prova:")
    for dg in st.session_state.detalhes_gabarito:
        with st.expander(f"Questão {dg['num']}: {dg['status']}"):
            st.write(f"**Enunciado:** {dg['pergunta']}")
            st.write(f"**Sua Resposta:** {dg['resposta_aluno']}")
            if dg['status'] == "❌ Incorreta":
                st.write(f"**Resposta Correta:** {dg['resposta_correta']}")
                
    st.info("🔒 Esta página de correção é apenas para visualização. Suas notas e respostas já estão salvas na planilha do professor e não podem ser refeitas nesta sessão.")
