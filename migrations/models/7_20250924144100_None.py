from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(100),
    "last_name" VARCHAR(100),
    "other_name" VARCHAR(100),
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "phone" VARCHAR(20),
    "birthday" DATE,
    "city" INT,
    "additional_info" TEXT,
    "is_admin" BOOL NOT NULL DEFAULT False,
    "password_hash" VARCHAR(128)
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
