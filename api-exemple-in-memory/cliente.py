import csv

import requests
import json

API_URL = "http://127.0.0.1:8000"
TIMEOUT = 10  # segundos de espera por resposta


def tratar_resposta(resp: requests.Response):
    """Imprime de forma amigável a resposta da API e devolve o JSON (ou None)."""
    try:
        data = resp.json()
    except ValueError:
        print(f"\nStatus: {resp.status_code}")
        print("Resposta sem JSON. Conteúdo:", resp.text)
        return None

    if resp.status_code >= 400:
        print(f"\nErro: ({resp.status_code})")

    print(json.dumps(data, indent=4, ensure_ascii=False))
    return data


def ler_ano(opcional=False):
    """Pergunta o ano até receber um inteiro positivo. Em branco só vale se opcional."""
    while True:
        texto = input("Digite o ano de publicação do livro: ").strip()
        if opcional and texto == "":
            return None
        try:
            ano = int(texto)
            if ano <= 0:
                raise ValueError("Ano deve ser maior que 0.")
            return ano
        except ValueError:
            if opcional:
                print("Entrada inválida. Digite um número inteiro positivo ou deixe em branco para não alterar.")
            else:
                print("Entrada inválida. Digite um número inteiro positivo.")

def importar_csv():
    caminho = input("Digite o caminho do arquivo CSV para importar: ").strip()
    try:
        with open(caminho, mode="rb") as f:
            leitor = csv.DictReader(f, delimiter=";")
            print("\nImportando livros do CSV...")
            total = 0
            for linha in leitor:
                payload = {
                    "autor": linha.get("autor", "").strip(),
                    "titulo": linha.get("titulo", "").strip(),
                    "editora": linha.get("editora", "").strip(),
                    "ano": int(linha.get("ano", 0)),
                }
                resp = requests.post(f"{API_URL}/livros/", json=payload, timeout=TIMEOUT)
                if resp.status_code == 201:
                    total += 1
                else:
                    print(f"Falha ao importar livro: {linha}. Status: {resp.status_code}")
                    tratar_resposta(resp)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar importar o CSV: {e}")


def listar_livros():
    print("\n Listar Livros com Paginação:")
    livros = []

    resp = requests.get(f"{API_URL}/livros/", params={"page": 1}, timeout=TIMEOUT)
    print("-" * 10 + " PÁGINA 1 " + "-" * 10)
    dados = tratar_resposta(resp)

    if resp.status_code != 200:
        return

    livros.extend(dados)
    total_paginas = int(resp.headers.get("X-Total-Pages", 1))

    for pagina in range(2, total_paginas + 1):
        resp = requests.get(f"{API_URL}/livros/", params={"page": pagina}, timeout=TIMEOUT)
        print("-" * 10 + f" PÁGINA {pagina} " + "-" * 10)
        dados = tratar_resposta(resp)

        if resp.status_code != 200:
            continue

        livros.extend(dados)

    print(f"\nTotal de livros listados: {len(livros)}")


def exibir_livro_por_id():
    livro_id = input("Digite o UUID do livro: ").strip()
    resp = requests.get(f"{API_URL}/livros/{livro_id}", timeout=TIMEOUT)
    print(f"\n Exibir Livro com UUID {livro_id}:")
    tratar_resposta(resp)


def adicionar_livro():
    print("\nDigite os dados do novo Livro:")
    autor = input("Digite o autor do livro: ").strip()
    titulo = input("Digite o título do livro: ").strip()
    editora = input("Digite a editora do livro: ").strip()
    ano = ler_ano()
    payload = {
        "autor": autor,
        "titulo": titulo,
        "editora": editora,
        "ano": ano,
    }
    resp = requests.post(f"{API_URL}/livros/", json=payload, timeout=TIMEOUT)
    print("\n Adicionar Livro:")
    tratar_resposta(resp)


def atualizar_totalmente_livro():
    livro_id = input("Digite o UUID do livro que deseja atualizar: ").strip()
    print("\nDigite os dados atualizados do livro:")
    autor = input("Digite o autor do livro: ").strip()
    titulo = input("Digite o título do livro: ").strip()
    editora = input("Digite a editora do livro: ").strip()
    ano = ler_ano()

    payload = {
        "autor": autor,
        "titulo": titulo,
        "editora": editora,
        "ano": ano,
    }
    resp = requests.put(f"{API_URL}/livros/{livro_id}", json=payload, timeout=TIMEOUT)
    print("\n Atualizar Livro:")
    tratar_resposta(resp)


def atualizar_parcial_livro():
    livro_id = input("Digite o UUID do livro que deseja atualizar parcialmente: ").strip()
    print("\nDigite os dados atualizados do livro (deixe em branco para não alterar):")
    autor = input("Digite o autor do livro: ").strip()
    titulo = input("Digite o título do livro: ").strip()
    editora = input("Digite a editora do livro: ").strip()
    ano = ler_ano(opcional=True)

    payload = {}
    if autor:
        payload["autor"] = autor
    if titulo:
        payload["titulo"] = titulo
    if editora:
        payload["editora"] = editora
    if ano is not None:
        payload["ano"] = ano

    if not payload:
        print("\nNenhum campo informado. Nada a atualizar.")
        return

    resp = requests.patch(f"{API_URL}/livros/{livro_id}", json=payload, timeout=TIMEOUT)
    print("\n Atualizar Livro Parcialmente:")
    tratar_resposta(resp)


def deletar_livro():
    livro_id = input("Digite o UUID do livro que deseja deletar: ").strip()
    confirmacao = input(f"Confirma a exclusão do livro {livro_id}? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Exclusão cancelada.")
        return

    resp = requests.delete(f"{API_URL}/livros/{livro_id}", timeout=TIMEOUT)
    print("\n Deletar Livro:")
    tratar_resposta(resp)

def menu():
    while True:
        print("\n" + "=" * 30)
        print("CLIENTE API DE LIVROS")
        print("=" * 30)
        print("1. Listar livros")
        print("2. Exibir livro pelo UUID")
        print("3. Adicionar livro")
        print("4. Editar totalmente o livro pelo UUID")
        print("5. Editar parcialmente o livro pelo UUID")
        print("6. Deletar livro pelo UUID")
        print("7. Importar livros de um arquivo CSV")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        try:
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
            elif opcao == "6":
                deletar_livro()
            elif opcao == "7":
                importar_csv()
            elif opcao == "0":
                print("Encerrando o cliente...")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except requests.exceptions.RequestException as erro:
            print(f"\nNão foi possível falar com a API: {erro}")


if __name__ == "__main__":
    menu()