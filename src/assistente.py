"""
Lógica principal do assistente virtual
Desenvolvido por Pedro Favoretti - Drope Dev
"""

import os
import re
import json
from typing import Dict, List, Any
from openai import OpenAI
from openai import AuthenticationError
from rag_system import RAGSystem
from prompts import *


class AssitenteVirtual:
    def __init__(self, openai_api_key: str, data_dir: str = "./data"):
        self.client = OpenAI(api_key=openai_api_key)
        self.rag_system = RAGSystem(openai_api_key)
        self.data_dir = data_dir
        
        # Carregar dados e criar índices
        self.rag_system.load_data(data_dir)
        self.rag_system.create_vector_stores()
        
        # Histórico de conversas (em produção, usar banco de dados)
        self.conversation_history = []
    
    def classify_intent(self, query: str) -> str:
        """Classifica a intenção do usuário"""
        query_lower = query.lower()
        
        # Padrões para identificar intenções
        # Priorizar consulta de pedido se houver um ID claro
        if re.search(r"#?\d+", query) and any(word in query_lower for word in ["pedido", "compra", "status", "entrega", "rastreamento", "onde está"]):
            return "consulta_pedido"
        
        # Busca de produto por ID ou nome exato
        if re.search(r"prod\d+", query_lower) or any(word in query_lower for word in ["qual o preço de", "informações sobre", "detalhes do"]):
            return "busca_produto_exata"

        if any(word in query_lower for word in ["trocar", "devolver", "política", "prazo", "garantia", "cancelar"]):
            return "politicas"
        
        if any(word in query_lower for word in ["recomendar", "sugerir", "indicar", "presente", "gift"]):
            return "recomendacao"
        
        if any(word in query_lower for word in ["buscar", "procurar", "quero", "preciso", "notebook", "smartphone", "celular", "computador", "tablet", "produto"]):
            return "busca_produto"
        
        if any(word in query_lower for word in ["oi", "olá", "bom dia", "boa tarde", "boa noite", "ajuda"]):
            return "conversa_geral"
        
        # Default: busca de produto genérica
        return "busca_produto"
    
    def extract_order_id(self, query: str) -> str:
        """Extrai ID do pedido da consulta"""
        # Procurar por padrões como #12345, pedido 12345, etc.
        patterns = [
            r"#(\d+)",
            r"pedido\s*(\d+)",
            r"número\s*(\d+)",
            r"(\d{4,})"  # Número com pelo menos 4 dígitos
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def process_query(self, query: str, user_id: str = "default") -> Dict[str, Any]:
        """Processa uma consulta do usuário"""
        intent = self.classify_intent(query)
        
        # Adicionar ao histórico
        self.conversation_history.append({
            "user_id": user_id,
            "query": query,
            "intent": intent
        })
        
        # Processar baseado na intenção
        if intent == "busca_produto":
            return self._handle_product_search(query)
        elif intent == "busca_produto_exata":
            return self._handle_exact_product_search(query)
        elif intent == "consulta_pedido":
            return self._handle_order_query(query)
        elif intent == "politicas":
            return self._handle_policy_query(query)
        elif intent == "recomendacao":
            return self._handle_recommendation(query)
        else:
            return self._handle_general_conversation(query)
    
    def _handle_product_search(self, query: str) -> Dict[str, Any]:
        """Processa busca de produtos"""
        # Extrair filtros da consulta
        max_price = self.rag_system.extract_price_from_query(query)
        category = self.rag_system.extract_category_from_query(query)
        
        # Buscar produtos
        products = self.rag_system.search_products(
            query, 
            max_price=max_price, 
            category=category
        )
        
        # Gerar resposta
        if products:
            products_text = "\n\n".join([
                f"**{p["nome"]}**\n"
                f"Categoria: {p["categoria"]}\n"
                f"Preço: R$ {p["preco"]:.2f}\n"
                f"Descrição: {p["descricao"]}\n"
                f"ID: {p["id"]}"
                for p in products
            ])
        else:
            products_text = "Nenhum produto encontrado com os critérios especificados."
        
        prompt = PRODUCT_SEARCH_PROMPT.format(
            query=query,
            products=products_text
        )
        
        response = self._generate_response(prompt)
        
        return {
            "intent": "busca_produto",
            "response": response,
            "products": products,
            "filters": {
                "max_price": max_price,
                "category": category
            }
        }

    def _handle_exact_product_search(self, query: str) -> Dict[str, Any]:
        """Processa busca exata de produtos por ID ou nome"""
        product_id_match = re.search(r"(prod\d+)", query, re.IGNORECASE)
        product_name_match = re.search(r"informações sobre (.+)|detalhes do (.+)|qual o preço de (.+)", query, re.IGNORECASE)

        product = None
        if product_id_match:
            product_id = product_id_match.group(1).upper()
            product = self.rag_system.find_product_by_id(product_id)
        elif product_name_match:
            product_name = next(g for g in product_name_match.groups() if g is not None)
            product = self.rag_system.find_product_by_name(product_name)

        if product:
            product_text = f"""
            **{product["nome"]}**\n
            Categoria: {product["categoria"]}\n
            Preço: R$ {product["preco"]:.2f}\n
            Descrição: {product["descricao"]}\n
            Especificações: {json.dumps(product.get("especificacoes", {}), ensure_ascii=False)}\n
            Disponível: {'Sim' if product.get('disponivel', True) else 'Não'}\n
            ID: {product["id"]}
            """
        else:
            product_text = "Produto não encontrado com o ID ou nome especificado."

        prompt = PRODUCT_SEARCH_PROMPT.format(
            query=query,
            products=product_text
        )

        response = self._generate_response(prompt)

        return {
            "intent": "busca_produto_exata",
            "response": response,
            "product": product
        }
    
    def _handle_order_query(self, query: str) -> Dict[str, Any]:
        """Processa consulta de pedidos"""
        order_id = self.extract_order_id(query)
        
        if order_id:
            order = self.rag_system.find_order(order_id)
            
            if order:
                order_text = f"""
                Pedido #{order["pedido_id"]}
                Status: {order["status"]}
                Data da compra: {order["data_compra"]}
                Previsão de entrega: {order["previsao_entrega"]}
                Produtos: {", ".join([p["nome"] for p in order["produtos"]])}
                """
            else:
                order_text = f"Pedido #{order_id} não encontrado."
        else:
            # Tentar buscar por status ou produto se não houver ID
            if "em trânsito" in query.lower() or "a caminho" in query.lower():
                orders = self.rag_system.search_orders_by_status("em trânsito")
                if orders:
                    order_text = "\n\n".join([
                        f"Pedido #{o["pedido_id"]}: Status: {o["status"]}" for o in orders
                    ])
                else:
                    order_text = "Nenhum pedido em trânsito encontrado."
            elif "entregue" in query.lower():
                orders = self.rag_system.search_orders_by_status("entregue")
                if orders:
                    order_text = "\n\n".join([
                        f"Pedido #{o["pedido_id"]}: Status: {o["status"]}" for o in orders
                    ])
                else:
                    order_text = "Nenhum pedido entregue encontrado."
            elif "cancelado" in query.lower():
                orders = self.rag_system.search_orders_by_status("cancelado")
                if orders:
                    order_text = "\n\n".join([
                        f"Pedido #{o["pedido_id"]}: Status: {o["status"]}" for o in orders
                    ])
                else:
                    order_text = "Nenhum pedido cancelado encontrado."
            elif "produto" in query.lower():
                product_name_match = re.search(r"produto (.+)", query, re.IGNORECASE)
                if product_name_match:
                    product_name = product_name_match.group(1)
                    orders = self.rag_system.search_orders_by_product(product_name)
                    if orders:
                        order_text = "\n\n".join([
                            f"Pedido #{o["pedido_id"]}: Status: {o["status"]}" for o in orders
                        ])
                    else:
                        order_text = f"Nenhum pedido encontrado com o produto {product_name}."
                else:
                    order_text = "ID do pedido não identificado e não foi possível buscar por status ou produto."
            else:
                order_text = "ID do pedido não identificado na consulta."
        
        prompt = ORDER_STATUS_PROMPT.format(
            query=query,
            order_info=order_text
        )
        
        response = self._generate_response(prompt)
        
        return {
            "intent": "consulta_pedido",
            "response": response,
            "order_id": order_id,
            "order": order if order_id else None
        }
    
    def _handle_policy_query(self, query: str) -> Dict[str, Any]:
        """Processa consultas sobre políticas"""
        policy_info = self.rag_system.search_policies(query)
        
        prompt = POLICY_PROMPT.format(
            query=query,
            policy_info=policy_info
        )
        
        response = self._generate_response(prompt)
        
        return {
            "intent": "politicas",
            "response": response,
            "policy_info": policy_info
        }
    
    def _handle_recommendation(self, query: str) -> Dict[str, Any]:
        """Processa pedidos de recomendação"""
        recommendations = self.rag_system.get_recommendations(query)
        
        if recommendations:
            rec_text = "\n\n".join([
                f"**{p["nome"]}**\n"
                f"Categoria: {p["categoria"]}\n"
                f"Preço: R$ {p["preco"]:.2f}\n"
                f"Descrição: {p["descricao"]}"
                for p in recommendations
            ])
        else:
            rec_text = "Não foi possível encontrar recomendações adequadas."
        
        prompt = RECOMMENDATION_PROMPT.format(
            query=query,
            recommendations=rec_text
        )
        
        response = self._generate_response(prompt)
        
        return {
            "intent": "recomendacao",
            "response": response,
            "recommendations": recommendations
        }
    
    def _handle_general_conversation(self, query: str) -> Dict[str, Any]:
        """Processa conversas gerais"""
        # Contexto das últimas interações
        recent_context = "\n".join([
            f"Usuário: {h["query"]}" 
            for h in self.conversation_history[-3:]
        ])
        
        prompt = GENERAL_CONVERSATION_PROMPT.format(
            query=query,
            context=recent_context
        )
        
        response = self._generate_response(prompt)
        
        return {
            "intent": "conversa_geral",
            "response": response,
            "context": recent_context
        }
    
    def _generate_response(self, prompt: str) -> str:
        """Gera resposta usando OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT.format(context="")},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        
        except openai.AuthenticationError:
            return "Desculpe, não foi possível conectar com o serviço de inteligência artificial. A chave da API OpenAI pode estar inválida ou ausente. Por favor, verifique a configuração."
        except Exception as e:
            return f"Desculpe, ocorreu um erro ao processar sua solicitação: {str(e)}"
    
    def get_conversation_history(self, user_id: str = "default") -> List[Dict]:
        """Retorna histórico de conversas do usuário"""
        return [h for h in self.conversation_history if h.get("user_id") == user_id]
    
    def clear_conversation_history(self, user_id: str = "default"):
        """Limpa histórico de conversas do usuário"""
        self.conversation_history = [
            h for h in self.conversation_history 
            if h.get("user_id") != user_id
        ]




