from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(
        ...,
        description="用户邮箱",
        pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    )
    is_active: bool = Field(True, description="是否激活")
    is_superuser: bool = Field(False, description="是否超级用户")
    full_name: str = Field(None, description="全名", max_length=255)
    create_time: str = Field(None, description="创建时间")


class UserCreate(BaseModel):
    email: str = Field(
        ...,
        description="用户邮箱",
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    )
    is_active: bool = Field(True, description="是否激活")
    is_superuser: bool = Field(False, description="是否超级用户")
    full_name: str = Field(None, description="全名", max_length=255)
    create_time: str = Field(None, description="创建时间")
    password: str = Field(None, description="密码")


class UserUpdate(BaseModel):
    is_active: bool = Field(True, description="是否激活")
    is_superuser: bool = Field(False, description="是否超级用户")
    full_name: str = Field(None, description="全名", max_length=255)
    create_time: str = Field(None, description="创建时间")
