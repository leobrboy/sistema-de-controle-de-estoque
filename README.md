
# 📦 Sistema de Controle de Estoque em Python (Tkinter + SQLite)

Este é um projeto de estudo de caso para a disciplina de Desenvolvimento com Python. A aplicação permite o gerenciamento de estoque de produtos com entrada/saída, autenticação de usuários e níveis de acesso (administrador e comum), tudo com interface gráfica utilizando Tkinter e banco de dados local SQLite.

---

## 🧰 Tecnologias Utilizadas

- Python 3.x
- Tkinter (interface gráfica)
- SQLite (banco de dados local)
- `bcrypt` (criptografia de senhas)

---

## 🚀 Funcionalidades

- Login com autenticação de usuário
- Perfis: **Administrador** e **Comum**
- Cadastro de novos usuários (restrito ao administrador)
- Cadastro de produtos com quantidade mínima
- Atualização de estoque (entrada e saída)
- Alerta visual para produtos abaixo do mínimo
- Interface intuitiva e validada
- Banco de dados local: **não precisa instalar nada**

---

## 📂 Estrutura do Projeto

```
controle_estoque/
├── main.py                   # Ponto de entrada da aplicação
├── login.py                  # Tela de login
├── dashboard.py              # Tela principal após login
├── cadastro_produto.py       # Cadastro de produtos
├── cadastro_usuario.py       # Cadastro de usuários (admin)
├── editar_estoque.py         # Entrada e saída de estoque
├── utils.py                  # Criptografia de senha
├── db.py                     # Conexão e criação do SQLite
├── estoque.db                # Banco de dados (gerado automaticamente)
└── README.md                 # Documentação
```

---

## ✅ Como Executar o Projeto

1. **Clonar o repositório ou extrair o .zip do projeto**
2. Instalar as dependências necessárias:

```bash
pip install bcrypt
```

> O SQLite já vem embutido com o Python, não precisa instalar nada.

3. Executar o projeto:

```bash
python main.py
```

4. O sistema criará automaticamente o banco de dados local `estoque.db` com as tabelas e um usuário inicial.

---

## 🔐 Usuário Inicial

Você pode fazer login com o seguinte usuário admin:

- **Usuário:** `leo`  
- **Senha:** `leo123`

Esse usuário já tem permissão para:
- Cadastrar produtos
- Cadastrar novos usuários
- Editar estoque

---

## 🧠 Aprendizados

Este projeto proporciona prática real em:
- Lógica de programação com Python
- Manipulação de banco de dados
- Criação de interfaces com Tkinter
- Criptografia de senha e controle de acesso
- Organização de projeto real com múltiplos arquivos
