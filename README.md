# RentSmart

Aplicação de orçamento de locação da R.M Imóveis, desenvolvida em Python com classes e objetos.

## Conteúdo

- app.py: aplicação de console.
- Relatorio_Teorico_RentSmart.pdf: análise, entradas/processamentos/saídas, classes, fluxograma e justificativa.
- projecao_exemplo_12_meses.csv: exemplo de referência com 12 meses.
- projecao_12_meses.csv: saída gerada ao executar a aplicação com o cenário ilustrativo.

## Executar

Requer Python 3.10 ou superior. O programa usa apenas a biblioteca padrão.

1. Abra um terminal nesta pasta.
2. Execute:

    python app.py

3. Informe as escolhas solicitadas. O resumo aparece no terminal e o programa gera projecao_12_meses.csv nesta pasta.

## Regras implementadas

- Apartamento: base de R$ 700,00; segundo quarto +R$ 200,00; garagem +R$ 300,00.
- Casa: base de R$ 900,00; segundo quarto +R$ 250,00; garagem +R$ 300,00.
- Estúdio: base de R$ 1.200,00; pacote opcional de duas vagas por R$ 250,00; vaga extra +R$ 60,00.
- Apartamento sem crianças: desconto de 5% após os adicionais.
- Taxa contratual: R$ 2.000,00, parcelada em até cinco parcelas.
- A projeção CSV cobre 12 meses e mantém aluguel e taxa contratual em colunas separadas. Se a divisão não fechar em centavos iguais, a última parcela ajusta a diferença.

## Exemplo do CSV

O cenário de exemplo considera um apartamento de dois quartos, uma vaga, cliente sem crianças e taxa em cinco parcelas. O aluguel mensal é R$ 1.140,00. Nos cinco primeiros meses, a projeção soma a parcela de R$ 400,00 da taxa ao aluguel; depois, mostra somente o aluguel.

## Publicar no GitHub

O enunciado pede um repositório GitHub com o código e os arquivos. O projeto local está pronto, mas não foi publicado em uma conta externa. Para concluir:

1. Crie um repositório vazio no GitHub com o nome RentSmart.
2. Abra um terminal nesta pasta e rode:

    git init
    git add app.py README.md Relatorio_Teorico_RentSmart.pdf projecao_exemplo_12_meses.csv projecao_12_meses.csv .gitignore
    git commit -m "Entrega do projeto RentSmart"
    git branch -M main
    git remote add origin https://github.com/SEU_USUARIO/RentSmart.git
    git push -u origin main

3. Substitua SEU_USUARIO pelo seu nome de usuário e cole o endereço real no campo de entrega da disciplina.

## Antes de entregar

- Confira se as regras de cada categoria atendem ao entendimento adotado na disciplina.
- Grave o vídeo pitch de até quatro minutos e publique o link, como pedido no enunciado.
- Acrescente o link do repositório à submissão.


