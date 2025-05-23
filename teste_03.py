class Tarefa:
    def __init__(self, id, descricao, prioridade="normal"):
        self.id = id
        self.descricao = descricao
        self.prioridade = prioridade
        self.concluida = False
        self.data_criacao = "2023-01-01"  # Simulação - em um sistema real seria datetime.now()
    
    def marcar_como_concluida(self):
        self.concluida = True
    
    def atualizar_descricao(self, nova_descricao):
        if not nova_descricao.strip():
            raise ValueError("Descrição não pode ser vazia")
        self.descricao = nova_descricao
    
    def aumentar_prioridade(self):
        if self.prioridade == "baixa":
            self.prioridade = "normal"
        elif self.prioridade == "normal":
            self.prioridade = "alta"
        # alta permanece alta

class GerenciadorTarefas:
    def __init__(self):
        self.tarefas = []
        self.contador_id = 1
    
    def adicionar_tarefa(self, descricao, prioridade="normal"):
        tarefa = Tarefa(self.contador_id, descricao, prioridade)
        self.tarefas.append(tarefa)
        self.contador_id += 1
        return tarefa
    
    def buscar_tarefa(self, id):
        for tarefa in self.tarefas:
            if tarefa.id == id:
                return tarefa
        return None
    
    def listar_tarefas(self, filtro=None):
        if filtro == "pendentes":
            return [t for t in self.tarefas if not t.concluida]
        elif filtro == "concluidas":
            return [t for t in self.tarefas if t.concluida]
        elif filtro == "prioridade":
            return sorted(self.tarefas, key=lambda x: (x.prioridade == "alta", x.prioridade == "normal"), reverse=True)
        return self.tarefas
    
    def remover_tarefa(self, id):
        tarefa = self.buscar_tarefa(id)
        if tarefa:
            self.tarefas.remove(tarefa)
            return True
        return False




import unittest

class TesteRegressaoGerenciadorTarefas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuração inicial para todos os testes"""
        cls.gerenciador = GerenciadorTarefas()
        
        # Adiciona tarefas de teste que representam o estado conhecido do sistema
        cls.tarefa1 = cls.gerenciador.adicionar_tarefa("Comprar leite", "baixa")
        cls.tarefa2 = cls.gerenciador.adicionar_tarefa("Estudar Python", "alta")
        cls.tarefa3 = cls.gerenciador.adicionar_tarefa("Lavar o carro")
    
    def test_regressao_adicionar_tarefa(self):
        """Verifica se a adição de tarefas continua funcionando"""
        nova_tarefa = self.gerenciador.adicionar_tarefa("Fazer exercícios")
        
        self.assertEqual(nova_tarefa.descricao, "Fazer exercícios")
        self.assertEqual(nova_tarefa.prioridade, "normal")
        self.assertFalse(nova_tarefa.concluida)
        self.assertEqual(len(self.gerenciador.listar_tarefas()), 4)
    
    def test_regressao_marcar_concluida(self):
        """Verifica se marcar como concluída continua funcionando"""
        self.tarefa1.marcar_como_concluida()
        
        self.assertTrue(self.tarefa1.concluida)
        self.assertEqual(len(self.gerenciador.listar_tarefas("concluidas")), 1)
        self.assertEqual(len(self.gerenciador.listar_tarefas("pendentes")), 2)
        
        # Desfaz para não afetar outros testes
        self.tarefa1.concluida = False
    
    def test_regressao_atualizar_descricao(self):
        """Verifica se a atualização de descrição continua funcionando"""
        self.tarefa2.atualizar_descricao("Estudar Python e Django")
        
        self.assertEqual(self.tarefa2.descricao, "Estudar Python e Django")
        
        # Testa tratamento de erro
        with self.assertRaises(ValueError):
            self.tarefa2.atualizar_descricao("")
        
        # Restaura descrição original
        self.tarefa2.atualizar_descricao("Estudar Python")
    
    def test_regressao_prioridade(self):
        """Verifica se o sistema de prioridades continua funcionando"""
        # Tarefa com prioridade baixa
        self.tarefa1.aumentar_prioridade()
        self.assertEqual(self.tarefa1.prioridade, "normal")
        
        # Tarefa com prioridade normal
        self.tarefa3.aumentar_prioridade()
        self.assertEqual(self.tarefa3.prioridade, "alta")
        
        # Tarefa com prioridade alta (não deve mudar)
        self.tarefa2.aumentar_prioridade()
        self.assertEqual(self.tarefa2.prioridade, "alta")
        
        # Restaura prioridades originais
        self.tarefa1.prioridade = "baixa"
        self.tarefa3.prioridade = "normal"
    
    def test_regressao_filtros(self):
        """Verifica se os filtros de listagem continuam funcionando"""
        # Filtro pendentes
        pendentes = self.gerenciador.listar_tarefas("pendentes")
        self.assertEqual(len(pendentes), 3)
        
        # Filtro concluídas
        concluidas = self.gerenciador.listar_tarefas("concluidas")
        self.assertEqual(len(concluidas), 0)
        
        # Filtro por prioridade
        por_prioridade = self.gerenciador.listar_tarefas("prioridade")
        self.assertEqual(por_prioridade[0].prioridade, "alta")
        self.assertEqual(por_prioridade[-1].prioridade, "baixa")
    
    def test_regressao_remocao(self):
        """Verifica se a remoção de tarefas continua funcionando"""
        tarefa_remover = self.gerenciador.adicionar_tarefa("Tarefa temporária")
        id_temp = tarefa_remover.id
        
        self.assertTrue(self.gerenciador.remover_tarefa(id_temp))
        self.assertIsNone(self.gerenciador.buscar_tarefa(id_temp))
        self.assertEqual(len(self.gerenciador.listar_tarefas()), 3)

# Execução no Colab
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
