from services.db import session
from model.Motorista import Motorista
from model.Funcionario import Funcionario
from model.Pessoa import Pessoa
from PyQt5 import uic, QtWidgets


class ConsultarMotoristas(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('telaConsultaMotorista.ui', self)
        self.show()
        self.menu_view     = None
        self.buscaLineEdit = self.findChild(QtWidgets.QLineEdit, 'textofiltro')
        self.limparfiltro  = self.findChild(QtWidgets.QPushButton, 'limparfiltro')
        self.buscarFiltro  = self.findChild(QtWidgets.QPushButton, 'botaofiltrar')
        self.VoltarMenu.clicked.connect(self.ChamarVoltarMenu)
        self.limparfiltro.clicked.connect(self.limpar_campos)
        self.buscarFiltro.clicked.connect(self.buscar_filtro)
        self.limparfiltro.clicked.connect(self.consultar)
        self.VoltarMenu.clicked.connect(self.ChamarVoltarMenu)
        self.tabelaConsulta.setColumnWidth(100, 70)
        self.consultar()

    def limpar_campos(self):
        self.buscaLineEdit.clear()

    def consultar(self):
        motoristas = session.query(Motorista).all()
        self.exibir_motoristas(motoristas)

    def ChamarVoltarMenu(self):
            self.close()

    def buscar_filtro(self):
        valor_busca = self.buscaLineEdit.text()
        consulta = session.query(Motorista).filter(
            (Motorista.NMMOTORISTA.like(f"%{valor_busca}%")) |
            (Motorista.FUNCIONARIO_NRMATRICULA.like(f"%{valor_busca}%"))
        ).all()
        self.exibir_motoristas(consulta)

    def exibir_motoristas(self, motoristas):
        tabela = self.findChild(QtWidgets.QTableWidget, 'tabelaConsulta')
        tabela.setRowCount(len(motoristas))
        for i, motorista in enumerate(motoristas):
            tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(str(motorista.FUNCIONARIO_NRMATRICULA)))
            tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(str(motorista.NMMOTORISTA)))

            # Consulta ao Funcionario para obter DSFUNÇÃO, TPSITUAÇÃO, DTADMISSAO
            funcionario = session.query(Funcionario).filter_by(NRMATRICULA=motorista.FUNCIONARIO_NRMATRICULA).first()
            if funcionario:
                tabela.setItem(i, 3, QtWidgets.QTableWidgetItem(str(funcionario.TPSITUACAO)))
                tabela.setItem(i, 4, QtWidgets.QTableWidgetItem(str(funcionario.DSFUNCAO)))
                tabela.setItem(i, 5, QtWidgets.QTableWidgetItem(str(funcionario.DTADMISSAO)))

            else:
                tabela.setItem(i, 3, QtWidgets.QTableWidgetItem("N/A"))
                tabela.setItem(i, 4, QtWidgets.QTableWidgetItem("N/A"))
                tabela.setItem(i, 5, QtWidgets.QTableWidgetItem("N/A"))

            # Consulta à Pessoa para obter NRCPF
            pessoa = session.query(Pessoa).filter_by(IDPESSOA=funcionario.PESSOA_IDPESSOA).first()
            if pessoa:
                tabela.setItem(i, 2, QtWidgets.QTableWidgetItem(str(pessoa.NRCPF)))
            else:
                tabela.setItem(i, 2, QtWidgets.QTableWidgetItem("N/A"))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ConsultarMotoristas()
    app.exec_()
