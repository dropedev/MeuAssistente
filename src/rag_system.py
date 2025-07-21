"""
Sistema RAG (Retrieval Augmented Generation) para o assistente virtual
Desenvolvido por Pedro Favoretti - Drope Dev
"""

import os
import json
import faiss
import numpy as np
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document


class RAGSystem:
    def __init__(self, openai_api_key: str):
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vector_stores = {}
        self.products_data = []
        self.orders_data = []
        self.policies_data = ""
        
    def load_data(self, data_dir: str):
        """Carrega todos os dados necessários"""
        # Carregar produtos
        products_file = os.path.join(data_dir, "produtos.json")
        if os.path.exists(products_file):
            with open(products_file, 'r', encoding='utf-8') as f:
                self.products_data = json.load(f)
        
        # Carregar pedidos
        orders_file = os.path.join(data_dir, "pedidos.json")
        if os.path.exists(orders_file):
            with open(orders_file, 'r', encoding='utf-8') as f:
                self.orders_data = json.load(f)
        
        # Carregar políticas
        policies_file = os.path.join(data_dir, "politicas.md")
        if os.path.exists(policies_file):
            with open(policies_file, 'r', encoding='utf-8') as f:
                self.policies_data = f.read()
    
    def create_vector_stores(self):
        """Cria os índices vetoriais para busca semântica"""
        
        # Criar índice para produtos
        if self.products_data:
            product_docs = []
            for product in self.products_data:
                content = f"""
                Nome: {product['nome']}
                Categoria: {product['categoria']}
                Preço: R$ {product['preco']}
                Descrição: {product['descricao']}
                Especificações: {json.dumps(product.get('especificacoes', {}), ensure_ascii=False)}
                Disponível: {'Sim' if product.get('disponivel', True) else 'Não'}
                """
                doc = Document(
                    page_content=content,
                    metadata={
                        "id": product['id'],
                        "tipo": "produto",
                        "categoria": product['categoria'],
                        "preco": product['preco']
                    }
                )
                product_docs.append(doc)
            
            self.vector_stores['produtos'] = FAISS.from_documents(
                product_docs, self.embeddings
            )
        
        # Criar índice para políticas
        if self.policies_data:
            policy_chunks = self.text_splitter.split_text(self.policies_data)
            policy_docs = [
                Document(
                    page_content=chunk,
                    metadata={"tipo": "politica"}
                ) for chunk in policy_chunks
            ]
            
            self.vector_stores['politicas'] = FAISS.from_documents(
                policy_docs, self.embeddings
            )
    
    def search_products(self, query: str, max_price: float = None, category: str = None, k: int = 5) -> List[Dict]:
        """Busca produtos usando similaridade semântica"""
        if 'produtos' not in self.vector_stores:
            return []
        
        # Busca semântica
        docs = self.vector_stores['produtos'].similarity_search(query, k=k*2)
        
        # Filtrar resultados
        results = []
        for doc in docs:
            product_id = doc.metadata['id']
            product = next((p for p in self.products_data if p['id'] == product_id), None)
            
            if product:
                # Aplicar filtros
                if max_price and product['preco'] > max_price:
                    continue
                if category and product['categoria'].lower() != category.lower():
                    continue
                if not product.get('disponivel', True):
                    continue
                
                results.append(product)
                
                if len(results) >= k:
                    break
        
        return results
    
    def search_policies(self, query: str, k: int = 3) -> str:
        """Busca informações sobre políticas da loja"""
        if 'politicas' not in self.vector_stores:
            return "Informações sobre políticas não disponíveis."
        
        docs = self.vector_stores['politicas'].similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in docs])
    
    def find_order(self, order_id: str) -> Dict:
        """Encontra um pedido pelo ID"""
        for order in self.orders_data:
            if order.get('pedido_id') == order_id:
                return order
        return None
    
    def get_recommendations(self, query: str, k: int = 5) -> List[Dict]:
        """Gera recomendações baseadas na consulta"""
        # Para recomendações, usamos busca semântica mais ampla
        if 'produtos' not in self.vector_stores:
            return []
        
        docs = self.vector_stores['produtos'].similarity_search(query, k=k)
        
        recommendations = []
        for doc in docs:
            product_id = doc.metadata['id']
            product = next((p for p in self.products_data if p['id'] == product_id), None)
            
            if product and product.get('disponivel', True):
                recommendations.append(product)
        
        return recommendations
    
    def extract_price_from_query(self, query: str) -> float:
        """Extrai valor máximo de preço da consulta"""
        import re
        
        # Procurar por padrões como "até R$ 1000", "máximo 500", etc.
        patterns = [
            r'até\s*R?\$?\s*(\d+(?:\.\d{3})*(?:,\d{2})?)',
            r'máximo\s*R?\$?\s*(\d+(?:\.\d{3})*(?:,\d{2})?)',
            r'no\s*máximo\s*R?\$?\s*(\d+(?:\.\d{3})*(?:,\d{2})?)',
            r'R?\$?\s*(\d+(?:\.\d{3})*(?:,\d{2})?)?\s*reais?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                price_str = match.group(1)
                # Converter para float (remover pontos de milhares e trocar vírgula por ponto)
                price_str = price_str.replace('.', '').replace(',', '.')
                try:
                    return float(price_str)
                except ValueError:
                    continue
        
        return None
    
    def extract_category_from_query(self, query: str) -> str:
        """Extrai categoria da consulta"""
        categories = {
            'eletrônicos': ['notebook', 'smartphone', 'celular', 'computador', 'tablet'],
            'roupas': ['camisa', 'calça', 'vestido', 'roupa', 'blusa'],
            'casa': ['móvel', 'decoração', 'cozinha', 'quarto', 'sala'],
            'esportes': ['tênis', 'bicicleta', 'academia', 'corrida', 'futebol']
        }
        
        query_lower = query.lower()
        for category, keywords in categories.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        
        return None

    def find_product_by_id(self, product_id: str) -> Dict:
        """Encontra um produto pelo ID exato"""
        for product in self.products_data:
            if product.get('id') == product_id:
                return product
        return None

    def find_product_by_name(self, product_name: str) -> Dict:
        """Encontra um produto pelo nome (busca parcial)"""
        product_name_lower = product_name.lower().strip()
        
        # Primeiro, busca exata
        for product in self.products_data:
            if product.get('nome', '').lower() == product_name_lower:
                return product
        
        # Depois, busca parcial
        for product in self.products_data:
            if product_name_lower in product.get('nome', '').lower():
                return product
        
        return None

    def search_orders_by_status(self, status: str) -> List[Dict]:
        """Busca pedidos por status"""
        status_lower = status.lower()
        matching_orders = []
        
        for order in self.orders_data:
            if status_lower in order.get('status', '').lower():
                matching_orders.append(order)
        
        return matching_orders

    def search_orders_by_product(self, product_name: str) -> List[Dict]:
        """Busca pedidos que contêm um produto específico"""
        product_name_lower = product_name.lower()
        matching_orders = []
        
        for order in self.orders_data:
            for product in order.get('produtos', []):
                if product_name_lower in product.get('nome', '').lower():
                    matching_orders.append(order)
                    break
        
        return matching_orders



