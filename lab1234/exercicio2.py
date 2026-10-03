from mpi4py import MPI
import random
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Total de pontos
N_TOTAL = 10_000_000

# Calcular quantos pontos cada processo vai gerar
pontos_por_proc = N_TOTAL // size
if rank < N_TOTAL % size:
    pontos_por_proc += 1

# Cada processo gera seus pontos e conta quantos caem dentro
inicio = time.time()

dentro_local = 0
for _ in range(pontos_por_proc):
    x = random.random()
    y = random.random()
    if x * x + y * y <= 1.0:
        dentro_local += 1

fim = time.time()
tempo_local = fim - inicio

# Reduce: soma todos os contadores
total_dentro = comm.reduce(dentro_local, op=MPI.SUM, root=0)

# Apenas o rank 0 imprime o resultado
if rank == 0:
    pi_estimado = 4.0 * total_dentro / N_TOTAL
    
    print("=" * 60)
    print("ESTIMATIVA DE PI - METODO DE MONTE CARLO")
    print("=" * 60)
    print(f"Processos MPI: {size}")
    print(f"Total de pontos: {N_TOTAL:,}")
    print(f"Pontos dentro do circulo: {total_dentro:,}")
    print(f"Pi estimado: {pi_estimado:.6f}")
    print(f"Valor real de pi: 3.141593")
    print(f"Erro: {abs(pi_estimado - 3.141592653589793):.6f}")
    print(f"Tempo total: {tempo_local * 1000:.2f} ms")
    print("=" * 60)