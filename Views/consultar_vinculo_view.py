from services.db import session
from model.CtVinculo import CtVinculo
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from model.Motorista import Motorista
from model.Veiculo_model import Veiculo
from datetime import datetime

class ConsultarVinculos(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('telaConsultaVinculo.ui', self)
        self.show()
        self.buscaLineEdit = self.findChild(QtWidgets.QLineEdit, 'textofiltro')
        self.buscarVinculosButton = self.findChild(QtWidgets.QPushButton, 'botaoFiltrarVinculosAtivos')
        self.buscarButton = self.findChild(QtWidgets.QPushButton, 'botaofiltrar')
        self.limparfiltro = self.findChild(QtWidgets.QPushButton, 'limparfiltro')
        self.buscarVinculosButton.clicked.connect(self.buscar_vinculos_ativos)
        self.limparfiltro.clicked.connect(self.consultar)
        self.limparfiltro.clicked.connect(self.limpar_campos)
        self.buscarButton.clicked.connect(self.buscar_vinculos_filtro)

    def limpar_campos(self):
        self.buscaLineEdit.clear()

    def consultar(self):
        vinculos = session.query(CtVinculo).all()
        tabela = self.findChild(QtWidgets.QTableWidget, 'tabelaConsulta')
        tabela.setRowCount(len(vinculos))
        self.exibirResultados(vinculos)


    def buscar_vinculos_ativos(self):
        valor_busca = self.buscaLineEdit.text()
        if valor_busca:
            # Remove a condição CtVinculo.DTDESVINCULO == valor_busca
            vinculos = session.query(CtVinculo).filter(CtVinculo.DTDESVINCULO == None).all()
        else:
            vinculos = session.query(CtVinculo).filter(CtVinculo.DTDESVINCULO == None).all()
        tabela = self.findChild(QtWidgets.QTableWidget, 'tabelaConsulta')
        tabela.setRowCount(len(vinculos))
        self.exibirResultados(vinculos)

    def buscar_vinculos_filtro(self):
        valor_busca = self.buscaLineEdit.text()
        buscaVeiculo = session.query(Veiculo).filter_by(NRFROTA=valor_busca).first()


        idVeic = buscaVeiculo.IDVEICULO if buscaVeiculo else None

        buscarMotora = session.query(Motorista).filter_by(FUNCIONARIO_NRMATRICULA=valor_busca).first()

        idMotora = buscarMotora.IDMOTORISTA if buscarMotora else None

        idVeic = buscaVeiculo.IDVEICULO
        consulta = session.query(CtVinculo).filter(
            (CtVinculo.VEICULO_IDVEICULO.like(f"%{idVeic}%"))
        ).all()

        self.exibirResultados(consulta)

    def exibirResultados(self, consulta):
        tabela = self.findChild(QtWidgets.QTableWidget, 'tabelaConsulta')
        tabela.clearContents()  # Limpa o conteúdo da tabela
        tabela.setRowCount(len(consulta))

        for i, vinculo in enumerate(consulta):
            tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(str(vinculo.DTVINCULO)))
            tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(str(vinculo.DTDESVINCULO)))
            frota = session.query(Veiculo).filter_by(IDVEICULO=vinculo.VEICULO_IDVEICULO).first()
            tabela.setItem(i, 2, QtWidgets.QTableWidgetItem(str(frota.NRFROTA) if frota else ""))
            motorista = session.query(Motorista).filter_by(IDMOTORISTA=vinculo.MOTORISTA_IDMOTORISTA).first()
            tabela.setItem(i, 3, QtWidgets.QTableWidgetItem(str(motorista.NMMOTORISTA) if motorista else ""))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ConsultarVinculos()
    window.consultar()
    app.exec()