import json
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import time

def create_consumer(topic, group_id):
     while True:
        try:
            print(f"[NOTIFICACAO] Tentando se conectar ao Kafka (Tópico: {topic})...")
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                group_id=group_id,
                auto_offset_reset='earliest'
            )
            print("[NOTIFICACAO] Conectado ao Kafka!")
            return consumer
        except NoBrokersAvailable:
            print("[NOTIFICACAO] Kafka não disponível. Tentando novamente em 5 segundos...")
            time.sleep(5)

consumer = create_consumer('pedidos_pagos', 'grupo_notificacao')

print("[NOTIFICACAO] Serviço de Notificação iniciado. Aguardando pedidos concluídos...")

for message in consumer:
    pedido = message.value
    pedido_id = pedido.get('id', 'desconhecido')
    cliente = pedido.get('cliente', 'cliente')
    
    print("\n[NOTIFICACAO] ----------------------------------------------------")
    print(f"[NOTIFICACAO] Pedido {pedido_id} CONCLUÍDO.")
    print(f"[NOTIFICACAO] Enviando E-mail/SMS para: {cliente}...")
    print(f"[NOTIFICACAO] E-mail: 'Olá, {cliente}. Seu pedido {pedido_id} foi pago e está sendo preparado para envio.'")
    print("[NOTIFICACAO] ----------------------------------------------------")