import streamlit as st
import pandas as pd
from io import BytesIO

# --- 1. CẤU HÌNH TRANG (Phải để đầu tiên) ---
st.set_page_config(page_title="CAS Regulatory Database", page_icon="🧪", layout="wide")

# --- 2. CSS "THẦN THÁNH" (TÙY BIẾN GIAO DIỆN) ---
st.markdown("""
<style>
    /* Ẩn header/footer mặc định */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}

    /* Style cho Header Custom */
    .custom-header {
        background-color: #2d3e50;
        color: #fff;
        padding: 15px 20px;
        border-bottom: 3px solid #f39c12;
        margin-bottom: 20px;
        border-radius: 4px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Tùy chỉnh Input (Vuông vức, giống Bootstrap) */
    .stTextInput input {
        border-radius: 0px;
        border: 1px solid #ced4da;
    }
    .stTextInput input:focus {
        border-color: #86b7fe;
        box-shadow: none;
    }
    
    /* Nút Search Đơn (Primary Button - Xanh) */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #3a5a40;
        color: white;
        border-radius: 0px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background-color: #2c4431;
    }

    /* Nút Search Batch (Secondary Button - Xanh dương) */
    div[data-testid="stButton"] > button[kind="secondary"] {
        background-color: #2980b9;
        color: white;
        border-radius: 0px;
        border: none;
        width: 100%;
    }
    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background-color: #1c6ea4;
        color: white; /* Fix lỗi chữ bị đen khi hover */
    }

    /* Style riêng cho khu vực Batch (Cột bên phải) */
    /* Hack: Tìm div chứa class batch-area-marker để tô màu nền cha của nó */
    [data-testid="stVerticalBlockBorderWrapper"]:has(.batch-area-marker) {
        background-color: #f8f9fa;
        border-left: 1px dashed #b0c4de;
        padding: 15px !important;
    }
    
    /* Chỉnh font size bảng kết quả */
    div[data-testid="stDataFrame"] {
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HÀM LOAD DỮ LIỆU TỪ GOOGLE SHEET ---
@st.cache_data(ttl=600)
def load_data():
    # Thay Link Google Sheet CSV của bạn vào đây
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-4uKzaw2LpN5lBOGyG4MB3DPbaC6p6SbtO-yhoEQHRVFx30UHgJOSGfwTn-dOHkhBjAMoDea8n0ih/pub?gid=0&single=true&output=csv"
    try:
        df = pd.read_csv(sheet_url, dtype=str)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

# --- 4. HÀM XUẤT EXCEL ---
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='KetQua')
    return output.getvalue()

# --- 5. HỆ THỐNG ĐĂNG NHẬP (GIỮ NGUYÊN) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login_screen():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.info("Vui lòng đăng nhập hệ thống")
        username = st.text_input("Tài khoản", placeholder="admin")
        password = st.text_input("Mật khẩu", type="password", placeholder="admin123")
        if st.button("Đăng nhập", type="primary", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Sai tài khoản/mật khẩu")

# --- 6. GIAO DIỆN CHÍNH ---
def main_app():
    # A. HEADER HTML
    st.markdown("""
    <div class="custom-header" style="display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 24px; margin-right: 15px;">🧪</div>
            <div>
                <h1 style="font-size: 1.4rem; margin: 0; text-transform: uppercase; font-family: sans-serif;">Chemical Regulatory Database</h1>
                <small style="opacity: 0.8; font-weight: 300;">Hệ thống tra cứu số CAS & Ngưỡng tồn trữ (NĐ 113/2017)</small>
            </div>
        </div>
        <span style="background: rgba(255,255,255,0.2); color: #fff; padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: bold;">
            👤 Admin User
        </span>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()

    # B. SEARCH PANEL
    with st.container(border=True):
        col_single, col_batch = st.columns([2.2, 1], gap="large")

        # --- CỘT TRÁI: TRA CỨU ĐƠN ---
        with col_single:
            st.markdown("##### <i class='fa-solid fa-filter'></i> TRA CỨU ĐƠN (FILTER)", unsafe_allow_html=True)
            st.write("") # Spacer
            
            # Layout 4 cột
            c1, c2, c3, c4 = st.columns([2, 3, 2, 1.5], vertical_alignment="bottom")
            
            with c1:
                cas_input = st.text_input("Số CAS", placeholder="VD: 67-64-1", key="s_cas")
            with c2:
                name_input = st.text_input("Tên hóa chất (EN/VI)", placeholder="Acetone...", key="s_name")
            with c3:
                formula_input = st.text_input("Công thức", placeholder="C3H6O", key="s_form")
            with c4:
                # Dùng type="primary" để CSS bắt được và tô màu xanh rêu
                btn_single = st.button("Tìm kiếm", type="primary", use_container_width=True)

            st.caption("ℹ️ *Nhập 1 hoặc kết hợp nhiều ô để lọc chính xác.*")

        # --- CỘT PHẢI: TRA CỨU BATCH ---
        with col_batch:
            # Marker để CSS tô màu nền cột này
            st.markdown('<div class="batch-area-marker"></div>', unsafe_allow_html=True)
            
            st.markdown("##### <i class='fa-solid fa-list'></i> TRA CỨU HÀNG LOẠT", unsafe_allow_html=True)
            
            cb1, cb2 = st.columns([4, 1], vertical_alignment="bottom")
            with cb1:
                batch_input = st.text_input("Nhập list CAS (;)", placeholder='"67-64-1"; "7664-93-9"', label_visibility="collapsed")
            with cb2:
                # Dùng type="secondary" để CSS bắt được và tô màu xanh dương
                btn_batch = st.button("🔎", type="secondary", use_container_width=True)

    # C. LOGIC XỬ LÝ & BẢNG KẾT QUẢ
    result_df = pd.DataFrame()
    
    # Logic Lọc
    if df is not None and not df.empty:
        result_df = df.copy()
        
        # Ưu tiên Batch Search trước
        if btn_batch and batch_input:
            cas_list = [x.strip().replace('"', '').replace("'", "") for x in batch_input.split(";") if x.strip()]
            if 'MaCAS' in result_df.columns:
                result_df = result_df[result_df["MaCAS"].isin(cas_list)]
        
        # Nếu không Batch thì check Single Search
        # (Hoặc nếu user không bấm nút nào thì hiện full bảng hoặc rỗng tùy bạn, ở đây mình để logic Auto-Filter khi nhập liệu)
        elif cas_input or name_input or formula_input:
             if cas_input and 'MaCAS' in result_df.columns:
                 result_df = result_df[result_df["MaCAS"].astype(str).str.contains(cas_input.strip(), case=False, na=False)]
             if name_input and 'Tên chất' in result_df.columns:
                 # Tìm trên cả cột Tên chất và Tên IUPAC (nếu có)
                 mask = result_df["Tên chất"].astype(str).str.contains(name_input.strip(), case=False, na=False)
                 if 'Tên khoa học (danh pháp IUPAC)' in result_df.columns:
                     mask = mask | result_df["Tên khoa học (danh pháp IUPAC)"].astype(str).str.contains(name_input.strip(), case=False, na=False)
                 result_df = result_df[mask]
             if formula_input and 'Công thức hóa học' in result_df.columns:
                 result_df = result_df[result_df["Công thức hóa học"].astype(str).str.contains(formula_input.strip(), case=False, na=False)]
        else:
             # Mặc định khi chưa tìm gì: Có thể để rỗng hoặc hiện 10 dòng đầu
             pass

    # D. HIỂN THỊ KẾT QUẢ
    st.markdown("---")
    
    col_info, col_export = st.columns([8, 2], vertical_alignment="center")
    with col_info:
        if not result_df.empty:
            st.success(f"Tìm thấy **{len(result_df)}** kết quả phù hợp.")
        else:
            st.info("Vui lòng nhập thông tin tìm kiếm.")
            
    with col_export:
        if not result_df.empty:
            excel_data = to_excel(result_df)
            st.download_button(
                label="📥 Xuất Excel",
                data=excel_data,
                file_name="KetQua_TraCuu.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    # Dùng st.dataframe (Native) - Đảm bảo không bị lỗi hiển thị
    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True,
        height=500,
        column_config={
            "STT": st.column_config.NumberColumn("STT", width="small"),
            "MaCAS": st.column_config.TextColumn("Mã CAS", width="small"),
            "Tên chất": st.column_config.TextColumn("Tên chất", width="large"),
            "Tên khoa học (danh pháp IUPAC)": st.column_config.TextColumn("Tên IUPAC", width="medium"),
            "Công thức hóa học": st.column_config.TextColumn("CTHH", width="small"),
            "Ngưỡng khối lượng hóa chất tồn trữ lớn nhất tại một thời điểm (kg)": st.column_config.TextColumn("Ngưỡng (kg)", width="medium", help="Theo NĐ 113/2017"),
            "Link văn bản": st.column_config.LinkColumn("Thao tác", display_text="Xem VB 🔗")
        }
    )

    # Footer
    st.markdown("""
    <div style="text-align: center; font-size: 12px; color: #888; margin-top: 30px; border-top: 1px solid #eee; padding-top: 10px;">
        © 2026 Shine Group Internal Tool. Data source: National Chemical Database.
    </div>
    """, unsafe_allow_html=True)

# --- RUN APP ---
if st.session_state['logged_in']:
    main_app()
else:
    login_screen()