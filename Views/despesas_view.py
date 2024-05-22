from PyQt5 import uic, QtWidgets
from services.db import session
from PyQt5.QtWidgets import QMessageBox
from sqlalchemy.exc import IntegrityError
from model.Veiculo_model import Veiculo
from model.Despesas import Despesas
from model.Fornecedor import Fornecedor

class DespesasView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('telaDespesas.ui', self)
        self.criando_nova_despesa()
        self.nrPlaca.textChanged.connect(self.validar_placa)
        self.nrCNPJ.textChanged.connect(self.preencher_fornecedor)
        self.VoltarMenu.clicked.connect(self.ChamarVoltarMenu)
        self.show()

    def ChamarVoltarMenu(self):
        # Pergunta ao usuário se ele deseja perder as alterações
        resposta = QtWidgets.QMessageBox.question(self, 'Voltar ao Menu',
                                                  'Deseja voltar ao menu? Todas as alterações não salvas serão perdidas.',
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                  QtWidgets.QMessageBox.No)
        if resposta == QtWidgets.QMessageBox.Yes:
            # Fecha a tela atual
            self.close()

    def validar_placa(self):  # Valida se a placa está cadastrada no sistema
        nrPlaca = self.nrPlaca.text()
        if len(nrPlaca) == 7:
            try:
                response = session.query(Veiculo).filter(Veiculo.NRPLACA == nrPlaca).scalar()
                if response is None:
                    self.nrPlaca.clear()
            except Exception as e:
                print(f"Erro ao buscar veiculo: {e}")
                self.nrPlaca.clear()

    def preencher_fornecedor(self):
        nrCNPJ = self.nrCNPJ.text()
        if len(nrCNPJ) == 14:  # Verifica se o CNPJ tem o tamanho correto
            try:
                response = session.query(Fornecedor).filter(Fornecedor.CNPJ == nrCNPJ).first()
                if response is not None:
                    self.nmFornecedor.setText(response.NMFORNECEDOR)
                else:
                    self.nmFornecedor.clear()
            except Exception as e:
                print(f"Erro ao buscar fornecedor: {e}")
                self.nmFornecedor.clear()  # Limpa o campo em caso de erro
        else:
            self.nmFornecedor.clear()  # Limpa o campo se o CNPJ não tiver o tamanho correto

    def criando_nova_despesa(self):
        self.BotaoCadastrarDespesa.clicked.connect(self.registro_despesa)

    @staticmethod
    def procurar_id_veiculo(nrPlaca): # Retorna o id do veículo
        response = session.query(Veiculo).filter(Veiculo.NRPLACA == nrPlaca).first()
        id_veiculo = response.IDVEICULO
        return id_veiculo

    @staticmethod
    def procurar_cod_forne(nrCNPJ): #Retorna o Codigo do Fornecedor
        response = session.query(Fornecedor).filter(Fornecedor.CNPJ == nrCNPJ).first()
        cod_forne = response.COD
        return cod_forne

    def registro_despesa(self):
        try:
            nrNota       = self.nrNota.text()
            vlTotal      = self.vlTotal.text()
            nrPlaca      = self.nrPlaca.text()
            nrCNPJ       = self.nrCNPJ.text()
            tpGastos     = self.tpGastos.currentText()
            dsObservacao = self.dsObservacao.toPlainText()
            dtEmissao    = self.dtEmissao.date().toPyDate()
            #nmFornecedor = self.nmFornecedor.text()

            campos_obrigatorios = [nrPlaca, nrNota, vlTotal, nrCNPJ, tpGastos, dtEmissao]
            if any(campo == "" or campo is None for campo in campos_obrigatorios):
                QMessageBox.critical(self, "Erro", "Todos os campos devem ser preenchidos.")
                return

            if float(vlTotal) <= 0: # Validar se o valor é maior que zero
                QMessageBox.critical(self, "Erro", "O valor da despesa deve ser maior que zero.")
                return
            cod_forne    = DespesasView.procurar_cod_forne(nrCNPJ)
            id_veiculo   = DespesasView.procurar_id_veiculo(nrPlaca)
            novo_despesa = Despesas(TPGASTOS=tpGastos, NRNOTA=nrNota,
                                   VALOR=vlTotal, DTEMISSAO=dtEmissao, OBSERVACAO=dsObservacao,
                                   VEICULO_IDVEICULO=id_veiculo, FORNECEDOR_COD=cod_forne)

            session.add(novo_despesa)
            session.commit()

            QMessageBox.information(self, "Sucesso", "Despesa lançada!")
            self.limpar_campos()
        except IntegrityError as e:
            session.rollback()
            QMessageBox.critical(self, "Erro", "Erro de integridade: pode haver um valor duplicado ou outro problema de restrição.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self,"Erro", f"Ocorreu um erro ao lançar a despesa: {e}")

    def limpar_campos(self): #Função para limpar a tela ao terminar
        self.nrPlaca.clear()
        self.nrNota.clear()
        self.vlTotal.clear()
        #self.tpGastos.clear()
        #self.dtEmissao.clear()
        self.dsObservacao.clear()
        self.nmFornecedor.clear()
        self.nrCNPJ.clear()

if __name__ == "__main__": #Inicando a tela
    app = QtWidgets.QApplication([])
    window = DespesasView()
    app.exec()


