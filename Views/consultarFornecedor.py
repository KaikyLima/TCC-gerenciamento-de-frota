from services.db import session
from model.Fornecedor import Fornecedor
from PyQt5 import uic, QtWidgets

class consultarFornecedor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('telaConsultaFornecedor.ui', self)
        self.show()
        self.buscaLineEdit = self.findChild(QtWidgets.QLineEdit, 'textofiltro')
        self.limparfiltro = self.findChild(QtWidgets.QPushButton, 'limparfiltro')
        self.limparfiltro.clicked.connect(self.limpar_campos)
        self.buscarFiltro = self.findChild(QtWidgets.QPushButton, 'botaofiltrar')
        self.buscarFiltro.clicked.connect(self.buscar_filtro)
        self.limparfiltro.clicked.connect(self.consultar)
        self.VoltarMenu.clicked.connect(self.ChamarVoltarMenu)
        self.tabelaConsulta.setColumnWidth(0, 50)
        self.tabelaConsulta.setColumnWidth(1, 100)
        self.tabelaConsulta.setColumnWidth(2, 400)

        self.consultar()

    def limpar_campos(self):
        self.buscaLineEdit.clear()

    def ChamarVoltarMenu(self):
        self.close()

    def consultar(self):
        fornecedores = session.query(Fornecedor).all()
        self.exibir_fornecedor(fornecedores)

    def buscar_filtro(self):
        valor_busca = self.buscaLineEdit.text()
        consulta = session.query(Fornecedor).filter(
            (Fornecedor.COD.like(f"%{valor_busca}%")) |
            (Fornecedor.CNPJ.like(f"%{valor_busca}%")) |
            (Fornecedor.NMFORNECEDOR.like(f"%{valor_busca}%"))
        ).all()
        self.exibir_fornecedor(consulta)

    def exibir_fornecedor(self, fornecedores):
        tabela = self.findChild(QtWidgets.QTableWidget, 'tabelaConsulta')
        tabela.setRowCount(len(fornecedores))
        for i, fornecedor in enumerate(fornecedores):
            tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(str(fornecedor.COD)))
            tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(str(fornecedor.CNPJ)))
            tabela.setItem(i, 2, QtWidgets.QTableWidgetItem(str(fornecedor.NMFORNECEDOR)))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = consultarFornecedor()
    app.exec_()
