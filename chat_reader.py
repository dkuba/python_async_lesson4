import argparse
import asyncio
import logging
import os
from time import strftime, localtime
import aiofiles

logger = logging.getLogger(__file__)


async def chat_reader():
    reader, writer = await asyncio.open_connection(os.environ['CHAT_HOST'],
                                                   os.environ['CHAT_PORT'])

    try:
        while True:
            async with aiofiles.open(os.environ['FILE_PATH'], mode='a') as f:
                data = await reader.readline()
                out_string = f'[{strftime("%d.%m.%y %H:%M", localtime())}] {data.decode("utf-8")}'
                logger.info(out_string)
                await f.write(out_string)
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Async chat sniffer service')
    parser.add_argument('--host', type=str, default='minechat.dvmn.org', help='Connection host', dest='host')
    parser.add_argument('--port', type=int, default=5000, help='IP-port', dest='port')
    parser.add_argument('--history', type=str, default='minechat.history', help='History file path', dest='history')
    args = parser.parse_args()

    os.environ['CHAT_HOST'] = args.host
    os.environ['CHAT_PORT'] = str(args.port)
    os.environ['FILE_PATH'] = args.history

    try:
        asyncio.run(chat_reader())
    except KeyboardInterrupt:
        pass

