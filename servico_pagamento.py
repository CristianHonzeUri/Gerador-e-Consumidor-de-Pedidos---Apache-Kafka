import json
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable
import time

def create_consumer(topic, group_id):
    while True:
        try:
            print(f"[PAGAMENTO] Tentando se conectar ao Kafka (Tópico: {topic})...")
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                group_id=group_id,
                auto_offset_reset='earliest'
            )
            print("[PAGAMENTO] Conectado ao Kafka!")
            return consumer
        except NoBrokersAvailable:
            print("[PAGAMENTO] Kafka não disponível. Tentando novamente em 5 segundos...")
            time.sleep(5)

def create_producer():
    while True:
        try:
            print("[PAGAMENTO] Tentando se conectar ao Kafka (Produtor)...")
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("[PAGAMENTO] Conectado ao Kafka (Produtor)!")
            return producer
        except NoBrokersAvailable:
            print("[PAGAMENTO] Kafka não disponível. Tentando novamente em 5 segundos...")
            time.sleep(5)

# --- Lógica Principal ---
consumer = create_consumer('pedidos_aprovados', 'grupo_pagamento')
producer = create_producer()

print("[PAGAMENTO] Serviço de Pagamento iniciado. Aguardando aprovações...")

for message in consumer:
    pedido = message.value
    pedido_id = pedido.get('id', 'desconhecido')
    print(f"\n[PAGAMENTO] Recebi pedido aprovado: {pedido_id}")
    
    # Simula processamento de pagamento
    print(f"[PAGAMENTO] Processando pagamento para pedido: {pedido_id}...")
    time.sleep(1) # Simulação de 1 segundo
    
    # Pagamento concluído
    print(f"[PAGAMENTO] Pedido {pedido_id} PAGO com sucesso.")
    producer.send('pedidos_pagos', pedido)
    producer.flush()