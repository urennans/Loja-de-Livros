Sistema de Livraria Distribuída - Trabalho 1

Sobre o Projeto
Sistema distribuído para gerenciamento de livraria online desenvolvido para a disciplina de **Sistemas Distribuídos (QXD0043)** da Universidade Federal do Ceará - Campus Quixadá.

Objetivo: Implementar comunicação entre processos usando sockets TCP e serialização personalizada de objetos.

---

Desenvolvedores
- Renan Campos
- Gabriel Barbosa

---

## 🔄 Base do Projeto
💡 **Importante:** Este sistema foi adaptado a partir de um projeto de um amigo https://github.com/DAVIMEDX/PerfumeShop. Mantivemos a mesma estrutura de classes mas adaptamos totalmente para o domínio de livraria:

- `Perfume` → `Produto`
- `PerfumeImportado` → `LivroFisico` 
- `PerfumeNacional` → `LivroDigital`
- `PerfumeLimited` → `LivroColecionavel`
- `LojaPerfume` → `LojaVirtual`

A lógica de negócio e estrutura de classes foram preservadas, mas todo o domínio e funcionalidades foram reimplementados para o contexto de livraria.

Loja de Livros/
├── model/ # Classes de domínio (POJOs)
│ ├── produto.py # Classe base abstrata
│ ├── livro_fisico.py # Livros físicos
│ ├── livro_digital.py # Livros digitais
│ ├── livro_colecionavel.py # Livros colecionáveis
│ ├── loja_virtual.py # Gerenciamento da loja
│ └── vendas.py # Interface de vendas
├── streams/ # Serialização personalizada
│ ├── livro_output_stream.py # Serializador (Item 2)
│ ├── livro_input_stream.py # Desserializador (Item 3)
│ └── socket_stream.py # Adaptador para sockets
├── server/ # Servidor TCP
│ └── servidor_livros.py # Servidor multi-threaded
├── client/ # Cliente TCP
│ └── cliente_livros.py # Cliente de teste
├── testes/ # Casos de teste
│ ├── test_system_out.py # Teste com System.out
│ ├── test_file_stream.py # Teste com arquivo
│ ├── test_input_stream.py # Teste de leitura
│ └── test_tcp.py # Teste completo TCP
└── README.md # Este arquivo

 Como Executar

1. Iniciar o Servidor
python server/servidor_livros.py

2.  Executar o Cliente
python client/cliente_livros.py

3. 🧪 Executar Testes Individuais
# Teste com System.out
python testes/test_system_out.py

# Teste com arquivo
python testes/test_file_stream.py

# Teste de leitura
python testes/test_input_stream.py
