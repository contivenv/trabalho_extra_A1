import json
from datetime import datetime

class Tarefa:
    def __init__(self, descricao, data):
        self.descricao = descricao
        self.concluida = False
        self.data = self.validar_data(data)

    def validar_data(self, data_str):
        """Valida e formata a data da tarefa"""
        try:
            # Tenta converter a string para objeto datetime
            data_obj = datetime.strptime(data_str, '%d/%m/%Y')
            return data_str  # Retorna no formato original se válido
        except ValueError:
            raise ValueError("Data inválida. Use o formato DD/MM/AAAA")

    def concluir(self):
        self.concluida = True

    def to_dict(self):
        return {
            'descricao': self.descricao,
            'concluida': self.concluida,
            'data': self.data
        }

    @staticmethod
    def from_dict(dado):
        tarefa = Tarefa(dado['descricao'], dado['data'])
        tarefa.concluida = dado['concluida']
        return tarefa

    def __str__(self):
        status = '✓' if self.concluida else '✗'
        return f"[{status}] {self.descricao} (Data: {self.data})"


class GerenciadorDeTarefas:
    def __init__(self, arquivo='tarefas.json'):
        self.arquivo = arquivo
        self.tarefas = []
        self.carregar()

    def adicionar_tarefa(self, descricao, data):
        try:
            nova_tarefa = Tarefa(descricao, data)
            self.tarefas.append(nova_tarefa)
            self.salvar()
            print("\nTarefa adicionada com sucesso!")
        except ValueError as e:
            print(f"\nErro: {e}")

    def listar_tarefas(self):
        if not self.tarefas:
            print("\nNenhuma tarefa cadastrada.")
            return
        
        print("\n=== LISTA DE TAREFAS ===")
        for i, tarefa in enumerate(self.tarefas, start=1):
            print(f"{i}. {tarefa}")

    def buscar_tarefas(self, termo):
        encontradas = [
            (i, tarefa) for i, tarefa in enumerate(self.tarefas, start=1) 
            if termo.lower() in tarefa.descricao.lower()
        ]
        
        if not encontradas:
            print("\nNenhuma tarefa encontrada com esse termo.")
            return
        
        print(f"\n=== TAREFAS ENCONTRADAS ({len(encontradas)}) ===")
        for i, tarefa in encontradas:
            print(f"{i}. {tarefa}")

    def concluir_tarefa(self, indice):
        try:
            indice = int(indice)
            if 1 <= indice <= len(self.tarefas):
                self.tarefas[indice - 1].concluir()
                self.salvar()
                print("\nTarefa marcada como concluída!")
            else:
                print("\nErro: Índice inválido.")
        except ValueError:
            print("\nErro: Digite um número válido.")

    def remover_tarefa(self, indice):
        try:
            indice = int(indice)
            if 1 <= indice <= len(self.tarefas):
                tarefa_removida = self.tarefas.pop(indice - 1)
                self.salvar()
                print(f"\nTarefa removida: {tarefa_removida.descricao}")
            else:
                print("\nErro: Índice inválido.")
        except ValueError:
            print("\nErro: Digite um número válido.")

    def salvar(self):
        try:
            with open(self.arquivo, 'w') as f:
                json.dump([tarefa.to_dict() for tarefa in self.tarefas], f, indent=4)
        except IOError as e:
            print(f"\nErro ao salvar as tarefas: {e}")

    def carregar(self):
        try:
            with open(self.arquivo, 'r') as f:
                tarefas_carregadas = json.load(f)
                self.tarefas = [Tarefa.from_dict(dado) for dado in tarefas_carregadas]
        except FileNotFoundError:
            self.tarefas = []
        except json.JSONDecodeError:
            print("\nAviso: Arquivo de tarefas corrompido. Iniciando com lista vazia.")
            self.tarefas = []
        except Exception as e:
            print(f"\nErro inesperado ao carregar tarefas: {e}")
            self.tarefas = []


def mostrar_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Adicionar nova tarefa")
    print("2. Listar todas as tarefas")
    print("3. Buscar tarefas por descrição")
    print("4. Marcar tarefa como concluída")
    print("5. Remover tarefa")
    print("6. Sair")
    return input("Escolha uma opção: ")


def main():
    gerenciador = GerenciadorDeTarefas()
    
    while True:
        opcao = mostrar_menu()
        
        if opcao == '1':
            descricao = input("Descrição da tarefa: ").strip()
            data = input("Data (DD/MM/AAAA): ").strip()
            gerenciador.adicionar_tarefa(descricao, data)
        
        elif opcao == '2':
            gerenciador.listar_tarefas()
        
        elif opcao == '3':
            termo = input("Termo de busca: ").strip()
            gerenciador.buscar_tarefas(termo)
        
        elif opcao == '4':
            gerenciador.listar_tarefas()
            if gerenciador.tarefas:
                indice = input("Número da tarefa a concluir: ").strip()
                gerenciador.concluir_tarefa(indice)
        
        elif opcao == '5':
            gerenciador.listar_tarefas()
            if gerenciador.tarefas:
                indice = input("Número da tarefa a remover: ").strip()
                gerenciador.remover_tarefa(indice)
        
        elif opcao == '6':
            print("\nSaindo do sistema...")
            break
        
        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")