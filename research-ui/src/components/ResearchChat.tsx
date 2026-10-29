
import { useState, type FormEvent, type KeyboardEvent } from "react";

import "./ResearchChat.css";

import { researchAgent } from "../agui/researchAgent";
import ResponseBlockRenderer from "./ResponseBlockRenderer";

import type {
  ConversationMessage,
  ResearchTask,
  ResponseBlock,
} from "../types/ConversationMessage";

import type { ResearchChart } from "../types/ConversationMessage";

type ResearchResponse = Extract<
  ConversationMessage,
  { type: "response" }
>;

export default function ResearchChat() {
  // ============================================================
  // 1. REACT STATE
  // ============================================================

  // Stores the text currently entered by the user.
  const [query, setQuery] = useState<string>("");

  // Stores the complete conversation history.
  //
  // Example:
  //
  // messages = [
  //   { id: "1", type: "query", content: "Analyze suppliers" },
  //   {
  //     id: "2",
  //     type: "response",
  //     blocks: [
  //       { id: "3", type: "text", content: "Analysis..." },
  //       { id: "4", type: "chart", chart: {...} }
  //     ],
  //     tasks: [...]
  //   }
  // ]
  const [messages, setMessages] = useState<ConversationMessage[]>([]);

  // Indicates whether an AG-UI request is currently running.
  const [isRunning, setIsRunning] = useState<boolean>(false);

  // Tracks which research execution panels are expanded.
  // Each response has its own entry.
  const [expandedResponses, setExpandedResponses] = useState<
    Record<string, boolean>
  >({});

  // ============================================================
  // 2. ADD A NEW TEXT BLOCK
  // ============================================================

  /**
   * Called when AG-UI sends TEXT_MESSAGE_START.
   *
   * We locate the assistant response and append an empty
   * text block to its blocks array.
   *
   * The block is identified by the AG-UI messageId.
   */
  const addTextBlock = (
    responseId: string,
    messageId: string,
  ) => {
    setMessages((previousMessages) => {
      const updatedMessages: ConversationMessage[] = [];

      // Examine every message in conversation history.
      for (const message of previousMessages) {
        if (
          message.type === "response" &&
          message.id === responseId
        ) {
          // We have found the assistant response that belongs
          // to the current AG-UI execution.

          const updatedBlocks: ResponseBlock[] = [];

          let blockAlreadyExists = false;

          // Copy existing blocks into a new array.
          for (const block of message.blocks) {
            updatedBlocks.push(block);

            if (block.id === messageId) {
              blockAlreadyExists = true;
            }
          }

          // Create a new text block only if it does not exist.
          if (blockAlreadyExists === false) {
            const newTextBlock: ResponseBlock = {
              id: messageId,
              type: "text",
              content: "",
            };

            updatedBlocks.push(newTextBlock);
          }

          // Create a new response object with updated blocks.
          const updatedResponse: ResearchResponse = {
            ...message,
            blocks: updatedBlocks,
          };

          updatedMessages.push(updatedResponse);
        } else {
          // Keep user queries and other responses unchanged.
          updatedMessages.push(message);
        }
      }

      // React receives a new conversation array.
      return updatedMessages;
    });
  };

  // ============================================================
  // 3. APPEND STREAMING TEXT TO AN EXISTING BLOCK
  // ============================================================

  /**
   * Called whenever AG-UI sends TEXT_MESSAGE_CONTENT.
   *
   * We find the text block whose ID matches event.messageId.
   *
   * Then we append the incoming delta to the existing content.
   *
   * Example:
   *
   * Existing content: "Supplier"
   * Incoming delta:   " analysis"
   *
   * Updated content:  "Supplier analysis"
   */
  const appendTextToBlock = (
    responseId: string,
    messageId: string,
    delta: string,
  ) => {
    setMessages((previousMessages) => {
      const updatedMessages: ConversationMessage[] = [];

      for (const message of previousMessages) {
        if (
          message.type === "response" &&
          message.id === responseId
        ) {
          const updatedBlocks: ResponseBlock[] = [];

          for (const block of message.blocks) {
            if (
              block.type === "text" &&
              block.id === messageId
            ) {
              // We found the correct text block.
              // Create an updated version with the new text.
              const updatedTextBlock: ResponseBlock = {
                id: block.id,
                type: "text",
                content: block.content + delta,
              };

              updatedBlocks.push(updatedTextBlock);
            } else {
              // Keep all other text and chart blocks unchanged.
              updatedBlocks.push(block);
            }
          }

          const updatedResponse: ResearchResponse = {
            ...message,
            blocks: updatedBlocks,
          };

          updatedMessages.push(updatedResponse);
        } else {
          updatedMessages.push(message);
        }
      }

      return updatedMessages;
    });
  };

  // ============================================================
  // 4. ADD OR UPDATE A CHART BLOCK
  // ============================================================

  /**
   * Called when AG-UI sends the custom event:
   *
   * research.chart.generated
   *
   * Charts are stored inside response.blocks, just like text.
   *
   * If the chart already exists, replace its data without
   * changing its position in the array.
   *
   * If it is a new chart, append it to the blocks array.
   */
  const addOrUpdateChart = (
    responseId: string,
    incomingChart: ResearchChart,
  ) => {
    setMessages((previousMessages) => {
      const updatedMessages: ConversationMessage[] = [];

      for (const message of previousMessages) {
        if (
          message.type === "response" &&
          message.id === responseId
        ) {
          const updatedBlocks: ResponseBlock[] = [];

          let chartAlreadyExists = false;

          for (const block of message.blocks) {
            if (block.type === "chart") {
              if (block.chart.id === incomingChart.id) {
                // The chart already exists.
                // Replace its data but preserve its position.
                const updatedChartBlock: ResponseBlock = {
                  id: block.id,
                  type: "chart",
                  chart: incomingChart,
                };

                updatedBlocks.push(updatedChartBlock);

                chartAlreadyExists = true;

                continue;
              }
            }

            // Preserve every other block.
            updatedBlocks.push(block);
          }

          // If the chart is new, add it to the end.
          if (chartAlreadyExists === false) {
            const newChartBlock: ResponseBlock = {
              id: `chart-${incomingChart.id}`,
              type: "chart",
              chart: incomingChart,
            };

            updatedBlocks.push(newChartBlock);
          }

          const updatedResponse: ResearchResponse = {
            ...message,
            blocks: updatedBlocks,
          };

          updatedMessages.push(updatedResponse);
        } else {
          updatedMessages.push(message);
        }
      }

      return updatedMessages;
    });
  };

  // ============================================================
  // 5. ADD OR UPDATE A RESEARCH TASK
  // ============================================================

  /**
   * Called when AG-UI sends:
   *
   * research.task.updated
   *
   * A task may arrive multiple times with different statuses.
   *
   * Example:
   * task-1 -> running
   * task-1 -> completed
   *
   * We replace the existing task rather than adding duplicates.
   */
  const updateResearchTask = (
    responseId: string,
    incomingTask: ResearchTask,
  ) => {
    setMessages((previousMessages) => {
      const updatedMessages: ConversationMessage[] = [];

      for (const message of previousMessages) {
        if (
          message.type === "response" &&
          message.id === responseId
        ) {
          const updatedTasks: ResearchTask[] = [];

          let taskAlreadyExists = false;

          for (const task of message.tasks) {
            if (task.taskId === incomingTask.taskId) {
              // Replace the previous task state.
              updatedTasks.push(incomingTask);

              taskAlreadyExists = true;
            } else {
              updatedTasks.push(task);
            }
          }

          // Append the task if it is appearing for the first time.
          if (taskAlreadyExists === false) {
            updatedTasks.push(incomingTask);
          }

          const updatedResponse: ResearchResponse = {
            ...message,
            tasks: updatedTasks,
          };

          updatedMessages.push(updatedResponse);
        } else {
          updatedMessages.push(message);
        }
      }

      return updatedMessages;
    });
  };

  // ============================================================
  // 6. UPDATE RESPONSE STATUS
  // ============================================================

  /**
   * Changes the execution status of a response.
   *
   * Possible statuses:
   * - streaming
   * - completed
   * - failed
   */
  const updateResponseStatus = (
    responseId: string,
    newStatus: ResearchResponse["status"],
  ) => {
    setMessages((previousMessages) => {
      const updatedMessages: ConversationMessage[] = [];

      for (const message of previousMessages) {
        if (
          message.type === "response" &&
          message.id === responseId
        ) {
          const updatedResponse: ResearchResponse = {
            ...message,
            status: newStatus,
          };

          updatedMessages.push(updatedResponse);
        } else {
          updatedMessages.push(message);
        }
      }

      return updatedMessages;
    });
  };

  // ============================================================
  // 7. SUBMIT A RESEARCH QUESTION
  // ============================================================

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    const trimmedQuery = query.trim();

    // Do not submit empty questions.
    if (trimmedQuery.length === 0) {
      return;
    }

    // Prevent multiple simultaneous research executions.
    if (isRunning === true) {
      return;
    }

    // Generate unique identifiers.
    const queryId = crypto.randomUUID();
    const responseId = crypto.randomUUID();
    const runId = crypto.randomUUID();

    // --------------------------------------------------------
    // 7.1 Create the user query
    // --------------------------------------------------------

    const userMessage: ConversationMessage = {
      id: queryId,
      type: "query",
      content: trimmedQuery,
    };

    // --------------------------------------------------------
    // 7.2 Create an empty assistant response
    // --------------------------------------------------------

    const assistantResponse: ResearchResponse = {
      id: responseId,
      type: "response",
      runId: runId,
      status: "streaming",
      blocks: [],
      tasks: [],
    };

    // --------------------------------------------------------
    // 7.3 Add both messages to conversation history
    // --------------------------------------------------------

    setMessages((previousMessages) => {
      const updatedMessages: ConversationMessage[] = [];

      for (const message of previousMessages) {
        updatedMessages.push(message);
      }

      updatedMessages.push(userMessage);
      updatedMessages.push(assistantResponse);

      return updatedMessages;
    });

    // Expand the task panel for the new response.
    setExpandedResponses((previousState) => {
      return {
        ...previousState,
        [responseId]: true,
      };
    });

    // Clear the input and indicate that execution has started.
    setQuery("");
    setIsRunning(true);

    // --------------------------------------------------------
    // 7.4 Add the user message to AG-UI history
    // --------------------------------------------------------

    researchAgent.addMessage({
      id: queryId,
      role: "user",
      content: trimmedQuery,
    });

    // --------------------------------------------------------
    // 7.5 Subscribe to AG-UI events
    // --------------------------------------------------------

    // IMPORTANT:
    //
    // We subscribe BEFORE calling runAgent().
    //
    // Every event handler captures responseId, which identifies
    // the assistant response belonging to this execution.
    const subscription = researchAgent.subscribe({
      // ------------------------------------------------------
      // CUSTOM EVENTS
      // ------------------------------------------------------

      onCustomEvent: ({ event }) => {
        // Research task progress event.
        if (event.name === "research.task.updated") {
          const task = event.value as ResearchTask;

          updateResearchTask(responseId, task);

          return;
        }

        // Dynamic chart generation event.
        if (event.name === "research.chart.generated") {
          const chart = event.value as ResearchChart;

          addOrUpdateChart(responseId, chart);

          return;
        }
      },

      // ------------------------------------------------------
      // TEXT_MESSAGE_START
      // ------------------------------------------------------

      onTextMessageStartEvent: ({ event }) => {
        // A new text message is starting.
        //
        // Create an empty text block inside the response.
        addTextBlock(responseId, event.messageId);
      },

      // ------------------------------------------------------
      // TEXT_MESSAGE_CONTENT
      // ------------------------------------------------------

      onTextMessageContentEvent: ({ event }) => {
        // Another chunk of text has arrived.
        //
        // Find the matching text block and append the delta.
        appendTextToBlock(
          responseId,
          event.messageId,
          event.delta,
        );
      },
    });

    // --------------------------------------------------------
    // 7.6 Execute the AG-UI request
    // --------------------------------------------------------

    try {
      await researchAgent.runAgent({
        runId: runId,
        tools: [],
        context: [],
        forwardedProps: {},
      });

      // The AG-UI execution completed successfully.
      updateResponseStatus(responseId, "completed");
    } catch (error) {
      console.error("AG-UI execution failed:", error);

      // Mark the response as failed.
      updateResponseStatus(responseId, "failed");
    } finally {
      // Remove this execution's event subscription.
      //
      // This prevents callbacks from accumulating across runs.
      subscription.unsubscribe();

      setIsRunning(false);
    }
  };

  // ============================================================
  // 8. HANDLE ENTER KEY
  // ============================================================

  const handleKeyDown = (
    event: KeyboardEvent<HTMLTextAreaElement>,
  ) => {
    if (event.key === "Enter" && event.shiftKey === false) {
      event.preventDefault();

      // Submit the form when Enter is pressed.
      event.currentTarget.form?.requestSubmit();
    }
  };

  // ============================================================
  // 9. EXPAND OR COLLAPSE RESEARCH TASKS
  // ============================================================

  const toggleTasks = (responseId: string) => {
    setExpandedResponses((previousState) => {
      const currentValue = previousState[responseId];

      let newValue = true;

      if (currentValue === true) {
        newValue = false;
      }

      return {
        ...previousState,
        [responseId]: newValue,
      };
    });
  };

  // ============================================================
  // 10. RENDER THE RESEARCH TASK PANEL
  // ============================================================

  const renderResearchTasks = (
    response: ResearchResponse,
  ) => {
    const tasks = response.tasks;

    // No task panel is displayed until task events arrive.
    if (tasks.length === 0) {
      return null;
    }

    // Count completed tasks.
    let completedTasks = 0;

    for (const task of tasks) {
      if (task.status === "completed") {
        completedTasks = completedTasks + 1;
      }
    }

    // Our current mock backend emits 10 research tasks.
    const totalTasks = 10;

    const progress = Math.round(
      (completedTasks / totalTasks) * 100,
    );

    const isExpanded = expandedResponses[response.id] === true;

    // Determine the execution status description.
    let executionDescription = "Research execution completed";

    if (response.status === "streaming") {
      executionDescription = "Analyzing your research question...";
    }

    if (response.status === "failed") {
      executionDescription = "Research execution failed";
    }

    return (
      <section className="research-tasks">
        <button
          type="button"
          className="research-tasks-header"
          onClick={() => toggleTasks(response.id)}
          aria-expanded={isExpanded}
        >
          <div className="research-tasks-heading">
            <div className="research-tasks-icon">✦</div>

            <div>
              <strong>Research execution</strong>
              <p>{executionDescription}</p>
            </div>
          </div>

          <span className="research-expand-icon">
            {isExpanded ? "⌃" : "⌄"}
          </span>
        </button>

        <div className="research-progress">
          <div className="research-progress-label">
            <span>Research progress</span>
            <strong>
              {completedTasks} / {totalTasks} tasks
            </strong>
          </div>

          <div className="research-progress-track">
            <div
              className="research-progress-fill"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {isExpanded && (
          <div className="research-tasks-list">
            {tasks.map((task) => {
              let statusSymbol = "•";

              if (task.status === "completed") {
                statusSymbol = "✓";
              }

              if (task.status === "running") {
                statusSymbol = "◌";
              }

              return (
                <div
                  className="research-task"
                  key={task.taskId}
                >
                  <div
                    className={`research-task-status ${task.status}`}
                  >
                    {statusSymbol}
                  </div>

                  <div className="research-task-details">
                    <strong>{task.title}</strong>
                    <p>{task.summary}</p>
                  </div>

                  <span
                    className={`research-task-label ${task.status}`}
                  >
                    {task.status}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </section>
    );
  };

  // ============================================================
  // 11. RENDER THE COMPONENT
  // ============================================================

  return (
    <div className="research-chat">
      {/* ----------------------------------------------------
          HEADER
      ---------------------------------------------------- */}

      <header className="research-header">
        <div className="research-brand">
          <div className="research-logo">✦</div>

          <div>
            <h1>Research Assistant</h1>
            <p>Powered by AG-UI</p>
          </div>
        </div>

        <span className="research-status">
          Research Lab
        </span>
      </header>

      {/* ----------------------------------------------------
          CONVERSATION
      ---------------------------------------------------- */}

      <main className="research-messages">
        {messages.length === 0 ? (
          // Display the welcome screen if conversation is empty.
          <div className="research-welcome">
            <div className="welcome-icon">✦</div>

            <h2>What would you like to research?</h2>

            <p>
              Ask questions, analyze documents and explore research insights.
            </p>
          </div>
        ) : (
          <div className="message-list">
            {/* Iterate through the conversation in order. */}
            {messages.map((message) => {
              // ----------------------------------------------
              // USER QUERY
              // ----------------------------------------------

              if (message.type === "query") {
                return (
                  <div
                    key={message.id}
                    className="chat-message user"
                  >
                    <div className="message-content">
                      {message.content}
                    </div>
                  </div>
                );
              }

              // ----------------------------------------------
              // ASSISTANT RESPONSE
              // ----------------------------------------------

              // Identify the most recent text block.
              // We use its ID to decide where the streaming
              // cursor should appear.
              let lastTextBlockId: string | null = null;

              for (const block of message.blocks) {
                if (block.type === "text") {
                  lastTextBlockId = block.id;
                }
              }

              return (
                <div
                  key={message.id}
                  className="research-response"
                >
                  {/* Research execution timeline */}
                  {renderResearchTasks(message)}

                  {/* Ordered text and chart blocks */}
                  <div className="research-response-blocks">
                    {message.blocks.map((block) => {
                      let showStreamingCursor = false;

                      if (message.status === "streaming") {
                        if (block.type === "text") {
                          if (block.id === lastTextBlockId) {
                            showStreamingCursor = true;
                          }
                        }
                      }

                      return (
                        <ResponseBlockRenderer
                          key={block.id}
                          block={block}
                          isStreaming={showStreamingCursor}
                        />
                      );
                    })}
                  </div>

                  {/* Display errors for failed executions */}
                  {message.status === "failed" && (
                    <p className="research-error">
                      Research execution failed.
                      Please try again.
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </main>

      {/* ----------------------------------------------------
          INPUT FOOTER
      ---------------------------------------------------- */}

      <footer className="research-footer">
        <form
          className="research-input-container"
          onSubmit={handleSubmit}
        >
          <textarea
            value={query}
            onChange={(event) => setQuery(event.target.value)}
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
