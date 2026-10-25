import { useState, type FormEvent, type KeyboardEvent } from "react";
import "./ResearchChat.css";

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

export default function ResearchChat() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isRunning, _setIsRunning] = useState(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const trimmedQuery = query.trim();

    if (!trimmedQuery || isRunning) return;

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: trimmedQuery,
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuery("");

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

            {isRunning && (
              <div className="research-thinking">
                <span className="thinking-dot" />
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