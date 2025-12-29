# ClarityAI

## AI-Powered Idea Discovery and Viability Analysis Tool

Stop wasting time on endless possibilities. Start building with confidence.

## 🎯 What is ClarityAI?

ClarityAI is an intelligent strategic co-pilot designed for creators, founders, marketers, and builders who need to quickly identify their next great idea—and determine whether it's worth pursuing. Instead of getting lost in endless brainstorming sessions, this system guides you toward focused, high-quality ideas using structured strategic thinking powered by multi-agent intelligence.

## 🚀 Key Features

### 💡 **Idea Discovery**

- **Structured Brainstorming**: Generate ideas using proven frameworks and strategic thinking patterns
- **Smart Prompting**: AI-guided questions that unlock creative potential
- **Context-Aware Suggestions**: Ideas tailored to your industry, skills, and market position

### 🔍 **Viability Analysis**

Once an idea is generated or submitted, ClarityAI evaluates its real-world potential through:

- **Audience Insights**: Deep analysis of target market fit and user needs
- **Competitor Mapping**: Comprehensive competitive landscape assessment  
- **SWOT-Style Assessment**: Strengths, weaknesses, opportunities, and threats analysis
- **Market Demand Signals**: Real-time market validation and trend analysis
- **Clarity-Driven Reasoning**: Multi-agent evaluation for balanced perspectives

### 📊 **Strategic Guidance**

- **Risk Assessment**: Clear evaluation of potential challenges and mitigation strategies
- **Execution Readiness**: Actionable next steps and implementation roadmaps
- **Resource Requirements**: Realistic assessment of time, money, and skill needs
- **Success Probability**: Data-driven confidence scoring for decision making

## 🤖 System Architecture

ClarityAI employs a sophisticated Multi-Agent System (MAS) to analyze ideas from multiple perspectives:

1.  **Interviewer Agent**: Engages with the user to clarify and refine the initial concept.
2.  **Planner Agent**: Structures the raw idea into a comprehensive proposal.
3.  **Market Agent**: Analyzes target audience, positioning, and competitive landscape.
4.  **Risk Agent**: Identifies potential pitfalls, regulatory issues, and market challenges.
5.  **Execution Agent**: Develops an MVP scope and implementation roadmap.
6.  **Judge Agent**: Synthesizes all findings to provide a final verdict and confidence score.

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, FastAPI, Agno (Agent Framework), LangChain
- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Data**: LanceDB (Vector Store), JSON (File Storage)
- **Tools**: `uv` (Python Package Manager)

## 🚦 Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js 18+ and npm
- [uv](https://github.com/astral-sh/uv) (Fast Python package installer)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/gksaurabh/probable-fiesta.git
    cd ClarityAI
    ```

2.  **Environment Setup**
    Create a `.env` file in the root directory with your API keys:
    ```bash
    OPENAI_API_KEY=your_key_here
    # Add other necessary keys
    ```

3.  **Install Dependencies**
    ```bash
    # Install Python dependencies
    uv sync

    # Install Frontend dependencies
    cd clarity-ui
    npm install
    cd ..
    ```

### Running the Application

You can run both the backend and frontend using the provided script:

```bash
./scripts/dev.sh
```

Or run them separately:

**Backend:**
```bash
uv run uvicorn src.api.server:app --reload --reload-dir src --reload-dir utils --port 8000
```

**Frontend:**
```bash
cd clarity-ui
npm run dev
```

Access the application at `http://localhost:5173` (default Vite port).

## 📂 Project Structure

```
ClarityAI/
├── charts/             # Helm charts / Deployment configs
├── clarity-ui/         # React Frontend Application
├── config/             # Configuration files
├── containers/         # Docker containers
├── data/               # Data storage (runs, raw, processed)
├── docs/               # Documentation
├── scripts/            # Utility scripts (dev.sh, etc.)
├── src/                # Backend Source Code
│   ├── agents/         # Agent definitions (Interviewer, Planner, etc.)
│   ├── api/            # FastAPI routes and server
│   ├── contracts/      # Data models and schemas
│   ├── prompts/        # LLM Prompts
│   └── storage/        # File-based storage logic
├── tests/              # Python tests
└── utils/              # Shared utilities
```

## 🎯 Who Is This For?

### **Creators & Content Builders**
- Discover viral content angles and creative project ideas
- Validate concepts before investing time and resources

### **Founders & Entrepreneurs**
- Generate and validate startup ideas with market potential
- Assess product-market fit before building

### **Marketers & Growth Teams**
- Uncover fresh marketing angles and campaign concepts
- Validate growth strategies and channel opportunities

### **Product Builders & Developers**
- Discover feature ideas and product opportunities
- Validate technical concepts with market demand

## 🤝 Contributing

We welcome contributions! Whether you're improving the analysis algorithms, adding new data sources, or enhancing the user interface, check out our [Contributing Guidelines](CONTRIBUTING.md).

## 📄 License

[MIT License](LICENSE)
