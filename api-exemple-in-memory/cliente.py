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
    autor = input("Digite o autor do livro: ").strip()
    titulo = input("Digite o título do livro: ").strip()
    editora = input("Digite a editora do livro: ").strip()
    ano = int(input("Digite o ano de publicação do livro: ").strip())
    payload = {
        "autor": autor,
        "titulo": titulo,
        "editora": editora,
        "ano": ano
    }
    resp = requests.post(f'{API_URL}/livros', json=payload)
    print("\n Adicionar Livro:")
    tratar_resposta(resp)

def atualizar_totalmente_livro():
    selected_uuid = input("Digite o UUID do livro que deseja atualizar: ").strip()
    livro_id = selected_uuid
    print("\nDigite os dados atualizados do livro:")
    autor = input("Digite o autor do livro: ").strip()
    titulo = input("Digite o título do livro: ").strip()
    editora = input("Digite a editora do livro: ").strip()
    while True:
        ano_input = input("Digite o ano de publicação do livro: ").strip()
        try:
            ano = int(ano_input)
            if ano <= 0:
                raise ValueError("Ano deve ser maior que 0.")
            break
        except ValueError:
            print("Entrada inválida. Digite um número inteiro positivo ou deixe em branco para não alterar.")

    payload = {
        "autor": autor,
        "titulo": titulo,
        "editora": editora,
        "ano": ano
    }
    resp = requests.put(f'{API_URL}/livros/{livro_id}', json=payload)
    print("\n Atualizar Livro:")
    tratar_resposta(resp)

def atualizar_parcial_livro():
    selected_uuid = input("Digite o UUID do livro que deseja atualizar parcialmente: ").strip()
    livro_id = selected_uuid
    print("\nDigite os dados atualizados do livro (deixe em branco para não alterar):")
    autor = input("Digite o autor do livro: ").strip()
    titulo = input("Digite o título do livro: ").strip()
    editora = input("Digite a editora do livro: ").strip()
    while True:
        ano_input = input("Digite o ano de publicação do livro: ").strip()
        if ano_input == "":
            ano = None
            break
        try:
            ano = int(ano_input)
            if ano <= 0:
                raise ValueError("Ano deve ser maior que 0.")
            break
        except ValueError:
            print("Entrada inválida. Digite um número inteiro positivo ou deixe em branco para não alterar.")

    payload = {}
    if autor:
        payload["autor"] = autor
    if titulo:
        payload["titulo"] = titulo
    if editora:
        payload["editora"] = editora
    if ano is not None:
        payload["ano"] = ano

    resp = requests.patch(f'{API_URL}/livros/{livro_id}', json=payload)
    print("\n Atualizar Livro Parcialmente:")
    tratar_resposta(resp)

def menu():
    while True:
        print("\n" + "="*30)
        print("CLIENTE API DE LIVROS")
        print("="*30)
        print("1. Listar livros")
        print("2. Exibir livro pelo UUID")
        print("3. Adicionar livro")
        print("4. Editar totalmente o livro pelo UUID")
        print("5. Editar parcialmente o livre pelo UUID")
        print("0. Sair")

        # .strip() para remover espaços em branco
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            listar_livros()
        elif opcao == "2":
            exibir_livro_por_id()
        elif opcao == "3":
            adicionar_livro()
        elif opcao == "4":
            atualizar_totalmente_livro()
        elif opcao == "5":
            atualizar_parcial_livro()
        elif opcao == "0":
            print("Encerrando o cliente...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()