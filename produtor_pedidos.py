import time
import json
import uuid
from kafka import KafkaProducer

# Configurações do Produtor
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Iniciando Produtor de Pedidos... (Enviando 10 pedidos)")

for i in range(1, 11):
    pedido_id = str(uuid.uuid4())
    cliente_id = f"cliente_{i % 3}" # Simula 3 clientes diferentes

    pedido = {
        'id_pedido': pedido_id,
        'cliente': cliente_id,
        'produto': f'Produto-{i}',
        'quantidade': 1
    }

    # Envia para o tópico 'novos_pedidos'
    producer.send('novos_pedidos', pedido)
    
    print(f"[PRODUTOR] Pedido enviado: {pedido_id} (Cliente: {cliente_id})")
    time.sleep(1) # Aguarda 1 seg para podermos ver o fluxo

producer.flush()
print("Produtor concluiu o envio.")