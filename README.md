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
