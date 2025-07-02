# 🚨 Falha na execução da Pipeline

A seguinte execução da pipeline falhou:

- **Workflow:** ${{ github.workflow }}
- **Repositório:** ${{ github.repository }}
- **Branch:** ${{ github.ref_name }}
- **Commit:** ${{ github.sha }}
- **Responsável pela execução:** ${{ github.actor }}
- **Execução:** <https://github.com/${{> github.repository }}/actions/runs/${{ github.run_id }}

---

## 🧪 Etapas envolvidas

- Lint
- Testes em Linux, Windows, macOS
- Análise de Segurança

---

### ✅ Ações recomendadas

- Verificar os logs da execução no link acima
- Corrigir os erros indicados nos jobs falhos
- Relançar a pipeline ou abrir um Pull Request com as correções

---

🔁 Esta issue foi criada automaticamente por GitHub Actions.
