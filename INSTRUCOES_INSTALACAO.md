# 📋 Instruções de Instalação - AssistentIA

## 🔑 PASSO 1: Configurar Chave da OpenAI (OBRIGATÓRIO)

### Onde encontrar sua chave:
1. Acesse: https://platform.openai.com/account/api-keys
2. Faça login na sua conta OpenAI
3. Clique em "Create new secret key"
4. Copie a chave gerada

### Onde colocar no projeto:
Abra o arquivo `.env` na raiz do projeto e substitua:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Por:

```env
OPENAI_API_KEY=sk-sua-chave-real-aqui
```

**⚠️ IMPORTANTE:** Sem esta configuração, o assistente não funcionará!

## 🚀 PASSO 2: Escolha o Método de Instalação

### Opção A: Instalação Local (Recomendada para Desenvolvimento)

#### Pré-requisitos:
- Python 3.11 ou superior
- Node.js 20 ou superior
- pnpm (ou npm)

#### 1. Instalar dependências do Backend:
```bash
cd meu-assistente-virtual
pip install -r deploy/requirements.txt
```

#### 2. Iniciar o Backend:
```bash
cd src
python api.py
```
O backend estará rodando em: http://localhost:5000

#### 3. Instalar dependências do Frontend (em outro terminal):
```bash
cd frontend
pnpm install
```

#### 4. Iniciar o Frontend:
```bash
pnpm run dev --host
```
O frontend estará rodando em: http://localhost:5173

### Opção B: Docker (Recomendada para Produção)

#### Pré-requisitos:
- Docker
- Docker Compose

#### 1. Configurar variáveis de ambiente:
Crie um arquivo `.env` na pasta `deploy/` com:
```env
OPENAI_API_KEY=sua_chave_openai_aqui
```

#### 2. Executar com Docker Compose:
```bash
cd deploy
docker-compose up --build
```

Acesse:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## 🧪 PASSO 3: Testar o Sistema

### Testes Obrigatórios:

1. **Busca de Produtos:**
   - Digite: "Quero um notebook para programar, até R$ 3.000"
   - Deve retornar produtos compatíveis

2. **Consulta de Pedidos:**
   - Digite: "Cadê meu pedido #12345?"
   - Deve mostrar informações do pedido

3. **Políticas da Loja:**
   - Digite: "Como faço para trocar um produto?"
   - Deve explicar a política de trocas

4. **Recomendações:**
   - Digite: "O que vocês recomendam para quem gosta de tecnologia?"
   - Deve sugerir produtos relacionados

5. **Conversa Natural:**
   - Digite: "Oi, preciso de ajuda"
   - Deve responder de forma amigável

## 🔧 Solução de Problemas

### Erro: "OPENAI_API_KEY não configurada"
- **Solução:** Configure sua chave da OpenAI no arquivo `.env`

### Erro: "Module not found"
- **Solução:** Instale as dependências:
  ```bash
  pip install -r deploy/requirements.txt
  ```

### Frontend não carrega
- **Solução:** Verifique se o Node.js está instalado e execute:
  ```bash
  cd frontend
  pnpm install
  pnpm run dev --host
  ```

### API não responde
- **Solução:** Verifique se o backend está rodando:
  ```bash
  curl http://localhost:5000/health
  ```

### Erro de CORS
- **Solução:** O CORS já está configurado. Verifique se está acessando as URLs corretas.

## 📱 Acessando a Aplicação

### URLs de Acesso:
- **Frontend:** http://localhost:5173 (desenvolvimento) ou http://localhost:3000 (Docker)
- **API:** http://localhost:5000
- **Documentação da API:** http://localhost:5000/docs

### Interface:
1. Abra o frontend no navegador
2. Use os botões de exemplo ou digite suas próprias mensagens
3. O sistema classificará automaticamente sua intenção
4. Receberá respostas contextualizadas

## 🎯 Funcionalidades Disponíveis

### ✅ Implementadas:
- [x] Busca inteligente de produtos
- [x] Consulta de pedidos
- [x] Políticas da loja
- [x] Recomendações personalizadas
- [x] Conversa natural
- [x] Interface web moderna
- [x] API REST completa
- [x] Sistema RAG com embeddings
- [x] Classificação automática de intenções

### 📊 Dados Inclusos:
- **15 produtos** em diversas categorias
- **6 pedidos** com diferentes status
- **Políticas completas** da loja
- **Base de conhecimento** estruturada

## 🚀 Deploy em Produção

### Para Render (Gratuito):
1. Faça fork do repositório
2. Conecte ao Render
3. Configure a variável `OPENAI_API_KEY`
4. Deploy automático

### Para Railway:
1. Conecte o repositório
2. Configure variáveis de ambiente
3. Deploy automático

### Para AWS/GCP:
1. Use os Dockerfiles fornecidos
2. Configure load balancer
3. Defina auto-scaling

## 📞 Suporte

Se encontrar problemas:

1. **Verifique os logs:**
   ```bash
   tail -f api.log
   ```

2. **Teste a API diretamente:**
   ```bash
   curl -X POST http://localhost:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "teste", "user_id": "test"}'
   ```

3. **Verifique as dependências:**
   ```bash
   pip list | grep -E "(fastapi|langchain|openai)"
   ```

## ✅ Checklist de Instalação

- [ ] Python 3.11+ instalado
- [ ] Node.js 20+ instalado
- [ ] Chave OpenAI configurada no `.env`
- [ ] Dependências do backend instaladas
- [ ] Backend rodando em localhost:5000
- [ ] Dependências do frontend instaladas
- [ ] Frontend rodando em localhost:5173
- [ ] Testes básicos realizados
- [ ] Sistema funcionando completamente

---

**🎉 Parabéns! Seu Assistente Virtual está pronto para uso!**

