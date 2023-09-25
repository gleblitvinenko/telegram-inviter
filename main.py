import os

from pyrogram import Client, filters
from pyrogram.types import Message

import aiofiles
import asyncio

from settings import API_ID, API_HASH
from data_validate import validate

app = Client("my_session", API_ID, API_HASH)
channel_group_url = None


@app.on_message(filters=filters.text)
async def set_url(client: Client, message: Message):
    command = message.text.split()[0]
    url = message.text.split()[-1]
    if command == "/set_url":
        global channel_group_url
        channel_group_url = url


@app.on_message(filters=filters.document)
async def handle_document(client: Client, message: Message):
    entity_id = await get_entity_id(channel_group_url.split("/")[-1])
    if message.document.mime_type == "text/plain":
        await process_document(client=client, message=message, entity_id=entity_id)

    else:
        print("TXT document required")


async def process_document(client: Client, message: Message, entity_id: int):
    """
    Process a text document and add chat members.

    Args:
        client (Client): The Pyrogram client.
        message (Message): The Pyrogram message object.
        entity_id (int): The chat entity ID.
    """
    document = await message.download()
    async with aiofiles.open(document, "r") as users:
        async for user in users:
            await client.add_chat_members(chat_id=entity_id, user_ids=await validate(user))
            await asyncio.sleep(1)

    try:
        os.remove(document)
    except:
        pass


async def get_entity_id(url: str) -> int:
    """
    Get the entity ID from a given URL.

    Args:
        url (str): The URL to extract the entity ID from.

    Returns:
        int: The extracted entity ID.
    """
    try:
        chat_info = await app.get_chat(url)
        return chat_info.id
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    app.run()
