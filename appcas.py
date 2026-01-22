import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="Chemical Regulatory Database", page_icon="🧪", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS "ÉP GIAO DIỆN" (FIXED & POLISHED) ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        /* RESET & FONT */
        body { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f6f9; font-size: 14px; color: #333; }
        
        /* Ẩn Header mặc định */
        #MainMenu, footer, header {visibility: hidden;}
        .block-container { padding-top: 0rem; padding-bottom: 2rem; padding-left: 1rem; padding-right: 1rem; }

        /* --- A. HEADER --- */
        .site-header {
            background-color: #2d3e50; color: #fff; padding: 15px 20px;
            border-bottom: 3px solid #f39c12; margin-bottom: 20px;
            display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        /* --- B. SEARCH PANEL --- */
        .search-container {
            background-color: #fff; border: 1px solid #dcdcdc; 
            border-top: 3px solid #007bff; /* Viền xanh trên cùng giống hình */
            box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 20px;
        }
        
        /* Cột Trái (Filter) */
        .search-section-left { padding: 20px; background-color: #fff; }
        /* Cột Phải (Batch) */
        .search-section-right { padding: 20px; background-color: #f8f9fa; border-left: 1px solid #eee; }

        /* Tiêu đề Section */
        .section-title {
            font-size: 14px; font-weight: 700; color: #444; text-transform: uppercase;
            margin-bottom: 15px; display: flex; align-items: center; gap: 8px;
        }
        .section-title i { color: #555; }

        /* Label giả lập */
        .custom-label {
            font-size: 12px; font-weight: 600; color: #555; margin-bottom: 5px; display: block;
        }

        /* --- C. INPUT STYLING (BOOTSTRAP LOOK) --- */
        /* Text Input vuông vức */
        div[data-testid="stTextInput"] input {
            border-radius: 0px; border: 1px solid #ced4da; height: 38px; color: #495057;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #80bdff; box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
        }
        
        /* Text Area (Batch) */
        div[data-testid="stTextArea"] textarea {
            border-radius: 0px; border: 1px solid #ced4da; font-family: 'Consolas', monospace; font-size: 13px;
        }

        /* BUTTONS */
        div.stButton > button {
            border-radius: 0px; font-weight: 600; border: none; height: 38px; width: 100%;
        }
        /* Nút Reset (Trắng viền xám) */
        .btn-reset button { background-color: #fff; color: #333; border: 1px solid #ced4da; }
        .btn-reset button:hover { background-color: #e2e6ea; }
        
        /* Nút Search (Xanh lá đậm) */
        .btn-search button { background-color: #2da44e; color: white; }
        .btn-search button:hover { background-color: #2c974b; }
        
        /* Nút Batch Search (Xanh dương) */
        .btn-batch button { background-color: #0d6efd; color: white; }
        .btn-batch button:hover { background-color: #0b5ed7; }
        
        /* Nút Export (Xanh lá viền) */
        div[data-testid="stDownloadButton"] button {
            background-color: #fff; color: #198754; border: 1px solid #198754; 
            border-radius: 4px; padding: 4px 12px; font-size: 13px; height: auto;
        }
        div[data-testid="stDownloadButton"] button:hover {
            background-color: #198754; color: white;
        }

        /* --- D. TABLE STYLING (QUAN TRỌNG NHẤT) --- */
        .table-wrapper {
            overflow-x: auto; border: 1px solid #dee2e6; background: #fff;
        }
        .custom-table {
            width: 100%; border-collapse: collapse; font-size: 13px;
        }
        .custom-table thead th {
            background-color: #e9ecef; color: #495057; font-weight: 700;
            padding: 10px; border-bottom: 2px solid #dee2e6; border-right: 1px solid #dee2e6;
            text-align: center; white-space: nowrap; vertical-align: middle;
        }
        .custom-table tbody td {
            padding: 8px 10px; border-bottom: 1px solid #dee2e6; border-right: 1px solid #dee2e6;
            vertical-align: middle; color: #212529;
        }
        .custom-table tbody tr:nth-child(even) { background-color: #f8f9fa; }
        .custom-table tbody tr:hover { background-color: #f1f3f5; }

        /* Badge Styles */
        .badge {
            display: inline-block; padding: 0.35em 0.65em; font-size: 0.75em; font-weight: 700;
            line-height: 1; text-align: center; white-space: nowrap; vertical-align: baseline;
            border-radius: 0.25rem; margin-right: 4px; margin-bottom: 4px; border: 1px solid transparent;
        }
        .badge-warning { color: #664d03; background-color: #fff3cd; border-color: #ffecb5; } /* Khai báo */
        .badge-danger { color: #842029; background-color: #f8d7da; border-color: #f5c2c7; } /* Hạn chế/Độc */
        .badge-info { color: #055160; background-color: #cff4fc; border-color: #b6effb; } /* Khác */
        
        .cas-text { font-family: 'Consolas', monospace; font-weight: 700; color: #d63384; text-align: center; }
        .threshold-text { color: #dc3545; font-weight: 700; text-align: right; }
        
        .link-btn {
            color: #0d6efd; text-decoration: none; font-size: 12px; display: inline-flex; align-items: center; gap: 4px;
        }
        .link-btn:hover { text-decoration: underline; }

    </style>
""", unsafe_allow_html=True)

# --- 3. XỬ LÝ DỮ LIỆU ---
@st.cache_data(ttl=600)
def load_data():
    # LINK GOOGLE SHEET CSV (Bạn thay link của bạn vào đây)
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-4uKzaw2LpN5lBOGyG4MB3DPbaC6p6SbtO-yhoEQHRVFx30UHgJOSGfwTn-dOHkhBjAMoDea8n0ih/pub?gid=0&single=true&output=csv"
    try:
        df = pd.read_csv(sheet_url, dtype=str)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame() # Trả về bảng rỗng nếu lỗi

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='KetQua')
    return output.getvalue()

# Callback Reset
def reset_inputs():
    st.session_state["f_cas"] = ""
    st.session_state["f_name"] = ""
    st.session_state["f_formula"] = ""
    st.session_state["batch_input"] = ""

# --- 4. GIAO DIỆN CHÍNH ---

# A. HEADER
st.markdown("""
<div class="site-header">
    <div style="display:flex; align-items:center; gap:15px;">
        <i class="fa-solid fa-database fa-2x"></i>
        <div>
            <div style="font-size:18px; font-weight:700; text-transform:uppercase;">Chemical Regulatory Database</div>
            <div style="font-size:12px; opacity:0.8;">Hệ thống tra cứu số CAS & Ngưỡng tồn trữ (NĐ 113/2017)</div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,0.1); padding:6px 12px; border-radius:4px; font-size:13px; border:1px solid rgba(255,255,255,0.2);">
        <i class="fa-solid fa-user-circle me-1"></i> Admin User
    </div>
</div>
""", unsafe_allow_html=True)

df = load_data()

# B. KHUNG TÌM KIẾM (SEARCH PANEL) - Chia layout bằng st.columns
with st.container():
    # Tạo khung bao ngoài giả lập CSS .search-container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Chia cột 70% - 30%
    c1, c2 = st.columns([7, 3], gap="small")
    
    # --- CỘT TRÁI: SINGLE FILTER ---
    with c1:
        st.markdown('<div class="search-section-left">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"><i class="fa-solid fa-filter"></i> TRA CỨU ĐƠN (FILTER)</div>', unsafe_allow_html=True)
        
        # Hàng input: CAS - Name - Formula - Nút
        col_in1, col_in2, col_in3, col_btn_reset, col_btn_search = st.columns([2, 3.5, 2, 1, 1], vertical_alignment="bottom")
        
        with col_in1:
            st.markdown('<label class="custom-label">Mã CAS</label>', unsafe_allow_html=True)
            f_cas = st.text_input("cas", key="f_cas", label_visibility="collapsed", placeholder="67-64-1")
        with col_in2:
            st.markdown('<label class="custom-label">Tên hóa chất (EN / IUPAC)</label>', unsafe_allow_html=True)
            f_name = st.text_input("name", key="f_name", label_visibility="collapsed", placeholder="Acetone...")
        with col_in3:
            st.markdown('<label class="custom-label">Công thức</label>', unsafe_allow_html=True)
            f_formula = st.text_input("formula", key="f_formula", label_visibility="collapsed", placeholder="C3H6O")
        with col_btn_reset:
            st.markdown('<div class="btn-reset">', unsafe_allow_html=True)
            st.button("↻", on_click=reset_inputs, use_container_width=True, help="Làm mới bộ lọc")
            st.markdown('</div>', unsafe_allow_html=True)
        with col_btn_search:
            st.markdown('<div class="btn-search">', unsafe_allow_html=True)
            btn_single = st.button("🔍", use_container_width=True, help="Tìm kiếm")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div style="margin-top:8px; font-size:11px; color:#888; font-style:italic;"><i class="fa-solid fa-circle-info me-1"></i>Hệ thống tự động lọc khi nhập liệu.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # End Left

    # --- CỘT PHẢI: BATCH SEARCH ---
    with c2:
        st.markdown('<div class="search-section-right" style="height:100%">', unsafe_allow_html=True)
        st.markdown('<div class="section-title text-primary"><i class="fa-solid fa-list-check"></i> TRA CỨU HÀNG LOẠT</div>', unsafe_allow_html=True)
        
        st.markdown('<label class="custom-label">Danh sách CAS (cách nhau dấu ;)</label>', unsafe_allow_html=True)
        batch_input = st.text_area("batch", key="batch_input", label_visibility="collapsed", height=38, placeholder='"67-64-1"; "7664-93-9"')
        
        st.markdown('<div class="btn-batch" style="margin-top:5px;">', unsafe_allow_html=True)
        btn_batch = st.button("Tra cứu danh sách", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # End Right

    st.markdown('</div>', unsafe_allow_html=True) # End Container

# --- LOGIC FILTER ---
df_result = pd.DataFrame()
if df is not None and not df.empty:
    df_result = df.copy()
    
    # Logic Batch
    if batch_input:
        keywords = [x.strip().replace('"', '').replace("'", "") for x in batch_input.split(';') if x.strip()]
        if 'MaCAS' in df_result.columns:
            df_result = df_result[df_result['MaCAS'].isin(keywords)]
    
    # Logic Single (Auto Filter)
    else:
        if f_cas and 'MaCAS' in df_result.columns:
            df_result = df_result[df_result['MaCAS'].astype(str).str.contains(f_cas.strip(), case=False, na=False)]
        if f_name and 'Tên chất' in df_result.columns:
            df_result = df_result[df_result['Tên chất'].astype(str).str.contains(f_name.strip(), case=False, na=False)]
        if f_formula and 'Công thức hóa học' in df_result.columns:
            df_result = df_result[df_result['Công thức hóa học'].astype(str).str.contains(f_formula.strip(), case=False, na=False)]

# --- C. HIỂN THỊ BẢNG KẾT QUẢ ---

# Header kết quả & Export
col_res1, col_res2 = st.columns([8, 2], vertical_alignment="center")
with col_res1:
    count = len(df_result)
    st.markdown(f"<h5 style='margin:0; color:#444;'>Kết quả tìm kiếm: <span style='color:#0d6efd'>{count}</span> bản ghi</h5>", unsafe_allow_html=True)
with col_res2:
    if count > 0:
        xls = to_excel(df_result)
        st.download_button("📥 Xuất Excel (.xlsx)", xls, "KetQua.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

# --- RENDER TABLE HTML (FIX LỖI HIỂN THỊ CODE) ---
# Chúng ta sẽ xây dựng chuỗi HTML và dùng st.markdown để render
html = """
<div class="table-wrapper">
    <table class="custom-table">
        <thead>
            <tr>
                <th style="width: 50px;">STT</th>
                <th>Tên chất</th>
                <th>Tên tiếng Anh / IUPAC</th>
                <th style="width: 100px;">Mã CAS</th>
                <th style="width: 100px;">Công thức</th>
                <th style="width: 120px;">Ngưỡng (kg)</th>
                <th>Phụ lục quản lý / Phân loại</th>
                <th style="width: 100px;">Tham khảo</th>
            </tr>
        </thead>
        <tbody>
"""

if count > 0:
    for idx, row in df_result.iterrows():
        # 1. Xử lý Badge Phụ lục
        pl_str = str(row.get('Phụ lục quản lý', ''))
        badges_html = ""
        if pl_str.lower() != 'nan' and pl_str.strip():
            # Tách các phụ lục (giả sử cách nhau bởi dấu phẩy hoặc xuống dòng)
            items = pl_str.replace('\n', ',').split(',')
            for item in items:
                item = item.strip()
                if not item: continue
                
                # Logic màu sắc
                b_class = "badge-info" # Mặc định xanh nhạt
                item_lower = item.lower()
                if any(x in item_lower for x in ['hạn chế', 'nguy hiểm', 'pl i', 'tiền chất', 'độc']):
                    b_class = "badge-danger" # Đỏ
                elif any(x in item_lower for x in ['khai báo', 'pl v']):
                    b_class = "badge-warning" # Vàng
                
                badges_html += f'<span class="badge {b_class}">{item}</span> '
        
        # 2. Xử lý Link
        link = str(row.get('Link văn bản', ''))
        link_html = ""
        if len(link) > 5:
            link_html = f'<a href="{link}" target="_blank" class="link-btn">Văn bản <i class="fa-solid fa-up-right-from-square"></i></a>'
            
        # 3. Xử lý Ngưỡng (Tô đỏ)
        nguong = str(row.get('Ngưỡng khối lượng hóa chất tồn trữ lớn nhất tại một thời điểm (kg)', ''))
        nguong_html = "-"
        if nguong.lower() != 'nan' and nguong.strip():
            nguong_html = f'<span class="threshold-text">{nguong}</span>'

        # 4. Row HTML
        html += f"""
            <tr>
                <td style="text-align:center;">{idx + 1}</td>
                <td style="font-weight:600;">{row.get('Tên chất', '')}</td>
                <td style="color:#555;">{row.get('Tên khoa học (danh pháp IUPAC)', '')}</td>
                <td class="cas-text">{row.get('MaCAS', '')}</td>
                <td style="text-align:center;">{row.get('Công thức hóa học', '')}</td>
                <td>{nguong_html}</td>
                <td>{badges_html}</td>
                <td style="text-align:center;">{link_html}</td>
            </tr>
        """
else:
    html += '<tr><td colspan="8" style="text-align:center; padding: 30px; color:#999;">Không tìm thấy dữ liệu phù hợp</td></tr>'

html += """
        </tbody>
    </table>
</div>
"""

# Render bảng ra màn hình
st.markdown(html, unsafe_allow_html=True)

# Footer
st.markdown("<div style='text-align:center; margin-top:30px; color:#aaa; font-size:12px;'>© 2026 Shine Group Internal Tool</div>", unsafe_allow_html=True)