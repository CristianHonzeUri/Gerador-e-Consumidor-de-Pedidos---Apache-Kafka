import time
import json
from kafka import KafkaConsumer, KafkaProducer

# Configurações do Consumidor
consumer = KafkaConsumer(
    'novos_pedidos',
    bootstrap_servers='localhost:29092',
    group_id='grupo_estoque', # Chave para a escalabilidade
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Configurações do Produtor (para enviar ao próximo tópico)
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("[ESTOQUE] Serviço de Estoque iniciado. Aguardando pedidos...")

for message in consumer:
    pedido = message.value
    print(f"\n[ESTOQUE] Recebi pedido: {pedido['id_pedido']}")
    
    # Simula o gargalo: verificação de estoque
    print("[ESTOQUE] Verificando estoque...")
    time.sleep(2) # Simulação de trabalho lento
    
    print(f"[ESTOQUE] Pedido {pedido['id_pedido']} APROVADO.")
    
    # Envia para o próximo estágio
    producer.send('pedidos_aprovados', pedido)
    producer.flush()