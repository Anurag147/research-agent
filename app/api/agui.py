import asyncio
import uuid

from ag_ui._generated.models import (
    TextMessageStartEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
)
from ag_ui.core import EventType, RunAgentInput, RunStartedEvent, RunFinishedEvent
from ag_ui.encoder import EventEncoder
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.simulated_research_service import generate_research_response

agui_router = APIRouter(
    prefix="/research",
    tags=["research"],
)

@agui_router.post("/research/")
async def research(input_data: RunAgentInput):
    user_message = next(
        (msg for msg in reversed(input_data.messages) if msg.role == "user"), None
    )
    print(user_message.content if user_message else "No user query")

    encoder = EventEncoder(accept="text/event-stream")

    async def event_generator():
        run_started = RunStartedEvent(
            type=EventType.RUN_STARTED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id,
        )

        yield encoder.encode(run_started)
        await asyncio.sleep(2)

        message_id = str(uuid.uuid4())
        message_started = TextMessageStartEvent(
            type=EventType.TEXT_MESSAGE_START, message_id=message_id, role="assistant"
        )

        yield encoder.encode(message_started)

        async for event in generate_research_response(user_message.content):
            message_content = TextMessageContentEvent(
                type=EventType.TEXT_MESSAGE_CONTENT,
                message_id=message_id,
                delta=event,
            )
            yield encoder.encode(message_content)

        message_ended = TextMessageEndEvent(
            type=EventType.TEXT_MESSAGE_END, message_id=message_id
        )

        yield encoder.encode(message_ended)

        run_finished = RunFinishedEvent(
            type=EventType.RUN_FINISHED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id,
        )
        yield encoder.encode(run_finished)

    return StreamingResponse(
        event_generator(), media_type="text/event-stream"
    )