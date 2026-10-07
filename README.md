# Prova pública — modelo de swing/day-trade para o WIN (Roberta)

> ## ⏸️ Acompanhamento pausado desde 05/10/2026
>
> **O que aconteceu:** ao rodar o modelo ao vivo, notamos uma diferença
> entre os dados semanais históricos e os dados semanais ao vivo.
> Investigando, encontramos a causa: os dados semanais históricos usados
> nas análises e no ajuste do modelo incorporavam o fechamento da semana
> antes de a semana terminar — ou seja, "antecipavam" uma informação que,
> ao vivo, ainda não existe. O primeiro sintoma disso já tinha
> aparecido na correção da linha de
> 18/09/2026 neste repositório (commit de 21/09/2026, que
> ajustou os valores semanais daquele dia) — na época tratado como um
> erro pontual de exportação, hoje sabemos que fazia parte do mesmo
> problema. Isso afeta todos os ativos acompanhados (WIN
> aqui, e WDO, BOVA11, ITAUSA e ZS1 no repositório
> [outros-ativos-prova-publica](https://github.com/rcfcastro-FANNI/outros-ativos-prova-publica)).
>
> **O que isso significa:** o modelo atual (v1) foi ajustado sobre dados
> com esse problema, então os resultados históricos que embasaram a
> escolha dele não são confiáveis. Por isso decidimos pausar o
> acompanhamento, revisar o modelo e testá-lo de novo antes de continuar.
>
> **O que NÃO muda:** o histórico publicado até a última atualização
> (05/10/2026) fica preservado exatamente como está — nenhuma linha será
> editada ou apagada, e a corrente de hash continua verificável com
> `python verificar_integridade.py`.
>
> **Próximos passos:** previsão de retorno em cerca de um mês (início de
> novembro de 2026). O modelo revisado (v2) será publicado separado do
> v1, com uma corrente de hash nova e data de início própria, para que os
> dois períodos nunca se misturem.

Este repositório contém só o **histórico de resultados**, dia a dia, de
um modelo de swing/day-trade para o mini-índice futuro (WIN) da B3 —
gerado automaticamente, sem intervenção manual, desde que essa automação
foi criada.

## O que tem aqui

- `registro_l3.csv` — sinais de entrada/saída do modelo L/3 (o modelo
  oficial em uso), com o estado de uma posição hipotética dia a dia:
  abriu, manteve, fechou.
- `registro_paper_trading.csv` — o veredito diário de um segundo modelo
  (mantido em paralelo), incluindo a leitura de curto prazo (24-48h).
- `verificar_integridade.py` — um script simples, só com Python padrão
  (nenhuma biblioteca externa), que qualquer pessoa pode rodar pra
  conferir a integridade do histórico acima (ver a seção seguinte).

**O que NÃO tem aqui, de propósito:** nenhum código do modelo em si — a
lógica, os limiares, as hipóteses testadas. Isso é mantido privado. Este
repositório existe só pra tornar os *resultados* verificáveis
publicamente, não pra expor como o modelo funciona por dentro.

## Por que confiar nesse histórico

Cada linha nova, a partir do dia em que essa proteção foi criada, carrega
um hash (SHA-256) calculado sobre os dados daquele dia mais o hash da
linha anterior — uma corrente. Se uma linha de um dia já fechado fosse
alterada depois (por exemplo, pra "corrigir" um sinal que deu errado),
essa corrente quebraria de um jeito detectável.

Rode, com Python instalado:

```
python verificar_integridade.py
```

Isso confere a corrente inteira e avisa exatamente qual linha (se
alguma) não bate mais com o que deveria. Além disso, o próprio histórico
de commits deste repositório no GitHub registra quando cada atualização
aconteceu — outra camada de verificação, independente do hash.

Linhas anteriores à criação dessa proteção não têm coluna `hash` — não
há como provar retroativamente a integridade de um histórico anterior à
própria ferramenta que prova integridade.

## Colunas manuais

Algumas colunas (`resultado_real`, `seguiu_o_sinal`, `observacoes`) são
preenchidas manualmente, depois, conforme o resultado real de cada dia
fica conhecido — ficam de fora do hash de propósito, porque mudar de
"em branco" pra "preenchido" depois é o comportamento esperado, não uma
adulteração.
