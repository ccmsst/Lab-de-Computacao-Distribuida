"""
Processamento Distribuído de Logs com MPI
Autor: Camila Huang
RA: 10419606
Descrição: Programa para processar logs de forma distribuída usando MPI Scatter
"""

from mpi4py import MPI
import random
import sys
import time

# ============================================
# INICIALIZAÇÃO MPI
# ============================================
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ============================================
# FUNÇÃO PARA GERAR LOGS (apenas rank 0)
# ============================================
def gerar_logs(qtd):
    """
    Gera uma lista de logs simulados.
    
    Args:
        qtd (int): Número de logs a serem gerados
        
    Returns:
        list: Lista de strings no formato "IP MÉTODO ENDPOINT STATUS"
    """
    ips = [f"192.168.1.{i}" for i in range(2, 254)]
    endpoints = [
        "/",
        "/login",
        "/products",
        "/cart",
        "/checkout",
        "/api/users",
        "/api/orders"
    ]
    metodos = ["GET", "POST"]
    # Status com pesos: 200 aparece 3x mais que 404 e 500
    status = ["200", "200", "200", "404", "500"]
    
    logs = []
    for _ in range(qtd):
        ip = random.choice(ips)
        metodo = random.choice(metodos)
        endpoint = random.choice(endpoints)
        status_code = random.choice(status)
        log = f"{ip} {metodo} {endpoint} {status_code}"
        logs.append(log)
    
    return logs

# ============================================
# FUNÇÃO PARA CONTAR ERROS
# ============================================
def contar_erros(logs):
    """
    Conta quantos logs têm status 404 ou 500.
    
    Args:
        logs (list): Lista de strings de log
        
    Returns:
        int: Número de erros encontrados
    """
    erros = 0
    for log in logs:
        # O status é o último campo da linha
        status = log.split()[-1]
        if status in ["404", "500"]:
            erros += 1
    return erros

# ============================================
# PROCESSO PRINCIPAL
# ============================================
def main():
    # ==========================================
    # ETAPA 1: Geração do Dataset (apenas rank 0)
    # ==========================================
    if rank == 0:
        print(f"\n{'='*70}")
        print(f"🚀 INICIANDO PROCESSAMENTO DISTRIBUÍDO DE LOGS")
        print(f"{'='*70}")
        print(f"📊 Total de processos MPI: {size}")
        print(f"⏰ Início: {time.strftime('%H:%M:%S')}")
        
        # Gerar 500.000 logs
        TOTAL_LOGS = 500_000
        print(f"📝 Gerando {TOTAL_LOGS:,} logs simulados...")
        
        inicio_geracao = time.time()
        logs_completos = gerar_logs(TOTAL_LOGS)
        fim_geracao = time.time()
        
        print(f"✅ {len(logs_completos):,} logs gerados em {fim_geracao - inicio_geracao:.2f}s")
        
        # ==========================================
        # ETAPA 2: Divisão dos Dados
        # ==========================================
        # Ajustar para divisão exata
        if len(logs_completos) % size != 0:
            logs_completos = logs_completos[:len(logs_completos) - (len(logs_completos) % size)]
            print(f"⚠️  Ajustado para {len(logs_completos):,} logs (divisível por {size})")
        
        tamanho_parte = len(logs_completos) // size
        print(f"📦 Cada processo receberá {tamanho_parte:,} logs")
        print(f"{'='*70}\n")
        
        # Preparar dados para scatter
        dados_para_scatter = []
        for i in range(size):
            inicio = i * tamanho_parte
            fim = inicio + tamanho_parte
            dados_para_scatter.append(logs_completos[inicio:fim])
        
        # ==========================================
        # ETAPA 3: Distribuição com Scatter
        # ==========================================
        print(f"📤 Distribuindo dados via Scatter...")
        inicio_scatter = time.time()
        minha_parte = comm.scatter(dados_para_scatter, root=0)
        fim_scatter = time.time()
        print(f"✅ Distribuição concluída em {fim_scatter - inicio_scatter:.3f}s\n")
        
    else:
        # Workers: recebem dados via Scatter
        minha_parte = comm.scatter(None, root=0)
    
    # ==========================================
    # ETAPA 4: Processamento Local (todos os processos)
    # ==========================================
    inicio_processamento = time.time()
    quantidade_linhas = len(minha_parte)
    erros_encontrados = contar_erros(minha_parte)
    fim_processamento = time.time()
    
    tempo_processamento = fim_processamento - inicio_processamento
    
    # ==========================================
    # ETAPA 5: Envio de Resultados para o Master
    # ==========================================
    mensagem = f"Processo {rank} analisou {quantidade_linhas:,} linhas e encontrou {erros_encontrados:,} erros (tempo: {tempo_processamento:.3f}s)"
    
    # Enviar mensagem para o master (rank 0)
    if rank != 0:
        # Workers enviam para o master
        comm.send(mensagem, dest=0, tag=rank)
    else:
        # Master coleta as mensagens de todos os processos
        print(f"\n{'='*70}")
        print(f"📊 RESULTADOS DO PROCESSAMENTO DISTRIBUÍDO")
        print(f"{'='*70}")
        
        # Primeiro, exibir o resultado do próprio master (rank 0)
        print(f"✅ {mensagem}")
        
        # Coletar mensagens dos workers (ranks 1 a size-1)
        for worker_rank in range(1, size):
            msg_recebida = comm.recv(source=worker_rank, tag=worker_rank)
            print(f"✅ {msg_recebida}")
        
        # Estatísticas finais
        total_erros = erros_encontrados
        total_linhas = quantidade_linhas
        
        print(f"\n{'='*70}")
        print(f"📈 RESUMO FINAL")
        print(f"{'='*70}")
        print(f"📊 Total de logs processados: {total_linhas * size:,}")
        print(f"❌ Total de erros encontrados: {total_erros * size:,}")
        print(f"📈 Taxa de erro: {(total_erros / total_linhas * 100):.2f}%")
        print(f"⏰ Término: {time.strftime('%H:%M:%S')}")
        print(f"{'='*70}\n")

# ============================================
# PONTO DE ENTRADA
# ============================================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Erro no processo {rank}: {e}")
        sys.exit(1)
