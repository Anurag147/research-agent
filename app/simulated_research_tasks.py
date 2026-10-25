import asyncio

RESEARCH_TASKS = [
    ("Understanding research question", "Identifying the user's research intent"),
    ("Planning research strategy", "Determining relevant sources and search approach"),
    ("Discovering documents", "Locating potentially relevant documents"),
    ("Retrieving metadata", "Collecting document titles and attributes"),
    ("Searching document content", "Finding relevant passages and clauses"),
    ("Evaluating relevance", "Ranking findings against the research question"),
    ("Cross-referencing evidence", "Comparing findings across sources"),
    ("Identifying key insights", "Extracting important observations"),
    ("Validating findings", "Checking consistency of supporting evidence"),
    ("Preparing research summary", "Organizing the final response"),
]


async def generate_research_tasks():
    for index, (title, summary) in enumerate(RESEARCH_TASKS, start=1):
        task_id = f"task-{index:02d}"

        yield {
            "taskId": task_id,
            "title": title,
            "status": "running",
            "summary": summary,
        }

        await asyncio.sleep(0.5)

        yield {
            "taskId": task_id,
            "title": title,
            "status": "completed",
            "summary": summary,
        }
