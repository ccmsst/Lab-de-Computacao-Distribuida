# Design de Logs - SCTEC
Nome: Camila Huang      RA:10419606
Nome: Xuanjun Jin          RA:10436456
## 1. Log de Auditoria (JSON)
```json
{
  "timestamp_utc": "2025-10-26T18:00:05.123Z",
  "level": "AUDIT",
  "event_type": "AGENDAMENTO_CRIADO",
  "service": "servico-agendamento",
  "details": {
    "agendamento_id": 123,
    "horario_inicio_utc": "2025-12-01T03:00:00Z"
  }
}
