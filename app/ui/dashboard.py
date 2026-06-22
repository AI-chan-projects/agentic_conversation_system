# app/ui/dashboard.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")
st.title("NPC World Dashboard")

world_id = st.text_input("Enter World ID", value="world_001")

# ── 사이드바: 컨트롤 패널
with st.sidebar:
    st.subheader("Control Panel")
    if st.button("Simulate Background Events"):
        with st.spinner("Simulating..."):
            response = requests.post(f"{API_BASE}/api/simulate/{world_id}")
            if response.status_code == 200:
                events = response.json().get("events", [])
                st.success(f"완료! 이벤트 {len(events)}건 발생")
                if events:
                    st.session_state["event_log"] = st.session_state.get("event_log", []) + events
            else:
                st.error("Simulation Failed.")

    if st.button("Refresh Data"):
        st.rerun()

    st.subheader("NPC List")
    res = requests.get(f"{API_BASE}/api/npcs")
    npcs = []
    if res.status_code == 200:
        npcs = res.json().get("npcs", [])
        for npc in npcs:
            st.write(f"- **{npc['name']}** ({npc['npc_id']})")

# ── 탭 구성
tab1, tab2, tab3, tab4 = st.tabs([
    "대화", "관계 그래프", "히트맵 & 타임라인", "메모리"
])

# ── TAB 1: 대화 UI
with tab1:
    st.subheader("NPC 대화")

    npc_options = {npc["name"]: npc["npc_id"] for npc in npcs}
    selected_name = st.selectbox("NPC 선택", list(npc_options.keys()))
    selected_npc_id = npc_options.get(selected_name, "")

    user_id = st.text_input("User ID", value="user_001")
    user_action = st.radio(
        "행동 선택",
        ["ask", "persuade", "threaten"],
        horizontal=True
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("메시지 입력...")
    if user_input and selected_npc_id:
        st.session_state["messages"].append({"role": "user", "content": user_input})

        with st.spinner("NPC 응답 중..."):
            chat_res = requests.post(f"{API_BASE}/api/chat", json={
                "npc_id": selected_npc_id,
                "user_id": user_id,
                "message": user_input,
                "user_action": user_action,
                "world_id": world_id
            })

        if chat_res.status_code == 200:
            npc_response = chat_res.json().get("npc_response", "")
            st.session_state["messages"].append({"role": "assistant", "content": f"**{selected_name}**: {npc_response}"})
            st.rerun()

# ── TAB 2: 관계 그래프
with tab2:
    st.subheader("NPC 관계 그래프")
    try:
        graph_res = requests.get(f"{API_BASE}/api/graph/{world_id}")
        if graph_res.status_code == 200:
            data = graph_res.json()
            nodes = [Node(id=n["id"], label=n["label"], size=20) for n in data["nodes"]]
            edges = [Edge(source=e["source"], target=e["target"], label=str(round(e["strength"], 2))) for e in data["edges"]]
            config = Config(width=700, height=500, directed=True, physics=True)
            agraph(nodes=nodes, edges=edges, config=config)
        else:
            st.info("시뮬레이션 후 그래프가 표시됩니다.")
    except:
        st.warning("백엔드 연결을 확인해주세요.")

# ── TAB 3: 히트맵 & 이벤트 타임라인
with tab3:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("관계 강도 히트맵")
        try:
            graph_res = requests.get(f"{API_BASE}/api/graph/{world_id}")
            if graph_res.status_code == 200:
                data = graph_res.json()
                if data["edges"]:
                    df = pd.DataFrame(data["edges"])
                    pivot = df.pivot_table(
                        index="source", columns="target",
                        values="strength", fill_value=0
                    )
                    fig = px.imshow(
                        pivot,
                        color_continuous_scale="RdBu",
                        zmin=-1, zmax=1,
                        title="NPC 관계 강도"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("관계 데이터 없음 — 시뮬레이션 먼저 실행해봐!")
        except:
            st.warning("데이터 로드 실패")

    with col_b:
        st.subheader("백그라운드 이벤트 타임라인")
        event_log = st.session_state.get("event_log", [])
        if event_log:
            df_events = pd.DataFrame(event_log)
            st.dataframe(df_events[["npc_a", "npc_b", "event", "delta", "timestamp"]], use_container_width=True)
        else:
            st.info("이벤트 없음 — 시뮬레이션 실행 후 확인해봐!")

# ── TAB 4: 메모리 현황
with tab4:
    st.subheader("메모리 누적 현황")
    mem_npc_id = st.text_input("NPC ID 입력", value="npc_w01")
    mem_user_id = st.text_input("User ID 입력", value="user_001")

    if st.button("메모리 조회"):
        mem_res = requests.get(f"{API_BASE}/api/memories/{mem_npc_id}/{mem_user_id}")
        if mem_res.status_code == 200:
            memories = mem_res.json().get("memories", [])
            if memories:
                for mem in memories:
                    st.markdown(f"**{mem['updated_at']}**")
                    st.write(mem["raw_log"])
                    st.divider()
            else:
                st.info("메모리 없음")
        else:
            st.warning("메모리 API 확인 필요")