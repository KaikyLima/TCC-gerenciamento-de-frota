from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from services.db import session
from model.Veiculo_model import Veiculo
from model.CtEngate import CtEngate
from consultar_engate_view import ConsultarEngates
from PyQt5.QtCore import QDate
import datetime

class EngateDesengateVeiculo(QtWidgets.QMainWindow):  #Trativas do ENGATE
    def __init__(self):
        super().__init__()
        uic.loadUi('telaCtEngate.ui', self)
        self.criando_novo_engate()
        self.nrFrota.textChanged.connect(self.preencher_placa_frota)
        self.nrConjunto.textChanged.connect(self.preencher_placa_conjunto)
        self.VoltarMenu.clicked.connect(self.ChamarVoltarMenu)
        self.botaoConsultaEngate.clicked.connect(self.ChamarConsulta)
        self.consultar_engate_view = None
        self.show()
        # Obter a data atual
        data_atual = datetime.date.today()
        # Configurar o campo de data para a data atual
        self.dtEngate.setDate(QDate.fromString(data_atual.strftime('%d-%m-%Y'), 'dd-MM-yyyy'))

    def ChamarConsulta(self):
        if not self.consultar_engate_view:
            self.consultar_engate_view = ConsultarEngates()
        self.consultar_engate_view.show()

    def ChamarVoltarMenu(self):
        # Pergunta ao usuário se ele deseja perder as alterações
        resposta = QtWidgets.QMessageBox.question(self, 'Voltar ao Menu',
                                                  'Deseja voltar ao menu? Todas as alterações não salvas serão perdidas.',
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                  QtWidgets.QMessageBox.No)
        if resposta == QtWidgets.QMessageBox.Yes:
            # Fecha a tela atual
            self.close()

    def preencher_placa_frota(self):
        nrFrota = self.nrFrota.text()
        response = session.query(Veiculo).filter(Veiculo.NRFROTA == nrFrota).first()
        if response is not None:
            self.nrPlacaFrota.setText(response.NRPLACA)
            self.tpVeic.setText(response.TPVEICULO)
        else:
            self.nrPlacaFrota.clear()
            self.tpVeic.clear()

    def preencher_placa_conjunto(self):
        nrConjunto = self.nrConjunto.text()
        # Procura os veículos com o número do conjunto
        veiculos = session.query(Veiculo).filter(Veiculo.NRCONJUNTO == nrConjunto).all()
        # Se não houver veículos com o conjunto informado, limpa os campos de placa
        if not veiculos:
            self.nrPlacaA.clear()
            self.nrPlacaB.clear()
            self.nrPlacaC.clear()
            self.nrPlacaD.clear()

            return
        # Se houver veículos com o conjunto informado, preenche os campos de placa
        # Considerando que a lista de veículos contenha apenas dois veículos com as placas A e B
        if len(veiculos) == 4:
            self.nrPlacaA.setText(veiculos[0].NRPLACA)
            self.nrPlacaB.setText(veiculos[1].NRPLACA)
            self.nrPlacaC.setText(veiculos[2].NRPLACA)
            self.nrPlacaD.setText(veiculos[3].NRPLACA)
        elif len(veiculos) == 3:
            self.nrPlacaA.setText(veiculos[0].NRPLACA)
            self.nrPlacaB.setText(veiculos[1].NRPLACA)
            self.nrPlacaC.setText(veiculos[2].NRPLACA)
        elif len(veiculos) == 2:
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

            idEngateFrota = self.localizar_id_engate_frota(nrFrota)
            if not idEngateFrota is None:
                raise ValueError("Frota já possui um engate ativo.")
            idEngateConjunto = self.localizar_id_engate_conjunto(nrConjunto)
            if not idEngateConjunto is None:
                raise ValueError("Conjunto já possui um engate ativo.")

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
    def localizar_id_engate_frota(self, nrFrota):
        # Localize o ID do engate com os atributos fornecidos e DTDESENGATE nulo
        idEngateFrota = session.query(CtEngate.ID).filter(CtEngate.NRFROTA    == nrFrota,
                                                     CtEngate.DTDESENGATE.is_(None)).scalar()
        return idEngateFrota
    def localizar_id_engate_conjunto(self, nrConjunto):
        # Localize o ID do engate com os atributos fornecidos e DTDESENGATE nulo
        idEngateConjunto = session.query(CtEngate.ID).filter(CtEngate.NRCONJUNTO == nrConjunto,
                                                     CtEngate.DTDESENGATE.is_(None)).scalar()
        return idEngateConjunto

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


if __name__ == "__main__":
    app    = QtWidgets.QApplication([])
    window = EngateDesengateVeiculo()
    app.exec()