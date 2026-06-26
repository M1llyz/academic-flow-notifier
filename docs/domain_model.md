# Modelo de Domínio

Esse documento descreve o modelo de domínio do projeto **Academic Flow Notifier**.

Seu objetivo é definir os principais conceitos utilizados pelo sistema antes da implementação da lógica de negócio, servindo como referência para toda a arquitetura do projeto.

O modelo de domínio representa como o sistema enxerga os eventos acadêmicos e como essas informações percorrem o fluxo de automação, e não ferramentas, ele separa justamente a arquitetura orientada ao negócio de uma arquitetura orientada à ferramenta, dessa forma, o projeto suporta trocas de ferramentas sem grandes problemas, permitindo maior escalabilidade e melhor manutenção.

---

# Visão Geral

O **Academic Flow Notifier** foi projetado utilizando uma arquitetura baseada em eventos. Em vez de cada componente conversar diretamente com o Trello ou com outras integrações externas, todo o sistema trabalha sobre um objeto central chamado **Academic Event**.

Esse objeto representa qualquer acontecimento relevante ocorrido no cronograma acadêmico. A partir dele, todos os outros componentes do sistema executam suas responsabilidades.

```text
Trello
        │
        ▼
Academic Event
        │
        ├────────► Identificação
        │
        ├────────► Templates
        │
        ├────────► Aprovação
        │
        └────────► Notificações
```

Essa abordagem reduz o acoplamento entre os componentes e facilita futuras evoluções da arquitetura.

---

# Entidade Principal

## Academic Event

Representa qualquer evento acadêmico detectado pelo sistema. Um Academic Event é criado sempre que uma alteração relevante ocorre no cronograma acadêmico.

Exemplos:

* Nova atividade criada
* Nova prova adicionada
* Alteração de prazo
* Atividade próxima do vencimento
* Atividade atrasada

Todas as automações futuras do projeto utilizarão esse objeto como entrada.

---

# Entidades Previstas

Além do Academic Event, o projeto deverá evoluir para trabalhar com outras entidades.

## Card

Representa uma atividade existente no Trello. Inicialmente será a principal fonte de dados do sistema.

---

## Notification

Representa uma mensagem gerada pelo sistema para comunicação com os alunos. No futuro poderá possuir diferentes formatos dependendo do canal de envio.

Exemplos:

* WhatsApp
* Outros canais futuros

---

## Approval

Representa o processo de validação humana antes do envio de uma notificação. A aprovação permite garantir maior controle sobre mensagens geradas automaticamente, principalmente quando houver utilização de Inteligência Artificial.

---

## Student

Representa um destinatário das notificações. Inicialmente será utilizado apenas para envio de e-mails, mas poderá ser expandido futuramente para outros canais de comunicação.

---

## Snapshot

Representa uma fotografia do estado atual do quadro Trello. Será utilizado para comparar diferentes execuções da automação e identificar alterações relevantes no cronograma.

---

# Fluxo Conceitual

De forma simplificada, o fluxo do sistema será composto pelas seguintes etapas:

```text
Trello
        │
        ▼
Leitura dos Cards
        │
        ▼
Detecção de Eventos
        │
        ▼
Academic Event
        │
        ▼
Construção da Mensagem
        │
        ▼
Aprovação
        │
        ▼
Notificação
```

Cada etapa possui uma responsabilidade específica e independente. Essa separação permite que novos componentes sejam adicionados futuramente sem necessidade de reestruturar toda a arquitetura.

---

# Evolução do Modelo

O modelo apresentado nesse documento representa apenas a primeira versão da arquitetura. Novas entidades poderão ser adicionadas conforme o projeto evoluir, mantendo sempre o princípio de baixo acoplamento entre os componentes.

O objetivo é permitir que futuras funcionalidades, como agentes de IA, novos canais de comunicação ou integrações adicionais, possam ser incorporadas sem exigir grandes alterações na estrutura existente.
