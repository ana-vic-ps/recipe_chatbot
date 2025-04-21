# Chef Virtual de Receitas

## Descrição

Um chatbot inteligente que encontra receitas deliciosas em português, traduzindo automaticamente os resultados da API Spoonacular.

## Funcionalidades

- 🔍 Busca receitas por ingrediente ou nome do prato
- 🌐 Traduz automaticamente para português
- 📚 Mantém histórico de receitas
- 🎲 Gera receitas aleatórias
- 📱 Interface amigável e responsiva

### Pré-requisitos

- Python 3.8+
- Conta na [Spoonacular](https://spoonacular.com/food-api) (para API key)

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/ana-vic-ps/recipe_chatbot.git
cd chef-virtual
```

2. Configure o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie o arquivo de configuração `.env`:

```
SPOONACULAR_API_KEY=sua_chave_aqui
```

## Como Usar

Inicie o aplicativo com:

```bash
streamlit run app.py
```

Acesse no navegador:  
[http://localhost:8501](http://localhost:8501)
