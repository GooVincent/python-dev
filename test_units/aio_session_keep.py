import aiohttp
import asyncio


class FileHandler:
    def __init__(self):
        self.session = None

    async def initialize_session(self):
        upload_timeout = aiohttp.ClientTimeout(sock_connect=4, sock_read=100)
        self.session = aiohttp.ClientSession(timeout=upload_timeout)

    async def close_session(self):
        await self.session.close()

    async def download_file(self, url):
        async with self.session.get(url) as response:
            print('here is download_file')

    async def upload_file(self, url, file_path):
        with open(file_path, 'rb') as file:
            async with self.session.post(url, data=file) as response:
                print(response)
                print('here is upload_file')


# Example usage
async def main():
    file_handler = FileHandler()
    await file_handler.initialize_session()

   #  await file_handler.download_file('http://example.com/large_file.txt')
    await file_handler.upload_file('http://10.23.2.12', 'file_to_upload.txt')

    await file_handler.close_session()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
