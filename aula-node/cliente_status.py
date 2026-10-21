import requests

def verificar_status(urls):
    """Função única que verifica status de qualquer servidor"""
    for url in urls:
        try:
            response = requests.get(url, timeout=3)
            dados = response.json()
            print(f"✅ {dados['service']:8} | Status: {dados['status']:6} | {dados['timestamp']}")
        except Exception as e:
            print(f"❌ {url}: offline ({e})")

if __name__ == "__main__":
    urls = [
        "http://localhost:5000/status",
        "http://localhost:3000/status"
    ]
    print("=" * 70)
    print("VERIFICAÇÃO DE STATUS DOS SERVIDORES")
    print("=" * 70)
    verificar_status(urls)
