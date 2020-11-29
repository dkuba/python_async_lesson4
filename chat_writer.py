import asyncio
import json

import config
import logging


logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


async def chat_writer(message):
    reader, writer = await asyncio.open_connection(config.app_config[config.HOST], 5050)

    data = await reader.readline()
    logger.debug(data.decode("utf-8"))

    writer.write(str(config.CHAT_TOKEN + '1\n').encode())

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


if __name__ == '__main__':
    asyncio.run(chat_writer('!!!ТЕСТОВОЕ СООБЩЕНИЕ!!!'))
