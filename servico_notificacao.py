import json
from kafka import KafkaConsumer

# Configurações do Consumidor
consumer = KafkaConsumer(
    'pedidos_concluidos',
    bootstrap_servers='localhost:29092',
    group_id='grupo_notificacao',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("[NOTIFICACAO] Serviço de Notificação iniciado. Aguardando pedidos concluídos...")

for message in consumer:
    pedido = message.value
    print(f"\n[NOTIFICACAO] ----------------------------------------------------")
    print(f"[NOTIFICACAO] Pedido {pedido['id_pedido']} CONCLUÍDO E PAGO.")
    print(f"[NOTIFICACAO] Enviando e-mail de confirmação para: {pedido['cliente']}")
    print(f"[NOTIFICACAO] ----------------------------------------------------")