#Nome: Camila Huang      RA:10419606
#Nome: Xuanjun Jin          RA:10436456
import requests
import concurrent.futures
import time

URL = "http://localhost:5000/agendamentos"

def enviar_requisicao(cientista_id):
    payload = {
        "telescopio_id": 1,
        "cientista_id": cientista_id,
        "horario_inicio_utc": "2025-12-01T03:00:00Z"
    }
    try:
        resposta = requests.post(URL, json=payload, timeout=10)
        return f"Cientista {cientista_id:2}: Status {resposta.status_code} - {resposta.text}"
    except Exception as e:
        return f"Cientista {cientista_id:2}: Erro - {e}"

if __name__ == '__main__':
    print("=" * 70)
    print("DISPARANDO 10 REQUISIÇÕES SIMULTÂNEAS PARA O MESMO HORÁRIO")
    print("=" * 70)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        resultados = list(executor.map(enviar_requisicao, range(1, 11)))
    
    for res in resultados:
        print(res)
    
    print("=" * 70)

