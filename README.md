# Sudoku Web (Flask) 

Aplicação web simples, feita em **Python + Flask**, que permite:

- ✅ **Gerar** um Sudoku (nível único, entre 40 e 50 casas vazias)  
- ✅ **Inserir números manualmente** em um tabuleiro em branco  
- ✅ **Resolver** qualquer tabuleiro válido e exibir **até 10 soluções**  
- ✅ Mostrar **estatísticas** de busca (tentativas e tempo em ms)  
- ✅ Alternar entre soluções encontradas  
- ✅ Interface responsiva sem dependências externas de front-end  
- ✅ 100 % *server-side*, sem banco de dados (estado via sessão Flask)

---

## 1. Requisitos

| Ferramenta | Versão Sugerida |
|------------|-----------------|
| Python     | 3.9 +           |
| Flask      | \>= 2.0         |

Instalação rápida:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt   # ou simplesmente: pip install flask

## 2. Como executar

# modo 1 — diretamente
python appsudoku.py

# modo 2 — usando FLASK_APP
export FLASK_APP=appsudoku.py      # no Windows: set FLASK_APP=appsudoku.py
flask run

## 3. Estrutura do Projeto

SUDOKU/
├── static/
│   └── style.css        # estilos do tabuleiro e botões
├── templates/
│   ├── index.html       # página inicial
│   ├── manual.html      # inserção manual
│   └── sudoku.html      # exibição/solução
├── appsudoku.py         # servidor Flask + lógica de geração/solução
├── README.md            # este arquivo
└── requirements.txt

## 4. API Interna

Principais rotas Flask:

| Rota            | Método | Ação                                   |
| --------------- | ------ | -------------------------------------- |
| `/`             | GET    | Página inicial                         |
| `/sudoku`       | GET    | Gera tabuleiro aleatório               |
| `/solve`        | GET    | Resolve o tabuleiro gerado             |
| `/next`         | GET    | Mostra próxima solução                 |
| `/manual`       | GET    | Tela de inserção manual                |
| `/add`          | POST   | Adiciona número (linha, coluna, valor) |
| `/solve_manual` | GET    | Resolve tabuleiro inserido             |

Contribuições são bem-vindas! Abra um issue ou faça um pull request.
Enois

