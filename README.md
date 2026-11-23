# RentSmart

Aplicativo de console em Python para calcular orçamentos de locação da R.M. Imóveis.

## O que o programa faz

- Calcula valores para apartamento, casa e estúdio.
- Aplica adicionais e o desconto previsto para apartamento sem crianças.
- Calcula e parcela a taxa contratual separadamente do aluguel.
- Exibe o resumo do orçamento e gera uma projeção de pagamentos para 12 meses em CSV.

## Requisitos e execução

Requer Python 3.10 ou superior. Usa apenas a biblioteca padrão.

Abra um terminal nesta pasta e execute:

```powershell
py app.py
```

O arquivo `projecao_12_meses.csv` será criado ou atualizado nesta pasta. Feche-o no Excel antes de executar novamente, para permitir que o programa o grave.

## Estrutura do código

`Imovel` é a classe-base. `Apartamento`, `Casa` e `Estudio` implementam regras específicas. `OrcamentoLocacao` calcula os valores, `ProjecaoPagamento` gera o CSV e `SistemaRentSmart` conduz a interação com a pessoa usuária.

## Regras de cálculo

- Apartamento: R$ 700,00 de base; segundo quarto +R$ 200,00; garagem +R$ 300,00; desconto de 5% sem crianças.
- Casa: R$ 900,00 de base; segundo quarto +R$ 250,00; garagem +R$ 300,00.
- Estúdio: R$ 1.200,00 de base; pacote de duas vagas por R$ 250,00; vaga extra +R$ 60,00.
- Taxa contratual: R$ 2.000,00, parcelável em até cinco vezes.
