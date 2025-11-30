# 🔄 Sistema RPC - Remote Procedure Call

> Sistema distribuído desenvolvido em Python para execução remota de operações matemáticas com cache inteligente e integração de notícias.

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Socket](https://img.shields.io/badge/Socket-TCP/IP-green?style=for-the-badge&logo=socketdotio)](https://docs.python.org/3/library/socket.html)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-4.x-orange?style=for-the-badge)](https://www.crummy.com/software/BeautifulSoup/)

---

## 📋 Sobre o Projeto

**Sistema RPC** é uma implementação de Remote Procedure Call que permite executar operações matemáticas complexas em um servidor remoto, com recursos de:

- 🧮 **Operações Matemáticas**: Soma, subtração, multiplicação, divisão, fatorial e verificação de primos
- 💾 **Cache Multinível**: Cache em memória (cliente) e cache em disco (servidor)
- 🔄 **Processamento Paralelo**: Uso de multiprocessing para operações pesadas
- 📰 **Web Scraping**: Integração com notícias do UOL
- ⚡ **Alta Performance**: Gerenciamento inteligente de cache com limite de tamanho
- 🛡️ **Fallback**: Sistema funciona mesmo com servidor offline usando cache

> **Disciplina**: Sistemas Distribuídos  
> **Curso**: Sistemas para Internet  
> **Tipo**: Trabalho Individual - Atividades Semanais

---

## 🚀 Tecnologias

### Core
- **Python 3.8+** - Linguagem principal
- **Socket TCP/IP** - Comunicação cliente-servidor
- **Multiprocessing** - Processamento paralelo

### Bibliotecas
- **BeautifulSoup4** - Web scraping de notícias
- **Requests** - Requisições HTTP
- **JSON** - Serialização de dados e cache

---

## 📦 Pré-requisitos

- [Python 3.8+](https://www.python.org/downloads/)
- pip (gerenciador de pacotes Python)

### Instalação das Dependências

```bash
pip install requests beautifulsoup4
```

---

## 📁 Estrutura do Projeto

```
projeto/
├── client/                    # Lógica do Cliente (Interface RPC)
│   ├── operations.py          # Classe de operações com decorators
│   ├── tcp_client.py          # Cliente TCP com cache em memória
│   ├── rpc_exception.py       # Exceções customizadas
│   └── teste_operacoes.py     # Script de testes
├── server/                    # Lógica do Servidor (Processamento)
│   ├── tcp_server.py          # Servidor TCP principal
│   ├── math_operations.py     # Implementação das operações
│   └── cache_operations.json  # Cache persistente (gerado automaticamente)
├── common/                    # Recursos compartilhados
│   └── enums.py              # Enumerações (comandos)
├── config/                    # Configurações
│   ├── config.py             # Carregador de configurações
│   └── configuracoes.txt     # Arquivo de configuração JSON
└── README.md
```

---

## ⚙️ Configuração

O arquivo `config/configuracoes.txt` contém as configurações do sistema:

```json
{
    "ip": "localhost",
    "port": 7767,
    "max_cache_size": 10000,
    "cache_expiration": 1
}
```

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `ip` | string | Endereço IP do servidor |
| `port` | int | Porta TCP para comunicação |
| `max_cache_size` | int | Tamanho máximo do cache em bytes |
| `cache_expiration` | int | Tempo de expiração do cache em minutos |

---

## 🎯 Funcionalidades Principais

### 1. Sistema de Cache Multinível

#### Cache em Memória (Cliente)
```python
# Armazena respostas recentes com timestamp
operations_cache = {
    'sum 5 2': {
        'response': 7.0,
        'timestamp': '2025-11-30T10:30:00'
    }
}
```

#### Cache em Disco (Servidor)
```python
# Persiste operações com gerenciamento de tamanho
def enforce_cache_limit(cache, file, max_size, new_key, new_value):
    # Remove entradas antigas se necessário (FIFO)
    # Valida tamanho antes de adicionar
    # Retorna True se adicionado com sucesso
```

### 2. Operações Matemáticas

#### Operações Básicas
```python
op = Operations()

# Soma de múltiplos números
result = op.sum(5, 2, 3, 1)  # 11.0

# Subtração sequencial
result = op.sub(10, 2, 3)    # 5.0

# Produto
result = op.prod(2, 3, 4)    # 24.0

# Divisão
result = op.div(100, 2, 5)   # 10.0
```

#### Fatorial
```python
# Calcula fatorial de n
result = op.fat(5)  # 120
```

#### Verificação de Primos (Multiprocessing)
```python
# Verifica múltiplos números em paralelo
numbers = [2, 3, 4, 5, 17, 20]
results = op.prim(*numbers)
# [True, True, False, True, True, False]
```

**Implementação Paralela:**
```python
def check_primes(number):
    # Usa Pool de 4 processos
    with multiprocessing.Pool(processes=4) as pool:
        result = pool.map(_is_prime, numbers_list)
    return result
```

### 3. Web Scraping de Notícias

```python
# Busca as 5 principais manchetes do UOL
news = op.news()

# Exemplo de saída:
# [
#   "Governo anuncia novo pacote econômico",
#   "Brasil vence competição internacional",
#   ...
# ]
```

**Implementação:**
```python
def get_news():
    response = requests.get('https://www.uol.com.br')
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = [h3.get_text(strip=True) for h3 in soup.find_all('h3')]
    return headlines[:5]
```

---

## 💻 Como Usar

### 1️⃣ Iniciar o Servidor

```bash
cd server
python tcp_server.py
```

O servidor ficará aguardando conexões na porta configurada (padrão: 7767).

### 2️⃣ Executar o Cliente

```bash
cd client
python teste_operacoes.py
```

### 3️⃣ Usar a API em Seu Código

```python
from client.operations import Operations

# Inicializa cliente
op = Operations()

# Operações básicas
print(op.sum(10, 20, 30))        # 60.0
print(op.prod(5, 4))             # 20.0
print(op.fat(10))                # 3628800

# Verificar primos (sem cache)
numeros = list(range(100))
primos = op.prim(*numeros)
print(sum(primos))  # Quantidade de primos até 100

# Buscar notícias
noticias = op.news()
for i, noticia in enumerate(noticias, 1):
    print(f"{i}. {noticia}")
```

---

## 🏗️ Arquitetura do Sistema

### Padrão RPC com Cache

```
┌──────────────────┐                    ┌──────────────────┐
│     Cliente      │                    │     Servidor     │
│                  │                    │                  │
│ ┌──────────────┐ │    TCP/IP          │ ┌──────────────┐ │
│ │  operations  │ │ ── Socket ──────>  │ │ tcp_server   │ │
│ │  (Interface) │ │                    │ │ (Dispatcher) │ │
│ └──────────────┘ │                    │ └──────────────┘ │
│        ↓         │                    │        ↓         │
│ ┌──────────────┐ │                    │ ┌──────────────┐ │
│ │  tcp_client  │ │                    │ │ math_ops     │ │
│ │ (Transport)  │ │                    │ │ (Business)   │ │
│ └──────────────┘ │                    │ └──────────────┘ │
│        ↓         │                    │        ↓         │
│ ┌──────────────┐ │                    │ ┌──────────────┐ │
│ │ Cache Memória│ │                    │ │ Cache Disco  │ │
│ │  (Temporário)│ │                    │ │ (Persistente)│ │
│ └──────────────┘ │                    │ └──────────────┘ │
└──────────────────┘                    └──────────────────┘
```

---

## 🔒 Recursos de Segurança e Confiabilidade

### 1. Tratamento de Erros
- ✅ Validação de divisão por zero
- ✅ Validação de fatorial para números negativos
- ✅ Try-catch em operações de I/O
- ✅ Verificação de disponibilidade do servidor

### 2. Gerenciamento de Cache
- ✅ Limite de tamanho configurável
- ✅ Política FIFO para remoção
- ✅ Expiração por tempo (cliente)
- ✅ Fallback para cache em disco se servidor offline

### 3. Performance
- ✅ Processamento paralelo para verificação de primos (4 processos)
- ✅ Suporte a números grandes (até 1.000.000 dígitos)
- ✅ Reutilização de conexões socket

---

## 🤝 Contribuindo

Este é um projeto acadêmico, mas sugestões são bem-vindas:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é um trabalho acadêmico desenvolvido para a disciplina de **Sistemas Distribuídos** do curso de **Sistemas para Internet**.

---

## 👨‍💻 Autor

**[Hugo Vinícius Rodrigues Pereira]**

[![GitHub](https://img.shields.io/badge/GitHub-seu--usuario-black?style=flat-square&logo=github)](https://github.com/hugovrp)

---

## 📞 Suporte

Encontrou um bug ou tem uma sugestão? [Abra uma issue](https://github.com/hugovrp/TSI-RPC_RemoteProcedureCall/issues)