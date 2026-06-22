# Agentic Conversation System: Genesis Arch

NPC의 페르소나와 관계 형성을 통해 독자적인 서사를 구축하는 에이전트 기반 시뮬레이션 시스템입니다. 

## 📖 프로젝트 개요
이 시스템은 고정된 스크립트 기반의 NPC에서 벗어나, **개인화된 페르소나**를 가진 NPC들이 서로 상호작용하고, 시간이 지남에 따라 자신의 페르소나를 자손 NPC에게 **유전(Inheritance)**시키며 세계의 역사를 스스로 써 내려가는 **'디지털 창세기'** 아키텍처입니다.

## 🚀 핵심 기능 (Core Features)
* **초 개인화 페르소나**: 플레이어의 행동과 대화 패턴에 따라 변화하는 동적 페르소나 시스템.
* **관계망 형성**: NPC 간의 우호도, 갈등, 유대감을 기반으로 한 관계 그래프 생성.
* **페르소나 유전 (Persona Inheritance)**: NPC의 성격과 기억이 다음 세대로 이어지는 진화적 대화 모델.
* **자율적 서사 생성**: 시스템 내부의 상호작용을 통해 실시간으로 생성되는 독자적인 세계관 데이터.

## 🛠 기술 스택 (Tech Stack)
* **Language**: Python 3.x
* **Core Architecture**: Modularized Structure (DB / Agents / Models / Routers)
* **Framework**: FastAPI (High-performance API communication)
* **AI/LLM**: Ollama (gemma2:2b - Local inference optimization)
* **Database**: SQLite (Structured data persistence with JSON parsing capabilities)

## 📋 설치 및 실행 방법
본 프로젝트는 다음 과정을 통해 로컬 환경에서 실행할 수 있습니다.

```bash
# 레포지토리 복제
git clone [https://github.com/](https://github.com/)[사용자ID]/agentic_conversation_system.git

# 의존성 설치
pip install -r requirements.txt

  # Ollama가 먼저 실행 중이어야 시스템이 정상적으로 모델을 호출할 수 있습니다.
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma2:2b

# 1. 프로젝트 폴더 이동
cd ~/code/portfolio/npc-agent

# 2. venv 활성화
source venv/bin/activate

# 3. Ollama 서버 시작 (새 터미널)
ollama serve

# 4. FastAPI 서버 시작 (새 터미널 - venv)
uvicorn app.main:app --reload

# 5. Streamlit 대시보드 시작 (새 터미널 - venv)
streamlit run app/ui/dashboard.py
```

