import asyncio

async def generate_research_response(query: str):
    await asyncio.sleep(2)

    response = f"Here is my research analysis for your query: {query}"

    for word in response.split():
        await asyncio.sleep(0.2)
        yield word + " "