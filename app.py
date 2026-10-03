import os
import streamlit as st
import streamlit.components.v1 as components

# Streamlit Page Configuration
st.set_page_config(
    page_title="COLREGS-3D | Bridge Simulator & Scoring",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide Streamlit header/footer and expand to full viewport
st.markdown("""
<style>
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    div[data-testid="stToolbar"] {visibility: hidden !important;}
    div[data-testid="stDecoration"] {visibility: hidden !important;}
    div[data-testid="stStatusWidget"] {visibility: hidden !important;}
    
    html, body, [class*="css"] {
        margin: 0 !important;
        padding: 0 !important;
        background-color: #040c14 !important;
        overflow: hidden !important;
    }
    
    .stApp {
        background-color: #040c14 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100vw !important;
        height: 100vh !important;
    }
    
    iframe {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        z-index: 9999 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load the 3D Simulator HTML
current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, "simulator.html")
js_dir = os.path.join(current_dir, "js")
three_path = os.path.join(js_dir, "three.min.js")
orbit_path = os.path.join(js_dir, "OrbitControls.js")

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Inline local Three.js and OrbitControls to guarantee 100% reliable offline loading in Streamlit iframe
    if os.path.exists(three_path):
        with open(three_path, "r", encoding="utf-8") as f:
            three_js = f.read()
        html_content = html_content.replace('<script src="js/three.min.js"></script>', f'<script>\n{three_js}\n</script>')
    
    if os.path.exists(orbit_path):
        with open(orbit_path, "r", encoding="utf-8") as f:
            orbit_js = f.read()
        html_content = html_content.replace('<script src="js/OrbitControls.js"></script>', f'<script>\n{orbit_js}\n</script>')

    quiz_path = os.path.join(js_dir, "quiz_bank.js")
    if os.path.exists(quiz_path):
        with open(quiz_path, "r", encoding="utf-8") as f:
            quiz_js = f.read()
        html_content = html_content.replace('<script src="js/quiz_bank.js"></script>', f'<script>\n{quiz_js}\n</script>')

    components.html(html_content, height=1000, scrolling=False)
else:
    st.error("Không tìm thấy file simulator.html. Vui lòng kiểm tra lại thư mục làm việc.")
