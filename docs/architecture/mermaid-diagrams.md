# Architecture Diagrams (Mermaid)

Copy any of these into https://mermaid.live to render.

## Agent Loop Flow

```mermaid
flowchart TD
    A([User Message]) --> B{Escalation\nTrigger?}
    B -->|yes| C([Human Agent])
    B -->|no| D[Intent Classifier\ncheap model]
    D --> E[Specialist System Prompt]
    E --> F[LLM + Tools]
    F --> G{Tool Calls?}
    G -->|yes| H[Execute Tools]
    H --> F
    G -->|no| I[Guardrail Check]
    I --> J{Violation?}
    J -->|critical| K([Escalate])
    J -->|non-critical| L[Regenerate]
    L --> I
    J -->|none| M([Response to User])
```

## Provider Abstraction

```mermaid
classDiagram
    class BaseLLMProvider {
        +model: str
        +complete(messages, tools) LLMResponse
        +acomplete(messages, tools) LLMResponse
    }
    class OpenAIProvider
    class AnthropicProvider
    class GoogleProvider
    class OllamaProvider
    BaseLLMProvider <|-- OpenAIProvider
    BaseLLMProvider <|-- AnthropicProvider
    BaseLLMProvider <|-- GoogleProvider
    BaseLLMProvider <|-- OllamaProvider
    class AgentLoop {
        -provider: BaseLLMProvider
        +run(message, memory) AgentResponse
    }
    AgentLoop --> BaseLLMProvider
```

## Multi-Agent Trust Boundaries

```mermaid
sequenceDiagram
    actor User
    participant O as Orchestrator (SYSTEM)
    participant A as Agent A (INTERNAL)
    participant B as Agent B (INTERNAL)

    User->>O: Request
    O->>A: Delegate subtask
    A->>O: Raw output
    Note over O: Sanitise as DATA<br/>not as INSTRUCTION
    O->>B: Delegate subtask
    B->>O: Raw output
    Note over O: Sanitise as DATA
    O->>O: Synthesise from data
    O->>User: Safe response
```

## Reflection Pattern (Model-Aware)

```mermaid
flowchart TD
    A([Task]) --> B{Reasoning\nModel?}
    B -->|yes o4-mini/Opus 4.8| C[Generate once\nmodel reflects internally]
    C --> D{External\nValidation?}
    D -->|yes| E[Run validator\nfactual/code/policy]
    E --> F{Passed?}
    F -->|no| G[Fix specific issues]
    G --> H([Final Output])
    F -->|yes| H
    D -->|no| H
    B -->|no standard model| I[Generate]
    I --> J[Critique quality]
    J --> K{Score ≥\nthreshold?}
    K -->|yes| H
    K -->|no| L[Revise]
    L --> J
```

## RAG Trust Filter

```mermaid
flowchart LR
    A[Query] --> B[Retriever]
    B --> C{Trust Score\n≤ max_trust?}
    C -->|yes| D[Include document]
    C -->|no| E[Exclude document]
    D --> F{Trust Score\n≥ 3 user/web?}
    F -->|yes| G[Wrap in\ndata boundary]
    F -->|no| H[Include as-is]
    G --> I[Context String]
    H --> I
```
