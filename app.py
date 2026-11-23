from abc import ABC, abstractmethod
from dataclasses import dataclass
import csv
from pathlib import Path

TAXA_CONTRATUAL_CENTAVOS = 200_000
MAX_PARCELAS_CONTRATO = 5
MESES_PROJECAO = 12


def formatar_reais(valor_centavos: int) -> str:
    valor = f"{valor_centavos / 100:,.2f}"
    valor = valor.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {valor}"


def formatar_csv(valor_centavos: int) -> str:
    return formatar_reais(valor_centavos).removeprefix("R$ ")


class Imovel(ABC):
    def __init__(self, categoria: str, aluguel_base_centavos: int):
        self.categoria = categoria
        self.aluguel_base_centavos = aluguel_base_centavos

    @abstractmethod
    def calcular_adicionais(self) -> dict[str, int]:
        raise NotImplementedError

    @abstractmethod
    def calcular_desconto(self, subtotal_centavos: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def descricao(self) -> str:
        raise NotImplementedError


class Apartamento(Imovel):
    def __init__(self, quartos: int, vaga_garagem: bool, possui_criancas: bool):
        super().__init__("Apartamento", 70_000)
        self.quartos = quartos
        self.vaga_garagem = vaga_garagem
        self.possui_criancas = possui_criancas

    def calcular_adicionais(self) -> dict[str, int]:
        adicionais = {}
        if self.quartos == 2:
            adicionais["Segundo quarto"] = 20_000
        if self.vaga_garagem:
            adicionais["Vaga de garagem"] = 30_000
        return adicionais

    def calcular_desconto(self, subtotal_centavos: int) -> int:
        return subtotal_centavos * 5 // 100 if not self.possui_criancas else 0

    def descricao(self) -> str:
        return f"Apartamento, {self.quartos} quarto(s)"


class Casa(Imovel):
    def __init__(self, quartos: int, vaga_garagem: bool):
        super().__init__("Casa", 90_000)
        self.quartos = quartos
        self.vaga_garagem = vaga_garagem

    def calcular_adicionais(self) -> dict[str, int]:
        adicionais = {}
        if self.quartos == 2:
            adicionais["Segundo quarto"] = 25_000
        if self.vaga_garagem:
            adicionais["Vaga de garagem"] = 30_000
        return adicionais

    def calcular_desconto(self, subtotal_centavos: int) -> int:
        return 0

    def descricao(self) -> str:
        return f"Casa, {self.quartos} quarto(s)"


class Estudio(Imovel):
    def __init__(self, pacote_duas_vagas: bool, vagas_adicionais: int):
        super().__init__("Estúdio", 120_000)
        self.pacote_duas_vagas = pacote_duas_vagas
        self.vagas_adicionais = vagas_adicionais

    def calcular_adicionais(self) -> dict[str, int]:
        adicionais = {}
        if self.pacote_duas_vagas:
            adicionais["Pacote inicial de duas vagas"] = 25_000
            if self.vagas_adicionais:
                adicionais[f"{self.vagas_adicionais} vaga(s) adicional(is)"] = (
                    self.vagas_adicionais * 6_000
                )
        return adicionais

    def calcular_desconto(self, subtotal_centavos: int) -> int:
        return 0

    def descricao(self) -> str:
        if self.pacote_duas_vagas:
            quantidade = 2 + self.vagas_adicionais
            return f"Estúdio, pacote de estacionamento ({quantidade} vaga(s))"
        return "Estúdio, sem pacote de estacionamento"


@dataclass
class OrcamentoLocacao:
    imovel: Imovel
    parcelas_contrato: int

    def __post_init__(self):
        if not 1 <= self.parcelas_contrato <= MAX_PARCELAS_CONTRATO:
            raise ValueError("A taxa contratual pode ser parcelada de 1 a 5 vezes.")

    @property
    def adicionais(self) -> dict[str, int]:
        return self.imovel.calcular_adicionais()

    @property
    def subtotal_centavos(self) -> int:
        return self.imovel.aluguel_base_centavos + sum(self.adicionais.values())

    @property
    def desconto_centavos(self) -> int:
        return self.imovel.calcular_desconto(self.subtotal_centavos)

    @property
    def aluguel_mensal_centavos(self) -> int:
        return self.subtotal_centavos - self.desconto_centavos

    @property
    def parcelas_contrato_centavos(self) -> list[int]:
        base, resto = divmod(TAXA_CONTRATUAL_CENTAVOS, self.parcelas_contrato)
        parcelas = [base] * self.parcelas_contrato
        parcelas[-1] += resto
        return parcelas

    @property
    def valor_parcela_contrato_centavos(self) -> int:
        return self.parcelas_contrato_centavos[0]


class ProjecaoPagamento:
    CABECALHO = [
        "mes",
        "aluguel_mensal_R$",
        "parcela_taxa_contratual_R$",
        "total_previsto_R$",
    ]

    def __init__(self, orcamento: OrcamentoLocacao):
        self.orcamento = orcamento

    def gerar_linhas(self) -> list[dict[str, str]]:
        linhas = []
        parcelas_contrato = self.orcamento.parcelas_contrato_centavos
        for mes in range(1, MESES_PROJECAO + 1):
            parcela = parcelas_contrato[mes - 1] if mes <= len(parcelas_contrato) else 0
            total = self.orcamento.aluguel_mensal_centavos + parcela
            linhas.append({
                "mes": str(mes),
                "aluguel_mensal_R$": formatar_csv(
                    self.orcamento.aluguel_mensal_centavos
                ),
                "parcela_taxa_contratual_R$": formatar_csv(parcela),
                "total_previsto_R$": formatar_csv(total),
            })
        return linhas

    def salvar_csv(self, caminho: Path) -> Path:
        with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(
                arquivo,
                fieldnames=self.CABECALHO,
                delimiter=";",
            )
            escritor.writeheader()
            escritor.writerows(self.gerar_linhas())
        return caminho


class SistemaRentSmart:
    def ler_inteiro(self, mensagem: str, opcoes: set[int]) -> int:
        while True:
            valor = input(mensagem).strip()
            if valor.isdecimal() and int(valor) in opcoes:
                return int(valor)
            print(
                f"Opção inválida. Escolha um destes valores: "
                f"{', '.join(map(str, sorted(opcoes)))}."
            )

    def ler_sim_nao(self, mensagem: str) -> bool:
        escolha = self.ler_inteiro(f"{mensagem} (1 = sim, 2 = não): ", {1, 2})
        return escolha == 1

    def ler_inteiro_nao_negativo(self, mensagem: str) -> int:
        while True:
            valor = input(mensagem).strip()
            if valor.isdecimal():
                return int(valor)
            print("Digite um número inteiro igual ou maior que zero.")

    def escolher_imovel(self) -> Imovel:
        print("\nCategorias disponíveis")
        print("1 - Apartamento (1 quarto: R$ 700,00)")
        print("2 - Casa (1 quarto: R$ 900,00)")
        print("3 - Estúdio (R$ 1.200,00)")
        categoria = self.ler_inteiro("Escolha a categoria: ", {1, 2, 3})

        if categoria == 1:
            quartos = self.ler_inteiro("Quantidade de quartos (1 ou 2): ", {1, 2})
            garagem = self.ler_sim_nao("Incluir uma vaga de garagem por R$ 300,00?")
            criancas = self.ler_sim_nao("O cliente possui crianças?")
            return Apartamento(quartos, garagem, criancas)

        if categoria == 2:
            quartos = self.ler_inteiro("Quantidade de quartos (1 ou 2): ", {1, 2})
            garagem = self.ler_sim_nao("Incluir uma vaga de garagem por R$ 300,00?")
            return Casa(quartos, garagem)

        pacote = self.ler_sim_nao(
            "Incluir o pacote inicial de duas vagas por R$ 250,00?"
        )
        vagas_adicionais = 0
        if pacote:
            vagas_adicionais = self.ler_inteiro_nao_negativo(
                "Quantidade de vagas adicionais (0 ou mais): "
            )
        return Estudio(pacote, vagas_adicionais)

    def exibir_orcamento(self, orcamento: OrcamentoLocacao) -> None:
        imovel = orcamento.imovel
        print("\n" + "=" * 48)
        print("RENTSMART | RESUMO DO ORÇAMENTO")
        print("=" * 48)
        print(f"Imóvel: {imovel.descricao()}")
        print(f"Aluguel-base: {formatar_reais(imovel.aluguel_base_centavos)}")
        for nome, valor in orcamento.adicionais.items():
            print(f"{nome}: {formatar_reais(valor)}")
        print(
            f"Subtotal antes do desconto: "
            f"{formatar_reais(orcamento.subtotal_centavos)}"
        )
        print(f"Desconto: {formatar_reais(orcamento.desconto_centavos)}")
        print(
            f"Aluguel mensal: "
            f"{formatar_reais(orcamento.aluguel_mensal_centavos)}"
        )
        print(
            f"Taxa contratual separada: "
            f"{formatar_reais(TAXA_CONTRATUAL_CENTAVOS)}"
        )
        valores_parcelas = orcamento.parcelas_contrato_centavos
        if len(set(valores_parcelas)) == 1:
            print(
                f"Parcelamento da taxa: {orcamento.parcelas_contrato}x de "
                f"{formatar_reais(valores_parcelas[0])}"
            )
        else:
            print(
                f"Parcelamento da taxa: {orcamento.parcelas_contrato - 1}x de "
                f"{formatar_reais(valores_parcelas[0])} e última de "
                f"{formatar_reais(valores_parcelas[-1])}"
            )
        print("=" * 48)

    def executar(self) -> None:
        imovel = self.escolher_imovel()
        parcelas = self.ler_inteiro(
            "Parcelas para a taxa contratual (1 a 5): ",
            set(range(1, MAX_PARCELAS_CONTRATO + 1)),
        )
        orcamento = OrcamentoLocacao(imovel, parcelas)
        self.exibir_orcamento(orcamento)

        arquivo = Path("projecao_12_meses.csv")
        ProjecaoPagamento(orcamento).salvar_csv(arquivo)
        print(f"\nProjeção dos 12 meses salva em: {arquivo.resolve()}")


if __name__ == "__main__":
    SistemaRentSmart().executar()
