import asyncio
import config


async def chat_writer(message):
    _, writer = await asyncio.open_connection(config.app_config[config.HOST], 5050)

    writer.write(str(config.CHAT_TOKEN + '\n').encode())
    writer.write(f'{message}\n\n'.encode())

if __name__ == '__main__':
    asyncio.run(chat_writer('!!!ТЕСТОВОЕ СООБЩЕНИЕ!!!'))
