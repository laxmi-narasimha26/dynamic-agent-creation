from typing import TypeVar, Generic, Optional, List
from abc import ABC, abstractmethod

T = TypeVar('T')


class BaseRepository(Generic[T], ABC):
    @abstractmethod
    async def create(self, entity: T) -> T: ...
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]: ...
    
    @abstractmethod
    async def update(self, entity: T) -> T: ...
    
    @abstractmethod
    async def delete(self, id: str) -> bool: ...
    
    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> List[T]: ...
