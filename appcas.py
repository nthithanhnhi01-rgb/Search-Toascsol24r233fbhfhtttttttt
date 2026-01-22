import streamlit as st
import pandas as pd

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Cơ sở dữ liệu Hóa chất Quốc gia", 
    page_icon="🇻🇳", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Arial', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* HEADER */
    .header-custom {
        background-color: #0066b3; padding: 15px 30px; display: flex;
        justify-content: space-between; align-items: center;
        border-bottom: 1px solid #004d88; color: white; margin-bottom: 20px;
    }
    .header-logo-area h1 {
        color: white !important; font-size: 20px !important; font-weight: 700 !important;
        margin: 0 !important; text-transform: uppercase; line-height: 1.2;
    }
    .header-logo-area p {
        color: #ffcc00 !important; font-size: 14px !important; font-weight: 600 !important; margin: 0 !important;
    }
    .user-profile {
        font-size: 14px; background: #005091; padding: 5px 15px; border-radius: 4px;
    }
    .navbar {
        background-color: #005a9e; padding: 8px 30px; display: flex; gap: 25px; border-bottom: 4px solid #e9ecef; margin-bottom: 20px;
    }
    .nav-item {
        color: white; text-decoration: none; font-size: 14px; font-weight: 500; display: flex; align-items: center; gap: 5px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 40px; background-color: #f0f2f6; border-radius: 4px 4px 0 0;
        padding-top: 10px; padding-bottom: 10px; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #007bff !important; color: white !important; }
    .custom-footer {
        background-color: #0066b3; color: white; padding: 20px; text-align: center;
        font-size: 13px; margin-top: 50px; border-top: 4px solid #ffcc00;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOAD DATA ---
@st.cache_data(ttl=600)
def load_data_from_sheet():
    # Link Google Sheet của bạn
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-4uKzaw2LpN5lBOGyG4MB3DPbaC6p6SbtO-yhoEQHRVFx30UHgJOSGfwTn-dOHkhBjAMoDea8n0ih/pub?gid=0&single=true&output=csv" 
    try:
        df = pd.read_csv(sheet_url, dtype=str)
        df.columns = df.columns.str.strip() # Xóa khoảng trắng tên cột
        return df
    except Exception:
        return None

# --- 4. LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login_screen():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
            <div style="background-color: #0066b3; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h3 style="margin:0">HỆ THỐNG TRA CỨU HÓA CHẤT</h3>
                <p style="margin:0; font-size: 12px">Dành cho khách hàng đăng ký</p>
            </div>
            <div style="background-color: white; padding: 30px; border: 1px solid #ddd; border-radius: 0 0 8px 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        """, unsafe_allow_html=True)
        username = st.text_input("Tài khoản", placeholder="admin")
        password = st.text_input("Mật khẩu", type="password", placeholder="admin123")
        if st.button("Đăng nhập", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Sai tài khoản hoặc mật khẩu!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. MAIN SCREEN ---
def main_screen():
    # Header
    st.markdown("""
        <div class="header-custom">
            <div class="header-logo-area">
                <h1>CƠ SỞ DỮ LIỆU CHUYÊN NGÀNH HÓA CHẤT</h1>
                <p>VIETNAM CHEMICAL DATABASE</p>
            </div>
            <div class="user-profile">👤 Người dùng: <b>Admin</b> | <a href="#" style="color:white;">Thoát</a></div>
        </div>
        <div class="navbar">
            <a href="#" class="nav-item">🏠 Trang chủ</a>
            <a href="#" class="nav-item">📚 Tài liệu</a>
            <a href="#" class="nav-item">🔍 Tìm kiếm</a>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<h2 style="color: #444; border-bottom: 2px solid #0066b3; padding-bottom: 10px;">Tra cứu Danh mục Hóa chất & Ngưỡng tồn trữ</h2>', unsafe_allow_html=True)

    df = load_data_from_sheet()
    if df is None:
        st.error("⚠️ Lỗi kết nối dữ liệu Google Sheet.")
        return

    # TẠO TABS
    tab1, tab2 = st.tabs(["🔍 Tra cứu đơn (Filter)", "🔢 Tra cứu hàng loạt"])

    # =========================================================
    # TAB 1: TRA CỨU ĐƠN (AUTO-FILTER & STACKED)
    # =========================================================
    with tab1:
        st.caption("Nhập thông tin vào các ô để lọc tự động (Logic AND: Thỏa mãn tất cả các ô đang nhập).")
        
        # Tạo 3 cột nhập liệu (Bỏ cột nút bấm đi)
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            # key='cas' để Streamlit nhớ giá trị
            f_cas = st.text_input("Mã CAS", placeholder="VD: 50, 106...", key="f_cas")
        with col_f2:
            f_name = st.text_input("Tên hóa chất (tiếng Anh)", placeholder="VD: Acid...", key="f_name")
        with col_f3:
            f_formula = st.text_input("Công thức hóa học", placeholder="VD: HCHO...", key="f_formula")

        # --- LOGIC LỌC CHỒNG (STACKED FILTER) ---
        # Bắt đầu với bảng gốc
        df_result = df.copy()

        # 1. Lọc CAS (Nếu ô CAS có chữ)
        if f_cas:
            # Lọc theo chuỗi (contains), case=False (không phân biệt hoa thường), na=False (bỏ qua ô trống)
            if 'CAS' in df_result.columns:
                df_result = df_result[df_result['MaCAS'].astype(str).str.contains(f_cas.strip(), case=False, na=False)]
        
        # 2. Lọc tiếp Tên (Nếu ô Tên có chữ) -> Lọc chồng lên kết quả trên
        if f_name:
            if 'Tên chất' in df_result.columns:
                df_result = df_result[df_result['Tên khoa học (danh pháp IUPAC)'].astype(str).str.contains(f_name.strip(), case=False, na=False)]
        
        # 3. Lọc tiếp Công thức (Nếu ô CT có chữ) -> Lọc chồng tiếp
        if f_formula:
             if 'Công thức hóa học' in df_result.columns:
                df_result = df_result[df_result['Công thức hóa học'].astype(str).str.contains(f_formula.strip(), case=False, na=False)]

        # --- HIỂN THỊ KẾT QUẢ NGAY LẬP TỨC ---
        st.success(f"Tìm thấy: **{len(df_result)}** kết quả")
        show_table(df_result)


    # =========================================================
    # TAB 2: TRA CỨU HÀNG LOẠT (GIỮ NGUYÊN)
    # =========================================================
    with tab2:
        st.caption("Nhập danh sách mã CAS ngăn cách bởi dấu chấm phẩy (;).")
        col_search, col_btn = st.columns([8, 1])
        with col_search:
            search_query = st.text_area("Danh sách mã CAS", height=80, placeholder='"50-00-0"; "67-64-1"')
        with col_btn:
            st.write("")
            st.write("")
            btn_batch_search = st.button("Tìm kiếm", type="primary", use_container_width=True)

        df_batch = pd.DataFrame()
        if search_query:
            keywords = [x.strip().replace('"', '').replace("'", "") for x in search_query.split(';') if x.strip() != '']
            if 'CAS' in df.columns:
                df_batch = df[df['CAS'].isin(keywords)]
            
            st.info(f"Đã tìm thấy **{len(df_batch)}** hóa chất.")
            show_table(df_batch)

    # Footer
    st.markdown('<div class="custom-footer">© 2026 Bản quyền thuộc Cục hóa chất.</div>', unsafe_allow_html=True)

# --- TABLE DISPLAY ---
def show_table(dataframe):
    st.dataframe(
        dataframe,
        use_container_width=True,
        height=500,
        hide_index=True,
        column_config={
            "STT": st.column_config.NumberColumn("STT", width="small"),
            "Tên chất": st.column_config.TextColumn("Tên chất", width="large"),
            "Tên khoa học (danh pháp IUPAC)": st.column_config.TextColumn("Tên IUPAC", width="medium"),
            "CAS": st.column_config.TextColumn("Mã CAS", width="small"),
            "Phụ lục quản lý": st.column_config.TextColumn("Phụ lục quản lý", width="large"),
            "Công thức hóa học": st.column_config.TextColumn("CTHH", width="small"),
            "Ngưỡng khối lượng hóa chất tồn trữ lớn nhất tại một thời điểm (kg)": st.column_config.NumberColumn("Ngưỡng (kg)", width="small"),
            "Link văn bản": st.column_config.LinkColumn("Thao tác", display_text="Xem chi tiết ℹ️")
        }
    )

# --- RUN ---
if st.session_state['logged_in']:
    main_screen()
else:
    login_screen()