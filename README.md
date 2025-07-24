# Aplicação Dash - Gerenciador de Livros

Esta é uma aplicação web desenvolvida com Dash (Python) que permite gerenciar uma biblioteca de livros através de uma interface gráfica intuitiva. A aplicação consome as APIs desenvolvidas na pasta `deploy`.

## Funcionalidades

- ✅ **Adicionar Livros**: Interface para cadastrar novos livros com título, autor e ano
- ✅ **Listar Livros**: Visualização em tabela com funcionalidades de filtro, ordenação e paginação
- ✅ **Validação de Dados**: Validação de campos obrigatórios e formatos
- ✅ **Atualização em Tempo Real**: Atualização automática da lista após adicionar novos livros
- ✅ **Interface Responsiva**: Design limpo e moderno

## Pré-requisitos

1. **API FastAPI ativa**: A aplicação da pasta `deploy` deve estar rodando na porta 8000
2. **Python 3.8+**
3. **Dependências instaladas** (veja seção de instalação)

## Instalação

1. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verificar se a API está rodando**:
   - A API deve estar acessível em `http://localhost:8000`
   - Você pode testar acessando `http://localhost:8000/docs` para ver a documentação da API

## Como Usar

1. **Iniciar a aplicação**:
   ```bash
   python app.py
   ```

2. **Acessar a interface**:
   - Abra seu navegador e vá para `http://localhost:8050`

3. **Usar a aplicação**:
   - **Adicionar livro**: Preencha os campos "Título", "Autor" e "Ano" e clique em "Adicionar Livro"
   - **Ver livros**: A tabela será carregada automaticamente. Use o botão "Atualizar Lista" se necessário
   - **Filtrar/Ordenar**: Use as funcionalidades da tabela para filtrar e ordenar os dados

## Estrutura do Projeto

```
dash_livros/
├── app.py              # Aplicação principal Dash
├── requirements.txt    # Dependências do projeto
└── README.md          # Este arquivo
```

## Validações Implementadas

- **Título**: Mínimo de 3 caracteres
- **Autor**: Mínimo de 3 caracteres  
- **Ano**: Deve ser maior que 1000

## Tecnologias Utilizadas

- **Dash**: Framework web para Python
- **Pandas**: Manipulação de dados
- **Requests**: Requisições HTTP para a API
- **Plotly**: Componentes de visualização

## Troubleshooting

### Erro de Conexão com a API
- Verifique se a API FastAPI está rodando em `http://localhost:8000`
- Confirme que não há firewall bloqueando as portas 8000 ou 8050

### Erro ao Adicionar Livros
- Verifique se todos os campos estão preenchidos corretamente
- Confirme que o banco de dados está acessível pela API

### Interface não carrega
- Verifique se a porta 8050 está disponível
- Confirme que todas as dependências foram instaladas corretamente

## Próximas Funcionalidades

- [ ] Editar livros existentes
- [ ] Excluir livros
- [ ] Busca avançada
- [ ] Exportar dados para CSV/Excel
- [ ] Gráficos e estatísticas
