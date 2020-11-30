import argparse
import asyncio
from time import strftime, localtime

import aiofiles

import config


async def chat_reader():
    reader, _ = await asyncio.open_connection(config.app_config[config.CHAT_HOST],
                                              config.app_config[config.CHAT_PORT])
    try:
        while True:
            async with aiofiles.open(config.app_config[config.FILE_PATH], mode='a') as f:
                data = await reader.readline()
                out_string = f'[{strftime("%d.%m.%y %H:%M", localtime())}] {data.decode("utf-8")}'
                print(f'[{strftime("%d.%m.%y %H:%M", localtime())}] {data.decode("utf-8")}')
                await f.write(out_string)
    finally:
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Async chat sniffer service')
    parser.add_argument('--host', type=str, default='minechat.dvmn.org', help='Connection host', dest='host')
    parser.add_argument('--port', type=int, default=5000, help='IP-port', dest='port')
    parser.add_argument('--history', type=str, default='minechat.history', help='History file path', dest='history')
    args = parser.parse_args()

    config.app_config[config.CHAT_HOST] = args.host
    config.app_config[config.CHAT_PORT] = args.port
    config.app_config[config.FILE_PATH] = args.history

    try:
        asyncio.run(chat_reader())
    except KeyboardInterrupt:
        pass

