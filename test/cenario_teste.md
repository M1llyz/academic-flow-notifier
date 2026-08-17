# Plano de Testes — Academic Flow Notifier

## Objetivo
Validar o fluxo completo antes da migração de ambiente local para produção/nuvem.

Este plano testa:

- detecção de novos cards no Trello;
- alteração de prazo;
- alteração de título;
- lembrete automático de prazo para amanhã;
- lembrete automático de prazo para 3 dias;
- aprovação manual pelo Google Sheets;
- envio automático pelo Gmail;
- registro no `Notification_Log`;
- remoção da fila `Pending_approval`;
- bloqueio de reenvio duplicado;
- tratamento de erro no envio.

---

## Preparação antes dos testes

### 1. Verificar containers

No terminal, rode:

```bash
docker compose ps
```

Confirme que estão ativos:

- `academic-flow-n8n`
- `academic-flow-python`

Se precisar subir novamente:

```bash
docker compose up -d
```

Se tiver alterado código Python antes dos testes:

```bash
docker compose build academic-flow-python
docker compose up -d academic-flow-python
```

---

### 2. Verificar n8n

Acesse:

```text
http://localhost:5678/home/workflows
```

Confirme que existem os dois workflows:

- Workflow 1: geração/envio de notificações;
- Workflow 2: despacho de aprovações.

---

### 3. Verificar Google Sheets

Na planilha `Academic Flow Control`, confira:

#### Aba `Students`

Para teste seguro, deixe apenas seu e-mail como apto a receber:

| situacao | aceita_receber_notificacao |
|---|---|
| ATIVO | SIM |

Para os demais alunos, deixe temporariamente:

| aceita_receber_notificacao |
|---|
| NÃO |

Assim você evita disparo acidental para a turma durante os testes.

#### Aba `Pending_approval`

Antes de começar, deve estar vazia.

#### Aba `Notification_Log`

Pode manter os registros antigos, mas anote a última linha para comparar depois.

---

## Cenário 1 — Novo card exige aprovação

### Objetivo
Validar que um card novo não é enviado automaticamente e entra em `Pending_approval`.

### Ação no Trello
Crie um card com:

```text
Título: TESTE 01 - Novo card para aprovação
Prazo: 07/07/2026
```

### Executar
No Workflow 1, execute manualmente.

### Resultado esperado no n8n
O item deve cair no ramo `false` do IF.

### Resultado esperado no Google Sheets
Na aba `Pending_approval`, deve aparecer uma linha com:

```text
nome_atividade = TESTE 01 - Novo card para aprovação
status_aprovacao = PENDENTE
status_envio = AGUARDANDO
data_envio = vazio
email_bcc = vazio
destinatarios = vazio
```

### Resultado esperado no Gmail
Nenhum e-mail deve ser enviado para os alunos.

---

## Cenário 2 — Aprovação manual envia e move para o log

### Objetivo
Validar o Workflow 2 completo: aprovar, enviar, registrar no log e remover da fila.

### Ação no Google Sheets
Na aba `Pending_approval`, localize o card:

```text
TESTE 01 - Novo card para aprovação
```

Altere:

```text
status_aprovacao: PENDENTE → APROVADO
```

Mantenha:

```text
status_envio = AGUARDANDO
```

### Executar
No Workflow 2, execute manualmente.

### Resultado esperado no Gmail
Você deve receber o e-mail da atividade.

### Resultado esperado em `Notification_Log`
Deve aparecer uma nova linha com:

```text
nome_atividade = TESTE 01 - Novo card para aprovação
status_aprovacao = APROVADO
status_envio = ENVIADO
data_envio preenchida
email_bcc preenchido
destinatarios preenchido
```

### Resultado esperado em `Pending_approval`
A linha do teste deve ser removida.

---

## Cenário 3 — Card novo pendente não deve ser enviado

### Objetivo
Validar que o Workflow 2 ignora registros ainda pendentes.

### Ação no Trello
Crie um card com:

```text
Título: TESTE 02 - Card pendente não enviar
Prazo: 08/07/2026
```

### Executar
Execute o Workflow 1.

### Ação no Google Sheets
Não aprove a linha. Mantenha:

```text
status_aprovacao = PENDENTE
status_envio = AGUARDANDO
```

### Executar
Execute o Workflow 2.

### Resultado esperado

- Nenhum e-mail deve ser enviado.
- A linha deve continuar em `Pending_approval`.
- Nenhuma linha nova referente a esse card deve aparecer em `Notification_Log`.

---

## Cenário 4 — Rejeição manual

### Objetivo
Validar que itens rejeitados não são enviados e são tratados corretamente.

### Ação no Google Sheets
Use o card do cenário anterior:

```text
TESTE 02 - Card pendente não enviar
```

Altere:

```text
status_aprovacao: PENDENTE → REJEITADO
```

### Executar
Execute o Workflow 2.

### Resultado esperado

O comportamento esperado depende da implementação atual:

- Se o fluxo de rejeição já estiver implementado:
  - não envia e-mail;
  - registra em `Notification_Log` com `status_aprovacao = REJEITADO`;
  - remove de `Pending_approval`.

- Se o fluxo de rejeição ainda não estiver implementado:
  - não envia e-mail;
  - a linha permanece em `Pending_approval`.

### Observação
Se a rejeição ainda não estiver implementada, registrar como ajuste pendente antes da produção.

---

## Cenário 5 — Alteração de prazo exige aprovação

### Objetivo
Validar que mudança de prazo não dispara automaticamente.

### Ação no Trello
Escolha um card existente e altere o prazo.

Sugestão:

```text
Título original: TESTE 03 - Alteração de prazo
Novo prazo: 09/07/2026
```

Se o card não existir, crie primeiro:

```text
Título: TESTE 03 - Alteração de prazo
Prazo inicial: 10/07/2026
```

Execute o Workflow 1 uma vez para registrar o snapshot.

Depois altere o prazo para:

```text
09/07/2026
```

Execute o Workflow 1 novamente.

### Resultado esperado
Na aba `Pending_approval`, deve aparecer:

```text
tipo_atividade = DUE_DATE_CHANGED
nome_atividade = TESTE 03 - Alteração de prazo
status_aprovacao = PENDENTE
status_envio = AGUARDANDO
```

Nenhum e-mail deve ser enviado automaticamente.

---

## Cenário 6 — Alteração de título exige aprovação

### Objetivo
Validar que mudança de título não dispara automaticamente.

### Ação no Trello
Crie ou escolha um card existente.

Sugestão inicial:

```text
Título: TESTE 04 - Título original
Prazo: 10/07/2026
```

Execute o Workflow 1 uma vez para registrar snapshot.

Depois altere o título para:

```text
TESTE 04 - Título atualizado
```

Execute o Workflow 1 novamente.

### Resultado esperado
Na aba `Pending_approval`, deve aparecer:

```text
tipo_atividade = TITLE_CHANGED
nome_atividade = TESTE 04 - Título atualizado
status_aprovacao = PENDENTE
status_envio = AGUARDANDO
```

Nenhum e-mail deve ser enviado automaticamente.

---

## Cenário 7 — Lembrete para amanhã envia automaticamente

### Objetivo
Validar envio automático para atividade que vence amanhã.

### Ação no Trello
Crie um card com prazo para amanhã.

Se hoje for `02/07/2026`, use:

```text
Título: TESTE 05 - Vence amanhã
Prazo: 03/07/2026
```

### Importante
Na primeira execução, um card novo pode gerar `NEW_CARD` e cair em aprovação.

Para testar o lembrete automático corretamente:

1. Crie o card.
2. Execute o Workflow 1 uma vez para registrar o card como novo.
3. Execute o Workflow 1 novamente.

### Resultado esperado
Na segunda execução, deve gerar:

```text
tipo_atividade = DEADLINE_TOMORROW
status_envio = ENVIADO
```

### Resultado esperado no Gmail
Você deve receber o e-mail automaticamente.

### Resultado esperado no `Notification_Log`
Deve aparecer uma linha com:

```text
nome_atividade = TESTE 05 - Vence amanhã
status_aprovacao = NÃO SE APLICA
status_envio = ENVIADO
```

---

## Cenário 8 — Lembrete para 3 dias envia automaticamente

### Objetivo
Validar envio automático para atividade que vence em 3 dias.

### Ação no Trello
Crie um card com prazo para daqui a 3 dias.

Se hoje for `02/07/2026`, use:

```text
Título: TESTE 06 - Vence em 3 dias
Prazo: 05/07/2026
```

### Importante
Assim como no cenário anterior:

1. Crie o card.
2. Execute o Workflow 1 uma vez para registrar `NEW_CARD`.
3. Execute o Workflow 1 novamente para detectar `DEADLINE_SOON`.

### Resultado esperado
Na segunda execução, deve gerar:

```text
tipo_atividade = DEADLINE_SOON
status_envio = ENVIADO
```

### Resultado esperado no Gmail
Você deve receber o e-mail automaticamente.

### Resultado esperado no `Notification_Log`
Deve aparecer:

```text
nome_atividade = TESTE 06 - Vence em 3 dias
status_aprovacao = NÃO SE APLICA
status_envio = ENVIADO
```

---

## Cenário 9 — Bloqueio de duplicidade no envio automático

### Objetivo
Garantir que o mesmo lembrete automático não seja enviado várias vezes.

### Pré-condição
Use o card do cenário 7 ou 8, que já foi enviado automaticamente.

### Executar
Execute o Workflow 1 novamente sem alterar nada no Trello.

### Resultado esperado

- Nenhum novo e-mail deve ser enviado para esse mesmo evento.
- Nenhuma nova linha duplicada deve ser criada em `Notification_Log`.
- O arquivo de estado/processamento deve impedir reenvio.

---

## Cenário 10 — Múltiplas aprovações ao mesmo tempo

### Objetivo
Validar que o Workflow 2 processa mais de uma linha aprovada sem apagar linha errada.

### Ação no Trello
Crie três cards:

```text
Título: TESTE 07 - Aprovação em lote A
Prazo: 11/07/2026
```

```text
Título: TESTE 08 - Aprovação em lote B
Prazo: 12/07/2026
```

```text
Título: TESTE 09 - Aprovação em lote C
Prazo: 13/07/2026
```

### Executar
Execute o Workflow 1.

### Ação no Google Sheets
Na aba `Pending_approval`, altere os três registros para:

```text
status_aprovacao = APROVADO
status_envio = AGUARDANDO
```

### Executar
Execute o Workflow 2.

### Resultado esperado

- Você recebe 3 e-mails.
- São criadas 3 linhas em `Notification_Log`.
- As 3 linhas somem de `Pending_approval`.
- Nenhuma linha pendente incorreta deve ser apagada.

---

## Cenário 11 — Mistura de aprovado e pendente

### Objetivo
Validar que o Workflow 2 só envia o que foi aprovado.

### Ação no Trello
Crie dois cards:

```text
Título: TESTE 10 - Aprovado na mistura
Prazo: 14/07/2026
```

```text
Título: TESTE 11 - Pendente na mistura
Prazo: 15/07/2026
```

### Executar
Execute o Workflow 1.

### Ação no Google Sheets
Na aba `Pending_approval`:

Para `TESTE 10`:

```text
status_aprovacao = APROVADO
status_envio = AGUARDANDO
```

Para `TESTE 11`:

```text
status_aprovacao = PENDENTE
status_envio = AGUARDANDO
```

### Executar
Execute o Workflow 2.

### Resultado esperado

- Apenas `TESTE 10` deve ser enviado.
- `TESTE 10` deve ir para `Notification_Log`.
- `TESTE 10` deve sair de `Pending_approval`.
- `TESTE 11` deve continuar em `Pending_approval`.

---

## Cenário 12 — Aluno inativo não recebe

### Objetivo
Validar filtro da aba `Students`.

### Ação no Google Sheets
Na aba `Students`, escolha um destinatário de teste e coloque:

```text
situacao = INATIVO
aceita_receber_notificacao = SIM
```

### Ação no Trello
Crie um card aprovado ou automático.

Sugestão:

```text
Título: TESTE 12 - Aluno inativo não recebe
Prazo: 16/07/2026
```

### Executar
Execute o fluxo correspondente.

### Resultado esperado

- O e-mail desse aluno não deve aparecer no `email_bcc`.
- O aluno não deve receber a notificação.

---

## Cenário 13 — Aluno ativo que não aceita receber não recebe

### Objetivo
Validar filtro `aceita_receber_notificacao`.

### Ação no Google Sheets
Na aba `Students`, escolha um destinatário e coloque:

```text
situacao = ATIVO
aceita_receber_notificacao = NÃO
```

### Ação no Trello
Crie um card aprovado ou automático.

Sugestão:

```text
Título: TESTE 13 - Não aceita receber
Prazo: 17/07/2026
```

### Resultado esperado

- O e-mail desse aluno não deve aparecer no `email_bcc`.
- O aluno não deve receber a notificação.

---

## Cenário 14 — Erro no envio automático gera log e alerta

### Objetivo
Validar tratamento de erro no Workflow 1.

### Ação no n8n
No node Gmail do Workflow 1, force temporariamente um erro.

Sugestões seguras:

- usar um destinatário inválido no campo `To`; ou
- remover temporariamente o BCC; ou
- usar um e-mail inválido controlado.

### Ação no Trello
Crie um card com envio automático.

Sugestão:

```text
Título: TESTE 14 - Erro no envio automático
Prazo: amanhã
```

### Executar
Execute o Workflow 1.

### Resultado esperado

- O Gmail falha.
- `Notification_Log` registra `status_envio = ERRO`.
- Você recebe um e-mail de alerta administrativo.

### Pós-teste
Desfaça a alteração que forçou o erro.

---

## Cenário 15 — Erro no envio aprovado gera log e alerta

### Objetivo
Validar tratamento de erro no Workflow 2.

### Ação no Trello
Crie um card:

```text
Título: TESTE 15 - Erro após aprovação
Prazo: 18/07/2026
```

Execute o Workflow 1 para gerar linha em `Pending_approval`.

### Ação no Google Sheets
Altere para:

```text
status_aprovacao = APROVADO
status_envio = AGUARDANDO
```

### Ação no n8n
Force erro temporário no Gmail do Workflow 2.

### Executar
Execute o Workflow 2.

### Resultado esperado

- O Gmail falha.
- `Notification_Log` registra `status_envio = ERRO`.
- Você recebe um e-mail de alerta administrativo.

### Pós-teste
Desfaça a alteração que forçou o erro.

---

## Cenário 16 — Execução sem eventos

### Objetivo
Validar que o sistema não faz nada quando não há novidades.

### Executar
Execute o Workflow 1 sem criar ou alterar cards.

### Resultado esperado

- Nenhum e-mail enviado.
- Nenhuma nova linha em `Pending_approval`.
- Nenhuma nova linha em `Notification_Log`.

Execute também o Workflow 2 sem linhas aprovadas.

### Resultado esperado

- Nenhum e-mail enviado.
- Nada removido de `Pending_approval`.
- Nada adicionado em `Notification_Log`.

---

## Checklist final de validação

Marque após concluir todos os testes:

```text
[ ] Novo card entra em Pending_approval
[ ] Aprovação manual envia e move para Notification_Log
[ ] Pendentes não são enviados
[ ] Rejeitados são tratados corretamente ou registrados como pendência de implementação
[ ] Alteração de prazo exige aprovação
[ ] Alteração de título exige aprovação
[ ] Prazo amanhã envia automaticamente
[ ] Prazo em 3 dias envia automaticamente
[ ] Envio automático não duplica
[ ] Múltiplas aprovações funcionam
[ ] Mistura APROVADO/PENDENTE funciona
[ ] Aluno INATIVO não recebe
[ ] Aluno com aceita_receber_notificacao = NÃO não recebe
[ ] Erro no Workflow 1 gera log e alerta
[ ] Erro no Workflow 2 gera log e alerta
[ ] Execução sem eventos não gera ações indevidas
```

---

## Observações para correção antes da produção

Use esta seção durante os testes:

```text
Problema encontrado:

Cenário:

Comportamento esperado:

Comportamento atual:

Ajuste necessário:

Status:
```

---

## Critério para considerar a V1 pronta para produção

A V1 pode ser considerada pronta para migração local → nuvem quando:

- todos os cenários críticos passarem;
- não houver envio duplicado;
- `Pending_approval` funcionar como fila limpa;
- `Notification_Log` registrar corretamente envios e erros;
- alunos inativos ou opt-out não receberem;
- alertas administrativos funcionarem;
- os workflows estiverem nomeados e organizados;
- os containers estiverem estáveis;
- as variáveis sensíveis estiverem no `.env`.
