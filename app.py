import streamlit as st
import pandas as pd
from pathlib import Path

# 1. 页面配置
st.set_page_config(
    page_title="特殊语言运用检索系统",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 自定义CSS样式
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

    :root {
        --primary-color: #1e3a5f;
        --secondary-color: #2d5a87;
        --accent-color: #64b5f6;
        --accent-light: #bbdefb;
        --bg-color: #f8fafc;
        --card-bg: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
    }

    * {
        font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main-header {
        background: linear-gradient(180deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 3.5rem 2rem 3rem;
        margin-bottom: 2rem;
        text-align: center;
    }

    .main-header h1 {
        font-family: 'Noto Serif SC', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: 0.1em;
    }

    .main-header .subtitle {
        font-size: 1.4rem;
        color: rgba(255,255,255,0.85);
        margin: 1rem 0;
        letter-spacing: 0.2em;
    }

    .project-badge {
        display: inline-block;
        background: rgba(100,181,246,0.15);
        border: 1px solid rgba(100,181,246,0.3);
        color: var(--accent-light);
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        font-size: 0.85rem;
    }

    /* 按钮基础样式 */
    div.stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        color: white !important;
        height: 2.6rem !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button:hover {
        opacity: 0.9 !important;
        box-shadow: 0 4px 10px rgba(30, 58, 95, 0.15) !important;
    }

    /* 结果卡片样式 */
    .result-card {
        background: var(--card-bg);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid var(--accent-color);
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .result-index {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 30px;
        height: 30px;
        background: var(--primary-color);
        color: white;
        border-radius: 50%;
        margin-right: 0.8rem;
        font-size: 0.9rem;
        padding: 0 5px;
    }

    .result-meta {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px dashed var(--border-color);
        font-size: 1rem;
    }

    /* 分页居中辅助样式 */
    .pagination-text {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 2.6rem;
        font-size: 0.95rem;
        color: var(--text-primary);
    }

    footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--text-secondary);
        font-size: 0.85rem;
        border-top: 1px solid var(--border-color);
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. 数据处理逻辑
DOMAIN_TYPES = ["所有类型", "网络语言", "诗歌特区", "标题口号"]
EXCEL_PATH = Path(__file__).parent / "语料库汇总【共14934条】.xlsx"

@st.cache_data
def load_data():
    try:
        return pd.read_excel(EXCEL_PATH)
    except Exception:
        st.error("无法加载语料库文件，请确保文件名正确。")
        return None

def main():
    df = load_data()
    if df is None: st.stop()
    
    # --- 重新编排“超常类型”下拉列表逻辑 ---
    raw_types = [str(t).strip() for t in df.iloc[:, 5].dropna().unique() if str(t).strip()]
    
    # 1. 固定开头组
    top_fixed = ["名词", "动词", "形容词", "数词", "量词", "代词"]
    # 2. 提取除固定组外，所有以“词”结尾的
    ends_with_ci = sorted([t for t in raw_types if t.endswith("词") and t not in top_fixed])
    # 3. 提取除上述外，所有2个字的
    len_two = sorted([t for t in raw_types if len(t) == 2 and t not in top_fixed and t not in ends_with_ci])
    # 4. 其余内容（如4个字的结构等）
    others = sorted([t for t in raw_types if t not in top_fixed and t not in ends_with_ci and t not in len_two])
    
    # 组合最终列表
    ALL_SUPERNORMAL_TYPES = ["所有"] + top_fixed + ends_with_ci + len_two + others

    if "page" not in st.session_state: st.session_state.page = 1

    # 4. 标题区
    st.markdown(f'''
    <div class="main-header">
        <h1>特殊语言运用领域的语言创新与规范研究</h1>
        <p class="subtitle">检索系统</p>
        <span class="project-badge">国家语言文字推广基地特色工作项目（项目编号：24JDTS14）</span>
    </div>
    ''', unsafe_allow_html=True)

    # 5. 检索功能区
    with st.container():
        col_left, col_right = st.columns(2)
        with col_left:
            selected_domain_type = st.selectbox("**领域类型**", options=DOMAIN_TYPES, index=0)
        with col_right:
            selected_super_type = st.selectbox("**超常类型**", options=ALL_SUPERNORMAL_TYPES, index=0)
        
        search_btn = st.button("🔍 开始检索", use_container_width=True)

    # 6. 检索逻辑
    if search_btn:
        res = df.copy()
        if selected_domain_type != "所有类型":
            target_val = "诗歌" if selected_domain_type == "诗歌特区" else selected_domain_type
            res = res[res.iloc[:, 6].astype(str).str.contains(target_val, na=False)]
        if selected_super_type != "所有":
            res = res[res.iloc[:, 5].astype(str) == selected_super_type]
        
        st.session_state.search_results = res
        st.session_state.search_done = True
        st.session_state.page = 1

    # 7. 结果展示区
    if st.session_state.get("search_done"):
        results = st.session_state.search_results
        total = len(results)
        
        if total == 0:
            st.warning("未找到匹配结果。")
        else:
            st.markdown(f"#### 📊 筛选到 {total:,} 条结果")
            
            p_size = 5
            t_pages = (total + p_size - 1) // p_size
            cp = st.session_state.page
            
            # --- 功能性分页导航（居中且文案优化） ---
            # m_col 为左右外间距，保持内容中心化
            m_col1, b1, b2, t1, t2, t3, b3, b4, m_col2 = st.columns([1.5, 0.8, 0.8, 0.8, 1, 0.4, 0.8, 0.8, 1.5])
            
            with b1:
                if st.button("首页", disabled=(cp == 1), use_container_width=True):
                    st.session_state.page = 1
                    st.rerun()
            with b2:
                if st.button("上一页", disabled=(cp == 1), use_container_width=True):
                    st.session_state.page -= 1
                    st.rerun()
            
            with t1:
                st.markdown('<div class="pagination-text">跳转至</div>', unsafe_allow_html=True)
            with t2:
                # 数字输入框
                jump_val = st.number_input("jump_input", min_value=1, max_value=t_pages, value=cp, 
                                          label_visibility="collapsed")
                if jump_val != cp:
                    st.session_state.page = jump_val
                    st.rerun()
            with t3:
                st.markdown('<div class="pagination-text">页</div>', unsafe_allow_html=True)
                    
            with b3:
                if st.button("下一页", disabled=(cp == t_pages), use_container_width=True):
                    st.session_state.page += 1
                    st.rerun()
            with b4:
                if st.button("末页", disabled=(cp == t_pages), use_container_width=True):
                    st.session_state.page = t_pages
                    st.rerun()
            
            # 页码指示
            st.markdown(f"<div style='text-align:center; margin-bottom:25px; font-size:0.9rem; color:#94a3b8;'>第 {cp} 页 / 共 {t_pages} 页</div>", unsafe_allow_html=True)

            # 渲染内容
            start_idx = (st.session_state.page - 1) * p_size
            current_batch = results.iloc[start_idx : start_idx + p_size]
            
            for i, (idx, row) in enumerate(current_batch.iterrows()):
                st.markdown(f'''
                <div class="result-card">
                    <div style="display: flex; align-items: flex-start;">
                        <span class="result-index">{start_idx + i + 1}</span>
                        <div style="font-size: 1.15rem; color: #1e3a5f; line-height: 1.5;"><b>实际用例：</b>{row.iloc[1]}</div>
                    </div>
                    <div class="result-meta">
                        <span>⚠️ <b>违反规则:</b> {row.iloc[3]}</span>
                        <span>🔍 <b>具体原因:</b> {row.iloc[4]}</span>
                        <span>🌐 <b>领域类型:</b> {row.iloc[6]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.info("💡 请从上方下拉列表选择分类，然后点击「开始检索」。")

    st.markdown('<footer><p>国家语言文字推广基地特色工作项目“特殊语言运用领域的语言创新与规范研究”<br>（项目编号：24JDTS14）</p></footer>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()