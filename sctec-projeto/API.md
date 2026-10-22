# Contrato da API REST - SCTEC
Nome: Camila Huang      RA:10419606
Nome: Xuanjun Jin          RA:10436456
## HATEOAS
Todas as respostas incluem links para ações futuras.

### 1. `POST /agendamentos`
Cria uma nova reserva.

**Request Body:**
```json
{
  "telescopio_id": 1,
  "cientista_id": 7,
  "horario_inicio_utc": "2025-12-01T03:00:00Z"
}