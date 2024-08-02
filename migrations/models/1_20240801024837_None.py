from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "latitude" DOUBLE PRECISION,
    "longitude" DOUBLE PRECISION
);
CREATE TABLE IF NOT EXISTS "franchises" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "type" SMALLINT NOT NULL,
    "location" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "rating" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "review_count" INT NOT NULL  DEFAULT 0,
    "is_approved" BOOL NOT NULL  DEFAULT False,
    "latitude" DOUBLE PRECISION,
    "longitude" DOUBLE PRECISION,
    "owner_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "franchises"."type" IS 'FARMER: 1\nBUTCHER: 2\nMEAT_STORE: 3\nRESTAURANT: 4';
CREATE TABLE IF NOT EXISTS "animal_types" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "animals" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "breed" VARCHAR(50) NOT NULL,
    "age" INT NOT NULL,
    "weight" DOUBLE PRECISION NOT NULL,
    "health_status" VARCHAR(50) NOT NULL,
    "price" DECIMAL(10,2) NOT NULL,
    "quantity" INT NOT NULL  DEFAULT 1,
    "image" VARCHAR(255),
    "owner_id" UUID NOT NULL REFERENCES "franchises" ("id") ON DELETE CASCADE,
    "type_id" UUID NOT NULL REFERENCES "animal_types" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "meat_types" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "meats" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "cut" VARCHAR(50) NOT NULL,
    "grade" VARCHAR(20) NOT NULL,
    "weight" DOUBLE PRECISION NOT NULL,
    "price" DECIMAL(10,2) NOT NULL,
    "is_frozen" BOOL NOT NULL  DEFAULT False,
    "is_fresh" BOOL NOT NULL  DEFAULT True,
    "stock_quantity" INT NOT NULL  DEFAULT 0,
    "image" VARCHAR(255),
    "franchise_id" UUID NOT NULL REFERENCES "franchises" ("id") ON DELETE CASCADE,
    "type_id" UUID NOT NULL REFERENCES "meat_types" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "recipes" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "ingredients" JSONB NOT NULL,
    "instructions" TEXT NOT NULL,
    "cooking_time" INT NOT NULL,
    "difficulty_level" VARCHAR(20) NOT NULL,
    "is_raw_material" BOOL NOT NULL  DEFAULT False,
    "price" DECIMAL(10,2) NOT NULL,
    "stock_quantity" INT NOT NULL  DEFAULT 0,
    "rating" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "review_count" INT NOT NULL  DEFAULT 0,
    "processing_stage" VARCHAR(6) NOT NULL,
    "cooking_method" VARCHAR(7) NOT NULL,
    "franchise_id" UUID NOT NULL REFERENCES "franchises" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "recipes"."processing_stage" IS 'RAW: raw\nCOOKED: cooked';
COMMENT ON COLUMN "recipes"."cooking_method" IS 'ROASTED: roasted\nFRIED: fried\nBOILED: boiled\nGRILLED: grilled\nSTEAMED: steamed\nBAKED: baked';
CREATE TABLE IF NOT EXISTS "recipeimage" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "image_url" VARCHAR(255) NOT NULL,
    "recipe_id" UUID NOT NULL REFERENCES "recipes" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "orders" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "items" JSONB NOT NULL,
    "total_amount" DECIMAL(10,2) NOT NULL,
    "status" SMALLINT NOT NULL  DEFAULT 1,
    "franchise_id" UUID NOT NULL REFERENCES "franchises" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "orders"."status" IS 'PENDING: 1\nPROCESSING: 2\nSHIPPED: 3\nDELIVERED: 4\nCANCELLED: 5';
CREATE TABLE IF NOT EXISTS "reviews" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "rating" DOUBLE PRECISION NOT NULL,
    "comment" TEXT NOT NULL,
    "is_flagged" BOOL NOT NULL  DEFAULT False,
    "franchise_id" UUID REFERENCES "franchises" ("id") ON DELETE CASCADE,
    "recipe_id" UUID REFERENCES "recipes" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tags" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "animals_tags" (
    "animals_id" UUID NOT NULL REFERENCES "animals" ("id") ON DELETE CASCADE,
    "tag_id" UUID NOT NULL REFERENCES "tags" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_animals_tag_animals_f48496" ON "animals_tags" ("animals_id", "tag_id");
CREATE TABLE IF NOT EXISTS "meats_tags" (
    "meats_id" UUID NOT NULL REFERENCES "meats" ("id") ON DELETE CASCADE,
    "tag_id" UUID NOT NULL REFERENCES "tags" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_meats_tags_meats_i_48c01f" ON "meats_tags" ("meats_id", "tag_id");
CREATE TABLE IF NOT EXISTS "recipes_tags" (
    "recipes_id" UUID NOT NULL REFERENCES "recipes" ("id") ON DELETE CASCADE,
    "tag_id" UUID NOT NULL REFERENCES "tags" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_recipes_tag_recipes_faea40" ON "recipes_tags" ("recipes_id", "tag_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
