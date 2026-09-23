import requests
import json

API_URL = "http://localhost:8000"


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
    pass


def menu():
    while True:
        print("\n" + "="*30)
        print("CLIENTE API DE LIVROS")
        print("="*30)
        print("1. Listar livros")
        print("2. Exibir livro pelo UUID")
        print("0. Sair")

        # .strip() para remover espaços em branco
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            listar_livros()
        elif opcao == "2":
            exibir_livro_por_id()
        elif opcao == "0":
            print("Encerrando o cliente...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()