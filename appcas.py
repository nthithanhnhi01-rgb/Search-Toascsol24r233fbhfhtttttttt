import streamlit as st
import pandas as pd
from io import BytesIO

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Chemical Regulatory Database", 
    page_icon="🧪", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. NHÚNG CSS CỦA BẠN VÀO STREAMLIT ---
# Tôi đã convert CSS của bạn để nó ép đè lên các widget của Streamlit
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        /* --- COPY CSS CỦA BẠN VÀO ĐÂY --- */
        :root {
            --header-bg: #2d3e50;
            --primary-btn: #3a5a40;
            --batch-btn: #2980b9;
            --batch-bg: #f0f4f8;
        }
        
        /* Ẩn mặc định của Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding-top: 0rem; padding-left: 1rem; padding-right: 1rem;}

        /* Header Custom */
        .site-header {
            background-color: var(--header-bg);
            color: #fff;
            padding: 15px 20px;
            border-bottom: 3px solid #f39c12;
            margin-bottom: 20px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .site-header h1 {
            font-size: 1.4rem; margin: 0; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Container khung search */
        .search-panel {
            background: #fff;
            border: 1px solid #ccc;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            border-radius: 4px;
            padding: 15px;
        }
        
        .search-label {
            font-weight: 700; color: #444; font-size: 0.9rem;
            margin-bottom: 15px; display: block; border-bottom: 2px solid #eee; padding-bottom: 5px;
        }

        /* Ép kiểu cho Input Streamlit giống Bootstrap */
        .stTextInput input {
            border-radius: 0px !important;
            border: 1px solid #bbb !important;
            height: 38px;
        }
        .stTextInput input:focus {
            border-color: #86b7fe !important;
            box-shadow: 0 0 0 0.25rem rgba(13,110,253,.25) !important;
        }

        /* Ép kiểu cho Nút bấm */
        div.stButton > button {
            border-radius: 0px !important;
            font-weight: 600 !important;
            border: none !important;
            height: 38px !important;
        }
        
        /* Footer */
        .custom-footer {
            border-top: 1px solid #dee2e6;
            margin-top: 30px;
            padding: 15px;
            text-align: center;
            font-size: 11px;
            color: #6c757d;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIC PYTHON (GIỮ NGUYÊN TÍNH NĂNG CŨ) ---
@st.cache_data(ttl=600)
def load_data_from_sheet():
    # >>>>> DÁN LINK GOOGLE SHEET CỦA BẠN VÀO ĐÂY <<<<<
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-4uKzaw2LpN5lBOGyG4MB3DPbaC6p6SbtO-yhoEQHRVFx30UHgJOSGfwTn-dOHkhBjAMoDea8n0ih/pub?gid=0&single=true&output=csv" 
    try:
        df = pd.read_csv(sheet_url, dtype=str)
        df.columns = df.columns.str.strip() 
        return df
    except Exception:
        return None

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='KetQuaTraCuu')
    return output.getvalue()

def clear_filter_callback():
    st.session_state["f_cas"] = ""
    st.session_state["f_name"] = ""
    st.session_state["f_formula"] = ""

def clear_batch_callback():
    st.session_state["batch_input"] = ""

# --- 4. HỆ THỐNG ĐĂNG NHẬP ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login_screen():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
            <div style="background-color: #2d3e50; color: white; padding: 20px; text-align: center; border-bottom: 3px solid #f39c12;">
                <h3 style="margin:0">CHEMICAL DATABASE</h3>
                <p style="margin:0; font-size: 12px">Login System</p>
            </div>
            <div style="background-color: white; padding: 30px; border: 1px solid #ddd; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        """, unsafe_allow_html=True)
        username = st.text_input("Tài khoản", placeholder="admin")
        password = st.text_input("Mật khẩu", type="password", placeholder="admin123")
        if st.button("ĐĂNG NHẬP", type="primary", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Sai thông tin đăng nhập")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. GIAO DIỆN CHÍNH (LAYOUT HTML BẠN GỬI) ---
def main_screen():
    # 5.1 HEADER HTML TĨNH (Giống hệt code bạn gửi)
    st.markdown("""
        <div class="site-header">
            <div style="display:flex; align-items:center;">
                <i class="fa-solid fa-layer-group fa-lg" style="margin-right: 15px;"></i>
                <div>
                    <h1>Chemical Regulatory Database</h1>
                    <small style="opacity: 0.8; font-weight: 300;">Hệ thống tra cứu số CAS & Ngưỡng tồn trữ (NĐ 113/2017)</small>
                </div>
            </div>
            <div>
                <span class="badge bg-light text-dark border"><i class="fa-solid fa-user me-1"></i> Admin User</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    df = load_data_from_sheet()
    if df is None:
        st.error("⚠️ Lỗi kết nối Google Sheet.")
        return

    # 5.2 KHUNG SEARCH PANEL (Mô phỏng layout HTML)
    with st.container():
        st.markdown('<div class="search-panel">', unsafe_allow_html=True)
        
        # Chia cột: 7 phần cho Single Search (Xanh rêu), 5 phần cho Batch Search (Xanh dương)
        col_single, col_sep, col_batch = st.columns([7, 0.5, 4.5])
        
        # --- CỘT TRÁI: SINGLE SEARCH ---
        with col_single:
            st.markdown('<label class="search-label"><i class="fa-solid fa-filter me-1"></i> TRA CỨU ĐƠN (FILTER)</label>', unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns([2.5, 4, 2.5, 3])
            with c1:
                st.markdown('<span style="font-size:11px; font-weight:bold; color:#666">Số CAS</span>', unsafe_allow_html=True)
                f_cas = st.text_input("CAS", placeholder="VD: 67-64-1", key="f_cas", label_visibility="collapsed")
            with c2:
                st.markdown('<span style="font-size:11px; font-weight:bold; color:#666">Tên hóa chất (EN/IUPAC)</span>', unsafe_allow_html=True)
                f_name = st.text_input("Name", placeholder="Acetone...", key="f_name", label_visibility="collapsed")
            with c3:
                st.markdown('<span style="font-size:11px; font-weight:bold; color:#666">Công thức</span>', unsafe_allow_html=True)
                f_formula = st.text_input("Formula", placeholder="C3H6O", key="f_formula", label_visibility="collapsed")
            with c4:
                st.markdown('<span style="font-size:11px; font-weight:bold; color:#666">&nbsp;</span>', unsafe_allow_html=True)
                # Nút Refresh (Style xám)
                st.button("🔄 Làm mới", on_click=clear_filter_callback, use_container_width=True)

        # Cột ngăn cách (cho đẹp)
        with col_sep:
            st.write("")

        # --- CỘT PHẢI: BATCH SEARCH ---
        with col_batch:
            # Bọc trong div màu nền nhạt giống design
            st.markdown("""
                <div style="background-color: #f0f4f8; padding: 10px; border-radius: 4px; height: 100%;">
                <label class="search-label" style="color:#2980b9; border-bottom-color:#b0c4de"><i class="fa-solid fa-list-check me-1"></i> TRA CỨU HÀNG LOẠT</label>
            """, unsafe_allow_html=True)
            
            batch_c1, batch_c2 = st.columns([3, 1])
            with batch_c1:
                 batch_input = st.text_input("Batch", placeholder='"67-64-1"; "7664-93-9"', key="batch_input", label_visibility="collapsed")
            with batch_c2:
                 # Nút Search Batch (Style Xanh Dương - Tùy chỉnh màu bằng CSS hack inline)
                 is_batch = st.button("🔎 Tra cứu", type="primary", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # Đóng div search-panel

    # 5.3 XỬ LÝ LOGIC TÌM KIẾM
    df_result = pd.DataFrame()
    mode = "single"

    # Ưu tiên Batch Search nếu bấm nút
    if is_batch and batch_input:
        mode = "batch"
        keywords = [x.strip().replace('"', '').replace("'", "") for x in batch_input.split(';') if x.strip() != '']
        if 'MaCAS' in df.columns:
            df_result = df[df['MaCAS'].isin(keywords)]
    else:
        # Mặc định là Single Filter (Auto)
        df_result = df.copy()
        if f_cas and 'MaCAS' in df_result.columns:
            df_result = df_result[df_result['MaCAS'].astype(str).str.contains(f_cas.strip(), case=False, na=False)]
        if f_name and 'Tên chất' in df_result.columns:
            df_result = df_result[df_result['Tên chất'].astype(str).str.contains(f_name.strip(), case=False, na=False)]
        if f_formula and 'Công thức hóa học' in df_result.columns:
            df_result = df_result[df_result['Công thức hóa học'].astype(str).str.contains(f_formula.strip(), case=False, na=False)]

    # 5.4 HIỂN THỊ KẾT QUẢ (Header bảng + Bảng)
    st.markdown("---")
    res_c1, res_c2 = st.columns([8, 2])
    with res_c1:
        st.markdown(f'<span class="fw-bold text-secondary">Kết quả: {len(df_result)} bản ghi</span>', unsafe_allow_html=True)
    with res_c2:
        if len(df_result) > 0:
            excel_data = to_excel(df_result)
            st.download_button(
                label="📥 Export XLS",
                data=excel_data,
                file_name='KetQua_TraCuu.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )

    # Bảng dữ liệu
    st.dataframe(
        df_result,
        use_container_width=True,
        height=600,
        hide_index=True,
        column_config={
            "STT": st.column_config.NumberColumn("STT", width="small"),
            "MaCAS": st.column_config.TextColumn("Mã CAS", width="small"),
            "Tên chất": st.column_config.TextColumn("Tên chất", width="large"),
            "Tên khoa học (danh pháp IUPAC)": st.column_config.TextColumn("IUPAC / EN", width="medium"),
            "Công thức hóa học": st.column_config.TextColumn("Công thức", width="small"),
            "Phụ lục quản lý": st.column_config.TextColumn("Phân loại / Phụ lục", width="large"),
            "Ngưỡng khối lượng hóa chất tồn trữ lớn nhất tại một thời điểm (kg)": st.column_config.NumberColumn("Ngưỡng (kg)", width="small"),
            "Link văn bản": st.column_config.LinkColumn("Tham khảo", display_text="Xem VB 🔗")
        }
    )

    # 5.5 FOOTER
    st.markdown("""
        <div class="container-fluid border-top mt-3 pt-2 pb-2 text-center text-muted" style="font-size: 11px;">
            © 2026 Shine Group Internal Tool. Data source: National Chemical Database.
        </div>
    """, unsafe_allow_html=True)

# --- RUN APP ---
if st.session_state['logged_in']:
    main_screen()
else:
    login_screen()