class Livro:
    def __init__(self, titulo, autor, id):
        self.titulo = titulo
        self.autor = autor
        self.id = id
        self.disponivel = True

class Usuario:
    def __init__(self, nome, id):
        self.nome = nome
        self.id = id
        self.livros_emprestados = []

class Biblioteca:
    def __init__(self):
        self.livros = []
        self.usuarios = []
        self.emprestimos = []
    
    def adicionar_livro(self, livro):
        self.livros.append(livro)
    
    def registrar_usuario(self, usuario):
        self.usuarios.append(usuario)
    
    def emprestar_livro(self, usuario_id, livro_id):
        usuario = next((u for u in self.usuarios if u.id == usuario_id), None)
        livro = next((l for l in self.livros if l.id == livro_id), None)
        
        if not usuario or not livro:
            raise ValueError("Usuário ou livro não encontrado")
        
        if not livro.disponivel:
            raise ValueError("Livro já emprestado")
        
        livro.disponivel = False
        usuario.livros_emprestados.append(livro)
        self.emprestimos.append((usuario_id, livro_id))
        return True
    
    def devolver_livro(self, usuario_id, livro_id):
        usuario = next((u for u in self.usuarios if u.id == usuario_id), None)
        livro = next((l for l in self.livros if l.id == livro_id), None)
        
        if not usuario or not livro:
            raise ValueError("Usuário ou livro não encontrado")
        
        if livro.disponivel:
            raise ValueError("Livro já está disponível")
        
        livro.disponivel = True
        usuario.livros_emprestados = [l for l in usuario.livros_emprestados if l.id != livro_id]
        self.emprestimos = [e for e in self.emprestimos if e != (usuario_id, livro_id)]
        return True





import unittest

class TestIntegracaoBiblioteca(unittest.TestCase):
    def setUp(self):
        self.biblioteca = Biblioteca()
        
        # Criar alguns livros
        self.livro1 = Livro("Python Essentials", "John Doe", 1)
        self.livro2 = Livro("Clean Code", "Robert Martin", 2)
        
        # Criar alguns usuários
        self.usuario1 = Usuario("Alice", 101)
        self.usuario2 = Usuario("Bob", 102)
        
        # Adicionar à biblioteca
        self.biblioteca.adicionar_livro(self.livro1)
        self.biblioteca.adicionar_livro(self.livro2)
        self.biblioteca.registrar_usuario(self.usuario1)
        self.biblioteca.registrar_usuario(self.usuario2)
    
    def test_fluxo_completo_emprestimo_devolucao(self):
        # Testa todo o fluxo de empréstimo e devolução
        self.assertTrue(self.biblioteca.emprestar_livro(101, 1))
        self.assertFalse(self.livro1.disponivel)
        self.assertEqual(len(self.usuario1.livros_emprestados), 1)
        
        # Tentar emprestar o mesmo livro para outro usuário
        with self.assertRaises(ValueError):
            self.biblioteca.emprestar_livro(102, 1)
        
        # Devolver o livro
        self.assertTrue(self.biblioteca.devolver_livro(101, 1))
        self.assertTrue(self.livro1.disponivel)
        self.assertEqual(len(self.usuario1.livros_emprestados), 0)
    
    def test_multiplos_usuarios_multiplos_livros(self):
        # Usuário 1 pega livro 1
        self.biblioteca.emprestar_livro(101, 1)
        # Usuário 2 pega livro 2
        self.biblioteca.emprestar_livro(102, 2)
        
        # Verificar estados
        self.assertEqual(len(self.biblioteca.emprestimos), 2)
        self.assertEqual(len(self.usuario1.livros_emprestados), 1)
        self.assertEqual(len(self.usuario2.livros_emprestados), 1)
        self.assertFalse(self.livro1.disponivel)
        self.assertFalse(self.livro2.disponivel)
        
        # Devoluções
        self.biblioteca.devolver_livro(101, 1)
        self.biblioteca.devolver_livro(102, 2)
        
        # Verificar estados após devolução
        self.assertEqual(len(self.biblioteca.emprestimos), 0)
        self.assertEqual(len(self.usuario1.livros_emprestados), 0)
        self.assertEqual(len(self.usuario2.livros_emprestados), 0)
        self.assertTrue(self.livro1.disponivel)
        self.assertTrue(self.livro2.disponivel)
    
    def test_tentativa_emprestimo_livro_inexistente(self):
        with self.assertRaises(ValueError):
            self.biblioteca.emprestar_livro(101, 999)  # ID de livro inexistente
    
    def test_tentativa_devolucao_nao_emprestado(self):
        with self.assertRaises(ValueError):
            self.biblioteca.devolver_livro(101, 1)  # Livro não foi emprestado

# Execução no Colab
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
