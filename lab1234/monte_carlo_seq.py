import random
import time

N_TOTAL = 10_000_000

print("=" * 60)
print("ESTIMATIVA DE PI - MONTE CARLO SEQUENCIAL")
print("=" * 60)

inicio = time.time()

dentro = 0
for _ in range(N_TOTAL):
    x = random.random()
    y = random.random()
    if x * x + y * y <= 1.0:
        dentro += 1

fim = time.time()
tempo_ms = (fim - inicio) * 1000

pi_estimado = 4.0 * dentro / N_TOTAL

print(f"Total de pontos: {N_TOTAL:,}")
print(f"Pontos dentro do circulo: {dentro:,}")
print(f"Pi estimado: {pi_estimado:.6f}")
print(f"Valor real de pi: 3.141593")
print(f"Erro: {abs(pi_estimado - 3.141592653589793):.6f}")
print(f"Tempo sequencial: {tempo_ms:.2f} ms")
print("=" * 60)