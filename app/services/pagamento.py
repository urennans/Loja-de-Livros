import requests
import uuid

MERCADO_PAGO_TOKEN = "APP_USR-593253950239496-071215-8e178141c9ad72d043e3237e29c4cdfd-295454225"  # Troque pelo seu token real

def gerar_pix(valor: float, descricao: str, email: str):
    valor_formatado = round(valor, 2) 
    url = "https://api.mercadopago.com/v1/payments"
    payload = {
        "transaction_amount": valor_formatado,
        "description": descricao,
        "payment_method_id": "pix",
        "payer": {
            "email": email
        }
    }
    headers = {
        "Authorization": f"Bearer {MERCADO_PAGO_TOKEN}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": str(uuid.uuid4())  # Gera chave única para cada requisição
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
    
def verificar_status(payment_id: str):
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {
        "Authorization": f"Bearer {MERCADO_PAGO_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()
