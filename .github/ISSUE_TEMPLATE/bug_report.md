name: 🐞 Bug Report
description: Reporte um problema ou comportamento inesperado no HTMLReader
title: "[Bug] "
labels: [bug]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        ## 📄 Descrição do problema
        Por favor, forneça uma descrição clara e concisa do problema.

  - type: textarea
    id: description
    attributes:
      label: Descrição do bug
      placeholder: Explique o problema que você encontrou...
      required: true

  - type: markdown
    attributes:
      value: |
        ## 🔁 Passos para reproduzir
        Liste os passos para reproduzir o problema:

  - type: textarea
    id: steps
    attributes:
      label: Passos para reproduzir
      placeholder: 1. Faça isso\n2. Faça aquilo\n3. Veja o erro
      required: true

  - type: markdown
    attributes:
      value: |
        ## ✅ Comportamento esperado
        O que você esperava que acontecesse?

  - type: textarea
    id: expected_behavior
    attributes:
      label: Comportamento esperado
      placeholder: Descreva o comportamento esperado
      required: true

  - type: markdown
    attributes:
      value: |
        ## 🧪 Ambiente de execução

  - type: checkboxes
    id: operating_system
    attributes:
      label: Sistema operacional
      description: Selecione todos que se aplicam
      options:
        - label: Windows
          value: windows
        - label: macOS
          value: macos
        - label: Linux
          value: linux

  - type: input
    id: python_version
    attributes:
      label: Versão do Python
      description: Exemplo: 3.12.0
      placeholder: Ex: 3.12.0

  - type: dropdown
    id: interface_used
    attributes:
      label: Interface usada
      options:
        - GUI (Tkinter)
        - CLI
        - API (FastAPI)

  - type: markdown
    attributes:
      value: |
        ## 📱 Informações sobre dispositivo móvel (se aplicável)

  - type: input
    id: device
    attributes:
      label: Dispositivo
      description: Exemplo: iPhone 13

  - type: input
    id: os_mobile
    attributes:
      label: Sistema Operacional do dispositivo móvel
      description: Exemplo: iOS 17

  - type: input
    id: browser_mobile
    attributes:
      label: Navegador móvel
      description: Exemplo: Safari

  - type: input
    id: browser_version_mobile
    attributes:
      label: Versão do navegador móvel
      description: Exemplo: 17.3.1

  - type: textarea
    id: additional_context
    attributes:
      label: Contexto adicional
      description: Logs, mensagens de erro, links, etc.

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist antes de enviar
      options:
        - label: Procurei se esse bug já foi reportado antes.
        - label: Usei a versão mais recente disponível do projeto.
        - label: Estou disposto(a) a ajudar com a correção (se possível).
      required: true
