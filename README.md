# 🤖 AssistentIA - Assistente Virtual E-commerce

Um assistente virtual inteligente desenvolvido para e-commerce que auxilia clientes em busca de produtos, consulta de pedidos, políticas da loja e recomendações personalizadas.

## 🎯 Funcionalidades

### ✅ Funcionalidades Implementadas

1. **🔍 Busca Inteligente de Produtos**
   - Busca semântica usando embeddings
   - Filtros por preço e categoria
   - Exemplo: "Quero um notebook para programar, até R$ 3.000"

2. **📋 Políticas da Loja**
   - Informações sobre trocas e devoluções
   - Prazos de entrega
   - Formas de pagamento
   - Exemplo: "Como faço para trocar um produto?"

3. **📦 Consulta de Pedidos**
   - Status de pedidos por ID
   - Informações de entrega
   - Histórico de compras
   - Exemplo: "Cadê meu pedido #12345?"

4. **⭐ Recomendações Personalizadas**
   - Sugestões baseadas em preferências
   - Análise de perfil do cliente
   - Exemplo: "O que vocês recomendam para quem gosta de tecnologia?"

5. **💬 Conversa Natural**
   - Interface conversacional intuitiva
   - Classificação automática de intenções
   - Respostas contextualizadas

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   OpenAI API    │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (GPT-3.5)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   RAG System    │
                       │   (FAISS +      │
                       │   Embeddings)   │
                       └─────────────────┘
```

## 🚀 Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **LangChain** - Framework para aplicações com LLM
- **OpenAI API** - Modelo de linguagem GPT-3.5-turbo
- **FAISS** - Busca vetorial eficiente
- **Python 3.11** - Linguagem de programação

### Frontend
- **React 18** - Biblioteca para interfaces de usuário
- **Vite** - Build tool moderna
- **Tailwind CSS** - Framework CSS utilitário
- **shadcn/ui** - Componentes de UI modernos
- **Lucide Icons** - Ícones SVG

### Deploy
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **Nginx** - Servidor web para frontend

## 📁 Estrutura do Projeto

```
meu-assistente-virtual/
├── src/                    # Código fonte do backend
│   ├── assistente.py      # Lógica principal do assistente
│   ├── rag_system.py      # Sistema RAG (busca vetorial)
│   ├── api.py             # Endpoints da API
│   └── prompts.py         # Templates de prompts
├── data/                  # Dados do sistema
│   ├── produtos.json      # Catálogo de produtos
│   ├── pedidos.json       # Base de pedidos
│   └── politicas.md       # Políticas da loja
├── frontend/              # Aplicação React
│   ├── src/
│   │   ├── App.jsx        # Componente principal
│   │   └── components/    # Componentes UI
│   └── public/
├── deploy/                # Arquivos de deploy
│   ├── Dockerfile         # Container do backend
│   ├── docker-compose.yml # Orquestração
│   └── requirements.txt   # Dependências Python
├── .env                   # Variáveis de ambiente
└── README.md             # Documentação
```

## ⚙️ Configuração e Instalação

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- Chave da API OpenAI

### 1. Configurar Chave da OpenAI

**⚠️ IMPORTANTE: Configure sua chave da OpenAI**

No arquivo `.env`, substitua:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

Por:
```env
OPENAI_API_KEY=sua_chave_real_da_openai_aqui
```

### 2. Instalação Local

#### Backend
```bash
cd meu-assistente-virtual
pip install -r deploy/requirements.txt
cd src
python api.py
```

#### Frontend
```bash
cd frontend
pnpm install
pnpm run dev --host
```

### 3. Deploy com Docker

```bash
cd meu-assistente-virtual/deploy
docker-compose up --build
```

Acesse:
- Frontend: http://localhost:3000
- API: http://localhost:5000

## 🧪 Testes

### Testes Obrigatórios Implementados

1. **Busca de Produtos**
   - Input: "Quero um smartphone Android, tela grande, até R$ 1.500"
   - ✅ Retorna produtos compatíveis com filtros

2. **Políticas**
   - Input: "Posso trocar um produto depois de 15 dias?"
   - ✅ Explica política de trocas

3. **Status de Pedido**
   - Input: "Meu pedido #12345 já saiu para entrega?"
   - ✅ Retorna status e previsão

4. **Recomendação**
   - Input: "Que presente vocês sugerem para uma pessoa que gosta de cozinhar?"
   - ✅ Sugere produtos relacionados

5. **Conversa Natural**
   - Input: "Oi, tudo bem? Estou procurando um presente para minha mãe"
   - ✅ Resposta amigável + direcionamento

## 📊 Dados de Exemplo

### Produtos
- 15 produtos em categorias variadas
- Eletrônicos, Casa, Esportes, Roupas, Livros
- Preços de R$ 89,99 a R$ 8.999,99

### Pedidos
- 6 pedidos com diferentes status
- IDs: 12345, 12346, 12347, 12348, 12349, 12350
- Status: Em trânsito, Entregue, Preparando, Cancelado, etc.

### Políticas
- Trocas e devoluções (7-60 dias)
- Prazos de entrega por região
- Formas de pagamento
- Garantias e atendimento

## 🔧 API Endpoints

### Principais Endpoints

- `GET /` - Health check
- `POST /chat` - Conversar com o assistente
- `GET /products` - Listar produtos
- `GET /orders` - Listar pedidos
- `GET /history/{user_id}` - Histórico de conversas

### Exemplo de Uso

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Quero um notebook para programar",
    "user_id": "user123"
  }'
```

## 🎨 Interface

### Características da UI
- Design moderno e responsivo
- Chat em tempo real
- Classificação visual de intenções
- Cards para produtos e pedidos
- Ações rápidas para testes
- Tema claro/escuro automático

### Componentes
- Chat interface com scroll automático
- Badges para classificação de intenções
- Cards de produtos com preços
- Informações detalhadas de pedidos
- Botões de ação rápida

## 🚀 Deploy em Produção

### Opções de Deploy

1. **Render** (Recomendado - Gratuito)
   - Fork do repositório
   - Conectar ao Render
   - Configurar variáveis de ambiente

2. **Railway** (Fácil - Pago)
   - Deploy direto do GitHub
   - Configuração automática

3. **AWS/GCP** (Profissional)
   - ECS/Cloud Run
   - Load balancer
   - Auto-scaling

### Variáveis de Ambiente para Produção

```env
OPENAI_API_KEY=sua_chave_openai
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=False
LOG_LEVEL=INFO
```

## 📈 Monitoramento

### Métricas Implementadas
- Classificação de intenções
- Tempo de resposta
- Histórico de conversas
- Logs de erro

### Logs
- Todas as interações são logadas
- Classificação automática de intenções
- Rastreamento de erros da OpenAI

## 🔒 Segurança

### Medidas Implementadas
- CORS configurado
- Validação de entrada com Pydantic
- Rate limiting (recomendado para produção)
- Sanitização de dados

### Recomendações
- Use HTTPS em produção
- Configure rate limiting
- Monitore uso da API OpenAI
- Implemente autenticação se necessário

## 🤝 Contribuição

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

### Roadmap
- [ ] Autenticação de usuários
- [ ] Integração com WhatsApp
- [ ] Dashboard de métricas
- [ ] Suporte a múltiplos idiomas
- [ ] Cache de respostas
- [ ] Análise de sentimento

## 📝 Licença

Este projeto foi desenvolvido como projeto final de curso e está disponível para fins educacionais.

## 👨‍💻 Desenvolvedor

Projeto desenvolvido utilizando:
- React + FastAPI + OpenAI
- Arquitetura RAG com FAISS
- Design moderno com Tailwind CSS
- Deploy containerizado com Docker

---

**🎯 Projeto Final Completo - Assistente Virtual E-commerce**

*Todas as funcionalidades obrigatórias implementadas e testadas*




**Créditos:**
- Pedro Favoretti - Drope Dev

