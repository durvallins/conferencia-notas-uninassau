#!/bin/bash
# Script para fazer o primeiro commit no GitHub
# Copie e cole estes comandos no terminal (ajuste SEU_USUARIO)

# 1. Inicializar repositório Git (se necessário)
git init

# 2. Adicionar arquivos essenciais
git add .gitignore
git add README.md
git add app.py
git add requirements.txt

# 3. Verificar o que será commitado
echo "Arquivos que serão commitados:"
git status

# 4. Fazer o commit
git commit -m "Sistema unificado de conferência de notas e gabaritos

- Sistema integrado para 2º período (POO) e 4º períodos (ML)
- Busca por nome para 2º período
- Busca por nome ou matrícula para 4º períodos
- Comparação de gabaritos (tipos A, B, C)
- Exibição de questões objetivas e discursivas
- Cálculo automático de aproveitamento e notas
- Interface responsiva com Streamlit
- Leitura direta de Google Sheets públicas"

# 5. Conectar ao GitHub (SUBSTITUA SEU_USUARIO)
# git remote add origin https://github.com/SEU_USUARIO/conferencia-notas.git
# git branch -M main
# git push -u origin main

echo ""
echo "✅ Commit realizado com sucesso!"
echo ""
echo "⚠️  PRÓXIMOS PASSOS:"
echo "1. Crie o repositório no GitHub: https://github.com/new"
echo "2. Substitua SEU_USUARIO no comando acima"
echo "3. Execute os 3 últimos comandos comentados (#)"
