"""
Confere a corrente de integridade (hash) dos logs deste repositório --
registro_l3.csv e registro_paper_trading.csv. Qualquer pessoa pode rodar
isso, sem precisar de nada além do Python (nenhuma biblioteca externa),
pra confirmar que nenhuma linha de um dia já fechado foi alterada depois
de publicada.

Uso (com Python instalado):
    python verificar_integridade.py

Como funciona: cada linha nova, quando é gerada, ganha um hash SHA-256
calculado sobre os campos "automáticos" dela (o que o modelo calculou
naquele dia) mais o hash da linha anterior -- uma corrente. Se uma linha
antiga fosse alterada, o hash salvo deixaria de bater com o que dá pra
recalcular a partir do conteúdo dela, e a corrente quebraria a partir
dali -- é exatamente isso que este script confere, linha por linha.

Colunas manuais (preenchidas depois, como resultado_real e observacoes)
ficam DE FORA do hash de propósito -- são pra serem editadas com o tempo
conforme o resultado real de cada dia fica conhecido, e isso não conta
como violação de integridade.

Este script não depende de nenhum código do modelo em si (que é mantido
privado) -- só dos nomes das colunas "automáticas" de cada arquivo,
listados abaixo, que já são visíveis no cabeçalho dos próprios CSVs.
Se um dia esses conjuntos de colunas mudarem no modelo original, esta
lista precisa ser atualizada aqui também para a verificação continuar
correta.
"""
import csv
import hashlib
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent

ARQUIVOS = {
    "registro_l3.csv": [
        "data", "h4_sinal_hoje", "h4_direcao_hoje", "h11_condicao_saida_hoje",
        "posicao_aberta", "direcao_posicao", "data_entrada", "dias_em_posicao", "evento",
    ],
    "registro_paper_trading.csv": [
        "data", "direcao_mes", "contexto", "semanas_em_correcao", "categoria_h2",
        "sincronia_score", "sinal_entrada_swing", "sinal_entrada_intraday", "sinal_saida",
        "sinais_apoio_favoraveis", "resumo", "leitura_24_48h_direcao",
        "leitura_24_48h_acerto_24h", "leitura_24_48h_acerto_48h", "rsi2_mensal",
        "rsi2_semanal", "rsi2_diario", "sinal_baixa_extrema", "sinal_maxima_extrema",
    ],
}


def calcular_hash_linha(campos_automaticos: dict, hash_anterior: str) -> str:
    base = hash_anterior + "|" + "|".join(
        f"{campo}={campos_automaticos[campo]}" for campo in sorted(campos_automaticos)
    )
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


def verificar(caminho: Path, campos_automaticos: list) -> list:
    if not caminho.exists():
        return [f"{caminho.name}: arquivo não encontrado nesta pasta."]

    with caminho.open("r", encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f, delimiter=";"))

    problemas = []
    hash_anterior = ""
    linhas_com_hash = 0
    for linha in linhas:
        salvo = linha.get("hash", "")
        if salvo:
            linhas_com_hash += 1
            automaticos = {campo: linha.get(campo, "") for campo in campos_automaticos}
            esperado = calcular_hash_linha(automaticos, hash_anterior)
            if salvo != esperado:
                problemas.append(
                    f"{caminho.name}, linha de {linha.get('data', '?')}: o hash salvo não bate "
                    "com o recalculado -- os campos automáticos dessa linha podem ter sido "
                    "alterados depois de publicados."
                )
        # propaga sempre o valor REALMENTE salvo (nunca o recalculado) --
        # é assim que o motor gera o hash da próxima linha, e isso isola
        # uma eventual adulteração só na linha alterada, sem "contaminar"
        # as seguintes.
        hash_anterior = salvo

    sem_hash = len(linhas) - linhas_com_hash
    print(f"{caminho.name}: {len(linhas)} linha(s) no total, {linhas_com_hash} com hash conferido"
          + (f" ({sem_hash} linha(s) mais antiga(s), de antes dessa proteção existir, sem hash)."
             if sem_hash else "."))
    return problemas


def main():
    todos_problemas = []
    for nome_arquivo, campos in ARQUIVOS.items():
        todos_problemas += verificar(PASTA / nome_arquivo, campos)

    print()
    if todos_problemas:
        print("PROBLEMAS ENCONTRADOS:")
        for problema in todos_problemas:
            print(f"  - {problema}")
        sys.exit(1)
    else:
        print("Corrente de integridade OK em todos os arquivos verificados.")


if __name__ == "__main__":
    main()
