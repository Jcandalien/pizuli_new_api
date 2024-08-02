import os
from dotenv import load_dotenv
load_dotenv()

TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
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