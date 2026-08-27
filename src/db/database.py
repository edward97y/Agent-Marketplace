from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from helpers import get_settings,get_logger
from contextlib import asynccontextmanager
settings = get_settings()
logger = get_logger(__name__)

# Create an asynchronous engine
logger.info(f"Connecting to database")
engine = create_async_engine(settings.DATABASE_URL,
                              echo=True)

# Create a session factory
logger.info(f"Creating session factory")
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    """Get a database session for FastAPI dependency injection."""
    async with async_session() as session:
        yield session


"""
for the feature to create a db u need to do 4 steps
1. create engine
2. create session
3. create base class all models must inherit from this class
4. u need to give every fastapi endpoint a db session to use it in the endpoint

Note : before production (Deployment) i need to change the echo=True to False 

"""