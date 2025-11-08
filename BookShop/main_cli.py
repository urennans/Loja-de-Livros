import sys
import requests

BASE_URL = "http://127.0.0.1:8000"  # URL do seu servidor FastAPI
TOKEN = ""  # Se houver autenticação JWT, colocar aqui

HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

# ------------------ Funções ------------------

def testar_conexao():
    try:
        r = requests.get(f"{BASE_URL}/")
        if r.status_code == 200:
            print("✅ Conectado ao servidor:", BASE_URL)
        else:
            print("⚠️ Servidor respondeu com status:", r.status_code)
    except requests.exceptions.RequestException as e:
        print("❌ Não foi possível conectar ao servidor:", e)
        sys.exit()

def listar_livros():
    try:
        r = requests.get(f"{BASE_URL}/livros/", headers=HEADERS)
        r.raise_for_status()
        livros = r.json()
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao buscar livros:", e)
        return

    if not livros:
        print("⚠️ Nenhum livro disponível.")
        return

    print("\n=== Livros Disponíveis ===")
    for livro in livros:
        print(f"ID: {livro['id']} | Nome: {livro['nome']} | Preço: R$ {livro['preco']:.2f}")
    print("==========================\n")

# ------------------ Carrinho ------------------

def adicionar_carrinho():
    listar_livros()
    livro_id = input("Digite o ID do livro para adicionar ao carrinho: ").strip()
    quantidade = input("Quantidade: ").strip()

    try:
        r = requests.post(
            f"{BASE_URL}/carrinho/adicionar",
            headers=HEADERS,
            json={"livro_id": int(livro_id), "quantidade": int(quantidade)}
        )
        r.raise_for_status()
        print("✅ Livro adicionado ao carrinho!")
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao adicionar ao carrinho:", e)

def ver_carrinho():
    try:
        r = requests.get(f"{BASE_URL}/carrinho/itens", headers=HEADERS)
        r.raise_for_status()
        itens = r.json()
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao listar carrinho:", e)
        return

    if not itens:
        print("⚠️ Carrinho vazio.\n")
        return

    print("\n=== Carrinho ===")
    for item in itens:
        livro = item.get("livro", {})
        print(f"Item ID: {item['id']} | Livro: {livro.get('nome','?')} | Quantidade: {item['quantidade']} | Preço: R$ {livro.get('preco',0):.2f}")
    print("================\n")

def remover_item_carrinho():
    item_id = input("Digite o ID do item do carrinho para remover: ").strip()
    try:
        r = requests.delete(f"{BASE_URL}/carrinho/{item_id}", headers=HEADERS)
        r.raise_for_status()
        print("✅ Item removido com sucesso!")
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao remover item:", e)

def atualizar_quantidade_carrinho():
    item_id = input("Digite o ID do item do carrinho: ").strip()
    nova_quantidade = input("Nova quantidade: ").strip()
    try:
        r = requests.patch(
            f"{BASE_URL}/carrinho/{item_id}",
            headers=HEADERS,
            json={"quantidade": int(nova_quantidade)}
        )
        r.raise_for_status()
        print("✅ Quantidade atualizada!")
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao atualizar quantidade:", e)

# ------------------ Pedido ------------------

def finalizar_compra():
    try:
        r = requests.post(f"{BASE_URL}/pedidos/", headers=HEADERS)
        r.raise_for_status()
        print("✅ Compra finalizada com sucesso!")
        print("Resumo:", r.json())
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao finalizar compra:", e)

# ------------------ Avaliação ------------------

def avaliar_livro():
    listar_livros()
    livro_id = input("Digite o ID do livro que deseja avaliar: ").strip()
    nota = input("Nota (1-5): ").strip()
    comentario = input("Comentário (opcional): ").strip()

    try:
        r = requests.post(
            f"{BASE_URL}/avaliacoes/",
            headers=HEADERS,
            json={"livro_id": int(livro_id), "nota": int(nota), "comentario": comentario}
        )
        r.raise_for_status()
        print("✅ Avaliação enviada com sucesso!")
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao enviar avaliação:", e)

# ------------------ Menu ------------------

def menu():
    while True:
        print("""
==========================
🧴 livroSHOP - CLIENTE
==========================
1 - Ver livros
2 - Adicionar ao carrinho
3 - Ver carrinho
4 - Atualizar quantidade no carrinho
5 - Remover item do carrinho
6 - Finalizar compra
7 - Avaliar livro
0 - Sair
""")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            listar_livros()
        elif opcao == "2":
            adicionar_carrinho()
        elif opcao == "3":
            ver_carrinho()
        elif opcao == "4":
            atualizar_quantidade_carrinho()
        elif opcao == "5":
            remover_item_carrinho()
        elif opcao == "6":
            finalizar_compra()
        elif opcao == "7":
            avaliar_livro()
        elif opcao == "0":
            print("👋 Saindo...")
            sys.exit()
        else:
            print("❌ Opção inválida.\n")

# ------------------ Main ------------------

if __name__ == "__main__":
    testar_conexao()
    menu()
