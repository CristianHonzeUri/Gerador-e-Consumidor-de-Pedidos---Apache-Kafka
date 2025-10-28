import json
import uuid
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import time
import os 

def create_producer():
    while True:
        try:
            print("[PRODUTOR] Tentando se conectar ao Kafka (Produtor)...")
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("[PRODUTOR] Conectado ao Kafka (Produtor)!")
            return producer
        except NoBrokersAvailable:
            print("[PRODUTOR] Kafka não disponível. Tentando novamente em 5 segundos...")
            time.sleep(5)

producer = create_producer()
clientes = ['cliente_0', 'cliente_1', 'cliente_2']
NUM_PEDIDOS = int(os.environ.get('NUM_PEDIDOS', 10))

print(f"Iniciando Produtor de Pedidos... (Enviando {NUM_PEDIDOS} pedidos)")
time.sleep(2)

for i in range(NUM_PEDIDOS):
    pedido = {
        'id': str(uuid.uuid4()),
        'cliente': clientes[i % len(clientes)],
        'produto': f'produto_{i % 5}',
        'quantidade': (i % 3) + 1
    }
    
    print(f"[PRODUTOR] Pedido enviado: {pedido['id']} (Cliente: {pedido['cliente']})")
    producer.send('novos_pedidos', pedido)
    time.sleep(0.1) # Um pequeno delay entre os envios

producer.flush()
print("Produtor concluiu o envio.")