# Modelos de Dados - SCTEC

## 1. Entidade: Cientista (`Cientista`)
Representa o usuário que solicita tempo de observação.

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Identificador único. |
| `nome` | String | Nome completo do cientista. |
| `email` | String | E-mail de contato (único). |
| `instituicao` | String | Universidade ou laboratório de origem. |

## 2. Entidade: Telescópio (`Telescopio`)
Representa o equipamento espacial.

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Identificador único. |
| `nome` | String | Nome do telescópio (ex: "Hubble-Acad"). |
| `status` | String | Status atual (ex: "Ativo", "Manutenção"). |

## 3. Entidade: Agendamento (`Agendamento`)
Representa a reserva de um slot de tempo no telescópio.

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Identificador único. |
| `telescopio_id` | Integer (FK) | Referência ao Telescópio. |
| `cientista_id` | Integer (FK) | Referência ao Cientista. |
| `horario_inicio_utc` | DateTime | Início da observação (UTC). |
| `horario_fim_utc` | DateTime | Fim da observação (UTC). |
| `status` | String | "Confirmado", "Cancelado". |
| `criado_em_utc` | DateTime | Timestamp da criação. |
