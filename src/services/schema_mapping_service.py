import asyncio

from .base_service import Base
from uuid import UUID
from repository.schema_mapping_repo import SchemaMappingRepository
from models.enums import EntityType
from sqlalchemy.ext.asyncio import AsyncSession
class SchemaMappingService(Base):
    def __init__(self,db:AsyncSession):
        super().__init__()
        self.repo=SchemaMappingRepository(db=db)
        self._mappings:dict[UUID,dict]={}
        self._lock=asyncio.Lock()

    async def get_company_mapping(self,company_id:UUID)->dict:
        mapping=self._mappings.get(company_id)
        if mapping is None:
            async with self._lock:
                mapping=self._mappings.get(company_id)
                if mapping is None:
                    mapping=await self.repo.get_by_company_id(company_id=company_id) or {}
                    self._mappings[company_id]=mapping
        return mapping

    async def get_entity_mapping(self,
                                  company_id:UUID,
                                  entity:EntityType)->dict:
        """
        use to get the entity out of mapping to other db or table
        example
        imagine u want the products of a company car,drinks..
        so u ask this function and it will tell u what is the product
        """
        self.logger.info("start the get entity mapping function")
        mapping=await self.get_company_mapping(company_id=company_id)

        result=mapping.get(entity.value)
      
        
        if result is None:
            raise ValueError(f"Entity '{entity.value}' is not found")
        return result
    
    async def get_entity_fields(
    self,
    company_id: UUID,
    entity: EntityType
    ):
        mapping = await self.get_entity_mapping(
            company_id=company_id,
            entity=entity
        )

        return mapping["fields"]

        
        

        