from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate
from services.db import session
from PyQt5.QtWidgets import QMessageBox
from sqlalchemy.exc import IntegrityError
from model.Veiculo_model import Veiculo
from consultar_veiculo_view import ConsultarVeiculo
import re
import datetime
class CadastroVeiculoView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('telaCadastro.ui', self)
        self.criando_novo_veiculo()
        self.VoltarMenu.clicked.connect(self.ChamarVoltarMenu)
        self.nrPlaca.textChanged.connect(self.verificar_cadastro_existente)
        self.botaoConsulta.clicked.connect(self.ChamarConsulta)
        self.consultar_veiculo_view = None
        self.show()

        # Obter a data atual
        data_atual = datetime.date.today()
        # Configurar o campo de data para a data atual
        self.dtAquisicao.setDate(QDate.fromString(data_atual.strftime('%d-%m-%Y'), 'dd-MM-yyyy'))

    def ChamarVoltarMenu(self):
        # Pergunta ao usuário se ele deseja perder as alterações
        resposta = QtWidgets.QMessageBox.question(self, 'Voltar ao Menu',
                                                  'Deseja voltar ao menu? Todas as alterações não salvas serão perdidas.',
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                  QtWidgets.QMessageBox.No)
        if resposta == QtWidgets.QMessageBox.Yes:
            self.close()
    def ChamarConsulta(self):
        if not self.consultar_veiculo_view:
            self.consultar_veiculo_view = ConsultarVeiculo()
        self.consultar_veiculo_view.show()

    def criando_novo_veiculo(self):
        self.botaoCadastrar.clicked.connect(self.registro_veiculo)

    def registro_veiculo(self):
        try: #FAZER OPERAÇÃO ISOLADA? OU DEIXAR? O Q FAZER
            veiculo = self.verificar_cadastro_existente()
            if veiculo:
                self.atualizar_veiculo(veiculo)
                return

            if not self.validar_campos():
                return

            novo_veiculo = Veiculo(NRPLACA=self.nrPlaca.text().upper(), DSMODELO=self.dsModelo.currentText(),
                                   TPTRACAO=self.tpTracao.currentText(), NRRENAVAM=self.nrRenavam.text(),
                                   DTAQUISICAO=self.dtAquisicao.date().toPyDate(), NRFROTA=self.nrFrota.text(),
                                   NRCONJUNTO=self.nrConjunto.text(), NRCHASSI=self.nrChassi.text(),
                                   QTEIXO=int(self.qtdEixo.text()), TPVEICULO=self.tpVeiculo.currentText())

            session.add(novo_veiculo)
            session.commit()

            QMessageBox.information(self, "Sucesso", "Veículo Cadastrado!")
            self.limpar_campos()
        except IntegrityError as e:
            session.rollback()
            QMessageBox.critical(self, "Erro", "Erro de integridade: pode haver um valor duplicado ou outro problema de restrição.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao realizar o cadastro: {e}")

    def validar_campos(self):
        nrFrota     = self.nrFrota.text()
        nrConjunto  = self.nrConjunto.text()
        nrPlaca     = self.nrPlaca.text().upper()
        nrRenavam   = self.nrRenavam.text()
        dsModelo    = self.dsModelo.currentText()
        tpVeiculo   = self.tpVeiculo.currentText()
        qtEixo      = self.qtdEixo.text()
        nrChassi    = self.nrChassi.text()
        tpTracao    = self.tpTracao.currentText()
        dtAquisicao = self.dtAquisicao.date().toPyDate()

        campos_obrigatorios = [nrPlaca, nrRenavam, dsModelo, tpVeiculo, qtEixo,
                               nrChassi, tpTracao, dtAquisicao]
        if any(campo == "" or campo is None for campo in campos_obrigatorios):
            QMessageBox.critical(self, "Erro", "Todos os campos devem ser preenchidos.")
            return False

        if nrFrota and nrConjunto:
            QMessageBox.critical(self, "Erro", "Apenas um dos campos 'Frota' ou 'Conjunto' deve ser preenchido.")
            return False

        if tpTracao in ["Reboque", "SemiReboque"] and nrFrota:
            QMessageBox.critical(self, "Erro", "A frota não pode ser um Reboque/SemiReboque. Verifique se é um Conjunto ou Corrija a Tração do Veículo.")
            return False

        if tpTracao in ["Automotor"] and nrConjunto:
            QMessageBox.critical(self, "Erro", "O Conjunto não pode ser um Automotor. Verifique se é uma Frota.")
            return False

        if not self.validar_placa(nrPlaca):
            QMessageBox.critical(self, "Erro", "Placa inválida!")
            return False

        return True

    # Validação da placa para Mercosul ou modelo antigo;
    def validar_placa(self, nrPlaca):
        padraoTradicional = r'^[A-Za-z]{3}\d{4}$'
        padraoMercosul    = r'^[A-Za-z]{3}\d[A-Za-z]\d{2}$'
        return re.match(padraoTradicional, nrPlaca) or re.match(padraoMercosul, nrPlaca)

    # Validação do renavam
    def validar_renavam(self, nrRenavam):
        renavam = str(nrRenavam).zfill(11)
        if len(renavam) == 9:
            renavam = "00" + renavam
        elif len(renavam) != 11:
            return False

        d = [int(x) for x in renavam]
        soma = sum(d[i] * int(peso) for i, peso in enumerate("3298765432"))
        resto = soma % 11
        dv = 11 - resto if resto > 1 else 0
        return dv == d[-1]

    # Validação do chassi
    def valida_chassi(self, nrChassi):
        padraoChassi = r'^[A-HJ-NPR-Z0-9]{17}$'
        return re.match(padraoChassi, nrChassi)

    def verificar_cadastro_existente(self):
        nrPlaca = self.nrPlaca.text()
        if nrPlaca:
            veiculo = session.query(Veiculo).filter_by(NRPLACA=nrPlaca).first()
            if veiculo:
                QMessageBox.information(self, "Cadastro Existente", "Veículo já cadastrado. Carregando informações.")
                self.carregar_informacoes(veiculo)
                return veiculo

    def carregar_informacoes(self, veiculo):

        self.nrRenavam.setText(veiculo.NRRENAVAM)
        self.dsModelo.setCurrentText(veiculo.DSMODELO)
        self.tpVeiculo.setCurrentText(veiculo.TPVEICULO)
        self.qtdEixo.setText(str(veiculo.QTEIXO))
        self.nrChassi.setText(veiculo.NRCHASSI)
        self.tpTracao.setCurrentText(veiculo.TPTRACAO)
        self.dtAquisicao.setDate(QDate.fromString(veiculo.DTAQUISICAO.strftime('%d-%m-%Y'), 'dd-MM-yyyy'))

        if veiculo.NRFROTA != "":
            self.nrFrota.setText(veiculo.NRFROTA)
            self.nrConjunto.clear()  # Limpa o campo de conjunto se a frota estiver definida
        elif veiculo.NRCONJUNTO != "":
            self.nrConjunto.setText(veiculo.NRCONJUNTO)
            self.nrFrota.clear()  # Limpa o campo de frota se o conjunto estiver definido

    def atualizar_veiculo(self, veiculo):
        veiculo.NRPLACA     = self.nrPlaca.text().upper()
        veiculo.NRFROTA     = self.nrFrota.text()
        veiculo.NRCONJUNTO  = self.nrConjunto.text()
        veiculo.NRRENAVAM   = self.nrRenavam.text()
        veiculo.DSMODELO    = self.dsModelo.currentText()
        veiculo.TPVEICULO   = self.tpVeiculo.currentText()
        veiculo.QTEIXO      = int(self.qtdEixo.text())
        veiculo.NRCHASSI    = self.nrChassi.text()
        veiculo.TPTRACAO    = self.tpTracao.currentText()
        veiculo.DTAQUISICAO = self.dtAquisicao.date().toPyDate()

        if not self.validar_campos():
            return

        session.commit()
        QMessageBox.information(self, "Sucesso", "Veículo atualizado com sucesso!")
        self.limpar_campos()

    def limpar_campos(self):
        self.nrFrota.clear()
        self.nrConjunto.clear()
        self.nrPlaca.clear()
        self.nrRenavam.clear()
        self.nrChassi.clear()
        self.dsModelo.setCurrentIndex(-1)
        self.tpVeiculo.setCurrentIndex(-1)
        self.qtdEixo.clear()
        self.tpTracao.setCurrentIndex(-1)
        self.dtAquisicao.setDate(QDate.currentDate())

# Chamada de tela
if __name__ == "__main__":
    app    = QtWidgets.QApplication([])
    window = CadastroVeiculoView()
    app.exec()

