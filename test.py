from __future__ import annotations
from typing import TypeVar

from pydantic import BaseModel


M = TypeVar("M", bound=BaseModel)


class Foo(BaseModel):
    x: int

    @classmethod
    def validate(cls: type[M], value: object) -> M:
        print("called `Foo.validate`")
        return super().validate(value)

    class Config:
        orm_mode = True
        from_attributes = True  # 添加这个配置


class A:
    def __init__(self, x: int):
        self.x = x


a_instance = A(x=1)
foo = Foo.from_orm(a_instance)
print(foo.json())
