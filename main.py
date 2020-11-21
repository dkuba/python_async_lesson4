import asyncio
from time import strftime, localtime
import aiofiles


async def tcp_chat_sniffer():

    reader, _ = await asyncio.open_connection('minechat.dvmn.org', 5000)
    try:
        while True:
            async with aiofiles.open('log.txt', mode='a') as f:
                data = await reader.readline()
                out_string = f'[{strftime("%d.%m.%y %H:%M", localtime())}] {data.decode("utf-8")}'
                print(f'[{strftime("%d.%m.%y %H:%M", localtime())}] {data.decode("utf-8")}')
                await f.write(out_string)
    except RuntimeError:
        return

if __name__ == '__main__':
    ioloop = asyncio.get_event_loop()
    tasks = [ioloop.create_task(tcp_chat_sniffer())]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
