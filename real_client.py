import lightning_pb2 as ln
import lightning_pb2_grpc as lnrpc
import grpc
import os
import codecs

# Due to updated ECDSA generated tls.cert we need to let gprc know that
# we need to use that cipher suite otherwise there will be a handshake
# error when we communicate with the lnd rpc server.
# lnd_client = LNDClient("127.0.0.1:10009", network='testnet', admin=True)

os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'

# Lnd cert is at ~/.lnd/tls.cert on Linux and
cert = open(os.path.expanduser('~/.lnd/tls.cert'), 'rb').read()
creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('localhost:10002', creds)
stub = lnrpc.LightningStub(channel)

with open(os.path.expanduser('~/.lnd/data/chain/bitcoin/testnet/admin.macaroon'), 'rb') as f:
    macaroon_bytes = f.read()
    macaroon = codecs.encode(macaroon_bytes, 'hex')

def initiate_payment(amount, message):
    print("Check LN Daemon logs...")
    print(f"Sending a payment of {amount} SAT...")
    payment_request = ln.Invoice(value=amount, memo=message)
    
    print("Get info...")
    stub.GetInfo(payment_request, metadata=[('macaroon', macaroon)])
    
    response = stub.WalletBalance(ln.WalletBalanceRequest(), metadata=[('macaroon', macaroon)])
    print(response.total_balance)
    
    print("Add invoice check in logs")
    stub.AddInvoice(payment_request, metadata=[('macaroon', macaroon)])
    
    print("Subscribe invoices check in logs")
    stub.SubscribeInvoices(payment_request, metadata=[('macaroon', macaroon)])
    
    
    
    
    return "thisisasamplemessage"

payment_request_str = initiate_payment(69, "this is a sample message")

print("Attached message (SA1):", payment_request_str)

