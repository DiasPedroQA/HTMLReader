# HTMLReader

Aplicação para leitura e análise de HTML com interface Tkinter e parsing com BeautifulSoup.

## Estrutura

- `app/frontend`: Interface gráfica
- `app/backend`: Lógica e tratamento de HTML
- `tests`: Testes automatizados
- `logs`: Armazenamento de logs de execução
- `.github/workflows`: Integração contínua

## Como rodar os testes

```bash
pytest
```

## Como usar o HTMLReader

O HTMLReader foi projetado para facilitar a leitura, análise e manipulação de arquivos HTML de forma intuitiva, tanto para usuários iniciantes quanto avançados. A interface gráfica permite abrir arquivos, visualizar seu conteúdo e aplicar análises automáticas, como contagem de palavras, linhas e extração de informações.

### Passos básicos de uso

1. **Abra o aplicativo**: Execute o script principal da interface gráfica.
2. **Selecione um arquivo HTML**: Use o navegador de arquivos para escolher o arquivo desejado.
3. **Visualize e analise**: O conteúdo será exibido e você poderá aplicar funções de análise, como contagem de palavras ou linhas.
4. **Salve ou exporte resultados**: Caso deseje, salve o conteúdo processado ou exporte relatórios.

### Estrutura do Projeto

O projeto está organizado para separar responsabilidades e facilitar a manutenção:

#### Estruturas Locais

- **Frontend (`app/frontend`)**: Contém todos os arquivos relacionados à interface gráfica, como telas, widgets e controladores de eventos.
- **Backend (`app/backend`)**: Responsável pela lógica de negócio, manipulação de arquivos, parsing de HTML e serviços de análise.
- **Tests (`tests`)**: Scripts de teste automatizado para garantir a qualidade e funcionamento dos módulos.

#### Estruturas Globais

- **Logs (`logs`)**: Diretório para armazenar logs de execução, úteis para depuração e auditoria.
- **Workflows (`.github/workflows`)**: Configurações de integração contínua para automação de testes e deploy.
- **README.md**: Este arquivo, com instruções de uso, estrutura e informações gerais do projeto.

### Recomendações

- Sempre utilize ambientes virtuais para instalar dependências.
- Consulte os testes automatizados para exemplos de uso dos módulos.
- Para contribuir, siga o padrão de organização e documentação do projeto.

---

Com essa estrutura, o HTMLReader busca ser acessível, modular e fácil de evoluir, atendendo tanto a quem deseja apenas usar quanto a quem pretende contribuir com o desenvolvimento.
