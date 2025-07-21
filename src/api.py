"""
API FastAPI para o assistente virtual
Desenvolvido por Pedro Favoretti - Drope Dev
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from assistente import AssitenteVirtual

# Carregar variáveis de ambiente
load_dotenv()

app = FastAPI(
    title="Assistente Virtual E-commerce",
    description="API para assistente virtual especializado em e-commerce",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar assistente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
    raise ValueError("OPENAI_API_KEY não configurada. Configure no arquivo .env")

assistente = AssitenteVirtual(OPENAI_API_KEY, data_dir="./data")


# Modelos Pydantic
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default"


class QueryResponse(BaseModel):
    intent: str
    response: str
    data: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    status: str
    message: str


# Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Endpoint de saúde da API"""
    return HealthResponse(
        status="ok",
        message="Assistente Virtual E-commerce API está funcionando!"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Verificação de saúde da API"""
    return HealthResponse(
        status="healthy",
        message="API está funcionando corretamente"
    )


@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """
    Endpoint principal para conversar com o assistente
    """
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query não pode estar vazia")
        
        # Processar consulta
        result = assistente.process_query(request.query, request.user_id)
        
        # Preparar dados adicionais
        data = {}
        if result["intent"] == "busca_produto":
            data = {
                "products": result.get("products", []),
                "filters": result.get("filters", {})
            }
        elif result["intent"] == "consulta_pedido":
            data = {
                "order_id": result.get("order_id"),
                "order": result.get("order")
            }
        elif result["intent"] == "recomendacao":
            data = {
                "recommendations": result.get("recommendations", [])
            }
        
        return QueryResponse(
            intent=result["intent"],
            response=result["response"],
            data=data
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.get("/history/{user_id}")
async def get_history(user_id: str):
    """
    Retorna histórico de conversas do usuário
    """
    try:
        history = assistente.get_conversation_history(user_id)
        return {"user_id": user_id, "history": history}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")


@app.delete("/history/{user_id}")
async def clear_history(user_id: str):
    """
    Limpa histórico de conversas do usuário
    """
    try:
        assistente.clear_conversation_history(user_id)
        return {"message": f"Histórico do usuário {user_id} limpo com sucesso"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar histórico: {str(e)}")


@app.get("/products")
async def list_products():
    """
    Lista todos os produtos disponíveis
    """
    try:
        return {"products": assistente.rag_system.products_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")


@app.get("/orders")
async def list_orders():
    """
    Lista todos os pedidos (para fins de demonstração)
    """
    try:
        return {"orders": assistente.rag_system.orders_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 5000))
    
    uvicorn.run(app, host=host, port=port)


