from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
import datetime
import matplotlib.pyplot as plt
from storage.storage import insert_data, select_data, delete_table
# Configuração de fonte e desativação do clipboard
font_size = 24

class UserInfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name_input = TextInput(hint_text="Nome", font_size=font_size)
        self.income_input = TextInput(hint_text="Rendimento Mensal", font_size=font_size)
        self.continue_button = Button(text="Continuar", font_size=font_size)
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.income_input)
        self.layout.add_widget(self.continue_button)
        self.add_widget(self.layout)

        self.continue_button.bind(on_release=self.on_continue)

    def on_continue(self, instance):
        name = self.name_input.text
        income = float(self.income_input.text)
        app = App.get_running_app()
        app.user_info = {"name": name, "income": income}
        app.root.current = "ExpenseScreen"

class ExpenseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        user_info_layout = GridLayout(cols=2)
        user_info_layout.add_widget(Label(text="Nome:", font_size=font_size))
        self.name_label = Label(text="", font_size=font_size)
        user_info_layout.add_widget(self.name_label)
        user_info_layout.add_widget(Label(text="Rendimento Mensal:", font_size=font_size))
        self.income_label = Label(text="", font_size=font_size)
        user_info_layout.add_widget(self.income_label)

        expense_input_layout = BoxLayout(orientation='vertical')
        self.partial_expense_input = TextInput(hint_text="Gasto Parcial", font_size=font_size)
        self.add_partial_button = Button(text="Adicionar Gasto Parcial", font_size=font_size)
        self.register_button = Button(text="Registrar Gasto Diário", font_size=font_size)
        self.budget_label = Label(text="Orçamento Diário: $0", font_size=font_size)
        self.generate_report_button = Button(text="Gerar Relatório", font_size=font_size)
        expense_input_layout.add_widget(self.partial_expense_input)
        expense_input_layout.add_widget(self.add_partial_button)
        expense_input_layout.add_widget(self.register_button)
        expense_input_layout.add_widget(self.budget_label)
        expense_input_layout.add_widget(self.generate_report_button)

        self.layout = GridLayout(cols=1)
        self.layout.add_widget(user_info_layout)
        self.layout.add_widget(expense_input_layout)
        self.add_widget(self.layout)

        self.register_button.bind(on_release=self.register_expense)
        self.add_partial_button.bind(on_release=self.add_partial_expense)
        self.generate_report_button.bind(on_release=self.generate_report)
    
    def fill_app_data(self):
        content_data = {
            "table_name":"users",
            "data_id":"objects"
        }
        select_rtn = select_data(content_data)
        self.name_label.text = select_rtn[0]["user_name"]
        income = select_rtn[0]["mensal_income"]
        self.budget = income / 30  # Reset the budget to the daily value
        self.budget_label.text = f"Orçamento Diário: ${self.budget:.2f}"
        self.income_label.text = f"${income:.2f}"
    
    def on_enter(self):
        app = App.get_running_app()
        user_info = app.user_info
        content_data = { "table_name": "users",
                         "json_content": [         
                                            {
                                              "user_name": user_info["name"] ,
                                              "mensal_income": user_info['income'],
                                              "user_phone":"+5511999991234"
                                            }
                                         ]
        }
        insert_data(content_data)
        self.fill_app_data()
    def add_partial_expense(self, instance):
        partial_expense = float(self.partial_expense_input.text)
        app = App.get_running_app()
        app.budget -= partial_expense
        self.budget_label.text = f"Orçamento Diário: ${app.budget:.2f}"
        self.partial_expense_input.text = ""

    def register_expense(self, instance):
        app = App.get_running_app()
        app.expenses.append(app.budget)
        app.budget = app.user_info["income"] / 30  # Reset the budget to the daily value
        self.budget_label.text = f"Orçamento Diário: ${app.budget:.2f}"

    def generate_report(self, instance):
        app = App.get_running_app()
        app.generate_report()

class FinanceManagerApp(App):
    user_info = {}
    expenses = []
    budget = 0

    def build(self):
        sm = ScreenManager()
        sm.add_widget(UserInfoScreen(name="UserInfoScreen"))
        sm.add_widget(ExpenseScreen(name="ExpenseScreen"))
        return sm

    def on_stop(self):
        # Remova a chamada para gerar o relatório ao encerrar a aplicação
        pass

    def generate_report(self):
        dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(len(self.expenses))]
        expenses = self.expenses

        plt.plot(dates, expenses, marker='o')
        plt.xlabel('Data')
        plt.ylabel('Despesas Diárias')
        plt.title('Relatório Financeiro Diário')
        plt.gcf().autofmt_xdate()
        plt.show()

if __name__ == '__main__':
    FinanceManagerApp().run()
