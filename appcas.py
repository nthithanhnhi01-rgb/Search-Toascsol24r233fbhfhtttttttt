import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Chemical Regulatory Database", 
    page_icon="🧪", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. NHÚNG CSS & HTML HEADER (GIỮ NGUYÊN CODE CSS CỦA BẠN) ---
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        /* --- COPY NGUYÊN VĂN CSS CỦA BẠN --- */
        :root {
            --header-bg: #2d3e50;
            --primary-btn: #3a5a40;
            --batch-btn: #2980b9;
            --batch-bg: #f0f4f8;
            --accent-color: #e9ecef;
            --border-color: #dee2e6;
        }
        
        /* Ẩn Header/Footer mặc định của Streamlit để full màn hình */
        #MainMenu, footer, header {visibility: hidden;}
        .block-container { padding-top: 0rem; padding-bottom: 0rem; padding-left: 0rem; padding-right: 0rem; }
        
        body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; background-color: #f5f7fa; }

        /* HEADER */
        .site-header {
            background-color: var(--header-bg); color: #fff; padding: 10px 20px;
            border-bottom: 3px solid #f39c12; margin-bottom: 15px;
        }
        .site-header h1 { font-size: 1.4rem; margin: 0; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }

        /* SEARCH PANEL */
        .search-panel {
            background: #fff; border: 1px solid #ccc; margin: 0 20px 15px 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05); overflow: hidden;
            display: flex; flex-wrap: wrap;
        }
        
        .search-label {
            font-weight: 700; color: #444; font-size: 0.9rem; margin-bottom: 8px;
            display: block; border-bottom: 2px solid #eee; padding-bottom: 5px;
        }
        .sub-label { font-size: 11px; font-weight: 600; color: #666; margin-bottom: 0px; display: block; }
        
        /* TÙY CHỈNH STREAMLIT WIDGET CHO GIỐNG INPUT CỦA BẠN */
        div[data-testid="stTextInput"] input {
            border-radius: 0; border: 1px solid #bbb; height: 32px; font-size: 13px;
        }
        div[data-testid="stTextInput"] input:focus { border-color: #86b7fe; box-shadow: 0 0 0 0.25rem rgba(13,110,253,.25); }
        div[data-testid="stTextArea"] textarea {
            border-radius: 0; border: 1px solid #bbb; font-family: 'Consolas', monospace; font-size: 12px;
        }

        /* KHU VỰC SINGLE & BATCH */
        .single-section { padding: 15px; background-color: #fff; flex: 2; border-right: 1px solid #eee; }
        .batch-section { background-color: var(--batch-bg); border-left: 1px dashed #b0c4de; padding: 15px; flex: 1; }

        /* RESULT TABLE STYLES */
        .result-container { padding: 0 20px 20px 20px; }
        .table-custom { width: 100%; border-collapse: collapse; font-size: 13px; background: white; border: 1px solid #ccc; }
        .table-custom thead th {
            position: sticky; top: 0; background-color: #e2e6ea; color: #333;
            padding: 8px; border-bottom: 2px solid #999; border-right: 1px solid #ccc;
            font-weight: 700; text-align: center; white-space: nowrap;
        }
        .table-custom tbody td {
            padding: 6px 8px; border-bottom: 1px solid #ddd; border-right: 1px solid #eee; vertical-align: middle;
        }
        .table-custom tbody tr:nth-child(even) { background-color: #f9f9f9; }
        .table-custom tbody tr:hover { background-color: #eef5f0; }
        
        /* Utility Classes */
        .col-center { text-align: center; }
        .col-cas { font-family: 'Consolas', monospace; font-weight: bold; color: #d63384; }
        .link-icon { color: #0d6efd; text-decoration: none; }
        .link-icon:hover { text-decoration: underline; }
        .reg-badge {
            display: inline-block; padding: 2px 6px; font-size: 11px;
            border: 1px solid #ccc; background: #fff; margin-right: 3px; margin-bottom: 2px; border-radius: 3px;
        }
        .reg-danger { border-color: #dc3545; color: #dc3545; background: #fff5f5; }
        .reg-warning { border-color: #ffc107; color: #856404; background: #fff3cd; }
        
        /* Chỉnh nút bấm Streamlit cho đẹp */
        div.stButton > button { border-radius: 0; font-weight: 600; width: 100%; }
    </style>
    
    <div class="site-header d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center">
            <i class="fa-solid fa-layer-group fa-lg me-3"></i>
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

# --- 3. XỬ LÝ DỮ LIỆU ---
@st.cache_data(ttl=600)
def load_data():
    # LINK GOOGLE SHEET CỦA BẠN
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-4uKzaw2LpN5lBOGyG4MB3DPbaC6p6SbtO-yhoEQHRVFx30UHgJOSGfwTn-dOHkhBjAMoDea8n0ih/pub?gid=0&single=true&output=csv" 
    try:
        df = pd.read_csv(sheet_url, dtype=str)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame() # Trả về bảng rỗng nếu lỗi

# Hàm xử lý xuất Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='KetQua')
    return output.getvalue()

# Callbacks làm mới
def reset_all():
    st.session_state["f_cas"] = ""
    st.session_state["f_name"] = ""
    st.session_state["f_formula"] = ""
    st.session_state["batch_input"] = ""

# --- 4. GIAO DIỆN CHÍNH (LAYOUT MÔ PHỎNG HTML) ---

df = load_data()

# KHUNG TÌM KIẾM (SEARCH PANEL)
# Chúng ta dùng st.container và CSS để tạo cái khung viền trắng
with st.container():
    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    
    # Chia cột: Bên trái (Single) 7 phần, Bên phải (Batch) 4 phần
    c1, c2 = st.columns([7, 4], gap="small")
    
    # --- CỘT TRÁI: SINGLE SEARCH ---
    with c1:
        st.markdown('<div class="single-section" style="height:100%">', unsafe_allow_html=True)
        st.markdown('<label class="search-label"><i class="fa-solid fa-filter me-1"></i> TRA CỨU ĐƠN (FILTER)</label>', unsafe_allow_html=True)
        
        # Hàng nhập liệu: CAS | Tên | Công thức | Nút Reset
        r1_col1, r1_col2, r1_col3, r1_col4 = st.columns([2, 4, 2, 1])
        
        with r1_col1:
            st.markdown('<label class="sub-label">Số CAS</label>', unsafe_allow_html=True)
            f_cas = st.text_input("CAS", label_visibility="collapsed", key="f_cas", placeholder="VD: 67-64-1")
        
        with r1_col2:
            st.markdown('<label class="sub-label">Tên hóa chất (EN / IUPAC)</label>', unsafe_allow_html=True)
            f_name = st.text_input("Name", label_visibility="collapsed", key="f_name", placeholder="Acetone...")
            
        with r1_col3:
            st.markdown('<label class="sub-label">Công thức</label>', unsafe_allow_html=True)
            f_formula = st.text_input("Formula", label_visibility="collapsed", key="f_formula", placeholder="C3H6O")
            
        with r1_col4:
            st.markdown('<label class="sub-label">&nbsp;</label>', unsafe_allow_html=True)
            st.button("↺", on_click=reset_all, help="Làm mới", use_container_width=True)

        st.markdown('<div class="mt-2 text-muted fst-italic" style="font-size: 11px;"><i class="fa-solid fa-circle-info me-1"></i>Nhập 1 hoặc kết hợp nhiều ô để lọc chính xác (Auto-Filter).</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # Đóng div single-section

    # --- CỘT PHẢI: BATCH SEARCH ---
    with c2:
        st.markdown('<div class="batch-section" style="height:100%">', unsafe_allow_html=True)
        st.markdown('<label class="search-label text-primary"><i class="fa-solid fa-list-check me-1"></i> TRA CỨU HÀNG LOẠT</label>', unsafe_allow_html=True)
        
        st.markdown('<label class="sub-label">Nhập danh sách CAS (cách nhau bởi dấu chấm phẩy)</label>', unsafe_allow_html=True)
        batch_input = st.text_area("Batch", label_visibility="collapsed", key="batch_input", height=67, placeholder='"67-64-1"; "7664-93-9"')
        
        st.markdown('</div>', unsafe_allow_html=True) # Đóng div batch-section

    st.markdown('</div>', unsafe_allow_html=True) # Đóng div search-panel


# --- 5. LOGIC LỌC DỮ LIỆU ---
df_result = pd.DataFrame()
if df is not None and not df.empty:
    df_result = df.copy()
    
    # Ưu tiên 1: Nếu có nhập Batch Search -> Lọc theo Batch
    if batch_input:
        keywords = [x.strip().replace('"', '').replace("'", "") for x in batch_input.split(';') if x.strip() != '']
        if 'MaCAS' in df_result.columns:
            df_result = df_result[df_result['MaCAS'].isin(keywords)]
    
    # Ưu tiên 2: Nếu không Batch thì lọc theo Single (Filter chồng)
    else:
        if f_cas and 'MaCAS' in df_result.columns:
            df_result = df_result[df_result['MaCAS'].astype(str).str.contains(f_cas.strip(), case=False, na=False)]
        
        if f_name and 'Tên chất' in df_result.columns:
            df_result = df_result[df_result['Tên chất'].astype(str).str.contains(f_name.strip(), case=False, na=False)]
            
        if f_formula and 'Công thức hóa học' in df_result.columns:
            df_result = df_result[df_result['Công thức hóa học'].astype(str).str.contains(f_formula.strip(), case=False, na=False)]
else:
    st.error("Chưa kết nối được dữ liệu!")

# --- 6. HIỂN THỊ KẾT QUẢ (VẼ HTML TABLE THỦ CÔNG) ---
st.markdown('<div class="result-container">', unsafe_allow_html=True)

# Header bảng kết quả + Nút Export
col_res_info, col_res_btn = st.columns([8, 2])
with col_res_info:
    st.markdown(f'<span class="fw-bold text-secondary">Kết quả: {len(df_result)} bản ghi</span>', unsafe_allow_html=True)
with col_res_btn:
    if len(df_result) > 0:
        xls_data = to_excel(df_result)
        st.download_button(
            label="📥 Export XLS",
            data=xls_data,
            file_name="KetQua_TraCuu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary"
        )

# --- VẼ BẢNG HTML (Magic Part) ---
# Đoạn này sẽ duyệt qua DataFrame và tạo chuỗi HTML y hệt mẫu bạn gửi
html_table = '<div class="table-container mt-2"><table class="table-custom"><thead><tr>'
html_table += '<th width="4%">STT</th><th width="15%">Tên chất</th><th width="15%">Tên tiếng Anh/IUPAC</th><th width="8%">Mã CAS</th><th width="8%">Công thức</th><th width="10%">Ngưỡng (kg)</th><th width="25%">Phụ lục quản lý</th><th width="10%">Tham khảo</th>'
html_table += '</tr></thead><tbody>'

if len(df_result) > 0:
    for index, row in df_result.iterrows():
        # Xử lý Badges (Phụ lục) - Tự động tô màu nếu phát hiện từ khóa nguy hiểm
        pl_raw = str(row.get('Phụ lục quản lý', ''))
        pl_html = ""
        # Tách các phụ lục bằng dấu phẩy hoặc xuống dòng để tạo badge riêng
        pl_items = pl_raw.split('\n') 
        for item in pl_items:
            if item.strip():
                badge_class = "reg-badge"
                # Logic tô màu badge
                if "Hạn chế" in item or "nguy hiểm" in item or "PL I" in item or "tiền chất" in item.lower():
                    badge_class += " reg-danger"
                elif "Khai báo" in item or "PL V" in item:
                    badge_class += " reg-warning"
                
                pl_html += f'<div class="{badge_class}">{item}</div>'

        # Link văn bản
        link_raw = str(row.get('Link văn bản', '#'))
        link_html = f'<a href="{link_raw}" target="_blank" class="link-icon">Văn bản <i class="fa-solid fa-up-right-from-square small"></i></a>' if len(link_raw) > 5 else ''

        # Ngưỡng tồn trữ (Tô đỏ nếu có số)
        nguong = str(row.get('Ngưỡng khối lượng hóa chất tồn trữ lớn nhất tại một thời điểm (kg)', ''))
        nguong_html = f'<span class="text-danger fw-bold">{nguong}</span>' if nguong and nguong != 'nan' else '<em class="text-muted">-</em>'

        html_table += f"""
        <tr>
            <td class="col-center">{row.get('STT', index+1)}</td>
            <td><strong>{row.get('Tên chất', '')}</strong></td>
            <td>{row.get('Tên khoa học (danh pháp IUPAC)', '')}</td>
            <td class="col-cas col-center">{row.get('MaCAS', '')}</td>
            <td class="col-center">{row.get('Công thức hóa học', '')}</td>
            <td class="text-end">{nguong_html}</td>
            <td>{pl_html}</td>
            <td class="col-center">{link_html}</td>
        </tr>
        """
else:
    html_table += '<tr><td colspan="8" class="text-center py-4 text-muted">Không tìm thấy dữ liệu phù hợp</td></tr>'

html_table += '</tbody></table></div>'
st.markdown(html_table, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True) # Đóng result-container

# FOOTER
st.markdown("""
    <div class="container-fluid border-top mt-3 pt-2 pb-2 text-center text-muted" style="font-size: 11px;">
        © 2026 Shine Group Internal Tool. Data source: National Chemical Database.
    </div>
""", unsafe_allow_html=True)