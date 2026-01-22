import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="Chemical Regulatory Database", page_icon="🧪", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS "ÉP GIAO DIỆN" (FIXED) ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        /* RESET CƠ BẢN */
        #MainMenu, footer, header {visibility: hidden;}
        .block-container { padding-top: 0rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; }
        
        body { font-family: 'Segoe UI', sans-serif; background-color: #f5f7fa; font-size: 14px; }

        /* HEADER */
        .site-header {
            background-color: #2d3e50; color: #fff; padding: 12px 20px;
            border-bottom: 3px solid #f39c12; margin-bottom: 20px;
            display: flex; justify-content: space-between; align-items: center;
        }
        
        /* KHUNG SEARCH PANEL */
        .search-panel-container {
            background: #fff; border: 1px solid #ccc; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        
        /* CHỈNH INPUT CỦA STREAMLIT CHO GIỐNG BOOTSTRAP */
        div[data-testid="stTextInput"] input {
            border-radius: 0; border: 1px solid #ced4da; height: 34px; font-size: 13px;
        }
        div[data-testid="stTextInput"] input:focus { border-color: #86b7fe; box-shadow: none; }
        
        div[data-testid="stTextArea"] textarea {
            border-radius: 0; border: 1px solid #ced4da; font-family: 'Consolas', monospace; font-size: 12px;
        }

        /* NÚT BẤM */
        div.stButton > button {
            border-radius: 0; border: none; font-weight: 600; font-size: 13px; height: 34px;
        }
        /* Nút Reset & Search (Xanh rêu) */
        .btn-green button { background-color: #3a5a40; color: white; }
        .btn-green button:hover { background-color: #2c4431; color: white; }
        
        /* Nút Batch (Xanh dương) */
        .btn-blue button { background-color: #2980b9; color: white; }
        .btn-blue button:hover { background-color: #1c6ea4; color: white; }

        /* Nút Reset trắng */
        .btn-light button { background-color: #f8f9fa; color: #333; border: 1px solid #ccc; }
        .btn-light button:hover { background-color: #e2e6ea; border-color: #adb5bd; color: #333; }
        
        /* EXPORT BUTTON STYLE (Đè lên nút download mặc định) */
        div[data-testid="stDownloadButton"] button {
            border: 1px solid #198754; color: #198754; background: white; font-size: 12px; padding: 4px 10px; height: auto;
        }
        div[data-testid="stDownloadButton"] button:hover {
            background-color: #198754; color: white;
        }

        /* LABEL GIẢ */
        .custom-label { font-size: 11px; font-weight: 700; color: #666; margin-bottom: 2px; display: block; text-transform: uppercase; }
        .section-title { font-weight: 700; color: #444; font-size: 0.95rem; border-bottom: 2px solid #eee; padding-bottom: 5px; margin-bottom: 10px; display: block;}

        /* TABLE STYLE (QUAN TRỌNG) */
        .table-custom { width: 100%; border-collapse: collapse; font-size: 13px; background: white; border: 1px solid #ccc; }
        .table-custom thead th {
            position: sticky; top: 0; background-color: #e9ecef; color: #495057; z-index: 1;
            padding: 10px; border-bottom: 2px solid #adb5bd; border-right: 1px solid #dee2e6;
            font-weight: 700; text-align: center; white-space: nowrap;
        }
        .table-custom tbody td {
            padding: 8px 10px; border-bottom: 1px solid #dee2e6; border-right: 1px solid #dee2e6; vertical-align: middle; color: #212529;
        }
        .table-custom tr:nth-child(even) { background-color: #f8f9fa; }
        .table-custom tr:hover { background-color: #e2e6ea; }

        .col-cas { font-family: 'Consolas', monospace; font-weight: bold; color: #d63384; text-align: center; }
        .reg-badge {
            display: inline-block; padding: 3px 6px; font-size: 11px;
            border: 1px solid #dee2e6; background: #fff; margin-right: 4px; margin-bottom: 4px; border-radius: 4px;
        }
        .reg-danger { border-color: #f5c6cb; color: #721c24; background: #f8d7da; }
        .reg-warning { border-color: #ffeeba; color: #856404; background: #fff3cd; }
        .link-icon { color: #0d6efd; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 5px;}
        .link-icon:hover { text-decoration: underline; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIC XỬ LÝ DỮ LIỆU ---
@st.cache_data(ttl=600)
def load_data():
    # LINK GOOGLE SHEET
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

def reset_all():
    st.session_state["f_cas"] = ""
    st.session_state["f_name"] = ""
    st.session_state["f_formula"] = ""
    st.session_state["batch_input"] = ""

# --- 4. GIAO DIỆN CHÍNH ---

# A. HEADER (HTML THUẦN)
st.markdown("""
    <div class="site-header">
        <div style="display:flex; align-items:center;">
            <i class="fa-solid fa-layer-group fa-lg" style="margin-right: 15px;"></i>
            <div>
                <div style="font-size: 1.4rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Chemical Regulatory Database</div>
                <div style="font-size: 0.85rem; opacity: 0.9; font-weight: 300;">Hệ thống tra cứu số CAS & Ngưỡng tồn trữ (NĐ 113/2017)</div>
            </div>
        </div>
        <div><span style="background:rgba(255,255,255,0.2); padding:5px 10px; border-radius:4px; font-size:13px;"><i class="fa-solid fa-user"></i> Admin User</span></div>
    </div>
""", unsafe_allow_html=True)

df = load_data()

# B. SEARCH PANEL (DÙNG CONTAINER ĐỂ BAO QUANH)
with st.container():
    st.markdown('<div class="search-panel-container" style="padding: 0;">', unsafe_allow_html=True)
    
    # Chia làm 2 cột lớn: Single (70%) - Batch (30%)
    col_single, col_batch = st.columns([7, 3], gap="large")
    
    # --- CỘT TRÁI: SINGLE SEARCH ---
    with col_single:
        st.markdown('<div style="padding: 15px;">', unsafe_allow_html=True) # Padding thủ công
        st.markdown('<span class="section-title"><i class="fa-solid fa-filter me-1"></i> TRA CỨU ĐƠN (FILTER)</span>', unsafe_allow_html=True)
        
        # Hàng nhập liệu (Chia 4 cột nhỏ)
        c1, c2, c3, c4 = st.columns([2, 4, 2, 2])
        
        with c1:
            st.markdown('<span class="custom-label">SỐ CAS</span>', unsafe_allow_html=True)
            f_cas = st.text_input("CAS", label_visibility="collapsed", key="f_cas", placeholder="67-64-1")
        with c2:
            st.markdown('<span class="custom-label">TÊN HÓA CHẤT (EN / IUPAC)</span>', unsafe_allow_html=True)
            f_name = st.text_input("Name", label_visibility="collapsed", key="f_name", placeholder="Acetone...")
        with c3:
            st.markdown('<span class="custom-label">CÔNG THỨC</span>', unsafe_allow_html=True)
            f_formula = st.text_input("Formula", label_visibility="collapsed", key="f_formula", placeholder="C3H6O")
        with c4:
            st.markdown('<span class="custom-label">&nbsp;</span>', unsafe_allow_html=True)
            # Nút Reset (Style class btn-light)
            st.markdown('<div class="btn-light">', unsafe_allow_html=True)
            st.button("↻ Làm mới", on_click=reset_all, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:8px; font-size:11px; color:#6c757d; font-style:italic;"><i class="fa-solid fa-circle-info me-1"></i>Hệ thống tự động lọc khi bạn nhập liệu (Auto-Filter).</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # End padding

    # --- CỘT PHẢI: BATCH SEARCH ---
    with col_batch:
        # Style nền xanh nhạt cho cột này
        st.markdown('<div style="background-color: #f8f9fa; height: 100%; padding: 15px; border-left: 1px solid #dee2e6;">', unsafe_allow_html=True)
        st.markdown('<span class="section-title" style="color:#0d6efd"><i class="fa-solid fa-list-check me-1"></i> TRA CỨU HÀNG LOẠT</span>', unsafe_allow_html=True)
        
        st.markdown('<span class="custom-label">DANH SÁCH CAS (CÁCH NHAU DẤU ;)</span>', unsafe_allow_html=True)
        batch_input = st.text_area("Batch", label_visibility="collapsed", key="batch_input", height=38, placeholder='"67-64-1"; "7664-93-9"')
        
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # End search-panel-container

# --- LOGIC LỌC ---
df_result = pd.DataFrame()
if df is not None and not df.empty:
    df_result = df.copy()
    if batch_input:
        keywords = [x.strip().replace('"', '').replace("'", "") for x in batch_input.split(';') if x.strip() != '']
        if 'MaCAS' in df_result.columns:
            df_result = df_result[df_result['MaCAS'].isin(keywords)]
    else:
        if f_cas and 'MaCAS' in df_result.columns:
            df_result = df_result[df_result['MaCAS'].astype(str).str.contains(f_cas.strip(), case=False, na=False)]
        if f_name and 'Tên chất' in df_result.columns:
            df_result = df_result[df_result['Tên chất'].astype(str).str.contains(f_name.strip(), case=False, na=False)]
        if f_formula and 'Công thức hóa học' in df_result.columns:
            df_result = df_result[df_result['Công thức hóa học'].astype(str).str.contains(f_formula.strip(), case=False, na=False)]

# --- C. BẢNG KẾT QUẢ ---

# Thanh công cụ bảng (Kết quả + Nút Export)
col_info, col_export = st.columns([8, 2])
with col_info:
    st.markdown(f'<div style="font-weight:700; color:#495057; margin-top:5px;">KẾT QUẢ TÌM KIẾM: <span style="color:#0d6efd">{len(df_result)}</span> bản ghi</div>', unsafe_allow_html=True)
with col_export:
    if len(df_result) > 0:
        excel_data = to_excel(df_result)
        st.download_button(
            label="📥 Xuất Excel (.xlsx)",
            data=excel_data,
            file_name='KetQua_TraCuu.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            use_container_width=True
        )

# TẠO HTML TABLE (FIX LỖI HIỂN THỊ)
table_html = '<div style="overflow-x:auto; margin-top:10px;"><table class="table-custom">'
table_html += '<thead><tr><th width="5%">STT</th><th width="20%">Tên chất</th><th width="15%">Tên IUPAC</th><th width="10%">Mã CAS</th><th width="8%">Công thức</th><th width="10%">Ngưỡng (kg)</th><th width="22%">Phụ lục quản lý</th><th width="10%">Văn bản</th></tr></thead><tbody>'

if len(df_result) > 0:
    for idx, row in df_result.iterrows():
        # Xử lý Phụ lục (Badges)
        pl_raw = str(row.get('Phụ lục quản lý', ''))
        pl_html = ""
        if pl_raw and pl_raw.lower() != 'nan':
             # Tách theo dòng hoặc dấu phẩy
             items = pl_raw.replace('\n', ';').split(';') 
             for item in items:
                 item = item.strip()
                 if item:
                     cls = "reg-badge"
                     if any(x in item.lower() for x in ['hạn chế', 'nguy hiểm', 'pl i', 'tiền chất']):
                         cls += " reg-danger"
                     elif any(x in item.lower() for x in ['khai báo', 'pl v']):
                         cls += " reg-warning"
                     pl_html += f'<span class="{cls}">{item}</span> '
        
        # Xử lý Link
        link_url = str(row.get('Link văn bản', '#'))
        link_display = f'<a href="{link_url}" target="_blank" class="link-icon">Xem <i class="fa-solid fa-up-right-from-square" style="font-size:10px;"></i></a>' if len(link_url) > 4 else ''
        
        # Xử lý Ngưỡng
        nguong = str(row.get('Ngưỡng khối lượng hóa chất tồn trữ lớn nhất tại một thời điểm (kg)', ''))
        nguong_display = f'<span style="color:#dc3545; font-weight:bold;">{nguong}</span>' if nguong and nguong.lower() != 'nan' else '-'

        table_html += f"""
        <tr>
            <td style="text-align:center;">{row.get('STT', idx+1)}</td>
            <td style="font-weight:600;">{row.get('Tên chất', '')}</td>
            <td>{row.get('Tên khoa học (danh pháp IUPAC)', '')}</td>
            <td class="col-cas">{row.get('MaCAS', '')}</td>
            <td style="text-align:center;">{row.get('Công thức hóa học', '')}</td>
            <td style="text-align:right;">{nguong_display}</td>
            <td>{pl_html}</td>
            <td style="text-align:center;">{link_display}</td>
        </tr>
        """
else:
    table_html += '<tr><td colspan="8" style="text-align:center; padding:20px; color:#6c757d;">Không tìm thấy dữ liệu phù hợp.</td></tr>'

table_html += "</tbody></table></div>"

# Render Table
st.markdown(table_html, unsafe_allow_html=True)

# FOOTER
st.markdown('<div style="margin-top:30px; border-top:1px solid #eee; padding-top:10px; text-align:center; color:#adb5bd; font-size:11px;">© 2026 Shine Group Internal Tool</div>', unsafe_allow_html=True)