import asyncio
import json

import config
import logging


logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


async def register(nickname):
    reader, writer = await asyncio.open_connection(config.app_config[config.HOST], 5050)

    data = await reader.readline()
    logger.debug(data.decode("utf-8"))

    writer.write('\n'.encode())

    data = await reader.readline()
    logger.debug(data.decode("utf-8"))

    writer.write(f'{nickname}\n'.encode())

    data = await reader.readline()
    config.CHAT_TOKEN = json.loads(data.decode("utf-8"))["account_hash"]

    logger.debug(data.decode("utf-8"))
    data = await reader.readline()
    logger.debug(data.decode("utf-8"))

    writer.close()
    await writer.wait_closed()


async def authorise():
    reader, writer = await asyncio.open_connection(config.app_config[config.HOST], 5050)

    data = await reader.readline()
    logger.debug(data.decode("utf-8"))

    writer.write(str(config.CHAT_TOKEN + '\n').encode())

    data = await reader.readline()

    if not json.loads(data.decode("utf-8")):
        print('введен неверный токен')
        return

    logger.debug(data.decode("utf-8"))
    data = await reader.readline()
    logger.debug(data.decode("utf-8"))


async def submit_message(message):
    reader, writer = await asyncio.open_connection(config.app_config[config.HOST], 5050)

    data = await reader.readline()
    logger.debug(data.decode("utf-8"))

    writer.write(str(config.CHAT_TOKEN + '\n').encode())

    data = await reader.readline()
    if not json.loads(data.decode("utf-8")):
        print('введен неверный токен')
        return

    logger.debug(data.decode("utf-8"))
    data = await reader.readline()
    logger.debug(data.decode("utf-8"))

    writer.write(f'{message}\n\n'.encode())

    data = await reader.readline()
    logger.debug(data.decode("utf-8"))


async def main(nickname, message):

    await register(nickname)

    await authorise()

    await submit_message(message)

if __name__ == '__main__':
    asyncio.run(main('David\n', '!!!HELLO!!!\n'))

