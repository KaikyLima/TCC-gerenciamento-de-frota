from services.db import session
from model.CtEngate import CtEngate
from model.Veiculo_model import Veiculo
from PyQt5 import uic, QtWidgets

class ConsultarEngates(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('telaConsultaEngate.ui', self)
        self.show()
        self.menu_view           = None
        self.buscaLineEdit       = self.findChild(QtWidgets.QLineEdit, 'textofiltro')
        self.buscarEngatesButton = self.findChild(QtWidgets.QPushButton, 'botaoFiltrarEngatesAtivos')
        self.limparfiltro        = self.findChild(QtWidgets.QPushButton, 'limparfiltro')
        self.buscarFiltro        = self.findChild(QtWidgets.QPushButton, 'botaofiltrar')
        self.buscarFiltro.clicked.connect(self.buscar_filtro)
        self.limparfiltro.clicked.connect(self.consultar)
        self.VoltarMenu.clicked.connect(self.ChamarVoltarMenu)
        self.limparfiltro.clicked.connect(self.limpar_campos)
        self.buscarEngatesButton.clicked.connect(self.buscar_engates_ativos)
        self.tabelaConsulta.setColumnWidth(100, 50) #Tamanho das colunas da grid
        self.consultar()

    def ChamarVoltarMenu(self):
            self.close()

    def limpar_campos(self):
        self.buscaLineEdit.clear()

    def consultar(self):
        engates = session.query(CtEngate).all()
        self.exibir_engates(engates)

    def buscar_engates_ativos(self):
        valor_busca = self.buscaLineEdit.text()
        if not valor_busca:
            engates = session.query(CtEngate).filter(
                CtEngate.DTENGATE.isnot(None),
                CtEngate.DTDESENGATE.is_(None)
            ).all()
        else:
            engates = session.query(CtEngate).filter(
                CtEngate.DTENGATE.is_(None),
                CtEngate.DTDESENGATE.isnot(None)
            ).all()
        self.exibir_engates(engates)

    def buscar_filtro(self):
        valor_busca = self.buscaLineEdit.text()
        consulta = session.query(CtEngate).filter(
            (CtEngate.NRFROTA.like(f"%{valor_busca}%")) |
            (CtEngate.NRCONJUNTO.like(f"%{valor_busca}%"))
        ).all()
        self.exibir_engates(consulta)

    def exibir_engates(self, engates):
        tabela = self.findChild(QtWidgets.QTableWidget, 'tabelaConsulta')
        tabela.setRowCount(len(engates))
        for i, engate in enumerate(engates):
            tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(str(engate.DTENGATE)))
            tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(str(engate.DTDESENGATE)))
            tabela.setItem(i, 2, QtWidgets.QTableWidgetItem(str(engate.NRFROTA)))
            tabela.setItem(i, 4, QtWidgets.QTableWidgetItem(str(engate.NRCONJUNTO)))

            # Adicione o número da placa (NRPLACA) à tabela
            veiculo = session.query(Veiculo).filter_by(NRFROTA=engate.NRFROTA).first()
            if veiculo:
                tabela.setItem(i, 3, QtWidgets.QTableWidgetItem(str(veiculo.NRPLACA)))
            else:
                tabela.setItem(i, 3, QtWidgets.QTableWidgetItem("N/A"))  # Se o veículo não for encontrado, exibe "N/A"


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ConsultarEngates()
    app.exec_()
