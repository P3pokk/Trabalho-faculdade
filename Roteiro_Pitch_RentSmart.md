# Roteiro do vídeo pitch — RentSmart

**Duração estimada:** 3 a 3 minutos e 30 segundos. Substitua a tela conforme as indicações entre colchetes.

## 1. Abertura e problema — 0:00 a 0:35

Olá, meu nome é Pedro de Souza Teixeira Pacheco Luciani, RA 230746. Este é o RentSmart, um sistema de orçamento de locação para a R.M. Imóveis.

O problema que o projeto resolve é a dificuldade de calcular rapidamente o aluguel com adicionais, descontos e taxa contratual, além de prever os pagamentos ao longo do tempo. Fazer essas contas manualmente pode gerar erros e deixar pouco claro quanto o cliente pagará em cada mês.

## 2. Lógica e fluxo — 0:35 a 1:10

O fluxo começa pela escolha do tipo de imóvel. O programa coleta as opções aplicáveis, como quantidade de quartos, garagem, crianças ou vagas adicionais. Depois valida as respostas, calcula o subtotal, aplica as regras de preço e desconto, pergunta em quantas parcelas a taxa contratual será paga e apresenta o resumo do orçamento. Por fim, gera um arquivo CSV com a previsão de doze meses.

[Mostre o fluxograma no relatório teórico por alguns segundos.]

## 3. Classes e orientação a objetos — 1:10 a 1:55

O projeto usa orientação a objetos para separar responsabilidades. A classe abstrata `Imovel` reúne o comportamento comum. `Apartamento`, `Casa` e `Estudio` implementam as regras específicas de cada categoria. `OrcamentoLocacao` concentra os cálculos do orçamento, `ProjecaoPagamento` prepara e salva as doze linhas do CSV, e `SistemaRentSmart` conduz a interação com a pessoa usuária.

Essa organização facilita a leitura e a manutenção: cada classe cuida de uma parte do problema, e novas regras de imóvel podem ser incorporadas sem concentrar toda a lógica em um único bloco.

## 4. Demonstração da aplicação — 1:55 a 3:10

[Abra o terminal na pasta do projeto e execute `python app.py` — ou mostre a aplicação já aberta.]

Vou demonstrar um apartamento de dois quartos, com garagem, sem crianças, e a taxa contratual em cinco parcelas. O aluguel-base é 700 reais. O segundo quarto acrescenta 200, e a garagem, 300. O subtotal é 1.200 reais. Como foi informado que não há crianças, o sistema aplica o desconto de 5%, chegando a um aluguel mensal de 1.140 reais.

A taxa contratual de 2.000 reais é exibida separadamente, parcelada em cinco vezes de 400 reais. O resumo deixa visíveis o subtotal, o desconto, o aluguel e o parcelamento.

[Abra `projecao_12_meses.csv`.]

O CSV apresenta os pagamentos mês a mês. Nos cinco primeiros meses, soma ao aluguel a parcela da taxa contratual. Depois, mostra somente o aluguel mensal. Assim, a taxa e o aluguel ficam discriminados e a projeção pode ser aberta em um programa de planilhas.

## 5. Encerramento — 3:10 a 3:25

O RentSmart reúne cálculos, validação de entradas e projeção financeira em uma aplicação simples de usar. O uso de classes deixa as regras mais organizadas e facilita futuras melhorias. Obrigado!

## Checklist de gravação

- Mostrar o fluxograma do relatório teórico.
- Mostrar brevemente as classes no `app.py`.
- Executar o cenário demonstrativo ou mostrar o resumo gerado.
- Abrir o CSV e mostrar os 12 meses.
- Publicar o vídeo e copiar o link para a entrega.
