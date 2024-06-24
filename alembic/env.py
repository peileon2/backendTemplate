from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

# 这个是您的模型导入路径，确保正确导入
from app.models.user import User as user_base
from app.models.sku import Sku as sku_base
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import pool
from alembic import context

# 获取 Alembic 配置对象
config = context.config

# 设置日志配置
fileConfig(config.config_file_name)

# 你的模型的元数据，用于自动生成迁移脚本
user_metadata = user_base.metadata
sku_metadata = sku_base.metadata
target_metadata = [user_metadata, sku_metadata]


def get_url():
    return config.get_main_option("sqlalchemy.url")


def run_migrations_offline():
    """以'离线'模式运行迁移。
    这种模式下，设置上下文配置为使用URL而不是引擎。
    这样，我们不需要实际创建数据库连接。
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """以'在线'模式运行迁移。
    这种模式下，需要创建引擎并与上下文关联一个连接。
    """
    connectable = create_async_engine(get_url(), poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
