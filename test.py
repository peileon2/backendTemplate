from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.config import settings
from sqlalchemy import select
from app.models.sku import Sku

# 定义数据库URL
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
# 创建异步引擎
async_engine = create_async_engine(DATABASE_URL, future=True, echo=True)


def get_session() -> AsyncSession:
    # 创建一个新的AsyncSession实例
    session: AsyncSession = AsyncSession(async_engine)
    return session


async def test_db_connection():
    try:
        async with get_session() as session:
            # 执行一个简单的异步查询来测试连接，例如查询sku表中的记录
            result = await session.execute(select(Sku.sku_name).limit(1))
            print("hahahah")
            print(result.scalar())
            # 检查查询结果
            if result.first():
                print("Database connection successful!")
            else:
                print("Database connection successful, but no records found.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        # 在函数内部关闭引擎
        await async_engine.dispose()

import asyncio


async def main():
    # 运行测试函数
    await test_db_connection()
    # 在函数外部关闭引擎
    await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
