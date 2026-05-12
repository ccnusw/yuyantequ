"""
特殊语言运用领域的语言创新与规范研究检索系统
国家语言文字推广基地特色工作项目
项目编号：24JDTS14
"""

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

# 2. 自定义CSS样式：彻底优化按钮形状与容器边框
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
        font-size: 3rem;
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

    /* 检索按钮优化：横向铺满，高度调窄 */
    div.stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        color: white !important;
        height: 2.8rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        border: none !important;
        margin-top: 0.5rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button:hover {
        opacity: 0.9 !important;
        box-shadow: 0 4px 12px rgba(30, 58, 95, 0.2) !important;
    }

    /* 结果卡片样式 */
    .result-card {
        background: var(--card-bg);
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 5px solid var(--accent-color);
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    .result-index {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background: var(--primary-color);
        color: white;
        border-radius: 50%;
        margin-right: 0.8rem;
        font-size: 0.9rem;
    }

    .result-meta {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.8rem;
        margin-top: 0.8rem;
        padding-top: 0.8rem;
        border-top: 1px dashed var(--border-color);
        font-size: 0.95rem;
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

# 3. 数据常量
WORD_CLASSES = ["名词", "方位词", "代词", "数词", "量词", "动词", "形容词", "副词", "介词", "连词", "助词", "叹词", "语气词", "拟声词", "成语"]
STRUCTURES = ["述宾结构", "述补结构", "状中结构", "连谓结构"]
ALL_SUPERNORMAL_TYPES = ["所有"] + WORD_CLASSES + STRUCTURES
TEXT_TYPES = ["所有类型", "网络语言", "诗歌特区", "标题口号"]

EXCEL_PATH = Path(__file__).parent / "语料库汇总【共13103条】【20260512】.xlsx"

@st.cache_data
def load_data():
    try:
        return pd.read_excel(EXCEL_PATH)
    except Exception:
        st.error("未找到语料库文件，请确保文件名正确。")
        return None

def main():
    df = load_data()
    if df is None: st.stop()
    if "page" not in st.session_state: st.session_state.page = 1

    # 4. 标题区
    st.markdown(f'''
    <div class="main-header">
        <h1>特殊语言运用领域的语言创新与规范研究</h1>
        <p class="subtitle">检索系统</p>
        <span class="project-badge">国家语言文字推广基地特色工作项目（项目编号：24JDTS14）</span>
    </div>
    ''', unsafe_allow_html=True)

    # 5. 检索功能区：彻底删除多余 HTML div 以消除幻影边框
    with st.container():
        col_left, col_right = st.columns(2)
        with col_left:
            selected_text_type = st.selectbox("**文本类型**", options=TEXT_TYPES, index=0)
        with col_right:
            selected_super_type = st.selectbox("**超常类型**", options=ALL_SUPERNORMAL_TYPES, index=0)
        
        # 按钮调用，CSS 会自动将其变为全宽调窄形状
        search_btn = st.button("🔍 开始检索", use_container_width=True)

    # 6. 检索逻辑
    if search_btn:
        res = df.copy()
        if selected_text_type != "所有类型":
            res = res[res.iloc[:, 6].astype(str) == selected_text_type]
        if selected_super_type != "所有":
            mask = res.iloc[:, 3].astype(str).str.contains(selected_super_type, na=False) | \
                   res.iloc[:, 5].astype(str).str.contains(selected_super_type, na=False)
            res = res[mask]
        
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
            
            p_size = 5  # 每页显示 5 条
            t_pages = (total + p_size - 1) // p_size
            cp = st.session_state.page
            
            # 分页导航
            nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 3])
            with nav_col1:
                if st.button("上一页") and cp > 1:
                    st.session_state.page -= 1
                    st.rerun()
            with nav_col2:
                st.markdown(f"<div style='text-align:center; line-height:3rem; font-weight:bold;'>{cp} / {t_pages}</div>", unsafe_allow_html=True)
            with nav_col3:
                if st.button("下一页") and cp < t_pages:
                    st.session_state.page += 1
                    st.rerun()

            # 渲染结果
            start_idx = (st.session_state.page - 1) * p_size
            for i, (idx, row) in enumerate(results.iloc[start_idx : start_idx + p_size].iterrows()):
                st.markdown(f'''
                <div class="result-card">
                    <div style="display: flex; align-items: flex-start;">
                        <span class="result-index">{start_idx + i + 1}</span>
                        <div style="font-size: 1.1rem; color: #1e3a5f; line-height: 1.4;">{row.iloc[1]}</div>
                    </div>
                    <div class="result-meta">
                        <span>🏷️ <b>违反规则:</b> {row.iloc[3]}</span>
                        <span>✨ <b>超常类型:</b> {row.iloc[5]}</span>
                        <span>📄 <b>文本类型:</b> {row.iloc[6]}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.info("💡 请从上方下拉列表选择分类，然后点击「开始检索」。")

    st.markdown('<footer><p>国家语言文字推广基地特色工作项目“特殊语言运用领域的语言创新与规范研究”<br>（项目编号：24JDTS14）</p></footer>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()