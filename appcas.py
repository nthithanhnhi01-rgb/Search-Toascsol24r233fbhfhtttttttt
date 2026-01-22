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

# --- 2. NHÚNG CSS & HTML CỦA BẠN VÀO STREAMLIT ---
# Tôi đã thêm một số class ".stTextInput" để ép kiểu ô nhập của Streamlit giống ô input HTML của bạn
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
        
        /* Ẩn Header mặc định của Streamlit */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top: 0px; padding-left: 1rem; padding-right: 1rem;}

        /* Header Custom */
        .site-header {
            background-color: var(--header-bg);
            color: #fff;
            padding: 10px 20px;
            border-bottom: 3px solid #f39c12;
            margin-bottom: 20px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .site-header h1 { font-size: 1.4rem; margin: 0; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }

        /* Search Panel */
        .search-panel {
            background: #fff;
            border: 1px solid #ccc;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-radius: 4px;
            overflow: hidden;
        }
        .search-label {
            font-weight: 700; color: #444; font-size: 0.9rem;
            margin-bottom: 8px; display: block; border-bottom: 2px solid #eee; padding-bottom: 5px;
        }
        .batch-section { background-color: var(--batch-bg); border-left: 1px dashed #b0c4de; height: 100%; padding: 15px; }
        .single-section { padding: 15px; background-color: #fff; }

        /* Tùy chỉnh Input Streamlit cho giống HTML */
        .stTextInput input {
            border-radius: 0; border-color: #bbb; font-size: 13px; height: 32px;
        }
        .stTextInput input:focus { border-color: #3a5a40; box-shadow: none; }
        
        /* Button Styles */
        div.stButton > button {
            border-radius: 0; font-weight: 600; font-size: 13px; width: 100%;
        }
        
        /* Badge Styles cho Bảng */
        .reg-badge { display: inline-block; padding: 2px 6px; font-size: 11px; border: 1px solid #ccc; background: #fff; margin-right: 3px; margin-bottom: 2px; border-radius: 3px; color: #333; }
        .reg-danger { border-color: #dc3545; color: #dc3545; background: #fff5f5; }
        .reg-warning { border-color: #ffc107; color: #856404; background: #fff3cd; }
        
        /* Table Styles */
        .table-custom { width: 100%; border-collapse: collapse; font-size: 13px; font-family: 'Segoe UI', sans-serif; }
        .table-custom thead th { background-color: #e2e6ea; color: #333; position: sticky; top: 0; padding: 8px; border-bottom: 2px solid #999; text-align: center; font-weight: 700; }
        .table-custom tbody td { padding: 6px 8px; border-bottom: 1px solid #ddd; vertical-align: middle; }
        .table-custom tbody tr:nth-child(even) { background-color: #f9f9f9; }
        .col-cas { font-family: 'Consolas', monospace; font-weight: bold; color: #d63384; text-align: center; }
        .col-center { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIC XỬ LÝ DỮ LIỆU ---
@st.cache_data(ttl=600)
def load_data_from_sheet():
    # LINK GOOGLE SHEET (Thay link của bạn vào đây)
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-4uKzaw2LpN5lBOGyG4MB3DPbaC6p6SbtO-yhoEQHRVFx30UHgJOSGfwTn-dOHkhBjAMoDea8n0ih/pub?gid=0&single=true&output=csv" 
    try:
        df = pd.read_csv(sheet_url, dtype=str)
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return None

def clear_callbacks():
    st.session_state["f_cas"] = ""
    st.session_state["f_name"] = ""
    st.session_state["f_formula"] = ""
    st.session_state["batch_input"] = ""

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='KetQua')
    return output.getvalue()

# --- 4. HÀM RENDER BẢNG HTML (Để hiển thị Badge đẹp như bạn muốn) ---
def render_html_table(df):
    html = '<div class="table-container"><table class="table-custom"><thead><tr>'
    headers = ["STT", "Tên chất", "Tên tiếng Anh/IUPAC", "Mã CAS", "Công thức", "Ngưỡng (kg)", "Phụ lục quản lý", "Link"]
    for h in headers:
        html += f'<th>{h}</th>'
    html += '</tr></thead><tbody>'

    if len(df) == 0:
        return html + '<tr><td colspan="8" class="col-center">Không tìm thấy dữ liệu</td></tr></tbody></table></div>'

    for index, row in df.iterrows():
        # Xử lý Logic Badge màu sắc
        pl_raw = str(row.get('Phụ lục quản lý', '')).split('\n')
        badges_html = ""
        for pl in pl_raw:
            pl = pl.strip()
            if not pl or pl == 'nan': continue
            
            # Logic gán màu badge
            css_class = "reg-badge"
            if "hạn chế" in pl.lower() or "nguy hiểm" in pl.lower() or "độc" in pl.lower():
                css_class += " reg-danger"
            elif "tiền chất" in pl.lower() or "khai báo" in pl.lower():
                css_class += " reg-warning"
            
            badges_html += f'<div class="{css_class}">{pl}</div>'

        # Link xử lý
        link_url = str(row.get('Link văn bản', '#'))
        link_html = f'<a href="{link_url}" target="_blank" style="color: #0d6efd; text-decoration: none;">Chi tiết <i class="fa-solid fa-up-right-from-square"></i></a>' if link_url != 'nan' else ''

        # Ngưỡng xử lý
        nguong = str(row.get('Ngưỡng khối lượng hóa chất tồn trữ lớn nhất tại một thời điểm (kg)', ''))
        nguong_html = f'<span class="text-danger fw-bold">{nguong}</span>' if nguong != 'nan' else '<span class="text-muted text-center">-</span>'

        html += f"""
        <tr>
            <td class="col-center">{row.get('STT', '')}</td>
            <td><strong>{row.get('Tên chất', '')}</strong></td>
            <td>{row.get('Tên khoa học (danh pháp IUPAC)', '')}</td>
            <td class="col-cas">{row.get('MaCAS', '')}</td>
            <td class="col-center">{row.get('Công thức hóa học', '')}</td>
            <td class="text-end">{nguong_html}</td>
            <td>{badges_html}</td>
            <td class="col-center">{link_html}</td>
        </tr>
        """
    html += '</tbody></table></div>'
    return html

# --- 5. GIAO DIỆN CHÍNH ---
def main():
    # A. HEADER (Dùng HTML tĩnh)
    st.markdown("""
        <div class="site-header">
            <div class="d-flex align-items-center">
                <i class="fa-solid fa-layer-group fa-lg me-3"></i>
                <div>
                    <h1>Chemical Regulatory Database</h1>
                    <small style="opacity: 0.8; font-weight: 300;">Hệ thống tra cứu số CAS & Ngưỡng tồn trữ (NĐ 113/2017)</small>
                </div>
            </div>
            <div><span class="badge bg-light text-dark border"><i class="fa-solid fa-user me-1"></i> Admin User</span></div>
        </div>
    """, unsafe_allow_html=True)

    # B. LOGIC & LAYOUT
    df = load_data_from_sheet()
    
    # Tạo container bọc ngoài panel search
    with st.container():
        st.markdown('<div class="search-panel">', unsafe_allow_html=True)
        
        # Chia cột Layout: Trái (Single - 65%) | Phải (Batch - 35%)
        col_single, col_batch = st.columns([65, 35])

        # --- CỘT TRÁI: TRA CỨU ĐƠN ---
        with col_single:
            st.markdown('<div class="single-section"><label class="search-label"><i class="fa-solid fa-filter me-1"></i> TRA CỨU ĐƠN (FILTER)</label>', unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns([3, 4, 3])
            with c1:
                st.markdown('<label style="font-size:11px; font-weight:600; color:#666;">Số CAS</label>', unsafe_allow_html=True)
                f_cas = st.text_input("cas", key="f_cas", label_visibility="collapsed", placeholder="VD: 67-64-1")
            with c2:
                st.markdown('<label style="font-size:11px; font-weight:600; color:#666;">Tên hóa chất (EN / IUPAC)</label>', unsafe_allow_html=True)
                f_name = st.text_input("name", key="f_name", label_visibility="collapsed", placeholder="Acetone...")
            with c3:
                st.markdown('<label style="font-size:11px; font-weight:600; color:#666;">Công thức hóa học</label>', unsafe_allow_html=True)
                f_formula = st.text_input("formula", key="f_formula", label_visibility="collapsed", placeholder="C3H6O")

            # Nút Reset nhỏ
            st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)
            if st.button("🔄 Xóa bộ lọc", key="btn_clear_single"):
                clear_callbacks()
                st.rerun()
            
            st.markdown('<div class="mt-2 text-muted fst-italic" style="font-size: 11px;"><i class="fa-solid fa-circle-info me-1"></i>Nhập và nhấn Enter để lọc.</div></div>', unsafe_allow_html=True)

        # --- CỘT PHẢI: TRA CỨU HÀNG LOẠT ---
        with col_batch:
            # Nhúng style background riêng cho cột này
            st.markdown("""
                <div class="batch-section">
                <label class="search-label text-primary"><i class="fa-solid fa-list-check me-1"></i> TRA CỨU HÀNG LOẠT</label>
            """, unsafe_allow_html=True)
            
            st.markdown('<label style="font-size:11px; font-weight:600; color:#666;">Danh sách CAS (ngăn cách bởi dấu ;)</label>', unsafe_allow_html=True)
            batch_input = st.text_area("batch", key="batch_input", label_visibility="collapsed", height=68, placeholder='"67-64-1"; "7664-93-9"')
            
            # Logic xử lý nút tìm kiếm
            # Lưu ý: Trong Streamlit button sẽ reload trang, ta dùng session state input để lọc
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # Đóng search-panel

    # C. XỬ LÝ DỮ LIỆU
    if df is not None:
        df_result = df.copy()
        
        # Logic 1: Batch Search (Ưu tiên nếu có nhập)
        if batch_input:
            keywords = [x.strip().replace('"', '').replace("'", "") for x in batch_input.split(';') if x.strip() != '']
            if 'MaCAS' in df_result.columns:
                df_result = df_result[df_result['MaCAS'].isin(keywords)]
        # Logic 2: Filter Search
        else:
            if f_cas and 'MaCAS' in df_result.columns:
                df_result = df_result[df_result['MaCAS'].astype(str).str.contains(f_cas.strip(), case=False, na=False)]
            if f_name and 'Tên chất' in df_result.columns:
                df_result = df_result[df_result['Tên chất'].astype(str).str.contains(f_name.strip(), case=False, na=False)]
            if f_formula and 'Công thức hóa học' in df_result.columns:
                df_result = df_result[df_result['Công thức hóa học'].astype(str).str.contains(f_formula.strip(), case=False, na=False)]

        # D. HIỂN THỊ KẾT QUẢ & NÚT EXCEL
        c_res1, c_res2 = st.columns([8, 2])
        with c_res1:
            st.markdown(f'<span class="fw-bold text-secondary">Kết quả: {len(df_result)} bản ghi</span>', unsafe_allow_html=True)
        with c_res2:
            if len(df_result) > 0:
                excel_data = to_excel(df_result)
                st.download_button(
                    label="📥 Export Excel",
                    data=excel_data,
                    file_name='KetQua_TraCuu.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    use_container_width=True
                )

        # RENDER BẢNG HTML
        html_table = render_html_table(df_result)
        st.markdown(html_table, unsafe_allow_html=True)
        
        st.markdown('<div class="container-fluid border-top mt-3 pt-2 pb-2 text-center text-muted" style="font-size: 11px;">© 2026 Shine Group Internal Tool. Data source: National Chemical Database.</div>', unsafe_allow_html=True)

    else:
        st.error("Lỗi kết nối database.")

if __name__ == "__main__":
    main()