# 🔧 Solução: ModuleNotFoundError: No module named 'flask'

## ⚡ Solução Rápida (Recomendada)

### Opção 1: Limpar e Recriar myenv do Zero ⭐

```bash
cd /Users/matildematosa/Desktop/Luna_Backend
./limpar_e_recriar_myenv.sh
```

Este script vai:
1. **Apagar** o ambiente virtual `myenv` antigo (limpo!)
2. **Criar** um novo ambiente virtual `myenv` do zero
3. Atualizar pip
4. Instalar todas as dependências do `requirements.txt`

Depois, inicia o servidor:
```bash
./start_backend.sh
```

---

### Opção 2: Instalar no myenv Existente

```bash
cd /Users/matildematosa/Desktop/Luna_Backend
./instalar_myenv.sh
```

---

### Opção 2: Instalação Manual

Se preferires fazer manualmente:

```bash
cd /Users/matildematosa/Desktop/Luna_Backend
source myenv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 app.py
```

---

### Opção 3: Usar Outro Ambiente Virtual

Se o `myenv` tiver problemas, podes usar o `venv_new`:

```bash
cd /Users/matildematosa/Desktop/Luna_Backend
./install_dependencies.sh
./start_backend.sh
```

---

## ✅ Verificar se Funcionou

Depois de instalar, verifica:

```bash
source myenv/bin/activate
python3 -c "import flask; print('✅ Flask instalado!')"
```

Se aparecer "✅ Flask instalado!", está tudo certo!

---

## 🚀 Iniciar o Servidor

```bash
cd /Users/matildematosa/Desktop/Luna_Backend
source myenv/bin/activate
python3 app.py
```

Ou simplesmente:
```bash
./start_backend.sh
```

