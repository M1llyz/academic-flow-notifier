# Arquitetura

Esse documento descreve a arquitetura conceitual do **Academic Flow Notifier**.

Seu objetivo é apresentar como os principais componentes do sistema se relacionam, quais responsabilidades cada um possui e como o fluxo de informações percorre a aplicação.

A arquitetura foi planejada priorizando:

* Baixo acoplamento entre componentes;
* Facilidade de evolução;
* Separação de responsabilidades;
* Preparação para futuras integrações com IA;
* Facilidade de manutenção.

Então, esse documento descreve a arquitetura em um nível conceitual. Os detalhes de implementação serão documentados conforme o projeto evoluir.

---

# Visão Geral

O Academic Flow Notifier é um sistema orientado a eventos.

Sempre que uma alteração relevante ocorre no cronograma acadêmico, o sistema identifica essa mudança, transforma-a em um **Academic Event** e inicia o fluxo responsável pela construção, aprovação e envio da notificação.

De forma simplificada, a arquitetura segue o fluxo abaixo.

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
         ┌─────────┼─────────┐
         ▼         ▼         ▼
    Templates      IA     Regras de Negócio
         └─────────┼─────────┘
                   ▼
      Construção da Mensagem
                   │
                   ▼
      Fila de Aprovação Humana
                   │
                   ▼
        Envio de Notificações
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
       Gmail        Outros canais futuros
```

---

# Princípios Arquiteturais

A arquitetura do projeto foi definida seguindo alguns princípios fundamentais.

## 1. Fonte única da verdade

O Trello será considerado a fonte oficial das informações relacionadas ao cronograma acadêmico. Todas as notificações serão geradas a partir dos dados presentes no quadro.

---

## 2. Arquitetura orientada a eventos

O sistema não trabalha diretamente com cards do Trello durante todo o fluxo.

Após a leitura dos dados, qualquer alteração relevante é convertida em um **Academic Event**, que passa a representar o evento para todos os demais componentes da aplicação.

Isso reduz o acoplamento entre integrações externas e regras internas do sistema.

---

## 3. Separação de responsabilidades

Cada componente possui apenas uma responsabilidade principal.

| Componente              | Responsabilidade                               |
| ----------------------- | ---------------------------------------------- |
| Trello                  | Fonte dos dados acadêmicos                     |
| Detector de Eventos     | Identificar alterações relevantes              |
| Modelo de Domínio       | Representar eventos acadêmicos                 |
| Construtor de Mensagens | Gerar notificações                             |
| IA                      | Aprimorar interpretação e comunicação (futuro) |
| Aprovação               | Validar mensagens antes do envio               |
| Notificação             | Enviar mensagens aos alunos                    |

---

## 4. Aprovação Humana

Mesmo com futuras integrações de Inteligência Artificial, nenhuma mensagem será enviada automaticamente sem respeitar a política de aprovação definida para o projeto. Essa decisão busca garantir maior confiabilidade, controle e segurança na comunicação com os alunos, evitando que mensagens equivocadas criadas pela IA sejam enviadas automaticamente.

---

# Componentes do Projeto

A estrutura inicial do projeto foi organizada de forma modular para facilitar futuras evoluções.

## src/integrations/trello

```text
Responsável pela comunicação com o Trello e obtenção dos dados do cronograma acadêmico.
```

---

## src/events

```text
Responsável por identificar alterações relevantes e convertê-las em eventos acadêmicos.
```

---

## src/messages

```text
Responsável por construir as notificações utilizando templates e, futuramente, Inteligência Artificial.
```

---

## src/approval

```text
Responsável por controlar o fluxo de aprovação antes do envio das notificações.
```

---

## src/persistence

```text
Responsável pelo armazenamento dos snapshots utilizados para comparação entre diferentes execuções do sistema.
```

---

## src/config

```text
Responsável por centralizar configurações da aplicação.
```

---

## workflows

```text
Responsável pelos fluxos de automação desenvolvidos no n8n.
```

---

## data

```text
Responsável pelo armazenamento de arquivos auxiliares utilizados durante a execução da aplicação.
```

---

## docs

```text
Responsável pela documentação técnica do projeto.
```

---

# Evolução da Arquitetura

O projeto foi planejado desde sua primeira versão para permitir evolução incremental. Entre as evoluções previstas estão:

* Integração com Inteligência Artificial;
* Agente para criação assistida de cards no Trello;
* Novos canais de notificação;
* Integração com calendário;
* Dashboard para acompanhamento;
* Novas regras inteligentes de comunicação.

A arquitetura busca permitir que essas funcionalidades sejam adicionadas sem necessidade de grandes refatorações no núcleo do sistema.