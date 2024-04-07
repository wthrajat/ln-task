from lndgrpc import LNDClient
import hashlib

def process_payment(payment_request_str):
    # Connect to your Lightning Network node
    lnd_client = LNDClient("127.0.0.1:10009", network='testnet', admin=True)

    # Decode the payment request string to get payment hash and amount
    payment_request = lnd_client.decode_payment_request(payment_request_str)
    payment_hash = payment_request.payment_hash
    amount = payment_request.num_satoshis

    # Check if payment is sufficient (not implemented in this example)
    payment_enough = True  # Assume payment is sufficient for this example

    if payment_enough:
        # Retrieve attached message from payment request
        message = lnd_client.get_message_from_invoice(payment_hash)

        # Dummy processing (hashing the message)
        processed_message = hashlib.sha256(message.encode()).hexdigest()

        return processed_message
    else:
        return None

# Example usage
# In a real system, payment request string would be received from the client
# For demonstration, we'll use the payment request string generated in the client-side example
processed_message = process_payment("thisisasamplemessage")

print("Processed message:", processed_message)