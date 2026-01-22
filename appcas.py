import streamlit as st
import pandas as pd
from io import BytesIO

# --- 1. CẤU HÌNH TRANG WEB (TAB BROWSER) ---
st.set_page_config(
    page_title="Cơ sở dữ liệu Hóa chất Quốc gia", 
    page_icon="🇻🇳", 
    layout="wide",
    initial_sidebar_state="collapsed" # Ẩn thanh bên cho giống web thật
)

# --- 2. CSS "THẦN THÁNH" (ĐỂ GIỐNG GIAO DIỆN CỤC HÓA CHẤT) ---
st.markdown("""
    <style>
    /* Chỉnh font chữ toàn trang */
    html, body, [class*="css"] {
        font-family: 'Arial', sans-serif;
    }
    
    /* Ẩn bớt các thành phần thừa của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;} /* Ẩn thanh màu trên cùng của Streamlit */

    /* HEADER XANH ĐẬM (GIỐNG ẢNH 1) */
    .header-custom {
        background-color: #0066b3; /* Màu xanh chuẩn Cục HC */
        padding: 15px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #004d88;
        color: white;
    }
    .header-logo-area h1 {
        color: white !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        text-transform: uppercase;
        padding: 0 !important;
        line-height: 1.2;
    }
    .header-logo-area p {
        color: #ffcc00 !important; /* Chữ vàng Vietnam Chemical Database */
        font-size: 14px !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }
    .user-profile {
        font-size: 14px;
        background: #005091;
        padding: 5px 15px;
        border-radius: 4px;
    }

    /* THANH MENU NGANG (Nav Bar) */
    .navbar {
        background-color: #005a9e;
        padding: 8px 30px;
        display: flex;
        gap: 25px;
        border-bottom: 4px solid #e9ecef;
    }
    .nav-item {
        color: white;
        text-decoration: none;
        font-size: 14px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .nav-item:hover { color: #ffcc00; }

    /* TIÊU ĐỀ TRANG (Chữ "Hóa chất" màu đỏ) */
    .page-title {
        color: #d93025;
        font-size: 26px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
        padding-left: 10px;
        border-left: 5px solid #d93025;
    }

    /* FOOTER (Chân trang) */
    .custom-footer {
        background-color: #0066b3;
        color: white;
        padding: 20px;
        text-align: center;
        font-size: 13px;
        margin-top: 50px;
        border-top: 4px solid #ffcc00;
    }

    /* Tùy chỉnh nút bấm Search cho giống */
    .stButton button {
        background-color: #f6b93b !important; /* Màu cam giống nút cộng */
        color: #000 !important;
        border: none !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DỮ LIỆU GIẢ LẬP (ĐỂ BẠN TEST KHI CHƯA CÓ FILE EXCEL CHUẨN) ---
# Khi nào chạy thật thì xóa đoạn này đi và dùng pd.read_excel
data_mock = {
    'STT': [1, 2, 3],
    'Mã': ['Nci No: \nHSCode:', 'Nci No: \nHSCode:', 'Nci No: \nHSCode:'],
    'Cas': ['50-00-0', '50-01-1', '50-02-2'],
    'Tên chất': [
        'Tiếng Việt: Formaldehyde\nQuốc tế: Formaldehyde', 
        'Tiếng Việt: Salt of hydrogen...\nQuốc tế: Salt of hydrogen...',
        'Tiếng Việt: 9-Fluoro...\nQuốc tế: 9-Fluoro...'
    ],
    'Phụ lục quản lý': [
        'Nghị định 113/2017/NĐ-CP: Hóa chất phải khai báo',
        'Không quy định',
        'Nghị định 113/2017/NĐ-CP: Hạn chế sản xuất'
    ],
    'LinkVanBan': ['https://vanban.chinhphu.vn', '', 'https://thuvienphapluat.vn']
}
df_mock = pd.DataFrame(data_mock)

# --- 4. HỆ THỐNG ĐĂNG NHẬP (GIỮ NGUYÊN) ---
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

# --- 5. GIAO DIỆN CHÍNH (SAU KHI LOGIN) ---
def main_screen():
    # A. HEADER HTML (Vẽ thủ công cho giống ảnh 1)
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
            <a href="#" class="nav-item">📞 Liên hệ</a>
        </div>
    """, unsafe_allow_html=True)

    # B. PHẦN NỘI DUNG CHÍNH
    st.markdown('<div class="page-title">Hóa chất</div>', unsafe_allow_html=True)

    # Thanh tìm kiếm (Mô phỏng)
    col_search, col_btn = st.columns([8, 1])
    with col_search:
        search_query = st.text_input("Nội dung cần tìm", label_visibility="collapsed", placeholder="Nhập tên chất, mã CAS, mã HS...")
    with col_btn:
        st.button("➕ Tìm kiếm")

    # Xử lý dữ liệu (Dùng file Excel thật nếu có, không thì dùng Mock)
    try:
        df = pd.read_excel("dataCAS.xlsx", dtype=str)
    except:
        df = df_mock # Dùng dữ liệu giả nếu không thấy file Excel

    # Hiển thị bảng kết quả
    st.markdown("##### Danh mục chất")
    
    # Cấu hình bảng cho đẹp
    st.dataframe(
        df,
        use_container_width=True,
        height=500,
        hide_index=True,
        column_config={
            "STT": st.column_config.NumberColumn("STT", width="small"),
            "Mã": st.column_config.TextColumn("Mã", width="small"), # Cột này chứa Nci No, HSCode
            "Cas": st.column_config.TextColumn("Cas", width="small"),
            "Tên chất": st.column_config.TextColumn("Tên chất", width="large"), # Cho rộng ra để hiện tên dài
            "Phụ lục quản lý": st.column_config.TextColumn("Phụ lục quản lý", width="large"),
            "LinkVanBan": st.column_config.LinkColumn("Thao tác", display_text="Xem chi tiết ℹ️")
        }
    )

    # C. FOOTER
    st.markdown("""
        <div class="custom-footer">
            © 2026 Bản quyền thuộc Cục hóa chất - Bộ Công thương.<br>
            Địa chỉ: 21 Ngô Quyền, Tràng Tiền, Hoàn Kiếm, Hà Nội.<br>
            Email: admin@chemicaldata.gov.vn. Website: www.cuchoachat.gov.vn
        </div>
    """, unsafe_allow_html=True)

# --- 6. CHẠY APP ---
if st.session_state['logged_in']:
    main_screen()
else:
    login_screen()