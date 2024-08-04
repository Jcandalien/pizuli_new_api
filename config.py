import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# Parse the DATABASE_URL
db_url = urlparse(os.getenv("DATABASE_URL", "postgres://jc:76765767@localhost:5432/pizuli"))

# Construct the Tortoise ORM compatible database URL
DATABASE_URL = f"postgres://{db_url.username}:{db_url.password}@{db_url.hostname}:{db_url.port}/{db_url.path[1:]}"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "db.models.user",
                "db.models.franchise",
                "db.models.animal",
                "db.models.meat",
                "db.models.recipe",
                "db.models.order",
                "db.models.review",
                "db.models.tag",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}