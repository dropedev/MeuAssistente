import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import {
  Send,
  Bot,
  User,
  ShoppingCart,
  Package,
  HelpCircle,
  Star,
  MessageCircle,
  Loader2
} from 'lucide-react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: 'Olá! Eu sou a CommercIA, sua assistente virtual para e-commerce. Como posso ajudá-lo hoje?',
      intent: 'conversa_geral',
      timestamp: new Date()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const getIntentIcon = (intent) => {
    switch (intent) {
      case 'busca_produto':
        return <ShoppingCart className="w-4 h-4" />
      case 'consulta_pedido':
        return <Package className="w-4 h-4" />
      case 'politicas':
        return <HelpCircle className="w-4 h-4" />
      case 'recomendacao':
        return <Star className="w-4 h-4" />
      default:
        return <MessageCircle className="w-4 h-4" />
    }
  }

  const getIntentLabel = (intent) => {
    switch (intent) {
      case 'busca_produto':
        return 'Busca de Produtos'
      case 'consulta_pedido':
        return 'Consulta de Pedido'
      case 'politicas':
        return 'Políticas da Loja'
      case 'recomendacao':
        return 'Recomendações'
      default:
        return 'Conversa Geral'
    }
  }

  const getIntentColor = (intent) => {
    switch (intent) {
      case 'busca_produto':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
      case 'consulta_pedido':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
      case 'politicas':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
      case 'recomendacao':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    }
  }

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      // Simular chamada para API (substitua pela URL real da sua API)
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          user_id: 'web_user'
        })
      })

      if (!response.ok) {
        throw new Error('Erro na comunicação com o servidor')
      }

      const data = await response.json()

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: data.response,
        intent: data.intent,
        data: data.data,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Desculpe, ocorreu um erro ao processar sua mensagem. Verifique se o servidor está rodando e tente novamente.',
        intent: 'error',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const renderProductCards = (products) => {
    if (!products || products.length === 0) return null

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        {products.slice(0, 4).map((product, index) => (
          <Card key={index} className="border border-gray-200 dark:border-gray-700">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">{product.nome}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground mb-2">{product.categoria}</p>
              <p className="text-lg font-bold text-green-600 dark:text-green-400">
                R$ {product.preco.toFixed(2)}
              </p>
              <p className="text-xs text-muted-foreground mt-2 line-clamp-2">
                {product.descricao}
              </p>
              <Badge variant="outline" className="mt-2">
                ID: {product.id}
              </Badge>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  const renderOrderInfo = (order) => {
    if (!order) return null

    return (
      <Card className="mt-4 border border-gray-200 dark:border-gray-700">
        <CardHeader>
          <CardTitle className="text-sm">Informações do Pedido</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm">
            <div><strong>Pedido:</strong> #{order.pedido_id}</div>
            <div><strong>Status:</strong> {order.status}</div>
            <div><strong>Data da Compra:</strong> {order.data_compra}</div>
            <div><strong>Previsão de Entrega:</strong> {order.previsao_entrega}</div>
            {order.produtos && (
              <div>
                <strong>Produtos:</strong>
                <ul className="list-disc list-inside ml-2">
                  {order.produtos.map((produto, index) => (
                    <li key={index}>{produto.nome}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    )
  }

  const quickActions = [
    { text: "Quero um notebook para programar, até R$ 3.000", icon: <ShoppingCart className="w-4 h-4" /> },
    { text: "Como faço para trocar um produto?", icon: <HelpCircle className="w-4 h-4" /> },
    { text: "Cadê meu pedido #12345?", icon: <Package className="w-4 h-4" /> },
    { text: "O que vocês recomendam para quem gosta de tecnologia?", icon: <Star className="w-4 h-4" /> }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Bot className="w-12 h-12 text-blue-600 dark:text-blue-400 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
              AssistentIA
            </h1>
          </div>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Seu assistente virtual para e-commerce
          </p>
        </div>

        {/* Chat Container */}
        <Card className="shadow-xl border-0 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm">
          <CardContent className="p-0">
            {/* Messages Area */}
            <ScrollArea className="h-96 p-6">
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg p-4 ${
                        message.type === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                      }`}
                    >
                      <div className="flex items-center mb-2">
                        {message.type === 'user' ? (
                          <User className="w-4 h-4 mr-2" />
                        ) : (
                          <Bot className="w-4 h-4 mr-2" />
                        )}
                        <span className="text-sm font-medium">
                          {message.type === 'user' ? 'Você' : 'AssistentIA'}
                        </span>
                        {message.intent && message.type === 'bot' && (
                          <Badge
                            variant="outline"
                            className={`ml-2 text-xs ${getIntentColor(message.intent)}`}
                          >
                            {getIntentIcon(message.intent)}
                            <span className="ml-1">{getIntentLabel(message.intent)}</span>
                          </Badge>
                        )}
                      </div>
                      <p className="whitespace-pre-wrap">{message.content}</p>
                      
                      {/* Render additional data based on intent */}
                      {message.data?.products && renderProductCards(message.data.products)}
                      {message.data?.order && renderOrderInfo(message.data.order)}
                      {message.data?.recommendations && renderProductCards(message.data.recommendations)}
                      
                      <div className="text-xs opacity-70 mt-2">
                        {message.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                ))}
                
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
                      <div className="flex items-center">
                        <Bot className="w-4 h-4 mr-2" />
                        <Loader2 className="w-4 h-4 animate-spin mr-2" />
                        <span className="text-sm">AssistentIA está digitando...</span>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>
            </ScrollArea>

            <Separator />

            {/* Quick Actions */}
            {messages.length === 1 && (
              <div className="p-4 bg-gray-50 dark:bg-gray-800">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  Experimente algumas dessas opções:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {quickActions.map((action, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      size="sm"
                      className="justify-start text-left h-auto p-3"
                      onClick={() => setInputValue(action.text)}
                    >
                      {action.icon}
                      <span className="ml-2 text-xs">{action.text}</span>
                    </Button>
                  ))}
                </div>
              </div>
            )}

            {/* Input Area */}
            <div className="p-4">
              <div className="flex space-x-2">
                <Input
                  ref={inputRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Digite sua mensagem..."
                  disabled={isLoading}
                  className="flex-1"
                />
                <Button 
                  onClick={sendMessage} 
                  disabled={!inputValue.trim() || isLoading}
                  size="icon"
                >
                  {isLoading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Send className="w-4 h-4" />
                  )}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center mt-8 text-sm text-gray-500 dark:text-gray-400">
          <p>
            AssistentIA - Desenvolvido com React, FastAPI e OpenAI
          </p>
          <p>
            Créditos: Pedro Favoretti - Drope Dev
          </p>
        </div>
      </div>
    </div>
  )
}

export default App

