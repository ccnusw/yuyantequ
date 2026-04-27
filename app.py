"""
特殊语言运用领域的语言创新与规范研究检索系统
国家语言文字推广基地特色工作项目
项目编号：24JDTS14
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import time

# 页面配置
st.set_page_config(
    page_title="特殊语言运用检索系统",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
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
        padding: 3.5rem 2rem 3.5rem;
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
        text-align: center;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--accent-color), transparent);
    }

    .main-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    }

    .header-decoration {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(212,165,116,0.08) 0%, transparent 70%);
        pointer-events: none;
    }

    .header-content {
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.8s ease-out;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .main-header h1 {
        font-family: 'Noto Serif SC', serif;
        font-size: 3.2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 0.5rem;
        letter-spacing: 0.12em;
        text-shadow: 0 2px 20px rgba(0,0,0,0.25);
    }

    .header-divider {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
    }

    .header-divider::before,
    .header-divider::after {
        content: '';
        width: 60px;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-color), transparent);
    }

    .header-icon {
        color: var(--accent-color);
        font-size: 1.2rem;
    }

    .main-header .subtitle {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.85);
        margin: 0;
        font-weight: 500;
        letter-spacing: 0.25em;
        text-transform: uppercase;
    }

    .project-badge {
        display: inline-block;
        background: rgba(100,181,246,0.15);
        border: 1px solid rgba(100,181,246,0.3);
        color: var(--accent-light);
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        font-size: 0.85rem;
        letter-spacing: 0.1em;
        margin-top: 1.5rem;
    }
    }

    /* 搜索卡片 */
    .search-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }

    /* 检索区域元素对齐 */
    .search-card [data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }

    /* 结果卡片样式 */
    .result-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--accent-color);
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }

    .result-index {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        background: var(--primary-color);
        color: white;
        border-radius: 50%;
        margin-right: 1rem;
    }

    .result-meta {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border-color);
    }

    .stat-item { text-align: center; }
    .stat-number { font-size: 2rem; font-weight: 700; color: var(--primary-color); }
    
    /* 按钮样式补丁：确保垂直居中 */
    div[data-testid="stButton"] {
        margin-top: 0px !important;
        display: flex !important;
        align-items: center !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        height: 2.8rem;
        border-radius: 8px;
        width: 100%;
    }

    /* 确保输入框与按钮高度一致 */
    .stTextInput > div > div > input {
        height: 2.8rem;
    }

    .stSelectbox > div > div {
        height: 2.8rem;
    }

    footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--text-secondary);
        font-size: 0.8rem;
        border-top: 1px solid var(--border-color);
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

PROJECT_INFO = "国家语言文字推广基地特色工作项目 \"特殊语言运用领域的语言创新与规范研究及语料库建设\"（24JDTS14）阶段性成果"

WORD_CLASSES = ["名词", "时间词", "处所词", "方位词", "区别词", "代词", "数词", "量词", "动词", "形容词", "状态词", "副词", "介词", "连词", "助词", "叹词", "语气词", "拟声词", "前接成分", "后接成分", "成语", "简称略语", "习用语"]
STRUCTURES = ["主谓结构", "述宾结构", "述补结构", "定中结构", "状中结构", "联合结构", "连谓结构"]
MORPHEMES = ["黏着性实语素", "自由性实语素", "黏着性虚语素", "自由性虚语素"]

EXCEL_PATH = Path(__file__).parent / "语料库汇总【共13103条】.xlsx"

@st.cache_data
def load_data():
    try:
        return pd.read_excel(EXCEL_PATH)
    except Exception:
        st.error("无法加载语料库文件，请检查文件路径。")
        return None

def main():
    df = load_data()
    if df is None: st.stop()
    if 'page' not in st.session_state: st.session_state.page = 1

    # 头部渲染
    st.markdown(f'''
    <div class="main-header">
        <div class="header-decoration"></div>
        <div class="header-content">
            <h1>特殊语言运用领域的语言创新与规范研究</h1>
            <div class="header-divider">
                <span class="header-icon">◈</span>
            </div>
            <p class="subtitle">检索系统</p>
            <span class="project-badge">国家语言文字推广基地 · 24JDTS14</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # --- 检索功能区 ---
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.8, 3.5, 0.7])

    with col1:
        category_type = st.selectbox("类型", ["所有类型", "词类", "结构", "语素"], label_visibility="collapsed")

    with col2:
        search_text = st.text_input("内容", placeholder="请输入检索内容...", label_visibility="collapsed")

    with col3:
        search_btn = st.button("🔍 开始检索", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 二级选择
    spec_cat = None
    if category_type != "所有类型":
        all_options = {"词类": WORD_CLASSES, "结构": STRUCTURES, "语素": MORPHEMES}.get(category_type, [])
        options = ["全部类型"] + all_options
        spec_cat = st.selectbox(f"具体{category_type}", options=options, index=0)

    # 检索逻辑处理
    if search_btn:
        res = df.copy()
        if search_text:
            res = res[res.iloc[:, 1].astype(str).str.contains(search_text, case=False, na=False)]
        if category_type != "所有类型" and spec_cat and spec_cat != "全部类型":
            mask = res.iloc[:, 3].astype(str).str.contains(spec_cat, na=False) | \
                   res.iloc[:, 5].astype(str).str.contains(spec_cat, na=False)
            res = res[mask]
        
        st.session_state.search_results = res
        st.session_state.search_done = True
        st.session_state.page = 1

    # 结果展示
    if st.session_state.get('search_done'):
        results = st.session_state.search_results
        total = len(results)
        
        if total == 0:
            st.warning("未找到匹配结果。")
        else:
            st.markdown(f"### 📊 找到 {total:,} 条结果")
            
            # 分页展示
            p_size = 5
            t_pages = (total + p_size - 1) // p_size
            
            # 简单的翻页控制
            cp = st.session_state.page
            nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 2])
            if nav_col1.button("首页"): st.session_state.page = 1; st.rerun()
            if nav_col2.button("上页") and cp > 1: st.session_state.page -= 1; st.rerun()
            if nav_col3.button("下页") and cp < t_pages: st.session_state.page += 1; st.rerun()
            with nav_col4:
                right_col1, right_col2, right_col3, right_col4, right_col5 = st.columns([1, 1, 1, 1, 1])
                with right_col1:
                    if st.button("尾页"): st.session_state.page = t_pages; st.rerun()
                with right_col2:
                    st.markdown(f"<div style='text-align:center; line-height: 2.8rem;'>第 {cp} / {t_pages} 页</div>", unsafe_allow_html=True)
                with right_col3:
                    st.markdown("<div style='line-height: 2.8rem;'>跳转到</div>", unsafe_allow_html=True)
                with right_col4:
                    jump_page = st.number_input("跳", min_value=1, max_value=t_pages, value=cp, label_visibility="collapsed", key="jump_input")
                with right_col5:
                    if st.button("跳转", key="jump_btn"):
                        if jump_page != cp:
                            st.session_state.page = jump_page
                            st.rerun()

            start_idx = (st.session_state.page - 1) * p_size
            for i, (idx, row) in enumerate(results.iloc[start_idx : start_idx + p_size].iterrows()):
                st.markdown(f'''
                <div class="result-card">
                    <div style="display: flex; align-items: center;">
                        <span class="result-index">{start_idx + i + 1}</span>
                        <div style="font-size: 1.1rem;">{row.iloc[1]}</div>
                    </div>
                    <div class="result-meta">
                        <span><b>违反规则:</b> {row.iloc[3]}</span>
                        <span><b>超常类型:</b> {row.iloc[5]}</span>
                        <span><b>文本类型:</b> {row.iloc[6]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.info("💡 请输入关键词或选择分类条件后点击「开始检索」。")

    st.markdown('<footer><p>国家语言文字推广基地特色工作项目 · 24JDTS14</p></footer>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()