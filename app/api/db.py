from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from core.config import settings

# 定义数据库URL
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

# 创建异步引擎
async_engine = create_async_engine(DATABASE_URL, future=True, echo=True)


# 创建一个函数来提供AsyncSession
async def get_session() -> AsyncSession:
    # 创建一个新的AsyncSession实例
    session: AsyncSession = AsyncSession(async_engine)
    return session
