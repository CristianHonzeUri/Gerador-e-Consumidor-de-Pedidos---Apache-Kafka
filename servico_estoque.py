import json
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable
import time

def create_consumer(topic, group_id):
 while True:
        try:
            print(f"[ESTOQUE] Tentando se conectar ao Kafka (Tópico: {topic})...")
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                group_id=group_id,
                auto_offset_reset='earliest'
            )
            print("[ESTOQUE] Conectado ao Kafka!")
            return consumer
        except NoBrokersAvailable:
            print("[ESTOQUE] Kafka não disponível. Tentando novamente em 5 segundos...")
            time.sleep(5)

def create_producer():
   while True:
        try:
            print("[ESTOQUE] Tentando se conectar ao Kafka (Produtor)...")
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("[ESTOQUE] Conectado ao Kafka (Produtor)!")
            return producer
        except NoBrokersAvailable:
            print("[ESTOQUE] Kafka não disponível. Tentando novamente em 5 segundos...")
            time.sleep(5)

# --- Lógica Principal ---
consumer = create_consumer('novos_pedidos', 'grupo_estoque')
producer = create_producer()

print("[ESTOQUE] Serviço de Estoque iniciado. Aguardando pedidos...")

for message in consumer:
    pedido = message.value
    pedido_id = pedido.get('id', 'desconhecido')
    print(f"\n[ESTOQUE] Recebi pedido: {pedido_id}")
    
    # Simula processamento lento do estoque
    print(f"[ESTOQUE] Processando estoque para pedido: {pedido_id}...")
    time.sleep(2) # Simulação de 2 segundos
    
    # Pedido aprovado no estoque
    print(f"[ESTOQUE] Pedido {pedido_id} APROVADO no estoque.")
    producer.send('pedidos_aprovados', pedido)
    producer.flush()