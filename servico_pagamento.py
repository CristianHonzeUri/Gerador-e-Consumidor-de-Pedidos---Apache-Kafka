import time
import json
from kafka import KafkaConsumer, KafkaProducer

# Configurações do Consumidor
consumer = KafkaConsumer(
    'pedidos_aprovados',
    bootstrap_servers='localhost:29092',
    group_id='grupo_pagamento', # Grupo diferente
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Configurações do Produtor
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("[PAGAMENTO] Serviço de Pagamento iniciado. Aguardando aprovações...")

for message in consumer:
    pedido = message.value
    print(f"\n[PAGAMENTO] Recebi pedido aprovado: {pedido['id_pedido']}")
    
    # Simula processamento de pagamento
    print("[PAGAMENTO] Processando cartão de crédito...")
    time.sleep(1) # Simulação de trabalho
    
    print(f"[PAGAMENTO] Pedido {pedido['id_pedido']} PAGO.")
    
    # Envia para o estágio final
    producer.send('pedidos_concluidos', pedido)
    producer.flush()