from tortoise import Tortoise
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


async def init():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={
            'models': [
                'models.model_user',
                'models.model_category',
                'models.model_book',
                'models.model_comment',
                'models.model_reply'

            ]
        }
    )
    await Tortoise.generate_schemas()

async def close():
    await Tortoise.close_connections()    