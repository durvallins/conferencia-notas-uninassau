import pandas as pd
import streamlit as st
import re

# Constantes
CACHE_TTL_DATA = 600

# URLs das planilhas
URLS = {
    "2º Período - POO": "https://docs.google.com/spreadsheets/d/e/2PACX-1vReM-efNOlMd4VoJL3GgRkaYI7oSHlawzwABQQe61idQmAQRUtDnJLeREaK4HxNaQ/pub?gid=239527333&single=true&output=csv",
    "4º Períodos - Machine Learning": "https://docs.google.com/spreadsheets/d/e/2PACX-1vS_6AVg9EF8qKKr1OsfDxZEwKx6hER0mVP85UWu4bETJ9PxAk1naBijTZptTr48SQ/pub?output=xlsx"
}

# Configuração da Página
st.set_page_config(
    page_title="📝 Sistema de Conferência de Notas",
    page_icon="✅",
    layout="centered",
)

# Funções auxiliares
def get_url_format(sheet_url):
    """Retorna 'xlsx' ou 'csv' baseado na URL"""
    if 'output=xlsx' in sheet_url or sheet_url.endswith('.xlsx'):
        return 'xlsx'
    return 'csv'

# ==================== PARSER DO GABARITO COMENTADO (VERSÃO ROBUSTA) ====================
@st.cache_data(ttl=CACHE_TTL_DATA)
def parse_gabarito_md(file_path="MAPEAMENTO_QUESTOES_MATERIAL_ESTUDO.md"):
    """
    Lê e processa o arquivo Markdown de mapeamento de questões usando um método
    de busca (finditer) para maior robustez.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return None

    data = {}
    # Encontra todos os blocos de Prova (A, B, C)
    prova_matches = re.finditer(
        r'# 🎯 PROVA TIPO (?P<tipo>[A-C])(?P<block>.*?)(?=# 🎯 PROVA TIPO|# 📊 ANÁLISE DE COBERTURA)',
        content,
        re.DOTALL
    )

    for prova_match in prova_matches:
        tipo_prova = prova_match.group('tipo')
        prova_block = prova_match.group('block')
        data[tipo_prova] = {}

        # Encontra todos os blocos de Questão dentro do bloco da Prova
        question_matches = re.finditer(
            r'## \*\*Q(?P<q_num>\d{2}) - (?P<q_content>.*?)(?=## \*\*Q\d{2} -|\Z)',
            prova_block,
            re.DOTALL
        )

        for q_match in question_matches:
            q_num_str = q_match.group('q_num')
            q_num = f"Q{q_num_str}"
            # O conteúdo completo da questão é o match inteiro
            full_q_content = q_match.group(0)

            titulo_match = re.search(r'## \*\*Q\d{2} - (.*?)\*\*', full_q_content)
            titulo = titulo_match.group(1).strip() if titulo_match else "N/A"

            gabarito_match = re.search(r'### 📌 \*\*GABARITO: ([A-E])\*\*', full_q_content)
            gabarito = gabarito_match.group(1) if gabarito_match else "N/A"

            boundary = r'(?=###|---|\Z)'

            localizacao_match = re.search(r'### 📍 \*\*LOCALIZAÇÃO NO MATERIAL\*\*(.*?)' + boundary, full_q_content, re.DOTALL)
            localizacao = localizacao_match.group(1).strip() if localizacao_match else ""

            pagina_pdf = ""
            if localizacao:
                pagina_match = re.search(r'Páginas: ([\d-]+)', localizacao)
                if pagina_match:
                    pagina_pdf = pagina_match.group(1)

            trecho_match = re.search(r'### 📖 \*\*TRECHO EXATO DO MATERIAL\*\*(.*?)' + boundary, full_q_content, re.DOTALL)
            trecho = trecho_match.group(1).strip() if trecho_match else ""

            # Regex flexível para as duas variações de "Fundamentação"
            fundamentacao_match = re.search(r'### (?:✅|📖) \*\*FUNDAMENTAÇÃO(?: DA RESPOSTA)?\*\*(.*?)' + boundary, full_q_content, re.DOTALL)
            fundamentacao = fundamentacao_match.group(1).strip() if fundamentacao_match else ""

            data[tipo_prova][q_num] = {
                "titulo": titulo,
                "gabarito": gabarito,
                "localizacao": localizacao,
                "pagina_pdf": pagina_pdf,
                "trecho_material": trecho,
                "fundamentacao": fundamentacao
            }
    return data


def render_gabarito_comentado():
    """Renderiza a interface do gabarito comentado para POO."""
    st.markdown("---")
    st.header("👨‍🏫 Gabarito Comentado - POO")
    st.write("Selecione o tipo de prova e a questão para ver a fundamentação completa baseada no material de estudo.")

    gabarito_data = parse_gabarito_md()

    if not gabarito_data:
        st.error("❌ Arquivo `MAPEAMENTO_QUESTOES_MATERIAL_ESTUDO.md` não encontrado ou falha ao processar.")
        return

    col1, col2 = st.columns(2)
    with col1:
        tipo_prova = st.selectbox(
            "Selecione o Tipo da Prova:",
            options=list(gabarito_data.keys())
        )
    
    if tipo_prova and tipo_prova in gabarito_data:
        questoes = list(gabarito_data[tipo_prova].keys())
        if not questoes:
            st.warning(f"Nenhuma questão encontrada para a Prova Tipo {tipo_prova}.")
            return

        with col2:
            questao_selecionada = st.selectbox(
                "Selecione a Questão:",
                options=questoes
            )

        if questao_selecionada and questao_selecionada in gabarito_data[tipo_prova]:
            dados_questao = gabarito_data[tipo_prova][questao_selecionada]
            
            st.info(f"**Questão:** {dados_questao.get('titulo', 'N/A')}\n\n**Gabarito Correto:** {dados_questao.get('gabarito', 'N/A')}")

            with st.popover("🔍 Ver Fundamentação Completa"):
                pagina_pdf = dados_questao.get("pagina_pdf")
                if pagina_pdf:
                    st.info(f"📄 **Confira no PDF:** Página(s) **{pagina_pdf}**")

                localizacao_content = dados_questao.get('localizacao')
                if localizacao_content:
                    st.subheader("📍 Localização no Material")
                    st.markdown(localizacao_content)
                
                trecho_material_content = dados_questao.get('trecho_material')
                if trecho_material_content:
                    st.subheader("📖 Trecho Exato do Material")
                    parts = re.split(r'(```(?:[a-zA-Z0-9]+)?\n.*?```)', trecho_material_content, re.DOTALL)
                    for part in parts:
                        if part.strip().startswith('```') and part.strip().endswith('```'):
                            lang_match = re.match(r'```([a-zA-Z0-9]+)?\n', part)
                            language = lang_match.group(1) if lang_match and lang_match.group(1) else 'plaintext'
                            code_content = re.sub(r'```(?:[a-zA-Z0-9]+)?\n', '', part, 1)
                            code_content = re.sub(r'```$', '', code_content, 1)
                            st.code(code_content.strip(), language=language)
                        elif part.strip():
                            st.markdown(part)
                
                fundamentacao_content = dados_questao.get('fundamentacao')
                if fundamentacao_content:
                    st.subheader("✅ Fundamentação da Resposta")
                    st.markdown(fundamentacao_content)

# ==================== SISTEMA 2º PERÍODO (GABARITOS) ====================
@st.cache_data(ttl=CACHE_TTL_DATA)
def load_2periodo_data(sheet_url):
    """Carrega planilha com gabaritos (2º C - POO)"""
    try:
        formato = get_url_format(sheet_url)
        if formato == 'xlsx':
            df = pd.read_excel(sheet_url, engine='openpyxl')
        else:
            df = pd.read_csv(sheet_url)
        
        if df.empty:
            return None, None, None, None, None, None
        
        disciplina = "POO - 2º C"
        gabaritos_dict = {}
        questoes_indices = []
        
        # Identifica colunas com questões
        for col_idx in range(2, len(df.columns)):
            valor = str(df.iloc[0, col_idx]).strip()
            if valor.isdigit():
                questoes_indices.append(col_idx)
            else:
                if questoes_indices:
                    break
        
        # Extrai gabaritos (linhas 1, 2, 3 = tipos A, B, C)
        for idx, tipo in [(1, 'A'), (2, 'B'), (3, 'C')]:
            if idx < len(df):
                gabarito = []
                for col_idx in questoes_indices:
                    if col_idx < len(df.columns):
                        valor = str(df.iloc[idx, col_idx]).strip().upper()
                        if valor and valor != 'NAN' and len(valor) == 1 and valor.isalpha():
                            gabarito.append(valor)
                        else:
                            break
                if gabarito:
                    gabaritos_dict[tipo] = gabarito
        
        if not gabaritos_dict:
            return None, None, None, None, None, None
        
        # Extrai dados dos alunos (começam na linha 6)
        inicio_alunos = 6
        for i in range(5, len(df)):
            primeira_col = str(df.iloc[i, 0]).strip()
            if primeira_col and primeira_col.lower() not in ['nan', 'aluno', '']:
                inicio_alunos = i
                break
        
        alunos_df = df.iloc[inicio_alunos:].copy()
        alunos_df = alunos_df.dropna(how='all', axis=0)
        alunos_df = alunos_df.reset_index(drop=True)
        
        if alunos_df.empty:
            return None, None, None, None, None, None
        
        # Identifica coluna de matrícula
        matricula_col_idx = None
        for col_idx, col_name in enumerate(alunos_df.columns):
            col_str = str(col_name).lower()
            if 'matrícula' in col_str or 'matricula' in col_str:
                matricula_col_idx = col_idx
                break

        # Identifica coluna FORM (atividade complementar)
        # A coluna FORM está na linha 5 (cabeçalho real), não nos nomes das colunas do pandas
        form_col_idx = None
        if len(df) > 5:  # Verifica se existe a linha de cabeçalho
            for col_idx in range(len(df.columns)):
                header_value = str(df.iloc[5, col_idx]).strip().upper()
                if header_value == 'FORM':
                    form_col_idx = col_idx
                    break

        return disciplina, gabaritos_dict, alunos_df, questoes_indices, matricula_col_idx, form_col_idx
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar planilha: {str(e)}")
        return None, None, None, None, None, None

def render_2periodo_system():
    """Renderiza interface do 2º Período"""
    st.title("📝 Conferência de Gabarito - 2º C POO")
    st.write("Digite seu **nome** para conferir suas respostas e o gabarito da prova.")
    
    nome_input = st.text_input("Digite seu Nome:", placeholder="Digite seu nome completo aqui", key="nome_2periodo")
    search_button = st.button("Pesquisar", key="btn_2periodo")
    
    if search_button and nome_input:
        nome_input = nome_input.strip()
        
        if not nome_input:
            st.warning("⚠️ Por favor, digite um nome válido.")
            # Mesmo com aviso, renderiza o gabarito comentado abaixo
            render_gabarito_comentado()
            return
        
        with st.spinner(f"🔍 Procurando **{nome_input}**..."):
            disciplina, gabaritos, alunos_df, questoes_indices, matricula_col_idx, form_col_idx = load_2periodo_data(URLS["2º Período - POO"])
            
            if alunos_df is None or alunos_df.empty or gabaritos is None:
                st.error("❌ Não foi possível carregar os dados.")
                render_gabarito_comentado()
                return
            
            # Busca pelo NOME (coluna 0)
            primeira_coluna = alunos_df.columns[0]
            alunos_df[primeira_coluna] = alunos_df[primeira_coluna].astype(str)
            resultado = alunos_df[alunos_df[primeira_coluna].str.contains(nome_input, case=False, na=False)]
            
            if not resultado.empty:
                aluno_dados = resultado.iloc[0]
                nome_completo = str(aluno_dados.iloc[0]).strip()
                tipo_prova = str(aluno_dados.iloc[1]).strip().upper()
                
                st.success(f"✅ **Aluno encontrado:** {nome_completo}")
                st.info(f"📚 **Disciplina:** {disciplina}")
                st.info(f"📋 **Tipo de Prova:** {tipo_prova}")
                
                if tipo_prova not in gabaritos:
                    st.error(f"❌ Gabarito não encontrado para o tipo: **{tipo_prova}**")
                else:
                    gabarito = gabaritos[tipo_prova]
                    
                    # Questões OBJETIVAS
                    respostas = []
                    for i in range(len(gabarito)):
                        if i < len(questoes_indices):
                            col_idx = questoes_indices[i]
                            if col_idx < len(aluno_dados):
                                resposta_aluno = str(aluno_dados.iloc[col_idx]).strip().upper()
                                if resposta_aluno == 'NAN' or not resposta_aluno:
                                    resposta_aluno = '-'
                            else:
                                resposta_aluno = '-'
                        else:
                            resposta_aluno = '-'
                        
                        gabarito_correto = gabarito[i]
                        status = "✅" if resposta_aluno == gabarito_correto else "❌"
                        
                        respostas.append({
                            "Questão": str(i + 1),
                            "Sua Resposta": resposta_aluno,
                            "Gabarito": gabarito_correto,
                            "Status": status
                        })
                    
                    # Questões DISCURSIVAS
                    questoes_discursivas = []
                    if len(aluno_dados) > 10:
                        nota_q9 = str(aluno_dados.iloc[10]).strip()
                        if nota_q9 and nota_q9.lower() != 'nan':
                            try:
                                questoes_discursivas.append({
                                    "Questão": "9 (Discursiva)",
                                    "Nota": f"{float(nota_q9):.1f}"
                                })
                            except:
                                pass
                    
                    if len(aluno_dados) > 11:
                        nota_q10 = str(aluno_dados.iloc[11]).strip()
                        if nota_q10 and nota_q10.lower() != 'nan':
                            try:
                                questoes_discursivas.append({
                                    "Questão": "10 (Discursiva)",
                                    "Nota": f"{float(nota_q10):.1f}"
                                })
                            except:
                                pass
                    
                    # Exibe resultados
                    df_respostas = pd.DataFrame(respostas)
                    st.subheader(f"📊 Comparativo - Tipo {tipo_prova}")
                    
                    st.write("**Questões Objetivas:**")
                    st.dataframe(df_respostas.set_index("Questão"), use_container_width=True, height=300)
                    
                    if questoes_discursivas:
                        st.write("**Questões Discursivas:**")
                        st.dataframe(pd.DataFrame(questoes_discursivas).set_index("Questão"), use_container_width=True)
                    
                    # Estatísticas
                    acertos_objetivas = df_respostas["Status"].value_counts().get("✅", 0)
                    erros_objetivas = df_respostas["Status"].value_counts().get("❌", 0)

                    # Calcula pontos das questões discursivas
                    pontos_discursivas = 0.0
                    num_discursivas = len(questoes_discursivas)
                    for questao in questoes_discursivas:
                        try:
                            nota_str = questao.get("Nota", "0.0")
                            pontos_discursivas += float(nota_str)
                        except:
                            pass

                    # Calcula pontos da atividade complementar (FORM)
                    atividade_pontos = 0.0
                    if form_col_idx is not None and form_col_idx < len(aluno_dados):
                        try:
                            atividade_valor = str(aluno_dados.iloc[form_col_idx]).strip()
                            if atividade_valor and atividade_valor.lower() != 'nan':
                                atividade_pontos = float(atividade_valor)
                        except (ValueError, IndexError):
                            pass

                    # TOTAL DE ACERTOS = objetivas + discursivas (sem contar FORM que é atividade extra)
                    total_acertos = float(acertos_objetivas) + pontos_discursivas

                    # TOTAL DE ERROS = pontos perdidos na prova
                    # Pontos totais da prova - acertos = erros
                    pontos_totais_prova = len(respostas) + num_discursivas  # 8 objetivas + 2 discursivas = 10
                    total_erros = pontos_totais_prova - total_acertos

                    # NOTA TOTAL = acertos objetivas + discursivas + FORM
                    nota_total = float(acertos_objetivas) + pontos_discursivas + atividade_pontos

                    # APROVEITAMENTO: considera objetivas (8 pts) + discursivas (2 pts) = 10 pontos totais da prova
                    percentual = (total_acertos / pontos_totais_prova * 100) if pontos_totais_prova > 0 else 0

                    # Exibe estatísticas
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("✅ Acertos", f"{total_acertos:.1f}")
                    col2.metric("❌ Erros", f"{total_erros:.1f}")
                    col3.metric("📈 Aproveitamento", f"{percentual:.1f}%")
                    col4.metric("🎯 Nota Total", f"{nota_total:.1f}")
                    
                    st.markdown("---") # Separador para a nova informação
                    if atividade_pontos > 0:
                        st.success(f"✅ **Atividade Complementar:** Você recebeu **{atividade_pontos:.1f} pontos** pela entrega da atividade, que foram somados à sua nota final.")
                    else:
                        st.warning("⚠️ **Atividade Complementar:** Não foi identificada a entrega da atividade complementar. Por isso, os 5.0 pontos correspondentes não foram somados à sua nota final.")
                    # --- Fim da Lógica para Atividade Complementar ---

            else:
                st.error(f"❌ **{nome_input}** não encontrado.")
                st.info("💡 **Dicas:**\n- Tente digitar apenas parte do nome (ex: 'David' ou 'Ranielly')\n- Verifique se você está cadastrado na planilha\n- Confira se não há erros de digitação")
    
    # Adiciona a nova funcionalidade no final, para que sempre apareça
    render_gabarito_comentado()

# ==================== SISTEMA 4º PERÍODOS (NOTAS DIRETAS) ====================
@st.cache_data(ttl=CACHE_TTL_DATA)
def load_4periodo_data(sheet_url):
    """Carrega planilha dos 4º períodos"""
    try:
        formato = get_url_format(sheet_url)
        if formato == 'xlsx':
            df = pd.read_excel(sheet_url, engine='openpyxl')
        else:
            df = pd.read_csv(sheet_url)
        
        # Disciplina (linha 1)
        disciplina = str(df.iloc[1, 0]) if len(df) > 1 else "Machine Learning"
        
        # Dados começam na linha 5
        alunos_df = df.iloc[5:].copy()
        alunos_df = alunos_df.dropna(how='all', axis=0)
        alunos_df = alunos_df.reset_index(drop=True)
        
        # Renomeia colunas
        if len(alunos_df.columns) >= 7:
            alunos_df.columns = ['Aluno', 'Matrícula', 'AV_01', 'AV_02', 'Final', 'Média', 'Situação']
        
        return disciplina, alunos_df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return None, None

def render_4periodo_system():
    """Renderiza interface do 4º Período"""
    st.title("📝 Consulta de Notas - 4º Períodos")
    st.write("Digite seu **nome** ou **matrícula** para consultar suas notas.")
    
    busca_input = st.text_input("Nome ou Matrícula:", placeholder="Ex: João Silva ou 1713448", key="busca_4periodo")
    search_button = st.button("Pesquisar", key="btn_4periodo")
    
    if search_button and busca_input:
        busca_input = busca_input.strip()
        
        if not busca_input:
            st.warning("⚠️ Por favor, digite um nome ou matrícula válida.")
            return
        
        with st.spinner(f"🔍 Procurando **{busca_input}**..."):
            disciplina, alunos_df = load_4periodo_data(URLS["4º Períodos - Machine Learning"])
            
            if alunos_df is None or alunos_df.empty:
                st.error("❌ Não foi possível carregar os dados.")
                return
            
            # Busca
            alunos_df['Aluno'] = alunos_df['Aluno'].astype(str)
            alunos_df['Matrícula'] = alunos_df['Matrícula'].astype(str)
            
            resultado = alunos_df[
                alunos_df['Aluno'].str.contains(busca_input, case=False, na=False) |
                alunos_df['Matrícula'].str.contains(busca_input, case=False, na=False)
            ]
            
            if not resultado.empty:
                aluno = resultado.iloc[0]
                
                st.success(f"✅ **Aluno encontrado:** {aluno['Aluno']}")
                st.info(f"📚 **Disciplina:** {disciplina}")
                st.info(f"🆔 **Matrícula:** {aluno['Matrícula']}")
                
                st.subheader("📊 Notas")
                
                # Tabela de notas
                notas_data = {
                    "Avaliação": ["AV.01", "AV.02", "Final", "Média"],
                    "Nota": [
                        str(aluno['AV_01']),
                        str(aluno['AV_02']),
                        str(aluno['Final']),
                        str(aluno['Média'])
                    ]
                }
                st.dataframe(pd.DataFrame(notas_data).set_index("Avaliação"), use_container_width=True)
                
                # Situação
                situacao = str(aluno['Situação']).strip()
                if situacao.upper() == 'APROVADO':
                    st.success(f"✅ **Situação:** {situacao}")
                elif situacao.upper() == 'REPROVADO':
                    st.error(f"❌ **Situação:** {situacao}")
                else:
                    st.warning(f"⚠️ **Situação:** {situacao}")
            else:
                st.error(f"❌ **{busca_input}** não encontrado.")
                st.info("💡 Tente digitar apenas parte do nome ou verifique a matrícula.")

# ==================== INTERFACE PRINCIPAL ====================
st.sidebar.title("🎓 Sistema de Consulta")
st.sidebar.write("Selecione seu período:")

periodo = st.sidebar.radio(
    "Período:",
    ["2º Período - POO", "4º Períodos - Machine Learning"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("📌 **Dica:** Selecione seu período acima e digite sua matrícula ou nome para consultar.")

# Renderiza sistema apropriado
if periodo == "2º Período - POO":
    render_2periodo_system()
else:
    render_4periodo_system()
