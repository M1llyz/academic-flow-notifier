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

# Contrato Inicial do Academic Event

O **Academic Event** será o objeto central utilizado para representar qualquer acontecimento relevante identificado no cronograma acadêmico.

Ele será gerado a partir de uma fonte externa, inicialmente o Trello, e consumido pelos demais componentes do sistema, como notificações, aprovação, automações e futuras integrações com IA.

A ideia é evitar que o restante do sistema dependa diretamente do formato bruto dos cards do Trello.

---

## Estrutura Base

```json
{
  "event_id": "evt_001",
  "event_type": "DEADLINE_SOON",
  "source": "trello",
  "source_id": "card_123",
  "source_url": "https://trello.com/c/example",
  "title": "Banco de Dados | ATV1",
  "discipline": "Banco de Dados",
  "category": "ATIVIDADES PRÁTICAS",
  "description": "Resolver exercícios 1 a 5.",
  "due_date": "2026-08-20",
  "days_left": 3,
  "priority": "medium",
  "requires_approval": true,
  "status": "PENDING"
}
```

---

## Campos

| Campo               | Descrição                                                     |
| ------------------- | ------------------------------------------------------------- |
| `event_id`          | Identificador único do evento acadêmico.                      |
| `event_type`        | Tipo do evento detectado.                                     |
| `source`            | Origem do evento (inicialmente `trello`).                      |
| `source_id`         | Identificador do item na origem, como o ID do card no Trello. |
| `source_url`        | Link para o item original.                                    |
| `title`             | Título principal do evento.                                   |
| `discipline`        | Disciplina relacionada ao evento.                             |
| `category`          | Categoria acadêmica, geralmente baseada na lista do Trello.   |
| `description`       | Descrição ou instruções principais.                           |
| `due_date`          | Data de vencimento ou entrega.                                |
| `days_left`         | Quantidade de dias restantes para o prazo.                    |
| `priority`          | Prioridade estimada do evento.                                |
| `requires_approval` | Indica se o evento precisa de aprovação antes do envio.       |
| `status`            | Status atual do evento no fluxo de aprovação/notificação.     |

---

## Tipos de Evento

| Tipo                | Descrição                                       |
| ------------------- | ----------------------------------------------- |
| `NEW_CARD`          | Novo card identificado no cronograma acadêmico. |
| `DEADLINE_SOON`     | Atividade próxima do prazo de vencimento.       |
| `DEADLINE_TOMORROW` | Atividade com vencimento no dia seguinte.       |
| `DUE_DATE_CHANGED`  | Prazo de um card alterado.                      |

---

## Status do Evento

| Status              | Descrição                                                    |
| ------------------- | ------------------------------------------------------------ |
| `PENDING`           | Evento identificado e aguardando processamento ou aprovação. |
| `APPROVED`          | Evento aprovado para envio.                                  |
| `REJECTED`          | Evento rejeitado e não deve ser enviado.                     |
| `REWRITE_REQUESTED` | Evento aguardando nova versão da mensagem.                   |
| `SENT`              | Notificação enviada com sucesso.                             |

---

## Prioridades Previstas

| Prioridade | Uso esperado                                                   |
| ---------- | -------------------------------------------------------------- |
| `low`      | Eventos informativos ou de baixo impacto.                      |
| `medium`   | Atividades e lembretes comuns.                                 |
| `high`     | Provas, entregas importantes e eventos próximos do vencimento. |

---

## Exemplo: Nova Atividade

```json
{
  "event_id": "evt_002",
  "event_type": "NEW_CARD",
  "source": "trello",
  "source_id": "card_456",
  "source_url": "https://trello.com/c/example",
  "title": "Engenharia de Software | Questionário de Requisitos",
  "discipline": "Engenharia de Software",
  "category": "ATIVIDADES GERAIS",
  "description": "Responder o questionário disponibilizado no Moodle.",
  "due_date": "2026-08-25",
  "days_left": 10,
  "priority": "medium",
  "requires_approval": true,
  "status": "PENDING"
}
```

---

## Exemplo: Prazo Próximo

```json
{
  "event_id": "evt_003",
  "event_type": "DEADLINE_SOON",
  "source": "trello",
  "source_id": "card_789",
  "source_url": "https://trello.com/c/example",
  "title": "PCE | Entrega da Especificação",
  "discipline": "Projeto Curricular Extensionista",
  "category": "PCE",
  "description": "Entrega da especificação inicial do projeto.",
  "due_date": "2026-09-01",
  "days_left": 3,
  "priority": "high",
  "requires_approval": true,
  "status": "PENDING"
}
```
---

## Observações Arquiteturais

O Academic Event deve ser independente da ferramenta de origem. Embora a primeira fonte seja o Trello, o sistema deve permitir que, futuramente, eventos também possam ser gerados a partir de outras fontes, como Google Calendar, Notion, Moodle ou entrada manual.

Por isso, componentes como notificações, aprovação, IA e envio de mensagens não devem depender diretamente da estrutura bruta do Trello. Eles devem consumir apenas o Academic Event padronizado.

 ---

# Motor de Detecção de Eventos

O Motor de Detecção de Eventos é responsável por identificar alterações relevantes no cronograma acadêmico e convertê-las em **Academic Events**.

Sua função é comparar diferentes estados do cronograma (snapshots) e determinar quais acontecimentos devem iniciar um fluxo de notificação.

O restante da aplicação não precisa conhecer como essa detecção acontece. Todos os componentes trabalham apenas com os eventos produzidos por este motor.

---

## Funcionamento Geral

Cada execução da automação seguirá, de forma simplificada, o fluxo abaixo.

```text
Leitura do Trello
        │
        ▼
Snapshot Atual
        │
        ▼
Comparação com Snapshot Anterior
        │
        ▼
Detecção de Alterações
        │
        ▼
Academic Events
```

Caso nenhuma alteração relevante seja encontrada, nenhum evento será gerado.

---

## Regras Iniciais de Detecção

Nessa primeira versão do projeto, o sistema deverá identificar os seguintes eventos.

---

### 1. NEW_CARD

Representa um novo card adicionado ao cronograma acadêmico.

```text
Condição

* O card existe no snapshot atual.
* O card não existia no snapshot anterior.
```

Objetivo: informar aos alunos que uma nova atividade, prova ou entrega foi adicionada ao cronograma.

---

### 2. DEADLINE_SOON

Representa uma atividade próxima do vencimento.

```text
Condição

* O card possui data de entrega definida.
* Restam **3 dias** para o vencimento.
```

Objetivo: enviar um lembrete preventivo antes da data limite.

---

### 3. DEADLINE_TOMORROW

Representa um lembrete final antes do vencimento.

```text
Condição

* O card possui data de entrega definida.
* Resta **1 dia** para o prazo final.
```

Objetivo: reduzir a possibilidade de esquecimento da atividade.

---

### 4. DUE_DATE_CHANGED

Representa uma alteração na data de entrega.

```text
Condição

* O card existe em ambos os snapshots.
* A data de vencimento foi alterada.
```

Objetivo: informar os alunos sempre que um professor alterar um prazo previamente divulgado.

---

## Evitando Eventos Duplicados

A automação poderá ser executada diversas vezes ao longo do dia. Então, para evitar notificações duplicadas, cada evento deverá possuir uma identidade única baseada em seus principais atributos.

Conceitualmente, um evento será considerado único pela combinação entre:

* Origem do evento;
* Identificador do card;
* Tipo do evento;
* Data de vencimento (quando aplicável).

Essa estratégia garante que o mesmo lembrete não seja enviado repetidamente caso a automação seja executada mais de uma vez antes que o estado do cronograma seja alterado.

---

## Responsabilidades do Motor

O Motor de Detecção possui apenas uma responsabilidade:

**identificar eventos.**

Ele **não deve**:

* construir mensagens;
* decidir se haverá envio;
* comunicar alunos;
* aplicar regras de aprovação;
* utilizar Inteligência Artificial.

Essas responsabilidades pertencem a outros componentes da arquitetura. Essa separação mantém o projeto desacoplado e facilita futuras evoluções sem necessidade de alterar a lógica principal de detecção.

---

# Evolução do Modelo

O modelo apresentado nesse documento representa apenas a primeira versão da arquitetura. Novas entidades poderão ser adicionadas conforme o projeto evoluir, mantendo sempre o princípio de baixo acoplamento entre os componentes.

O objetivo é permitir que futuras funcionalidades, como agentes de IA, novos canais de comunicação ou integrações adicionais, possam ser incorporadas sem exigir grandes alterações na estrutura existente.
