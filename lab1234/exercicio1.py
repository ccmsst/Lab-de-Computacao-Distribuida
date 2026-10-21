

from mpi4py import MPI
import random
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = 1000

def gerar_matriz(n):
    return [[random.random() for _ in range(n)] for _ in range(n)]

def multiplicar_fatia(A, B, inicio, fim):
    n = len(B)
    resultado = []
    for i in range(inicio, fim):
        linha = [0.0] * n
        for j in range(n):
            soma = 0.0
            for k in range(n):
                soma += A[i][k] * B[k][j]
            linha[j] = soma
        resultado.append(linha)
    return resultado

A = None
B = None

if rank == 0:
    print("=" * 60)
    print("MULTIPLICACAO DE MATRIZES DISTRIBUIDA - N =", N)
    print("=" * 60)
    print("Processos MPI:", size)
    A = gerar_matriz(N)
    B = gerar_matriz(N)
    print("Matrizes geradas!")

A, B = comm.bcast((A, B), root=0)

linhas_por_proc = N // size
inicio = rank * linhas_por_proc
fim = inicio + linhas_por_proc
if rank == size - 1:
    fim = N

inicio_calc = time.time()
parte_local = multiplicar_fatia(A, B, inicio, fim)
fim_calc = time.time()

todas_partes = comm.gather(parte_local, root=0)

if rank == 0:
    C = []
    for parte in todas_partes:
        C.extend(parte)
    soma_C = sum(sum(linha) for linha in C)
    print("Calculo concluido!")
    print("Soma de C:", round(soma_C, 4))
    print("Tempo:", round((fim_calc - inicio_calc) * 1000, 2), "ms")
    print("=" * 60)