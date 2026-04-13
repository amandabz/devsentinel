import asyncio
from telegram import Bot


class TelegramAlerter:
    def __init__(self, token: str, chat_id: str):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send_message(self, text: str) -> None:
        async with self.bot:
            await self.bot.send_message(chat_id=self.chat_id, text=text)

    def alert(self, text: str) -> None:
        asyncio.run(self.send_message(text))
