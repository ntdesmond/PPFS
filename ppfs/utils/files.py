from motor.motor_asyncio import AsyncIOMotorGridOut


async def get_file_chunks(stream: AsyncIOMotorGridOut):
    while chunk := await stream.readchunk():
        yield chunk
