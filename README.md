# LabDoor
Sistema que contém o servidor e código base da porta automática usando tecnologia RFiD

## Tecnologias utilizadas

- Node.js (como servidor broker MQTT)
- Micro Python

### Pré-requisitos

Antes de começar a utilizar o projeto você necessita ter instalado em sua máquina as seguintes ferramentas:

- Git, Python, Node.js, Yarn

### Rodando o broker MQTT

```bash
# Clone este repositório
$ git clone https://github.com/Natalnet/Lar-Door.git

# Acesse a pasta do broker no terminal/cmd
$ cd server

# Instale as dependências necessárias
$ yarn

# Coloque o IP da sua máquina local para hospedar o MQTT em myIp no server.ts

# Execute um primeiro terminal para executar o servidor
$ yarn dev:broker

# Execute um segundo terminal para verificar as mensagens enviadas pela porta
$ yarn dev:subscriber

```

#### Créditos

- Código base do broker MQTT em Node JS: (https://github.com/pedroksty)

- Código base da tecnologia RFiD em Micro Python: (https://github.com/Jmathbr/)
