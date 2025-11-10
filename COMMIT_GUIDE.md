# 🚀 Guia Rápido de Commit

## 📦 Estrutura Final do Repositório

```
conferencia-notas/
├── .gitignore           # Arquivos a ignorar
├── README.md           # Documentação completa
├── app.py              # Sistema unificado (2º e 4º períodos)
├── requirements.txt    # Dependências Python
└── venv/              # (ignorado pelo git)
```

## ✅ Comandos para Commit

### 1️⃣ Inicializar Git (se ainda não foi feito)

```bash
cd /home/durval/Documentos/PROJETOS/conferencia-notas
git init
```

### 2️⃣ Adicionar Arquivos

```bash
# Adiciona apenas os arquivos essenciais
git add .gitignore
git add README.md
git add app.py
git add requirements.txt
```

### 3️⃣ Fazer o Commit

```bash
git commit -m "Sistema unificado de conferência de notas e gabaritos

- Sistema integrado para 2º período (POO) e 4º períodos (ML)
- Busca por nome para 2º período
- Busca por nome ou matrícula para 4º períodos
- Comparação de gabaritos (tipos A, B, C)
- Exibição de questões objetivas e discursivas
- Cálculo automático de aproveitamento e notas
- Interface responsiva com Streamlit
- Leitura direta de Google Sheets públicas"
```

### 4️⃣ Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Nome: `conferencia-notas` ou `sistema-conferencia-notas`
3. Descrição: `Sistema web para conferência de notas e gabaritos - Streamlit + Google Sheets`
4. Público ou Privado (sua escolha)
5. **NÃO marque** "Initialize with README"
6. Clique em **Create repository**

### 5️⃣ Conectar ao GitHub

```bash
# Substitua SEU_USUARIO pelo seu username do GitHub
git remote add origin https://github.com/SEU_USUARIO/conferencia-notas.git
git branch -M main
git push -u origin main
```

## 🔄 Commits Futuros

Para atualizações futuras:

```bash
git add .
git commit -m "Descrição das alterações"
git push origin main
```

## 🌐 Deploy no Streamlit Cloud

Após o push para GitHub:

1. Acesse: https://share.streamlit.io
2. Faça login com GitHub
3. Clique em **New app**
4. Selecione:
   - Repository: `seu-usuario/conferencia-notas`
   - Branch: `main`
   - Main file: `app.py`
5. Clique em **Deploy!**

**⏱️ Tempo de deploy:** 2-5 minutos

## ✅ Checklist Pré-Commit

- [x] Removidos arquivos de backup (`.backup`, `_old.py`, etc.)
- [x] Removidos notebooks de teste (`.ipynb`)
- [x] Removidos arquivos de configuração local (`links.txt`, etc.)
- [x] `.gitignore` atualizado
- [x] `README.md` completo e atualizado
- [x] URLs das planilhas configuradas em `app.py`
- [x] `requirements.txt` com todas as dependências

## 📋 Dependências no requirements.txt

```txt
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.0.0
```

## 🔐 URLs das Planilhas

As URLs já estão configuradas no `app.py`:

- **2º Período (CSV):** Com gabaritos e questões
- **4º Períodos (XLSX):** Com notas diretas

**⚠️ Importante:** As planilhas devem estar públicas no Google Sheets!

## 🎯 Resultado Esperado

Após o push, seu repositório terá:

- ✅ Código limpo e organizado
- ✅ Documentação completa
- ✅ Pronto para deploy no Streamlit Cloud
- ✅ Fácil manutenção futura

## 📞 Ajuda

Se encontrar problemas:

1. Verifique se as URLs das planilhas estão corretas
2. Confirme que as planilhas estão públicas
3. Teste localmente antes de fazer push: `streamlit run app.py`

---

**🎉 Pronto para commit!**
