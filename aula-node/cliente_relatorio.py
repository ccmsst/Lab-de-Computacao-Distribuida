import requests

def buscar_relatorio(id_produto):
    url_flask = f"http://localhost:5000/detalhes/{id_produto}"
    url_node = f"http://localhost:3000/estoque/{id_produto}"
    
    try:
        res_flask = requests.get(url_flask)
        fiscal = res_flask.json()
        
        res_node = requests.get(url_node)
        estoque = res_node.json()
        
        # Combinar os dois JSONs
        resultado = {
            "id": id_produto,
            "nome": estoque.get("nome"),
            "preco": fiscal.get("preco"),
            "estoque": estoque.get("estoque")
        }
        
        print("=" * 70)
        print(f"ID: {resultado['id']} | Nome: {resultado['nome']} | "
              f"Preço: R$ {resultado['preco']} | Estoque: {resultado['estoque']}")
        print("=" * 70)
        
    except Exception as e:
        print(f"Erro: {e}")
        print("Verifique se ambos os servidores estão rodando!")

if __name__ == "__main__":
    id_input = input("Digite o ID do produto (1 ou 2): ")
    buscar_relatorio(id_input)

