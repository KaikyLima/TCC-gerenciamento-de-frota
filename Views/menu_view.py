from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate
from cadastro_veiculo_view import CadastroVeiculoView
from vinculo_motorista_veiculo_view import VincularDesvincularMotorista
from cadastro_funcionario_view import CadastroFuncionarioView
from engate_view import EngateDesengateVeiculo
from despesas_view import DespesasView
from consultarFornecedor import consultarFornecedor
from consultar_veiculo_view import ConsultarVeiculo
from consultar_vinculo_view import ConsultarVinculos
from consultar_engate_view import ConsultarEngates
import datetime
class MenuInicial(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('telaMenu.ui', self)
        self.show()
        self.botaoEntrarCadastroVeic.clicked.connect(self.ChamarCadastroVeiculo)
        self.botaoCtVinculo.clicked.connect(self.ChamarCtVinculoMotorista)
        self.botaoEngateDesengate.clicked.connect(self.ChamarEngateDesengate)
        self.botaoCadastroFunc.clicked.connect(self.CadastroFuncionario)
        self.botaoDespesa.clicked.connect(self.ChamarTelaDespesa)
        self.botaoConsultaVinculos.clicked.connect(self.ChamarTelaConsultaVinculo)
        self.botaoCadastroForne.clicked.connect(self.ChamarTelaCadastroForne)
        self.botaoConsultaVeic.clicked.connect(self.ChamarTelaConsultaVeic)
        self.botaoConsultaEngate.clicked.connect(self.ChamarTelaConsultaEngate)

        self.cadastro_veiculo_view          = None
        self.vinculo_motorista_veiculo_view = None
        self.engate_desengate_view          = None
        self.cadatro_funcionario_view       = None
        self.despesas_view                  = None
        self.consultarFornecedor            = None
        self.consultar_veiculo_view         = None
        self.consultar_vinculo_view         = None
        self.consultar_engate_view          = None

        # Obter a data atual
        data_atual = datetime.date.today()

        # Configurar o campo de data para a data atual
        self.dtAtual.setDate(QDate.fromString(data_atual.strftime('%d-%m-%Y'), 'dd-MM-yyyy'))

    def ChamarTelaCadastroForne(self):
        if not self.consultarFornecedor:
            self.consultarFornecedor = consultarFornecedor()
        self.consultarFornecedor.show()

    def ChamarTelaConsultaVeic(self):
        if not self.consultar_veiculo_view:
            self.consultar_veiculo_view = ConsultarVeiculo()
        self.consultar_veiculo_view.show()

    def ChamarTelaConsultaVinculo(self):
        if not self.consultar_vinculo_view:
            self.consultar_vinculo_view = ConsultarVinculos()
        self.consultar_vinculo_view.show()
    def ChamarTelaConsultaEngate(self):
        if not self.consultar_engate_view:
            self.consultar_engate_view = ConsultarEngates()
        self.consultar_engate_view.show()
    def CadastroFuncionario(self):
        if not self.cadatro_funcionario_view:
            self.cadatro_funcionario_view = CadastroFuncionarioView()
        self.cadatro_funcionario_view.show()
    def ChamarCadastroVeiculo(self):
        if not self.cadastro_veiculo_view:
            self.cadastro_veiculo_view = CadastroVeiculoView()
        self.cadastro_veiculo_view.show()

    def ChamarTelaDespesa(self):
        if not self.despesas_view:
            self.despesas_view = DespesasView()
        self.despesas_view.show()
    def ChamarCtVinculoMotorista(self):
        if not self.vinculo_motorista_veiculo_view:
            self.vinculo_motorista_veiculo_view = VincularDesvincularMotorista()
        self.vinculo_motorista_veiculo_view.show()

    def ChamarEngateDesengate(self):
        if not self.engate_desengate_view:
            self.engate_desengate_view = EngateDesengateVeiculo()
        self.engate_desengate_view.show()



if __name__ == "__main__": #Inicando a tela
    app = QtWidgets.QApplication([])
    window = MenuInicial()
    app.exec()