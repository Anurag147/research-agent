import asyncio
import uuid

from ag_ui._generated.models import (
    CustomEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
    TextMessageStartEvent,
)
from ag_ui.core import EventType, RunAgentInput, RunFinishedEvent, RunStartedEvent
from ag_ui.encoder import EventEncoder
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.simulated_research_service import generate_research_response
from app.simulated_research_tasks import generate_research_tasks

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
        async for task in generate_research_tasks():
            task_event = CustomEvent(name="research.task.updated", value=task)
            yield encoder.encode(task_event)
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

        charts = [
            {
                "id": "spend-distribution",
                "type": "pie",
                "title": "Supplier Spend Distribution",
                "data": [
                    {"name": "Microsoft", "value": 40},
                    {"name": "Google", "value": 30},
                    {"name": "Amazon", "value": 20},
                    {"name": "Others", "value": 10},
                ],
            },
            {
                "id": "delivery-performance",
                "type": "bar",
                "title": "Supplier Delivery Performance",
                "data": [
                    {"name": "Microsoft", "value": 94},
                    {"name": "Google", "value": 87},
                    {"name": "Amazon", "value": 82},
                    {"name": "Others", "value": 76},
                ],
            },
            {
                "id": "quarterly-trend",
                "type": "line",
                "title": "Quarterly Performance Trend",
                "data": [
                    {"name": "Q1", "value": 65},
                    {"name": "Q2", "value": 72},
                    {"name": "Q3", "value": 81},
                    {"name": "Q4", "value": 89},
                ],
            },
        ]

        for chart in charts:
            yield encoder.encode(
                CustomEvent(
                    name="research.chart.generated",
                    value=chart,
                )
            )
        run_finished = RunFinishedEvent(
            type=EventType.RUN_FINISHED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id,
        )
        yield encoder.encode(run_finished)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
