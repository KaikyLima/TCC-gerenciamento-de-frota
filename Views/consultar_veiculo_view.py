from model.Veiculo_model import Veiculo
from services.db import session
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
class ConsultarVeiculo(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('telaConsultaVeiculo.ui', self)
        self.show()
        self.menu_view = None
        self.buscaLineEdit = self.findChild(QtWidgets.QLineEdit, 'textofiltro')
        self.buscarButton  = self.findChild(QtWidgets.QPushButton, 'botaofiltra')
        self.limparfiltro  = self.findChild(QtWidgets.QPushButton, 'limparfiltro')
        self.VoltarMenu.clicked.connect(self.ChamarVoltarMenu)
        self.buscarButton.clicked.connect(self.buscar)
        self.limparfiltro.clicked.connect(self.consultar)
        self.limparfiltro.clicked.connect(self.limpar_campos)

    def limpar_campos(self):
        self.buscaLineEdit.clear()

    def ChamarVoltarMenu(self):
        self.close()

    def consultar(self):
        consulta = session.query(Veiculo).all()
        tabela   = self.findChild(QtWidgets.QTableWidget, 'tabelaConsulta')
        tabela.setRowCount(len(consulta))
        self.exibirResultados(consulta)
        '''for i, veiculos in enumerate(consulta):
            tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(str(veiculos.NRPLACA)))
            tabela.setItem(i, 3, QtWidgets.QTableWidgetItem(str(veiculos.DSMODELO)))
            tabela.setItem(i, 4, QtWidgets.QTableWidgetItem(str(veiculos.TPTRACAO)))
            tabela.setItem(i, 5, QtWidgets.QTableWidgetItem(str(veiculos.NRRENAVAM)))
            tabela.setItem(i, 6, QtWidgets.QTableWidgetItem(str(veiculos.DTAQUISICAO)))
            tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(str(veiculos.NRFROTA)))
            tabela.setItem(i, 2, QtWidgets.QTableWidgetItem(str(veiculos.NRCONJUNTO)))
            tabela.setItem(i, 7, QtWidgets.QTableWidgetItem(str(veiculos.NRCHASSI)))
            tabela.setItem(i, 8, QtWidgets.QTableWidgetItem(str(veiculos.QTEIXO)))
            tabela.setItem(i, 9, QtWidgets.QTableWidgetItem(str(veiculos.TPVEICULO)))'''


    def buscar(self):
        textoBusca = self.buscaLineEdit.text()

        try:
            consulta = session.query(Veiculo).filter(
                (Veiculo.NRPLACA.like(f"%{textoBusca}%")) |
                (Veiculo.DSMODELO.like(f"%{textoBusca}%")) |
                (Veiculo.TPTRACAO.like(f"%{textoBusca}%")) |
                (Veiculo.NRRENAVAM.like(f"%{textoBusca}%")) |
                (Veiculo.NRFROTA.like(f"%{textoBusca}%")) |
                (Veiculo.NRCONJUNTO.like(f"%{textoBusca}%")) |
                (Veiculo.NRCHASSI.like(f"%{textoBusca}%")) |
                (Veiculo.QTEIXO.like(f"%{textoBusca}%")) |
                (Veiculo.TPVEICULO.like(f"%{textoBusca}%"))
            ).all()
            self.exibirResultados(consulta)
        except Exception as e:
            QMessageBox.critical(self, "Erro ao buscar", str(e))

    def exibirResultados(self, consulta):
        tabela = self.findChild(QtWidgets.QTableWidget, 'tabelaConsulta')
        tabela.clearContents()  # Limpa o conteúdo da tabela
        tabela.setRowCount(len(consulta))

        for i, veiculo in enumerate(consulta):
            tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(str(veiculo.NRPLACA)))
            tabela.setItem(i, 3, QtWidgets.QTableWidgetItem(str(veiculo.DSMODELO)))
            tabela.setItem(i, 4, QtWidgets.QTableWidgetItem(str(veiculo.TPTRACAO)))
            tabela.setItem(i, 5, QtWidgets.QTableWidgetItem(str(veiculo.NRRENAVAM)))
            tabela.setItem(i, 6, QtWidgets.QTableWidgetItem(str(veiculo.DTAQUISICAO)))
            tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(str(veiculo.NRFROTA)))
            tabela.setItem(i, 2, QtWidgets.QTableWidgetItem(str(veiculo.NRCONJUNTO)))
            tabela.setItem(i, 7, QtWidgets.QTableWidgetItem(str(veiculo.NRCHASSI)))
            tabela.setItem(i, 8, QtWidgets.QTableWidgetItem(str(veiculo.QTEIXO)))
            tabela.setItem(i, 9, QtWidgets.QTableWidgetItem(str(veiculo.TPVEICULO)))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ConsultarVeiculo()
    window.consultar()
    app.exec()