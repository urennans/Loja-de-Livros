import sys
import requests
import json

# URL do servidor FastAPI
BASE_URL = "http://127.0.0.1:8000"  # altere se seu servidor estiver em outro host/porta

# Testa se o servidor está online
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

# Listar livros
def listar_livros():
    try:
        r = requests.get(f"{BASE_URL}/livros/")
        r.raise_for_status()
        livros = r.json()
    except requests.exceptions.RequestException as e:
        print("❌ Erro de conexão:", e)
        return
    except ValueError:
        print("❌ Resposta do servidor não está em JSON:", r.text)
        return

    if not livros:
        print("\n⚠️ Nenhum livro cadastrado.\n")
        return

    print("\n=== Lista de livros ===")
    for p in livros:
        print(f"ID: {p.get('id', '?')} | Nome: {p.get('nome', '?')} | Preço: R$ {p.get('preco', 0):.2f}")
    print("=========================\n")

# Adicionar livro
def adicionar_livro():
    print("\nPreencha os dados do livro:")
    nome = input("Nome: ").strip()
    marca = input("Marca: ").strip()
    preco = input("Preço: ").strip()
    estoque = input("Estoque: ").strip()
    volume = input("Volume: ").strip()
    descricao = input("Descrição: ").strip()
    imagem_url = input("URL da imagem (opcional): ").strip()

    try:
        payload = {
            "nome": nome,
            "marca": marca,
            "preco": float(preco),
            "estoque": int(estoque),
            "volume": volume,
            "descricao": descricao,
            "imagem_url": imagem_url
        }
    except ValueError:
        print("❌ Preço ou estoque inválido. Tente novamente.")
        return

    try:
        r = requests.post(f"{BASE_URL}/livros/", json=payload)
        r.raise_for_status()
        print(f"\n✅ Livro '{nome}' adicionado com sucesso!\n")
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao adicionar livro:", e)
        if r is not None:
            print("Detalhe do servidor:", r.text)

# Deletar livro
def deletar_livro():
    listar_livros()
    livro_id = input("Digite o ID do livro a deletar: ").strip()
    if not livro_id.isdigit():
        print("❌ ID inválido.")
        return

    try:
        r = requests.delete(f"{BASE_URL}/livros/{livro_id}")
        r.raise_for_status()
        print(f"🗑️ Livro {livro_id} deletado com sucesso!\n")
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao deletar livro:", e)
        if r is not None:
            print("Detalhe do servidor:", r.text)

# Menu principal do administrador
def menu():
    while True:
        print("""
==========================
🧴 livroSHOP - ADMIN
==========================
1 - Listar livros
2 - Adicionar livro
3 - Deletar livro
0 - Sair
""")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            listar_livros()
        elif opcao == "2":
            adicionar_livro()
        elif opcao == "3":
            deletar_livro()
        elif opcao == "0":
            print("👋 Saindo...")
            sys.exit()
        else:
            print("❌ Opção inválida. Tente novamente.\n")

if __name__ == "__main__":
    testar_conexao()
    menu()
