# Lab Kafka na Prática: Construindo um Sistema de Pedidos à Prova de Falhas

Bem-vindo! Este é o repositório do laboratório prático sobre Sistemas Distribuídos usando Apache Kafka.

**Objetivo:** Demonstrar visualmente como o Kafka permite construir sistemas robustos, cobrindo na prática os conceitos de:
* Comunicação Assíncrona
* Desacoplamento de Serviços
* Tolerância a Falhas
* Escalabilidade Horizontal

## A Nossa Arquitetura

Vamos simular um fluxo de E-commerce. O fluxo é dividido em 4 serviços independentes que só se comunicam via Kafka:

**`Produtor`** -> `[Tópico: novos_pedidos]` -> **`Serviço Estoque`** -> `[Tópico: pedidos_aprovados]` -> **`Serviço Pagamento`** -> `[Tópico: pedidos_concluidos]` -> **`Serviço Notificação`**

---

## Parte 1: Preparando o Ambiente (10 min)

**Pré-requisitos:**
* [Git](https://git-scm.com/downloads)
* [Docker](https://www.docker.com/products/docker-desktop/)
* [Python 3.x](https://www.python.org/downloads/)

**Passo 1: Clonar o Projeto**
```bash
git clone [URL_DO_SEU_REPOSITORIO]
cd lab-kafka
```

**Passo 2: Instalar Dependências (Python)**
```bash
pip install -r requirements.txt
```

**Passo 3: Iniciar o Kafka (com Docker)**
Este comando irá baixar as imagens do Kafka e Zookeeper e iniciá-las em background.
```bash
docker-compose up -d
```
*Para verificar se tudo subiu corretamente, rode `docker ps`.*

---

## Parte 2: O Caminho Feliz (20 min)

Vamos ver o sistema funcionando perfeitamente. Você precisará de **4 terminais**.

**Terminal 1: Serviço de Notificação** (O fim da linha)
```bash
python servico_notificacao.py
```

**Terminal 2: Serviço de Pagamento** (O penúltimo)
```bash
python servico_pagamento.py
```

**Terminal 3: Serviço de Estoque** (O primeiro consumidor)
```bash
python servico_estoque.py
```

**Terminal 4: Produtor de Pedidos**
Agora, vamos enviar 10 pedidos para a fila:
```bash
python produtor_pedidos.py
```

**O que observar:**
Veja as mensagens "pulando" de terminal em terminal!
1.  O **Produtor** envia 10 pedidos (e termina).
2.  O **Estoque** (T3) recebe um por um, "trabalha" por 2 segundos e aprova.
3.  O **Pagamento** (T2) recebe as aprovações, "trabalha" por 1 segundo e paga.
4.  A **Notificação** (T1) imprime a mensagem final.

**Conceitos Vistos:**
* **Assincronia:** O Produtor disparou 10 pedidos e encerrou em segundos, ele não esperou o estoque ou o pagamento.
* **Desacoplamento:** O Produtor não tem ideia de quem vai consumir a mensagem. O Estoque não sabe quem é o Pagamento. Eles só conhecem o Kafka.

---

## Parte 3: Teste de Fogo 1 (Tolerância a Falhas)

Vamos simular uma falha crítica no meio do processo.

**Passo 1: "Matar" o Serviço de Pagamento**
* Vá ao **Terminal 2 (Pagamento)**.
* Pressione `Ctrl + C` para parar o serviço.

**Passo 2: Enviar novos pedidos**
* Vá ao **Terminal 4 (Produtor)**.
* Rode novamente o produtor para enviar mais 10 pedidos:
    ```bash
    python produtor_pedidos.py
    ```

**O que observar:**
* O Produtor (T4) funciona.
* O Estoque (T3) funciona e processa os 10 novos pedidos, enviando-os para o tópico `pedidos_aprovados`.
* O Pagamento (T2) está **morto**.
* A Notificação (T1) não recebe **nada**.
* **As mensagens NÃO foram perdidas!** Elas estão na fila do Kafka, esperando no tópico `pedidos_aprovados`.

**Passo 3: "Restaurar" o Serviço**
* No **Terminal 2**, reinicie o serviço de pagamento:
    ```bash
    python servico_pagamento.py
    ```

**Resultado Imediato:**
O Serviço de Pagamento vai "engolir" a fila de 10 pedidos pendentes de uma só vez, processá-los, e enviá-los para a Notificação.

**Conceito Visto:**
* **Tolerância a Falhas:** O Kafka atuou como um *buffer*. O sistema continuou aceitando pedidos (Estoque) mesmo com um componente vital (Pagamento) offline. Nenhuma informação foi perdida.

---

## Parte 4: Teste de Fogo 2 (Escalabilidade Horizontal)

O `Serviço de Estoque` (T3) é nosso gargalo (demora 2s por pedido). Vamos escalar horizontalmente para dobrar a capacidade.

**Passo 1: Abrir um 5º Terminal**
* Abra um terminal totalmente novo.

**Passo 2: Iniciar uma *segunda instância* do Estoque**
* Neste novo **Terminal 5**, rode o *mesmo* script do Terminal 3:
    ```bash
    python servico_estoque.py
    ```
* **Importante:** Note que ele se registra no mesmo `group_id='grupo_estoque'`. O Kafka agora sabe que tem 2 "funcionários" para esta tarefa.

**Passo 3: Enviar mais pedidos**
* Vá ao **Terminal 4 (Produtor)** e envie mais 10 pedidos:
    ```bash
    python produtor_pedidos.py
    ```

**O que observar:**
* Olhe para o **Terminal 3** e o **Terminal 5** ao mesmo tempo.
* Os logs `[ESTOQUE] Recebi pedido...` aparecerão **intercalados** entre os dois terminais!
* Ex: T3 pode pegar os pedidos 1, 3, 5, 7, 9...
* Ex: T5 pode pegar os pedidos 2, 4, 6, 8, 10...

**Conceito Visto:**
* **Escalabilidade Horizontal:** O Kafka automaticamente rebalanceou a carga do tópico `novos_pedidos` (que tem 3 partições) entre os consumidores disponíveis do mesmo grupo. Dobramos a capacidade de processamento sem parar o sistema.