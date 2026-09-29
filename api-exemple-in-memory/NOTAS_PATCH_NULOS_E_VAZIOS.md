# Tratamento de campos nulos e vazios em PATCH

Esta nota registra como tratar campos omitidos, `null` e valores em branco em uma atualização parcial com FastAPI e Pydantic 2.

## Contrato de entrada

Em um `PATCH`, cada campo deve poder ser omitido. A omissão significa "não altere este campo"; ela é diferente de enviar `null` ou uma string vazia.

```python
from pydantic import BaseModel, field_validator


class LivroPatch(BaseModel):
    autor: str | None = None
    titulo: str | None = None
    editora: str | None = None
    ano: int | None = None

    @field_validator("autor", "titulo", "editora", "ano")
    @classmethod
    def nao_aceitar_null(cls, valor):
        if valor is None:
            raise ValueError("não pode ser null; omita o campo para não alterá-lo")
        return valor
```

Os defaults `None` permitem a omissão. O validador rejeita `null` enviado explicitamente e o FastAPI responde com `422`; o endpoint não chega a gravar a alteração. É necessário importar `field_validator` de `pydantic`.

### Strings vazias ou em branco

O validador acima **não** rejeita `""` nem strings contendo apenas espaços: essas entradas são strings válidas e podem ser gravadas. Se esses valores não forem permitidos, valide os campos textuais também:

```python
    @field_validator("autor", "titulo", "editora")
    @classmethod
    def validar_texto(cls, valor):
        texto = valor.strip()
        if not texto:
            raise ValueError("não pode ser vazio ou conter apenas espaços")
        return texto
```

Esse validador é chamado para valores textuais fornecidos; campos omitidos continuam sem alteração. O `strip()` também normaliza o texto aceito antes da gravação. Para `ano`, uma string vazia não é um inteiro válido e é rejeitada pela validação do tipo.

## Gravação na memória

Use `model_dump(exclude_unset=True)` para produzir somente os campos que vieram na requisição e mesclá-los ao registro existente:

```python
alteracoes = livro_update.model_dump(exclude_unset=True)
livro_atualizado = {**livro_existente, **alteracoes}
livros_db[id] = livro_atualizado
```

Assim, campos omitidos preservam os valores atuais. Não use `exclude_none=True` como substituto da validação quando `null` deve ser erro: isso esconderia o `null` enviado em vez de rejeitá-lo. Depois da mesclagem, o registro completo é validado pelo modelo de resposta.

## Saída e persistência

- O modelo de resposta `Livro` declara os campos como não nulos. Um `null` no registro atualizado não satisfaz esse contrato e causa erro na validação da resposta.
- String vazia não é o mesmo que `null`: modelos com campos `str` aceitam `""`. Rejeite ou normalize texto em branco na entrada se ele não deve aparecer na saída nem ser gravado.
- Em um banco de dados real, aplique a mesma regra antes do `UPDATE`. Campo omitido deve ficar fora do comando de atualização; `null` só deve ser gravado se o contrato e a coluna permitirem; vazio deve ser tratado como um valor explícito ou rejeitado pela validação.
- `POST` e `PUT` normalmente exigem todos os campos do recurso. A semântica de omissão descrita aqui é específica da atualização parcial com `PATCH`.

## Comportamento do exemplo atual

No arquivo `api.py`, o `PATCH` já mescla os campos com `exclude_unset=True` e tenta rejeitar `null`. Porém, o validador não rejeita strings vazias ou compostas só por espaços. Além disso, `field_validator` precisa ser importado; sem esse import, a definição do modelo falha ao carregar o módulo.