import lightning_pb2 as ln
import lightning_pb2_grpc as lnrpc
import grpc
import os
import codecs

# Due to updated ECDSA generated tls.cert we need to let gprc know that
# we need to use that cipher suite otherwise there will be a handshake
# error when we communicate with the lnd rpc server.
os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'

# Lnd cert is at ~/.lnd/tls.cert on Linux and
# ~/Library/Application Support/Lnd/tls.cert on Mac
cert = open(os.path.expanduser('~/.lnd/tls.cert'), 'rb').read()
creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('localhost:10009', creds)
stub = lnrpc.LightningStub(channel)

with open(os.path.expanduser('~/.lnd/data/chain/bitcoin/testnet/admin.macaroon'), 'rb') as f:
    macaroon_bytes = f.read()
    macaroon = codecs.encode(macaroon_bytes, 'hex')

def initiate_payment(amount, message):
    # lnd_client = LNDClient("127.0.0.1:10009", network='testnet', admin=True)
    
    payment_request = ln.Invoice(memo=message, value=amount)
    stub.AddInvoice(payment_request, metadata=[('macaroon', macaroon)])

    # "lets listen for the invoice"
    

    # Generate the payment request string
    # payment_request_str = lnd_client.get_payment_request(payment_hash)

    # return payment_request_str

# Example usage
payment_amount = 6969
message_to_attach = "This is a sample message."

# Initiate payment with attached message
payment_request_str = initiate_payment(payment_amount, message_to_attach)

# Display the attached message (SA1)
print("Attached message (SA1):", payment_request_str)

