import requests
import json

API_URL = "http://127.0.0.1:8000"


# implementando o tratamento da resposta da API
def tratar_resposta(resp: requests.Response):
    """ Imprimir de forma amigável a resposta da API, trantando erros."""
    try:
        # Levanta um erro para códigos de status 4xx ou 5xx
        data = resp.json()
    except ValueError:
        print(f"\nStatus: {resp.status_code}")
        print("Resposta sem JSON. Conteúdo:", resp.text)
        return
    if resp.status_code > 400:
        print(f"\nErro: ({resp.status_code})")

    print(json.dumps(data, indent=4, ensure_ascii=False))
    

# implementando a função para listar livros
def listar_livros():
    resp = requests.get(f'{API_URL}/livros')
    print("\n Listar Livros:")
    tratar_resposta(resp)


# implementando a função para exibir livro pelo UUID
def exibir_livro_por_id():
    livro_id = input("Digite o UUID do livro: ").strip()
    resp = requests.get(f'{API_URL}/livros/{livro_id}')
    print(f"\n Exibir Livro com UUID {livro_id}:")
    tratar_resposta(resp)

def adicionar_livro():
    print("\nDigite os dados do novo Livro:")
    autor = input("Digite o autor do livro: ")
    titulo = input("Digite o título do livro: ")
    editora = input("Digite a editora do livro: ")
    ano = int(input("Digite o ano de publicação do livro: "))
    payload = {
        "autor": autor,
        "titulo": titulo,
        "editora": editora,
        "ano": ano
    }
    resp = requests.post(f'{API_URL}/livros', json=payload)
    print("\n Adicionar Livro:")
    tratar_resposta(resp)


def menu():
    while True:
        print("\n" + "="*30)
        print("CLIENTE API DE LIVROS")
        print("="*30)
        print("1. Listar livros")
        print("2. Exibir livro pelo UUID")
        print("3. Adicionar livro")
        print("0. Sair")

        # .strip() para remover espaços em branco
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            listar_livros()
        elif opcao == "2":
            exibir_livro_por_id()
        elif opcao == "3":
            adicionar_livro()
        elif opcao == "0":
            print("Encerrando o cliente...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()