from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate
from services.db import session
from model.Funcionario import Funcionario
from model.Pessoa import Pessoa
from model.Motorista import Motorista
from PyQt5.QtWidgets import QMessageBox
from sqlalchemy.exc import IntegrityError
from consultar_motorista_view import ConsultarMotoristas
import datetime
'''
class CadastroFuncionarioView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('CadastroFuncionario.ui', self)
        self.criar_novo_funcionario()
        self.botaoConsultaFunc.clicked.connect(self.ChamarConsulta)
        self.consultar_motorista_view = None
        self.show()

        # Obter a data atual
        data_atual = datetime.date.today()

        # Configurar o campo de data para a data atual
        self.dtAdmissao.setDate(QDate.fromString(data_atual.strftime('%d-%m-%Y'), 'dd-MM-yyyy'))

    def ChamarConsulta(self):
        if not self.consultar_motorista_view:
            self.consultar_motorista_view = ConsultarMotoristas()
        self.consultar_motorista_view.show()
    def criar_novo_funcionario(self):
        self.BotaoCadastrarFunc.clicked.connect(self.registrar_funcionario)
        self.nrCPF.textChanged.connect(self.verificar_existencia_funcionario)
        self.nrMatricula.textChanged.connect(self.verificar_existencia_funcionario)

    def verificar_existencia_funcionario(self):
        nrCPF = self.nrCPF.text()
        nrMatricula = self.nrMatricula.text()

        if nrCPF:
            pessoa = session.query(Pessoa).filter(Pessoa.NRCPF == nrCPF).first()
            if pessoa:
                funcionario = session.query(Funcionario).filter(Funcionario.PESSOA_IDPESSOA == pessoa.IDPESSOA).first()
                if funcionario:
                    self.carregar_dados_funcionario(funcionario)

        if nrMatricula:
            funcionario = session.query(Funcionario).filter(Funcionario.NRMATRICULA == nrMatricula).first()
            if funcionario:
                self.carregar_dados_funcionario(funcionario)

    def carregar_dados_funcionario(self, funcionario):
        self.nrCPF.setText(funcionario.pessoa.NRCPF)
        self.dtNascimento.setDate(funcionario.pessoa.DTNASCIMENTO)
        self.nmFuncionario.setText(funcionario.NMFUNCIONARIO)
        self.dsFuncao.setCurrentText(funcionario.DSFUNCAO)
        self.tpSituacao.setCurrentText(funcionario.TPSITUACAO)
        self.nrMatricula.setText(funcionario.NRMATRICULA)
        self.dtAdmissao.setDate(funcionario.DTADMISSAO)

    def registrar_funcionario(self):
        try:
            nrCPF         = self.nrCPF.text()
            dtNascimento  = self.dtNascimento.date().toPyDate()
            nmFuncionario = self.nmFuncionario.text()
            dsFuncao      = self.dsFuncao.currentText()
            tpSituacao    = self.tpSituacao.currentText()
            nrMatricula   = self.nrMatricula.text()
            dtAdmissao    = self.dtAdmissao.date().toPyDate()

            campos_obrigatorios = [nrCPF, dtNascimento, nmFuncionario, dsFuncao, tpSituacao, dtAdmissao]
            if any(campo == "" or campo is None for campo in campos_obrigatorios):
                QMessageBox.critical(self, "Erro", "Todos os campos devem ser preenchidos.")
                return

            # Inserir na tabela Pessoa
            nova_pessoa = Pessoa(NMPESSOA=nmFuncionario, NRCPF=nrCPF, DTNASCIMENTO=dtNascimento)
            session.add(nova_pessoa)
            session.flush()  # Obter o IDPESSOA gerado
            session.commit()

            # Inserir na tabela Funcionario
            novo_funcionario = Funcionario(NRMATRICULA=nrMatricula, NMFUNCIONARIO=nmFuncionario,
                                           DSFUNCAO=dsFuncao, DTADMISSAO=dtAdmissao,
                                           PESSOA_IDPESSOA=nova_pessoa.IDPESSOA)
            session.add(novo_funcionario)
            session.flush()
            session.commit()

            # Se a função for "Motorista", inserir na tabela Motorista também
            if dsFuncao == "Motorista":
                novo_motorista = Motorista(NMMOTORISTA=nmFuncionario,TPSITUACAO=tpSituacao ,FUNCIONARIO_NRMATRICULA=nrMatricula)
                session.add(novo_motorista)
                session.flush()
                session.commit()

            QMessageBox.information(self, "Sucesso", "Funcionário cadastrado com sucesso!")
            self.limpar_campos()
        except IntegrityError as e:
            session.rollback()
            QMessageBox.critical(self, "Erro",
                                 "Erro de integridade: pode haver um valor duplicado ou outro problema de restrição.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao realizar o cadastro: {e}")

    def limpar_campos(self):
        self.nrCPF.clear()
        self.dtNascimento.setDate(datetime.now())  # Definir data atual como padrão
        self.nmFuncionario.clear()
        self.dsFuncao.clear()
        self.tpSituacao.setCurrentIndex(0)  # Definir o primeiro item como padrão
        self.nrMatricula.clear()
        self.dtAdmissao.setDate(datetime.now())  # Definir data atual como padrão

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = CadastroFuncionarioView()
    app.exec()
'''
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate
from services.db import session
from model.Funcionario import Funcionario
from model.Pessoa import Pessoa
from model.Motorista import Motorista
from PyQt5.QtWidgets import QMessageBox
from sqlalchemy.exc import IntegrityError
from consultar_motorista_view import ConsultarMotoristas
import datetime
from sqlalchemy.orm import joinedload


class CadastroFuncionarioView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('CadastroFuncionario.ui', self)
        self.criar_novo_funcionario()
        self.botaoConsultaFunc.clicked.connect(self.ChamarConsulta)
        self.consultar_motorista_view = None
        self.nrCPF.textChanged.connect(self.verificar_existencia_funcionario)
        self.nrMatricula.textChanged.connect(self.verificar_existencia_funcionario)
        self.show()

        # Obter a data atual
        data_atual = datetime.date.today()

        # Configurar o campo de data para a data atual
        self.dtAdmissao.setDate(QDate.fromString(data_atual.strftime('%d-%m-%Y'), 'dd-MM-yyyy'))

    def ChamarConsulta(self):
        if not self.consultar_motorista_view:
            self.consultar_motorista_view = ConsultarMotoristas()
        self.consultar_motorista_view.show()

    def criar_novo_funcionario(self):
        self.BotaoCadastrarFunc.clicked.connect(self.registrar_funcionario)

    def verificar_existencia_funcionario(self):
        nrCPF = self.nrCPF.text()
        nrMatricula = self.nrMatricula.text()

        if nrCPF:
            pessoa = session.query(Pessoa).filter(Pessoa.NRCPF == nrCPF).first()
            if pessoa:
                funcionario = session.query(Funcionario).filter(Funcionario.PESSOA_IDPESSOA == pessoa.IDPESSOA).first()
                if funcionario:
                    self.carregar_dados_funcionario(funcionario, pessoa)

        if nrMatricula:
            funcionario = session.query(Funcionario).filter(Funcionario.NRMATRICULA == nrMatricula).first()
            if funcionario:
                pessoa = session.query(Pessoa).filter(Pessoa.IDPESSOA == funcionario.PESSOA_IDPESSOA).first()
                if pessoa:
                    self.carregar_dados_funcionario(funcionario, pessoa)

    def carregar_dados_funcionario(self,funcionario, pessoa):
        # Carrega os dados do funcionário nos campos correspondentes
        self.nrCPF.setText(pessoa.NRCPF)
        self.dtNascimento.setDate(pessoa.DTNASCIMENTO)
        self.nmFuncionario.setText(funcionario.NMFUNCIONARIO)
        self.dsFuncao.setCurrentText(funcionario.DSFUNCAO)
        self.tpSituacao.setCurrentText(funcionario.TPSITUACAO)
        self.nrMatricula.setText(str(funcionario.NRMATRICULA))
        self.dtAdmissao.setDate(funcionario.DTADMISSAO)

    def registrar_funcionario(self):
        try:
            nrCPF         = self.nrCPF.text()
            dtNascimento  = self.dtNascimento.date().toPyDate()
            nmFuncionario = self.nmFuncionario.text()
            dsFuncao      = self.dsFuncao.currentText()
            tpSituacao    = self.tpSituacao.currentText()
            nrMatricula   = self.nrMatricula.text()
            dtAdmissao    = self.dtAdmissao.date().toPyDate()

            campos_obrigatorios = [nrCPF, dtNascimento, nmFuncionario, dsFuncao, tpSituacao, dtAdmissao]
            if any(campo == "" or campo is None for campo in campos_obrigatorios):
                QMessageBox.critical(self, "Erro", "Todos os campos devem ser preenchidos.")
                return

            # Verificar se é edição ou criação
            if nrCPF or nrMatricula:
                funcionario_existente = session.query(Funcionario).filter(
                    Funcionario.NRMATRICULA == nrMatricula).first()
                if funcionario_existente:
                    self.atualizar_funcionario(funcionario_existente)
                    return 0

            # Inserir na tabela Pessoa
            nova_pessoa = Pessoa(NMPESSOA=nmFuncionario, NRCPF=nrCPF, DTNASCIMENTO=dtNascimento)
            session.add(nova_pessoa)
            session.flush()  # Obter o IDPESSOA gerado
            session.commit()

            # Inserir na tabela Funcionario
            novo_funcionario = Funcionario(NRMATRICULA=nrMatricula, NMFUNCIONARIO=nmFuncionario,
                                           DSFUNCAO=dsFuncao, DTADMISSAO=dtAdmissao,
                                           PESSOA_IDPESSOA=nova_pessoa.IDPESSOA)
            session.add(novo_funcionario)
            session.flush()
            session.commit()

            # Se a função for "Motorista", inserir na tabela Motorista também
            if dsFuncao == "Motorista":
                novo_motorista = Motorista(NMMOTORISTA=nmFuncionario,FUNCIONARIO_NRMATRICULA=nrMatricula)
                session.add(novo_motorista)
                session.flush()
                session.commit()

            QMessageBox.information(self, "Sucesso", "Funcionário cadastrado com sucesso!")
            self.limpar_campos()
        except IntegrityError as e:
            session.rollback()
            QMessageBox.critical(self, "Erro",
                                 "Erro de integridade: pode haver um valor duplicado ou outro problema de restrição.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao realizar o cadastro: {e}")
            self.limpar_campos()
    def atualizar_funcionario(self, funcionario_existente):
        try:
            # Atualizar os dados da pessoa
            pessoa = funcionario_existente.pessoa
            pessoa.NRCPF = self.nrCPF.text()
            pessoa.DTNASCIMENTO = self.dtNascimento.date().toPyDate()
            session.commit()

            # Atualizar os dados do funcionário
            funcionario_existente.NMFUNCIONARIO = self.nmFuncionario.text()
            funcionario_existente.DSFUNCAO = self.dsFuncao.currentText()
            funcionario_existente.TPSITUACAO = self.tpSituacao.currentText()
            funcionario_existente.NRMATRICULA = self.nrMatricula.text()
            funcionario_existente.DTADMISSAO = self.dtAdmissao.date().toPyDate()
            session.commit()

            QMessageBox.information(self, "Sucesso", "Funcionário atualizado com sucesso!")
            self.limpar_campos()
        except IntegrityError as e:
            session.rollback()
            QMessageBox.critical(self, "Erro",
                                 "Erro de integridade: pode haver um valor duplicado ou outro problema de restrição.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao atualizar o funcionário: {e}")

    def limpar_campos(self):
        self.nrCPF.clear()
        self.dtNascimento.setDate(datetime.datetime.now().date())  # Definir data atual como padrão
        self.nmFuncionario.clear()
        self.dsFuncao.setCurrentIndex(0)  # Definir o primeiro item como padrão
        self.tpSituacao.setCurrentIndex(0)  # Definir o primeiro item como padrão
        self.nrMatricula.clear()
        self.dtAdmissao.setDate(datetime.datetime.now().date())  # Definir data atual como padrão

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = CadastroFuncionarioView()
    app.exec()
