from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from services.db import session
from model.Veiculo_model import Veiculo
from model.CtEngate import CtEngate
class EngateDesengateVeiculo(QtWidgets.QMainWindow):  #Trativas do ENGATE
    def __init__(self):
        super().__init__()
        uic.loadUi('telaCtEngate.ui', self)
        self.criando_novo_engate()
        #self.botaoTelaDesengate.clicked.connect(self.chamar_tela_desengate)
        self.nrFrota.textChanged.connect(self.preencher_placa_frota)
        self.nrConjunto.textChanged.connect(self.preencher_placa_conjunto)
        self.show()
        self.desengate_view = None

    def preencher_placa_frota(self):
        nrFrota = self.nrFrota.text()
        response = session.query(Veiculo).filter(Veiculo.NRFROTA == nrFrota).first()
        if response is not None:
            self.nrPlacaFrota.setText(response.NRPLACA)
        else:
            self.nrPlacaFrota.clear()

    def preencher_placa_conjunto(self):
        nrConjunto = self.nrConjunto.text()
        # Procura os veículos com o número do conjunto
        veiculos = session.query(Veiculo).filter(Veiculo.NRCONJUNTO == nrConjunto).all()
        # Se não houver veículos com o conjunto informado, limpa os campos de placa
        if not veiculos:
            self.nrPlacaA.clear()
            self.nrPlacaB.clear()
            return
        # Se houver veículos com o conjunto informado, preenche os campos de placa
        # Considerando que a lista de veículos contenha apenas dois veículos com as placas A e B
        if len(veiculos) == 2:
            self.nrPlacaA.setText(veiculos[0].NRPLACA)
            self.nrPlacaB.setText(veiculos[1].NRPLACA)
        else:
            QMessageBox.warning(self, "Aviso", "Mais de dois veículos encontrados com o mesmo conjunto.")

    def criando_novo_engate(self):
        self.botaoSalvar.clicked.connect(self.criando_engate)
        self.botaoSalvarDesengate.clicked.connect(self.desengateVeiculo)

    def criando_engate(self):
        try:
            dtEngate   = self.dtEngate.date().toPyDate()
            nrFrota    = self.nrFrota.text()
            nrConjunto = self.nrConjunto.text()

            id_frota,cd_frota = EngateDesengateVeiculo.frota_existe(nrFrota)
            cd_conjunto       = EngateDesengateVeiculo.conjunto_existe(nrConjunto)

            novo_engate = CtEngate(DTENGATE=dtEngate, DTDESENGATE=None,
                                   NRFROTA=cd_frota, NRCONJUNTO=cd_conjunto,
                                   VEICULO_IDVEICULO=id_frota)
            session.add(novo_engate)
            session.commit()

            QMessageBox.information(self, "Sucesso", "Veículo engatado/desengatado!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro no Engate/Desengate: {str(e)}")
    def desengateVeiculo(self):
        try:
            nrFrota     = self.nrFrota.text()
            nrConjunto  = self.nrConjunto.text()
            dtDesengate = self.dtEngate.date().toPyDate()

            # Localize o ID do engate com os atributos fornecidos e DTDESENGATE nulo
            idEngate = self.localizar_id_engate(nrFrota, nrConjunto)
            if idEngate is None:
                raise ValueError("Engate não encontrado ou já desengatado.")

            # Atualize o campo DTDESENGATE com a nova data
            engate             = session.query(CtEngate).get(idEngate)
            engate.DTDESENGATE = dtDesengate
            session.commit()

            QMessageBox.information(self, "Sucesso", "Data de desengate atualizada com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar data de desengate: {str(e)}")

    def localizar_id_engate(self, nrFrota, nrConjunto):
        # Localize o ID do engate com os atributos fornecidos e DTDESENGATE nulo
        idEngate = session.query(CtEngate.ID).filter(CtEngate.NRFROTA    == nrFrota,
                                                     CtEngate.NRCONJUNTO == nrConjunto,
                                                     CtEngate.DTDESENGATE.is_(None)).scalar()
        return idEngate

    @staticmethod
    def frota_existe(nrFrota):  # Verificar se o número da frota informado existe no banco
        response = session.query(Veiculo).filter(Veiculo.NRFROTA == nrFrota).first()  # Função para procurar na tabela
        id_frota = response.IDVEICULO
        cd_frota = response.NRFROTA
        return id_frota, cd_frota
    @staticmethod
    def conjunto_existe(nrConjunto): #Verificar se o número do conjunto informado existe no banco
        response    = session.query(Veiculo).filter(Veiculo.NRCONJUNTO == nrConjunto).first() #Função para procurar na tabela
        cd_conjunto = response.NRCONJUNTO
        return cd_conjunto

    def engate(self):
        self.engate_ou_desengate('engate')
    def desengate(self):
        self.engate_ou_desengate('desengate')

    def engate_ou_desengate(self,acao):
        if acao =='engate':
            self.criando_engate()
        if acao =='desengate':
            self.desengateVeiculo()


if __name__ == "__main__":
    app    = QtWidgets.QApplication([])
    window = EngateDesengateVeiculo()
    app.exec()