import asyncio
from core.database import engine, Base
from models.user import User
from models.database_todo import Todo
from models.session_token import SessionToken
# Note: Conversation and Message use SQLModel which might need different handling, 
# but for now we focus on core Auth tables to fix login/signup.

async def create_tables():
    print("Connecting to database and creating tables...")
    async with engine.begin() as conn:
        # This will create all tables defined in models that don't exist yet
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())
