import argparse
import asyncio
import json
import os

import logging

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__file__)


async def register(nickname):
    try:
        reader, writer = await asyncio.open_connection(os.environ['CHAT_HOST'], int(os.environ['CHAT_PORT']))

        data = await reader.readline()
        logger.debug(data.decode("utf-8"))

        writer.write('\n'.encode())

        data = await reader.readline()
        logger.debug(data.decode("utf-8"))

        writer.write(f'{nickname}\n'.encode())
        await writer.drain()

        data = await reader.readline()
        os.environ['CHAT_TOKEN'] = json.loads(data.decode("utf-8"))["account_hash"]

        logger.debug(data.decode("utf-8"))
        data = await reader.readline()
        logger.debug(data.decode("utf-8"))
    finally:
        writer.close()
        await writer.wait_closed()


async def authorise():
    try:
        reader, writer = await asyncio.open_connection(os.environ['CHAT_HOST'], int(os.environ['CHAT_PORT']))

        data = await reader.readline()
        logger.debug(data.decode("utf-8"))

        writer.write(str(os.environ['CHAT_TOKEN'] + '\n').encode())
        await writer.drain()

        data = await reader.readline()

        if not json.loads(data.decode("utf-8")):
            print('введен неверный токен')
            return

        logger.debug(data.decode("utf-8"))
        data = await reader.readline()
        logger.debug(data.decode("utf-8"))
    finally:
        writer.close()
        await writer.wait_closed()


async def submit_message(message):
    try:
        reader, writer = await asyncio.open_connection(os.environ['CHAT_HOST'], int(os.environ['CHAT_PORT']))

        data = await reader.readline()
        logger.debug(data.decode("utf-8"))

        writer.write(str(os.getenv('CHAT_TOKEN') + '\n').encode())

        data = await reader.readline()
        if not json.loads(data.decode("utf-8")):
            print('введен неверный токен')
            return

        logger.debug(data.decode("utf-8"))
        data = await reader.readline()
        logger.debug(data.decode("utf-8"))

        writer.write(f'{message}\n\n'.encode())
        await writer.drain()

        data = await reader.readline()
        logger.debug(data.decode("utf-8"))
    finally:
        writer.close()
        await writer.wait_closed()


async def main():

    if os.environ['CHAT_USER_NAME']:
        await register(os.environ['CHAT_USER_NAME'])

    await authorise()

    await submit_message(os.getenv('CHAT_MESSAGE'))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Async writer')
    parser.add_argument('--host', type=str, default='minechat.dvmn.org', help='Connection host', dest='host')
    parser.add_argument('--port', type=int, default=5050, help='IP-port', dest='port')
    parser.add_argument('--token', type=str, default=os.getenv('CHAT_TOKEN'), help='chat token',
                        dest='token')
    parser.add_argument('--username', type=str, default='', help='username', dest='username')
    parser.add_argument('--message', type=str, default='Hello world!', help='your message', dest='message')

    args = parser.parse_args()

    os.environ['CHAT_HOST'] = args.host
    os.environ['CHAT_PORT'] = str(args.port)
    os.environ['CHAT_TOKEN'] = args.token
    os.environ['CHAT_USER_NAME'] = args.username
    os.environ['CHAT_MESSAGE'] = args.message

    asyncio.run(main())

