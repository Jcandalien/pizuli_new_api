from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "is_fallback_delivery_user" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "franchises" ADD "is_open" BOOL NOT NULL  DEFAULT True;
        ALTER TABLE "franchises" ADD "open_time" TIMETZ NOT NULL;
        ALTER TABLE "franchises" ADD "is_paused" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "franchises" ADD "close_time" TIMETZ NOT NULL;
        CREATE TABLE IF NOT EXISTS "animalimage" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "image_url" VARCHAR(255) NOT NULL,
    "animal_id" UUID NOT NULL REFERENCES "animals" ("id") ON DELETE CASCADE
);
        ALTER TABLE "meats" ADD "is_chilled" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "meats" DROP COLUMN "image";
        CREATE TABLE IF NOT EXISTS "meatimage" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "image_url" VARCHAR(255) NOT NULL,
    "meat_id" UUID NOT NULL REFERENCES "meats" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "payments" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "payment_method" VARCHAR(50) NOT NULL,
    "payment_status" VARCHAR(50) NOT NULL,
    "amount_paid" DECIMAL(10,2) NOT NULL,
    "transaction_id" VARCHAR(100),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "order_id" UUID NOT NULL UNIQUE REFERENCES "orders" ("id") ON DELETE CASCADE
);
        CREATE UNIQUE INDEX "uid_franchises_name_685032" ON "franchises" ("name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_franchises_name_685032";
        ALTER TABLE "meats" ADD "image" VARCHAR(255);
        ALTER TABLE "meats" DROP COLUMN "is_chilled";
        ALTER TABLE "users" DROP COLUMN "is_fallback_delivery_user";
        ALTER TABLE "franchises" DROP COLUMN "is_open";
        ALTER TABLE "franchises" DROP COLUMN "open_time";
        ALTER TABLE "franchises" DROP COLUMN "is_paused";
        ALTER TABLE "franchises" DROP COLUMN "close_time";
        DROP TABLE IF EXISTS "animalimage";
        DROP TABLE IF EXISTS "meatimage";
        DROP TABLE IF EXISTS "payments";"""
