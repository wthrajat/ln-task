import asyncio
from lndgrpc import AsyncLNDClient

async_lnd = AsyncLNDClient(ip_address='127.0.0.1:10009', network='testnet', admin=False, cert=None,
                 cert_filepath=None, macaroon=None, macaroon_filepath=None)

async def subscribe_invoices():
    print('Listening for invoices...')
    async for invoice in async_lnd.subscribe_invoices():
        print(invoice)

async def get_info():
    while True:
        info = await async_lnd.get_info()
        print(info)
        await asyncio.sleep(5)

async def run():
    coros = [subscribe_invoices(), get_info()]
    await asyncio.gather(*coros)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())