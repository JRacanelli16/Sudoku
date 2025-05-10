
# Sudoku Web App (Flask)

Este é um aplicativo web de Sudoku feito com Python (Flask) que permite:

- Inserção manual interativa de números
- Geração de Sudoku com níveis de dificuldade (Fácil, Médio, Difícil)
- Visualização da solução
- Botão para gerar outro tabuleiro da mesma dificuldade
- Interface amigável via navegador

## ✅ Como rodar

### 1. Instale o Flask

```bash
pip install flask
```

### 2. Execute o servidor

Navegue até a pasta do projeto e rode:

```bash
python app.py
```

### 3. Acesse no navegador

Abra o navegador em:

```
http://localhost:5000
```

## 📁 Estrutura

```
sudoku_web/
├── app.py
├── templates/
│   ├── index.html
│   ├── sudoku.html
│   └── manual.html
├── static/
│   └── style.css
```

## 💡 Observações

- A inserção manual agora usa linha e coluna de 1 a 9.
- Há um botão "Gerar Outro" ao lado de "Ver Solução".
- Botões na página inicial estão alinhados horizontalmente.

Feito com ❤️ usando Python + Flask.
