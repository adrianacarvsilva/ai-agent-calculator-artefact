# AI Agent with Tool Routing (Calculator)

This project implements a simple AI assistant capable of deciding when to:
- answer a user question directly using a Language Model (LLM), or
- delegate an exact mathematical calculation to an external tool (calculator).

The goal of this project is to demonstrate reasoning, decision-making, and tool
integration using LLMs, following a clear and deterministic execution flow.

---

## 🧠 Problem Overview

The assistant must:
- Receive a user question
- Decide whether the question requires an exact mathematical calculation
- If so, extract the mathematical expression and delegate it to a calculator
- Otherwise, respond directly using the LLM

Examples:
- **"Who was Albert Einstein?"** → answered directly by the LLM
- **"What is 128 times 46?"** → delegated to the calculator tool

Mixed-intent questions (e.g., calculation + general knowledge) are explicitly rejected.

---

## 🏗️ Architecture Overview

The solution is composed of three main layers:

1. **Prompt Contract**
   - Defines strict rules for the LLM output
   - Enforces structured responses (`CALC`, `TEXT`, `REJECT`)
   - Prevents the model from solving math by itself

2. **LLM Layer**
   - Uses a Hugging Face conversational model
   - Responsible only for reasoning and decision-making

3. **Routing Layer**
   - Interprets the LLM output
   - Safely executes the calculator tool when required
   - Ensures deterministic and predictable behavior

---

## 🔧 Technology Stack

- **Python 3.11**
- **LangChain (modular architecture)**
  - `langchain-core`
  - `langchain-huggingface`
- **Hugging Face Inference API**
- **Pytest** (for functional testing)

---

## 🚀 How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/adrianacarvsilva/ai-agent-calculator-artefact.git
cd ai-agent-calculator-artefact

```

### 2. Create and activate a virtual environment

Create a Python virtual environment to isolate project dependencies:

```bash

python -m venv .venv
source .venv/Scripts/activate   # Windows (PowerShell)

```

3. Install dependencies

Install the required Python packages:

```bash

pip install -r requirements.txt

```

### 4. Configure environment variables

Create a `.env` file in the project root directory and add your Hugging Face API token:

```bash
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

### 5. Run the AI agent

```bash

python -m app.main

```
6. Run tests

```bash

python -m pytest app/tests/test_agent.py

```

## ✨ What I would improve with more time

With more time, I would evolve the solution in the following ways:

- Introduce an explicit intent classifier (e.g. math, text, mixed) before the main prompt, reducing reliance on the model’s implicit behavior and increasing the predictability of the execution flow.

- Structure model outputs using typed formats, such as JSON objects, instead of free-form text. This would reduce coupling to the LLM, eliminate manual text parsing, and make the system more robust and maintainable.

- Add more automated tests, including scenarios involving linguistic ambiguity, malicious inputs, and edge cases, to improve reliability and application safety.

- Implement an observability layer, with structured logs, error metrics, and latency tracking, enabling better monitoring of the agent’s behavior across different decision paths.

- Evaluate and replace the current model, prioritizing an LLM with stronger adherence to output contracts and more reliable support for agents and tool usage. This would allow for simpler prompts and cleaner routing logic.


