import streamlit as st
import pandas as pd
from io import BytesIO

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Chemical Regulatory Database", page_icon="🧪", layout="wide")

# --- 2. CSS "CARD UI" (TẠO KHỐI NỔI 3D) ---
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* Ẩn header/footer mặc định */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}

    /* HEADER STYLE */
    .custom-header {
        background: linear-gradient(90deg, #2d3e50 0%, #4b6cb7 100%);
        color: #fff;
        padding: 20px 25px;
        border-bottom: 4px solid #f39c12;
        margin-bottom: 30px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* CARD STYLE (BIẾN KHUNG THÀNH KHỐI NỔI) */
    /* Target vào container có viền của Streamlit */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px; /* Bo góc mềm mại */
        border: 1px solid #f0f0f0; /* Viền mờ */
        background-color: white;
        /* ĐỔ BÓNG TẠO ĐỘ NỔI (Shadow) */
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s; /* Hiệu ứng nhún nhẹ nếu muốn */
        padding: 10px;
    }
    
    /* CARD HEADER (TIÊU ĐỀ TRONG KHỐI) */
    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #f1f1f1;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .card-icon {
        color: #0066b3; /* Màu xanh icon */
        font-size: 1.2rem;
    }

    /* INPUT STYLE */
    .stTextInput input {
        border-radius: 6px;
        border: 1px solid #d1d5db;
        padding: 8px 12px;
    }
    .stTextInput input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
    }

    /* BUTTONS */
    div[data-testid="stButton"] > button {
        border-radius: 6px;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.2s;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    
    /* BẢNG KẾT QUẢ */
    div[data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOAD DATA ---
@st.cache_data(ttl=600)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-4uKzaw2LpN5lBOGyG4MB3DPbaC6p6SbtO-yhoEQHRVFx30UHgJOSGfwTn-dOHkhBjAMoDea8n0ih/pub?gid=0&single=true&output=csv"
    try:
        df = pd.read_csv(sheet_url, dtype=str)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='KetQua')
    return output.getvalue()

# --- 4. AUTH ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        # Dùng container border=True để nó tự nhận CSS Shadow ở trên
        with st.container(border=True):
            st.markdown("<h3 style='text-align:center;'>Đăng nhập hệ thống</h3>", unsafe_allow_html=True)
            u = st.text_input("Tài khoản")
            p = st.text_input("Mật khẩu", type="password")
            if st.button("Đăng nhập", type="primary", use_container_width=True):
                if u == "admin" and p == "admin123":
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("Sai thông tin")

# --- 5. MAIN APP ---
def main_app():
    # A. HEADER
    st.markdown("""
    <div class="custom-header">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:15px;">
                <i class="fa-solid fa-flask-vial fa-2xl"></i>
                <div>
                    <h1 style="margin:0; font-size:1.5rem; text-transform:uppercase;">Chemical Regulatory Database</h1>
                    <div style="opacity:0.9; font-size:0.9rem;">Hệ thống tra cứu số CAS & Ngưỡng tồn trữ</div>
                </div>
            </div>
            <div style="background:rgba(255,255,255,0.2); padding:5px 15px; border-radius:20px; font-weight:bold;">
                <i class="fa-regular fa-user"></i> Admin
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()

    # B. GIAO DIỆN TÌM KIẾM (2 KHỐI SONG SONG CÓ BÓNG ĐỔ)
    # Tỷ lệ 2.5 : 1
    col_single, col_batch = st.columns([2.5, 1], gap="medium")

    # --- KHỐI 1: TRA CỨU ĐƠN ---
    with col_single:
        # st.container(border=True) sẽ tự động nhận CSS box-shadow ở trên
        with st.container(border=True):
            # Header có Icon
            st.markdown("""
                <div class="card-title">
                    <i class="card-icon fa-solid fa-filter"></i> TRA CỨU ĐƠN (FILTER)
                </div>
            """, unsafe_allow_html=True)
            
            # Input Area
            c1, c2, c3 = st.columns([1.5, 3, 1.5])
            with c1:
                cas_input = st.text_input("Số CAS", placeholder="VD: 67-64-1")
            with c2:
                name_input = st.text_input("Tên hóa chất (EN/VI)", placeholder="Acetone...")
            with c3:
                formula_input = st.text_input("Công thức", placeholder="C3H6O")
            
            # Nút tìm kiếm nằm riêng 1 dòng cho thoáng hoặc để cùng dòng tùy bạn
            # Ở đây tôi để nút Tìm kiếm Full width phía dưới cho đẹp
            st.write("")
            btn_single = st.button("🔍 Tìm kiếm ngay", type="primary", use_container_width=True)

    # --- KHỐI 2: TRA CỨU HÀNG LOẠT ---
    with col_batch:
        with st.container(border=True):
            # Header có Icon
            st.markdown("""
                <div class="card-title">
                    <i class="card-icon fa-solid fa-list-check"></i> TRA CỨU HÀNG LOẠT
                </div>
            """, unsafe_allow_html=True)
            
            # Input Area
            batch_input = st.text_area("Nhập list CAS", height=108, placeholder='"67-64-1"; "7664-93-9"', label_visibility="collapsed")
            
            st.write("")
            btn_batch = st.button("🚀 Tra cứu Batch", type="secondary", use_container_width=True)

    # C. LOGIC LỌC DỮ LIỆU
    result_df = pd.DataFrame()
    if df is not None and not df.empty:
        # Logic Batch
        if btn_batch and batch_input:
            keywords = [x.strip().replace('"', '').replace("'", "") for x in batch_input.split(';') if x.strip()]
            if 'MaCAS' in df.columns:
                result_df = df[df['MaCAS'].isin(keywords)]
        # Logic Single (Auto Filter khi bấm nút hoặc gõ)
        elif cas_input or name_input or formula_input:
            result_df = df.copy()
            if cas_input and 'MaCAS' in result_df.columns:
                result_df = result_df[result_df["MaCAS"].astype(str).str.contains(cas_input.strip(), case=False, na=False)]
            if name_input and 'Tên chất' in result_df.columns:
                 mask = result_df["Tên chất"].astype(str).str.contains(name_input.strip(), case=False, na=False)
                 if 'Tên khoa học (danh pháp IUPAC)' in result_df.columns:
                     mask = mask | result_df["Tên khoa học (danh pháp IUPAC)"].astype(str).str.contains(name_input.strip(), case=False, na=False)
                 result_df = result_df[mask]
            if formula_input and 'Công thức hóa học' in result_df.columns:
                result_df = result_df[result_df["Công thức hóa học"].astype(str).str.contains(formula_input.strip(), case=False, na=False)]
        else:
            # Nếu chưa làm gì thì để trống hoặc hiện tất cả (tùy bạn), ở đây mình để trống cho gọn
            pass

    # D. HIỂN THỊ KẾT QUẢ
    st.write("---")
    
    # Thanh công cụ kết quả
    c_res_1, c_res_2 = st.columns([8, 2], vertical_alignment="center")
    with c_res_1:
        if not result_df.empty:
            st.success(f"✅ Tìm thấy **{len(result_df)}** kết quả phù hợp.")
        else:
            if btn_single or btn_batch:
                st.warning("Không tìm thấy kết quả nào.")
            else:
                st.info("👋 Vui lòng nhập thông tin để tra cứu.")

    with c_res_2:
        if not result_df.empty:
            excel_data = to_excel(result_df)
            st.download_button("📥 Xuất Excel", excel_data, "KetQua.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

    # Bảng dữ liệu
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
            "Ngưỡng khối lượng hóa chất tồn trữ lớn nhất tại một thời điểm (kg)": st.column_config.TextColumn("Ngưỡng (kg)", width="medium"),
            "Link văn bản": st.column_config.LinkColumn("Văn bản", display_text="Xem ngay 🔗")
        }
    )

    st.markdown("<div style='text-align:center; color:#999; margin-top:50px; font-size:12px;'>© 2026 Shine Group System</div>", unsafe_allow_html=True)

# --- RUN ---
if st.session_state['logged_in']:
    main_app()
else:
    login_screen()