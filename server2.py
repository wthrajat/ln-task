from lndgrpc import LNDClient

def initiate_payment():
    lnd_client = LNDClient("127.0.0.1:10009", network='testnet', admin=True)
    
    subscribe_rajat = lnd_client.subscribe_invoices()
    for invoice in subscribe_rajat:
        print("hahahahahhahahahah")
        print(invoice)

initiate_payment()