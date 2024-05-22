from PyQt5.QtWidgets import QMessageBox
from sqlalchemy.exc import IntegrityError
from services.db import session
from model.Fornecedor import Fornecedor
from consultarFornecedor import consultarFornecedor
from PyQt5 import uic, QtWidgets
class cadastroFornecedor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('telaCadastroFornecedor.ui', self)
        self.criar_novo_fornecedor()
        self.VoltarMenu.clicked.connect(self.ChamarVoltarMenu)
        self.botaoConsulta.clicked.connect(self.ChamarConsulta)
        self.consultarFornecedor = None
        self.show()

    def ChamarVoltarMenu(self):
        # Pergunta ao usuário se ele deseja perder as alterações
        resposta = QtWidgets.QMessageBox.question(self, 'Voltar ao Menu',
                                                  'Deseja voltar ao menu? Todas as alterações não salvas serão perdidas.',
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                  QtWidgets.QMessageBox.No)
        if resposta == QtWidgets.QMessageBox.Yes:
            self.close()

    def ChamarConsulta(self):
        if not self.consultarFornecedor:
            self.consultarFornecedor = consultarFornecedor()
        self.consultarFornecedor.show()

    def criar_novo_fornecedor(self):
        self.botaoCadastrar.clicked.connect(self.registrar_fornecedor)

    def verificar_existencia_fornecedor(cnpj):
        fornecedor = session.query(Fornecedor).filter(Fornecedor.CNPJ == cnpj).first()
        if fornecedor:
            return True
        else:
            return False

    def registrar_fornecedor(self):
        try:
            cnpj = self.CnpjFornecedor.text()
            nmFornecedor = self.nomeFornecedor.text()


            cod_forne = cadastroFornecedor.verificar_existencia_fornecedor(cnpj)
            if cadastroFornecedor.verificar_existencia_fornecedor(cnpj):
                QMessageBox.critical(self, "Erro", "CNPJ já cadastrado")
                return

            campos_obrigatorios = [cnpj, nmFornecedor]
            if any(campo == "" or campo is None for campo in campos_obrigatorios):
                QMessageBox.critical(self, "Erro", "Todos os campos devem ser preenchidos.")
                return

            novo_fornecedor = Fornecedor(CNPJ = cnpj, NMFORNECEDOR = nmFornecedor)
            session.add(novo_fornecedor)
            session.flush()  # Obter o IDFORNECEDOR gerado
            session.commit()

            QMessageBox.information(self, "Sucesso", "Fornecedor cadastrado com sucesso!")
            self.limpar_campos()
        except IntegrityError as e:
            session.rollback()
            QMessageBox.critical(self, "Erro",
                                 "Erro de integridade: pode haver um valor duplicado ou outro problema de restrição.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao realizar o cadastro: {e}")


    def limpar_campos(self):
        self.CnpjFornecedor.clear()
        self.nomeFornecedor.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = cadastroFornecedor()
    app.exec()