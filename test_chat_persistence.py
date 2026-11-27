import asyncio
from uuid import uuid4

from app.db.models.conversations import Conversation
from app.db.models.message import Message
from app.db.postgres_database import PostgresSessionLocal


async def test_conversation():
    async with PostgresSessionLocal() as session:
        conversation = Conversation(
            user_id=uuid4(),
            title="Risk Analysis",
        )

        session.add(conversation)

        await session.flush()

        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content="Identify termination risks in manufacturing agreements.",
        )

        session.add(user_message)

        await session.commit()

        print(conversation.id)
        print(conversation.created_at)


if __name__ == "__main__":
    asyncio.run(test_conversation())