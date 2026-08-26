from .base_service import Base
from uuid import UUID
from repository.schema_mapping_repo import SchemaMappingRepository
from models.enums import EntityType
class SchemaMappingService(Base):
    def __init__(self,db):
        super().__init__()
        self.repo=SchemaMappingRepository(db=db)

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
        mapping=await self.repo.get_by_company_id(company_id=company_id)
     
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

        
        

        