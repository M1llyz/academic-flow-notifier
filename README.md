# 📆 Academic Flow Notifier

> Automação acadêmica para monitoramento de cronogramas, geração de notificações e comunicação com alunos utilizando Trello, Python, n8n Google Sheets e estrutura preparada para IA.

## ℹ️ Sobre o projeto

O **Academic Flow Notifier** é um projeto que estou desenvolvendo para automatizar a comunicação acadêmica entre representantes de turma (eu) e alunos (minha turma), reduzindo o risco de perda de prazos importantes e facilitando o acompanhamento das atividades do semestre.

O projeto surgiu a partir de uma necessidade real que observei durante minha atuação como representante da turma na graduação.

Atualmente, o cronograma acadêmico é organizado em um quadro Kanban no Trello que criei e gerencio, onde adiciono prazos de provas, trabalhos, projetos, atividades práticas e demais entregas da turma. Apesar de facilitar a visualização das atividades, o Trello não oferece uma solução gratuita que permita notificar automaticamente alunos que acessam apenas o quadro público (O butler e power ups funciona somente pra membros do quadro). 

Já que só pra contextualizar, minha turma tem 20+ alunos e o plano free do Trello só permite 10 membros por quadro, então, deixar o quadro como uma url pública foi a única solução que encontrei, até tentei outros sistemas, mas o Trello foi o único que teve maior adesão pelos alunos, até pela interface intuitiva.

O objetivo desse projeto é então preencher essa lacuna através de uma arquitetura de automação externa capaz de monitorar alterações no cronograma acadêmico, identificar eventos relevantes e gerar notificações para os alunos de forma organizada, segura e escalável.

Esse projeto é complementar ao repositório **notion-wiki-academic-assistant**, responsável pela centralização e organização dos conteúdos acadêmicos da turma.

Enquanto a Wiki Acadêmica resolve o problema de **organização do conhecimento**, o Academic Flow Notifier resolve o problema de **comunicação e acompanhamento dos prazos acadêmicos**.

---

# 🎯 Objetivos

O projeto pretende automatizar tarefas como:

* Detectar novas atividades adicionadas ao Trello.
* Identificar atividades próximas do vencimento.
* Detectar alterações de prazo.
* Identificar atividades atrasadas.
* Gerar notificações acadêmicas de forma padronizada.
* Centralizar o fluxo de aprovação antes do envio das mensagens.
* Facilitar futuras integrações com IA para geração de mensagens com interpretação de contexto (evitando o uso de templates engessados).

---

# 🛠️ Tecnologias previstas

Esse projeto foi planejado para utilizar:

* Python
* Trello API
* n8n
* Google Sheets
* Gmail
* Inteligência Artificial (evolução futura, ainda em analise pois demanda orçamento para uso da API)

A arquitetura foi desenhada para permitir evolução incremental, mantendo baixo acoplamento entre os componentes e facilitando futuras integrações.

---

# 📂 Estrutura inicial

```text
academic-flow-notifier/
│
├── workflows/
├── src/
├── data/
├── docs/
├── README.md
└── main.py
```

A documentação técnica detalhada será mantida na pasta `docs/`.

---

# 📌 Status do projeto

Atualmente o projeto encontra-se na fase de planejamento da arquitetura.

## Concluído

* Definição do problema.
* Definição do objetivo do projeto.
* Estrutura inicial do repositório.
* Planejamento inicial da arquitetura.

## Em andamento

* Modelagem do domínio.
* Definição da arquitetura completa.
* Planejamento da V1.
* Integração com Trello.
* Motor de detecção de eventos com n8n.
* Sistema de aprovação.
* Envio automático de e-mails.

## Evoluções futuras

* Integração com IA.
* Agente para criação de cards no Trello.
* Novos canais de notificação.

---

# 🗺️ Roadmap

### V1

* Monitoramento do quadro Trello.
* Detecção de eventos acadêmicos com n8n.
* Sistema de aprovação.
* Envio de notificações por e-mail.
* Estrutura preparada para IA.

### V2

* Integração com IA para geração de mensagens.
* Agente para criação assistida de cards no Trello.
* Templates inteligentes.
* Aprimoramento das regras de classificação.

### V3

* Novos canais de notificação.
* Integração com calendário.
* Dashboard de acompanhamento.

---

# 📖 Documentação

A documentação técnica do projeto será organizada em:

* `docs/architecture.md`
* `docs/domain_model.md`
* `docs/decisions.md`
* `docs/backlog.md`
* `docs/lessons_learned.md`

---

> [!NOTE]
> Esse projeto foi desenvolvido a e continua evoluindo conforme novas necessidades surgem. Esse projeto está sendo desenvolvido para fins de estudo, aprendizado e construção de portfólio, além para resolver um problema real para apoiar a organização acadêmica da turma.


<p align="center">
  <img src="https://img.shields.io/badge/Feito%20com%20%E2%9D%A4%20por-Millyz%20%20-darkblue" alt="Feito por Millyz">
  <br>
</p>

