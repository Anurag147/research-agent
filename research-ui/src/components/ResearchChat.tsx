import {useState, type FormEvent, type KeyboardEvent} from "react";
import "./ResearchChat.css";
import {researchAgent} from "../agui/researchAgent.ts";

type ChatMessage = {
    id: string;
    role: "user" | "assistant";
    content: string;
};

type ResearchTask = {
    taskId: string;
    title: string;
    status: "pending" | "running" | "completed" | "failed";
    summary: string;
};

export default function ResearchChat() {
    const [query, setQuery] = useState("");
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isRunning, setIsRunning] = useState(false);
    const [tasks, setTasks] = useState<ResearchTask[]>([]);
    const [isTasksExpanded, setIsTasksExpanded] = useState(true);
    const completedTasks = tasks.filter(
        (task) => task.status === "completed"
    ).length;

    const progress = Math.round((completedTasks / 10) * 100);

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const trimmedQuery = query.trim();
        if (!trimmedQuery || isRunning) return;
        const userMessage: ChatMessage = {
            id: crypto.randomUUID(),
            role: "user",
            content: trimmedQuery,
        };
        researchAgent.addMessage({
            id: userMessage.id,
            role: "user",
            content: userMessage.content,
        });

        const subscription = researchAgent.subscribe({
            onCustomEvent: ({event}) => {
                if (event.name !== "research.task.updated") return;

                const task = event.value as ResearchTask;

                setTasks((prev) => {
                    const exists = prev.some((t) => t.taskId === task.taskId);

                    if (!exists) {
                        return [...prev, task];
                    }

                    return prev.map((t) =>
                        t.taskId === task.taskId ? task : t
                    );
                });
            },

            onTextMessageContentEvent: ({event}) => {
                console.log("Text chunk:", event.delta);
            },
        });

        setIsRunning(true);


        setMessages((prev) => [...prev, userMessage]);
        setQuery("");

        try {
            await researchAgent.runAgent({
                runId: crypto.randomUUID(),
                tools: [],
                context: [],
                forwardedProps: {},
            });
        } catch (error) {
            console.error("AG-UI execution failed:", error);
        } finally {
            subscription.unsubscribe();
            setIsRunning(false);
        }


        // TODO: AG-UI integration
        // 1. Send query through HttpAgent
        // 2. Receive AG-UI events
        // 3. Update assistant message incrementally
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            e.currentTarget.form?.requestSubmit();
        }
    };

    return (
        <div className="research-chat">
            <header className="research-header">
                <div className="research-brand">
                    <div className="research-logo">✦</div>
                    <div>
                        <h1>Research Assistant</h1>
                        <p>Powered by AG-UI</p>
                    </div>
                </div>
                <span className="research-status">Research Lab</span>
            </header>

            <main className="research-messages">
                {messages.length === 0 ? (
                    <div className="research-welcome">
                        <div className="welcome-icon">✦</div>
                        <h2>What would you like to research?</h2>
                        <p>
                            Ask questions, analyze documents and explore research insights.
                        </p>
                    </div>
                ) : (
                    <div className="message-list">
                        {messages.map((message) => (
                            <div
                                key={message.id}
                                className={`chat-message ${message.role}`}
                            >
                                {message.role === "assistant" && (
                                    <div className="assistant-avatar">✦</div>
                                )}

                                <div className="message-content">{message.content}</div>
                            </div>
                        ))}
                        {tasks.length > 0 && (
                            <section className="research-tasks">
                                <button
                                    type="button"
                                    className="research-tasks-header"
                                    onClick={() => setIsTasksExpanded((prev) => !prev)}
                                    aria-expanded={isTasksExpanded}
                                >
                                    <div className="research-tasks-heading">
                                        <div className="research-tasks-icon">✦</div>

                                        <div>
                                            <strong>Research execution</strong>
                                            <p>
                                                {isRunning
                                                    ? "Analyzing your research question..."
                                                    : "Research execution completed"}
                                            </p>
                                        </div>
                                    </div>

                                    <span className="research-expand-icon">
        {isTasksExpanded ? "⌃" : "⌄"}
      </span>
                                </button>

                                <div className="research-progress">
                                    <div className="research-progress-label">
                                        <span>Research progress</span>
                                        <strong>{completedTasks} / 10 tasks</strong>
                                    </div>

                                    <div className="research-progress-track">
                                        <div
                                            className="research-progress-fill"
                                            style={{width: `${progress}%`}}
                                        />
                                    </div>
                                </div>

                                {isTasksExpanded && (
                                    <div className="research-tasks-list">
                                        {tasks.map((task) => (
                                            <div className="research-task" key={task.taskId}>
                                                <div className={`research-task-status ${task.status}`}>
                                                    {task.status === "completed"
                                                        ? "✓"
                                                        : task.status === "running"
                                                            ? "◌"
                                                            : "•"}
                                                </div>

                                                <div className="research-task-details">
                                                    <strong>{task.title}</strong>
                                                    <p>{task.summary}</p>
                                                </div>

                                                <span className={`research-task-label ${task.status}`}>
              {task.status}
            </span>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </section>
                        )}
                        {isRunning && (
                            <div className="research-thinking">
                                <span className="thinking-dot"/>
                                Researching...
                            </div>
                        )}
                    </div>
                )}
            </main>

            <footer className="research-footer">
                <form className="research-input-container" onSubmit={handleSubmit}>
          <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a research question..."
              rows={2}
              disabled={isRunning}
          />

                    <div className="input-actions">
                        <span>Shift + Enter for new line</span>
                        <button
                            type="submit"
                            disabled={!query.trim() || isRunning}
                            aria-label="Send message"
                        >
                            ↑
                        </button>
                    </div>
                </form>

                <p className="research-disclaimer">
                    Research Lab · AG-UI Protocol
                </p>
            </footer>
        </div>
    );
}