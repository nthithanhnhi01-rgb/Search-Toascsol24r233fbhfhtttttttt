import streamlit as st
import pandas as pd

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Cơ sở dữ liệu Hóa chất Quốc gia", 
    page_icon="🇻🇳", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS "THẦN THÁNH" ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Arial', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* HEADER */
    .header-custom {
        background-color: #0066b3;
        padding: 15px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #004d88;
        color: white;
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
        background-color: #005a9e; padding: 8px 30px; display: flex; gap: 25px; border-bottom: 4px solid #e9ecef;
    }
    .nav-item {
        color: white; text-decoration: none; font-size: 14px; font-weight: 500; display: flex; align-items: center; gap: 5px;
    }
    .nav-item:hover { color: #ffcc00; }

    /* CONTENT */
    .page-title {
        color: #d93025; font-size: 26px; font-weight: bold;
        margin-top: 20px; margin-bottom: 15px; padding-left: 10px; border-left: 5px solid #d93025;
    }
    .custom-footer {
        background-color: #0066b3; color: white; padding: 20px; text-align: center;
        font-size: 13px; margin-top: 50px; border-top: 4px solid #ffcc00;
    }
    .stButton button {
        background-color: #f6b93b !important; color: #000 !important; border: none !important; font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HÀM LOAD DỮ LIỆU TỪ GOOGLE SHEETS (QUAN TRỌNG) ---
# Dùng @st.cache_data để không phải tải lại mỗi khi bấm nút (giúp web nhanh hơn)
@st.cache_data(ttl=600) # 600 giây (10 phút) sẽ tự cập nhật dữ liệu mới 1 lần
def load_data_from_sheet():
    # -----------------------------------------------------------------------------------------
    # BƯỚC QUAN TRỌNG: DÁN LINK CSV CỦA BẠN VÀO DƯỚI ĐÂY
    # (File -> Share -> Publish to Web -> Chọn CSV -> Copy Link)
    # -----------------------------------------------------------------------------------------
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-4uKzaw2LpN5lBOGyG4MB3DPbaC6p6SbtO-yhoEQHRVFx30UHgJOSGfwTn-dOHkhBjAMoDea8n0ih/pub?gid=0&single=true&output=csv" 
    
    try:
        # Nếu chưa có link (đang test), dùng dữ liệu giả
        if "HÃY_DÁN" in sheet_url:
            return None 
            
        df = pd.read_csv(sheet_url, dtype=str)
        return df
    except Exception as e:
        return None

# Dữ liệu giả lập (Backup khi chưa có link thật)
def get_mock_data():
    data_mock = {
        'STT': [1, 2, 3],
        'Mã': ['Nci No: 123', 'Nci No: 456', 'Nci No: 789'],
        'Cas': ['50-00-0', '50-01-1', '50-02-2'],
        'Tên chất': ['Formaldehyde', 'Salt of hydrogen', 'Fluoro-11beta'],
        'Phụ lục quản lý': ['Khai báo', 'Không quy định', 'Hạn chế'],
        'LinkVanBan': ['https://vanban.chinhphu.vn', '', '']
    }
    return pd.DataFrame(data_mock)

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
    # Header & Navbar HTML
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

    st.markdown('<div class="page-title">Hóa chất</div>', unsafe_allow_html=True)

    # --- KHUNG TÌM KIẾM ---
    col_search, col_btn = st.columns([8, 1])
    with col_search:
        # Ô nhập liệu
        search_query = st.text_input("Nội dung cần tìm", label_visibility="collapsed", placeholder="Nhập mã CAS (ví dụ: 50-00-0; 50-01-1)...")
    with col_btn:
        # Nút bấm
        btn_search = st.button("➕ Tìm kiếm")

    # --- XỬ LÝ DỮ LIỆU ---
    df = load_data_from_sheet()
    
    # Nếu tải Google Sheet lỗi hoặc chưa nhập link thì dùng dữ liệu giả
    if df is None:
        if "HÃY_DÁN" in "HÃY_DÁN": # Chỉ hiện thông báo này khi bạn chưa sửa code
            st.warning("⚠️ Bạn chưa dán link Google Sheet vào code. Đang hiển thị dữ liệu mẫu.")
        df = get_mock_data()

    # --- LOGIC LỌC DỮ LIỆU (SEARCH) ---
    # Nếu người dùng bấm nút Tìm hoặc đã nhập chữ và Enter
    if search_query:
        # Tách chuỗi nhập vào bằng dấu chấm phẩy ; (Ví dụ: "50-00-0; 64-17-5")
        keywords = [x.strip() for x in search_query.split(';') if x.strip() != '']
        
        # Lọc trong cột 'Cas' (Bạn phải đảm bảo Google Sheet có cột tên là 'Cas')
        # Nếu muốn tìm cả Tên chất thì dùng logic OR (|)
        if 'Cas' in df.columns:
            df = df[df['Cas'].isin(keywords)]
        else:
            st.error("Lỗi: Dữ liệu không có cột tên là 'Cas'. Hãy kiểm tra lại Google Sheet.")

    # --- HIỂN THỊ BẢNG KẾT QUẢ ---
    st.markdown(f"##### Danh mục chất ({len(df)} kết quả)")
    
    st.dataframe(
        df,
        use_container_width=True,
        height=500,
        hide_index=True,
        column_config={
            "STT": st.column_config.NumberColumn("STT", width="small"),
            "Tên chất": st.column_config.TextColumn("Tên chất", width="large"),
"Tên khoa học (danh pháp IUPAC)":st.column_config.TextColumn("Tên khoa học (danh pháp IUPAC)", width="small"),
            "CAS": st.column_config.TextColumn("MaCAS", width="medium"),
            "Tên chất": st.column_config.TextColumn("Tên chất", width="large"),
            "Phụ lục quản lý": st.column_config.TextColumn("Phụ lục quản lý", width="large"),
"Công thức hóa học":st.column_config.TextColumn("Công thức hóa học", width="small"),
"Ngưỡng khối lượng hóa chất tồn trữ lớn nhất tại một thời điểm (kg)":st.column_config.TextColumn("Ngưỡng khối lượng hóa chất tồn trữ lớn nhất tại một thời điểm (kg)", width="small"),
            "Link văn bản": st.column_config.LinkColumn("Thao tác", display_text="Xem chi tiết ℹ️")
        }
    )

    st.markdown("""
        <div class="custom-footer">
            © 2026 Bản quyền thuộc Cục hóa chất - Bộ Công thương.<br>
            Email: admin@chemicaldata.gov.vn.
        </div>
    """, unsafe_allow_html=True)

# --- 6. CHẠY APP ---
if st.session_state['logged_in']:
    main_screen()
else:

    login_screen()
