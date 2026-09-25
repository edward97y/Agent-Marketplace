from uuid import UUID
from datetime import datetime

from sqlalchemy import MetaData, Table, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.enums import EntityType
from models.schemas.order_schema import CreateOrderInput

from .base_service import Base
from .schema_mapping_service import SchemaMappingService
from .company_db_maker_service import CompanyDBServices
from .db_services.tool_calls_service import ToolDBService
from models.enums.tool_enum import toolTypes
from fastapi.encoders import jsonable_encoder

class OrderActionService(Base):

    def __init__(
        self,
        db: AsyncSession,
        company_db_service: CompanyDBServices,
        company_database_url: str,
    ):
        super().__init__()

        self.db = db
        self.mapping = SchemaMappingService(db=db)
        self.company_db_service = company_db_service
        self.company_url = company_database_url

    async def create_order(
        self,
        company_id: UUID,
        agents_runs_id: UUID,
        customer_id: UUID,
        data: CreateOrderInput,
    ):
        self.logger.info("Start create order")

        try:

            order_mapping = await self.mapping.get_entity_mapping(
                company_id=company_id,
                entity=EntityType.ORDER,
            )

            order_fields = order_mapping["fields"]
            order_table_name = order_mapping["table"]

            order_item_mapping = await self.mapping.get_entity_mapping(
                company_id=company_id,
                entity=EntityType.ORDER_ITEMS,
            )

            item_fields = order_item_mapping["fields"]
            item_table_name = order_item_mapping["table"]

            product_mapping = await self.mapping.get_entity_mapping(
                company_id=company_id,
                entity=EntityType.PRODUCT,
            )

            product_fields = product_mapping["fields"]
            product_table_name = product_mapping["table"]

            customer_mapping = await self.mapping.get_entity_mapping(
                company_id=company_id,
                entity=EntityType.CUSTOMER,
            )

            customer_fields = customer_mapping["fields"]
            customer_table_name = customer_mapping["table"]

            SessionLocal = self.company_db_service.get_sessionmaker(
                company_id=company_id,
                url=self.company_url,
            )

            async with SessionLocal() as company_db:

                metadata = MetaData()
                connection = await company_db.connection()


                order_table = await connection.run_sync(
                    lambda conn: Table(
                        order_table_name,
                        metadata,
                        autoload_with=conn,
                    )
                )

                item_table = await connection.run_sync(
                    lambda conn: Table(
                        item_table_name,
                        metadata,
                        autoload_with=conn,
                    )
                )

                product_table = await connection.run_sync(
                    lambda conn: Table(
                        product_table_name,
                        metadata,
                        autoload_with=conn,
                    )
                )

                customer_table = await connection.run_sync(
                    lambda conn: Table(
                        customer_table_name,
                        metadata,
                        autoload_with=conn,
                    )
                )
                customer_id_mapping = order_fields.get("customer_id")

                if not customer_id_mapping:
                    raise ValueError(
                        "Field 'customer_id' is not mapped for orders"
                    )

                customer_entity_id_mapping = customer_fields.get("customer_id")

                if not customer_entity_id_mapping:
                    raise ValueError(
                        "Field 'customer_id' is not mapped for customers"
                    )

                product_id_mapping = product_fields.get("product_id")

                if not product_id_mapping:
                    raise ValueError(
                        "Field 'product_id' is not mapped for products"
                    )

                price_mapping = product_fields.get("price")

                if not price_mapping:
                    raise ValueError(
                        "Field 'price' is not mapped for products"
                    )

                stock_mapping = product_fields.get("in_stock")

                if not stock_mapping:
                    raise ValueError(
                        "Field 'in_stock' is not mapped for products"
                    )
                customer_column = customer_table.c[
                    customer_entity_id_mapping["column"]
                ]

                customer_stmt = select(customer_table).where(
                    customer_column == customer_id
                )

                customer_result = await company_db.execute(
                    customer_stmt
                )

                customer = customer_result.mappings().first()

                if not customer:
                    raise ValueError(
                        f"Customer not found"
                    )


                product_id_column = product_table.c[
                    product_id_mapping["column"]
                ]

                price_column = product_table.c[
                    price_mapping["column"]
                ]

                stock_column = product_table.c[
                    stock_mapping["column"]
                ]

                resolved_items = []
                total_amount = 0

                for item in data.items:

                    stmt = select(product_table).where(
                        product_id_column == item.product_id
                    )

                    result = await company_db.execute(stmt)

                    product = result.mappings().first()

                    if not product:
                        raise ValueError(
                            f"Product not found"
                        )

                    if not product[stock_mapping["column"]]:
                        raise ValueError(
                            f"Product is not available"
                        )

                    unit_price = product[price_mapping["column"]]

                    subtotal = unit_price * item.quantity

                    total_amount += subtotal

                    resolved_items.append(
                        {
                            "product_id": item.product_id,
                            "quantity": item.quantity,
                            "unit_price": unit_price,
                            "subtotal": subtotal,
                        }
                    )


                order_values = {
                    order_fields["customer_id"]["column"]: customer_id,
                    order_fields["status"]["column"]: "pending",
                    order_fields["total_amount"]["column"]: total_amount,
                }

                order_stmt = (
                    order_table
                    .insert()
                    .values(**order_values)
                    .returning(order_table)
                )

                order_result = await company_db.execute(order_stmt)

                created_order = order_result.mappings().one()

                order_id = created_order[
                    order_fields["order_id"]["column"]
                ]


                for item in resolved_items:

                    item_values = {
                        item_fields["order_id"]["column"]: order_id,
                        item_fields["product_id"]["column"]: item["product_id"],
                        item_fields["quantity"]["column"]: item["quantity"],
                        item_fields["unit_price"]["column"]: item["unit_price"],
                        item_fields["subtotal"]["column"]: item["subtotal"],
                    }

                    item_stmt = item_table.insert().values(
                        **item_values
                    )

                    await company_db.execute(item_stmt)

               

                await company_db.commit()

               

                output = {
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "status": "pending",
                    "total_amount": total_amount,
                    "items": resolved_items,
                }

            self.logger.info(
                f"Order created successfully: {output['order_id']}"
            )
            tool_call = ToolDBService(db=self.db)

            await tool_call.save_tool_calls(
                run_id=agents_runs_id,
                tool=toolTypes.CREATE_ORDER,
                input=jsonable_encoder(data),
                output=jsonable_encoder(output),
            )

            return output

        except SQLAlchemyError:
            self.logger.error(
                "SQLAlchemy error while creating order",
                exc_info=True,
            )
            raise

        except Exception:
            self.logger.error(
                "Error while creating order",
                exc_info=True,
            )
            raise