import os
from dotenv import load_dotenv

load_dotenv()

# Hardcoded database URL (temporary for debugging)
DATABASE_URL = "postgres://jc:76765767@localhost:5432/pizuli"

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