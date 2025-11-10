# 📝 Sistema de Conferência de Notas

Sistema web unificado usando **Streamlit** para permitir que alunos consultem suas notas e comparem suas respostas com o gabarito oficial de suas provas.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

## ✨ Funcionalidades

### 🎓 2º Período - POO (Programação Orientada a Objetos)
- **🔍 Busca por Nome:** Digite seu nome ou parte dele (ex: "David" ou "Arthur")
- **📊 Comparativo de Gabaritos:** Respostas do aluno vs gabarito correto (tipos A, B ou C)
- **📝 Questões Objetivas:** 8 questões de múltipla escolha com status ✅/❌
- **✍️ Questões Discursivas:** Notas das questões 9 e 10 (0.0 a 1.0 pontos cada)
- **📈 Estatísticas Completas:** Acertos, erros, aproveitamento percentual e nota total

### 🎓 4º Períodos - Machine Learning
- **🔍 Busca por Nome ou Matrícula:** Pesquisa flexível por qualquer um dos dois
- **📊 Notas Completas:** AV.01, AV.02, Prova Final e Média geral
- **✅ Situação Acadêmica:** Aprovado/Reprovado
- **🎯 Interface Intuitiva:** Visualização clara de todas as avaliações

### 🌟 Recursos Gerais
- **☁️ Google Sheets:** Carrega dados diretamente de planilhas públicas (CSV/Excel)
- **🔄 Cache Inteligente:** Atualização automática a cada 10 minutos
- **📱 Totalmente Responsivo:** Funciona perfeitamente em desktop e mobile
- **🚀 Deploy Simples:** Pronto para Streamlit Cloud em 2 minutos

## 🚀 Deploy Rápido

### Streamlit Cloud (Recomendado)

1. **Fork** este repositório
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Faça login com GitHub
4. Clique em **"New app"**
5. Selecione:
   - **Repository:** `seu-usuario/conferencia-notas`
   - **Branch:** `main`
   - **Main file:** `app.py`
6. Clique em **"Deploy!"**

⏱️ **Em 2-5 minutos** seu app estará no ar!

## 💻 Instalação Local

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/conferencia-notas.git
cd conferencia-notas

# 2. Crie um ambiente virtual (recomendado)
python -m venv venv

# 3. Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute o sistema
streamlit run app.py
```

🌐 O sistema abrirá automaticamente em: **http://localhost:8501**

## 📖 Como Usar

### Para Alunos do 2º Período (POO)
1. Na barra lateral, selecione **"2º Período - POO"**
2. Digite seu **nome** (pode ser parcial, ex: "David" ou "Ranielly")
3. Clique em **"Pesquisar"**
4. Visualize:
   - ✅ Suas respostas comparadas com o gabarito oficial
   - 📊 Estatísticas de acertos e erros
   - �� Notas das questões discursivas (9 e 10)
   - 🎯 Nota total da avaliação

### Para Alunos do 4º Período (Machine Learning)
1. Na barra lateral, selecione **"4º Períodos - Machine Learning"**
2. Digite seu **nome** ou **matrícula**
3. Clique em **"Pesquisar"**
4. Visualize:
   - 📊 Todas as suas notas (AV.01, AV.02, Final, Média)
   - ✅ Sua situação acadêmica (Aprovado/Reprovado)

## ⚙️ Configuração das Planilhas

### URLs das Planilhas

As URLs das planilhas estão configuradas no arquivo `app.py` (linhas 7-10):

```python
URLS = {
    "2º Período - POO": "URL_DA_PLANILHA_2_PERIODO",
    "4º Períodos - Machine Learning": "URL_DA_PLANILHA_4_PERIODOS"
}
```

### Como Tornar uma Planilha Pública

Para que o sistema possa ler os dados, as planilhas do Google Sheets devem estar **públicas**:

1. Abra a planilha no Google Sheets
2. Clique em **"Compartilhar"** (canto superior direito)
3. Clique em **"Alterar para qualquer pessoa com o link"**
4. Escolha: **"Qualquer pessoa com o link"** → **"Leitor"**
5. Clique em **"Concluído"**
6. Copie o link de compartilhamento

### Formato das Planilhas

#### 2º Período - POO (com Gabaritos)
```
Linha 1: Números das questões (1, 2, 3, ...)
Linha 2: Gabarito Tipo A
Linha 3: Gabarito Tipo B  
Linha 4: Gabarito Tipo C
Linha 5: Cabeçalhos (Aluno, Tipo Prova, questões...)
Linha 6+: Dados dos alunos
```

**Colunas importantes:**
- Coluna 0: Nome do Aluno
- Coluna 1: Tipo de Prova (A, B ou C)
- Colunas 2-9: Respostas das questões objetivas (1-8)
- Coluna 10: Nota questão discursiva 9 (0.0-1.0)
- Coluna 11: Nota questão discursiva 10 (0.0-1.0)
- Coluna 15: TOTAL GERAL (nota final)

#### 4º Períodos - Machine Learning
```
Linha 5: Cabeçalhos (Aluno, Matrícula, AV.01, AV.02, Final, Média, Situação)
Linha 6+: Dados dos alunos
```

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)** - Framework web para Python
- **[Pandas](https://pandas.pydata.org/)** - Manipulação e análise de dados
- **[openpyxl](https://openpyxl.readthedocs.io/)** - Leitura de arquivos Excel
- **[Google Sheets](https://www.google.com/sheets/about/)** - Armazenamento de dados

## 📁 Estrutura do Projeto

```
conferencia-notas/
├── app.py                   # ⭐ Aplicação principal (sistema unificado)
├── app_4periodos.py         # Sistema separado 4º períodos (backup)
├── requirements.txt         # Dependências do projeto
├── README.md               # Este arquivo
├── DEPLOY.md               # Guia detalhado de deploy
├── .gitignore              # Arquivos ignorados pelo Git
└── links.txt               # URLs das planilhas (exemplo)
```

## 🔧 Dependências

```txt
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.0.0
```

## 🐛 Solução de Problemas

### Erro: "Não foi possível carregar os dados"
**Causa:** Planilha não está pública ou URL incorreta  
**Solução:** 
1. Verifique se a planilha está pública (veja seção "Configuração das Planilhas")
2. Teste a URL diretamente no navegador
3. Confirme que o formato é CSV ou XLSX

### Erro: "Aluno não encontrado"
**Causa:** Nome digitado incorretamente ou aluno não está cadastrado  
**Solução:**
1. Tente digitar apenas parte do nome (ex: "David" ao invés de "David Ranielly Pereira Silva")
2. Verifique a grafia do nome
3. Confirme se o aluno está cadastrado na planilha

### Cache não atualiza
**Causa:** Streamlit está usando dados em cache  
**Solução:**
1. Pressione `C` no navegador enquanto o app está aberto (Clear Cache)
2. Ou adicione `?v=1` no final da URL (incremente quando precisar atualizar)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autor

Desenvolvido para facilitar a consulta de notas e gabaritos dos alunos dos cursos de Análise e Desenvolvimento de Sistemas.

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📞 Suporte

- 📧 Email: [seu-email@exemplo.com](mailto:seu-email@exemplo.com)
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/conferencia-notas/issues)
- 📚 Documentação Streamlit: [docs.streamlit.io](https://docs.streamlit.io)

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
