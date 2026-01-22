import streamlit as st
import pandas as pd

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Cơ sở dữ liệu Hóa chất Quốc gia", 
    page_icon="🇻🇳", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS TÙY CHỈNH GIAO DIỆN (TAB & HEADER) ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Arial', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* HEADER XANH */
    .header-custom {
        background-color: #0066b3;
        padding: 15px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #004d88;
        color: white;
        margin-bottom: 20px;
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

    /* NAVBAR */
    .navbar {
        background-color: #005a9e; padding: 8px 30px; display: flex; gap: 25px; border-bottom: 4px solid #e9ecef; margin-bottom: 20px;
    }
    .nav-item {
        color: white; text-decoration: none; font-size: 14px; font-weight: 500; display: flex; align-items: center; gap: 5px;
    }
    .nav-item:hover { color: #ffcc00; }

    /* TÙY CHỈNH TAB (Để giống nút bấm màu xanh trong hình) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #007bff !important;
        color: white !important;
    }

    /* FOOTER */
    .custom-footer {
        background-color: #0066b3; color: white; padding: 20px; text-align: center;
        font-size: 13px; margin-top: 50px; border-top: 4px solid #ffcc00;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HÀM LOAD DỮ LIỆU ---
@st.cache_data(ttl=600)
def load_data_from_sheet():
    # Link Google Sheet CSV của bạn
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-4uKzaw2LpN5lBOGyG4MB3DPbaC6p6SbtO-yhoEQHRVFx30UHgJOSGfwTn-dOHkhBjAMoDea8n0ih/pub?gid=0&single=true&output=csv" 
    
    try:
        df = pd.read_csv(sheet_url, dtype=str)
        # Chuẩn hóa tên cột: Xóa khoảng trắng thừa ở tên cột (nếu có) để tránh lỗi không tìm thấy cột
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return None

# --- 4. HỆ THỐNG ĐĂNG NHẬP ---
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

# --- 5. GIAO DIỆN CHÍNH ---
def main_screen():
    # Header & Navbar
    st.markdown("""
        <div class="header-custom">
            <div class="header-logo-area">
                <h1>CƠ SỞ DỮ LIỆU CHUYÊN NGÀNH HÓA CHẤT</h1>
                <p>VIETNAM CHEMICAL DATABASE</p>
            </div>
            <div class="user-profile">
                👤 Người dùng: <b>Admin</b> | <a href="#" style="color:white; text-decoration:none;">Thoát</a>
            </div>
        </div>
        <div class="navbar">
            <a href="#" class="nav-item">🏠 Trang chủ</a>
            <a href="#" class="nav-item">📚 Tài liệu</a>
            <a href="#" class="nav-item">🔍 Tìm kiếm</a>
        </div>
    """, unsafe_allow_html=True)

    # Tiêu đề trang
    st.markdown('<h2 style="color: #444; border-bottom: 2px solid #0066b3; padding-bottom: 10px;">Tra cứu Danh mục Hóa chất & Ngưỡng tồn trữ</h2>', unsafe_allow_html=True)

    # Tải dữ liệu
    df = load_data_from_sheet()
    
    if df is None:
        st.error("⚠️ Không tải được dữ liệu từ Google Sheet. Vui lòng kiểm tra lại đường link hoặc quyền truy cập.")
        return

    # --- TẠO 2 TAB TRA CỨU (TAB GIAO DIỆN) ---
    tab1, tab2 = st.tabs(["🔍 Tra cứu đơn (Filter)", "🔢 Tra cứu hàng loạt"])

    # ==========================
    # TAB 1: TRA CỨU ĐƠN (FILTER)
    # ==========================
    with tab1:
        st.caption("Nhập thông tin vào các ô bên dưới để lọc dữ liệu (Hỗ trợ tìm kiếm theo tên hoặc mã CAS).")
        
        # Tạo 4 cột nhập liệu giống hình mẫu
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        
        with col_f1:
            filter_cas = st.text_input("Mã CAS", placeholder="VD: 50-00-0")
        with col_f2:
            filter_name = st.text_input("Tên hóa chất (Tiếng Anh/Việt)", placeholder="VD: Formaldehyde")
        with col_f3:
            filter_formula = st.text_input("Công thức hóa học", placeholder="VD: HCHO")
        with col_f4:
            st.write("") # Placeholder cho cân đối
            st.info("Nhập và nhấn Enter để tìm")

        # Logic lọc dữ liệu cho Tab 1
        df_result_t1 = df.copy()
        
        if filter_cas:
            # Lọc theo CAS (chứa chuỗi nhập vào)
            if 'CAS' in df.columns:
                df_result_t1 = df_result_t1[df_result_t1['CAS'].astype(str).str.contains(filter_cas.strip(), case=False, na=False)]
        
        if filter_name:
            # Lọc theo Tên chất (chứa chuỗi nhập vào)
            if 'Tên chất' in df.columns:
                df_result_t1 = df_result_t1[df_result_t1['Tên chất'].astype(str).str.contains(filter_name.strip(), case=False, na=False)]
        
        if filter_formula:
             if 'Công thức hóa học' in df.columns:
                df_result_t1 = df_result_t1[df_result_t1['Công thức hóa học'].astype(str).str.contains(filter_formula.strip(), case=False, na=False)]

        # Hiển thị kết quả Tab 1
        st.write(f"Tìm thấy: **{len(df_result_t1)}** kết quả")
        show_table(df_result_t1)


    # ==========================
    # TAB 2: TRA CỨU HÀNG LOẠT
    # ==========================
    with tab2:
        st.caption("Nhập danh sách mã CAS ngăn cách bởi dấu chấm phẩy (;). Ví dụ: \"50-00-0\"; \"67-64-1\"")
        
        col_search, col_btn = st.columns([8, 1])
        with col_search:
            search_query = st.text_area("Nhập danh sách mã CAS", height=80, placeholder='"50-00-0"; "67-64-1"; 7732-18-5')
        with col_btn:
            st.write("")
            st.write("")
            btn_batch_search = st.button("Tìm kiếm", type="primary", use_container_width=True)

        # Logic lọc dữ liệu cho Tab 2
        df_result_t2 = pd.DataFrame() # Mặc định rỗng
        
        if search_query:
            # XỬ LÝ CHUỖI NHẬP VÀO:
            # 1. Tách bằng dấu chấm phẩy
            # 2. Xóa khoảng trắng thừa
            # 3. Xóa dấu ngoặc kép " hoặc ' nếu có (để xử lý trường hợp user copy từ Excel có format text)
            keywords = [x.strip().replace('"', '').replace("'", "") for x in search_query.split(';') if x.strip() != '']
            
            if 'CAS' in df.columns:
                # Dùng hàm .isin để tìm chính xác các mã trong list
                df_result_t2 = df[df['CAS'].isin(keywords)]
            else:
                st.error("Lỗi: File dữ liệu không có cột tên là 'CAS'. Vui lòng kiểm tra Google Sheet.")
        
        # Hiển thị kết quả Tab 2
        if search_query:
            st.success(f"Đã tìm thấy **{len(df_result_t2)}** hóa chất khớp với danh sách.")
            show_table(df_result_t2)
        else:
            st.info("Vui lòng nhập mã CAS để bắt đầu tra cứu.")

    # Footer
    st.markdown("""
        <div class="custom-footer">
            © 2026 Bản quyền thuộc Cục hóa chất - Bộ Công thương.<br>
            Email: admin@chemicaldata.gov.vn.
        </div>
    """, unsafe_allow_html=True)

# --- HÀM HIỂN THỊ BẢNG (Dùng chung cho cả 2 tab) ---
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
            "Công thức hóa học": st.column_config.TextColumn("Công thức", width="small"),
            "Ngưỡng khối lượng hóa chất tồn trữ lớn nhất tại một thời điểm (kg)": st.column_config.NumberColumn("Ngưỡng tồn trữ (kg)", width="small"),
            "Link văn bản": st.column_config.LinkColumn("Thao tác", display_text="Xem chi tiết ℹ️")
        }
    )

# --- 6. CHẠY APP ---
if st.session_state['logged_in']:
    main_screen()
else:
    login_screen()