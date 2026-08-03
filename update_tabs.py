import sys
import re

def update_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add CSS
    css = """
        .sidebar-tabs {
            display: flex;
            background: #0f172a;
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 60px;
            z-index: 40;
        }
        .tab-btn {
            flex: 1;
            background: none;
            border: none;
            color: #94a3b8;
            padding: 12px 2px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.2s;
        }
        .tab-btn.active {
            color: var(--accent-color);
            border-bottom-color: var(--accent-color);
        }
        .tab-btn:hover {
            color: #f8fafc;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
"""
    if '.sidebar-tabs' not in content:
        content = content.replace("</style>", css + "\n    </style>")

    # 2. Add JS
    js = """
        function switchTab(tabId, btn) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            btn.classList.add('active');
        }
"""
    if 'function switchTab' not in content:
        content = content.replace("<script>", "<script>\n" + js)

    # 3. Rewrite Nav
    # We will find the nav-sections using regex and group them
    
    # Extract the whole nav block
    nav_match = re.search(r'(<nav id="sidebar">.*?</nav>)', content, re.DOTALL)
    if not nav_match:
        print("Could not find nav sidebar")
        return
    nav_html = nav_match.group(1)
    
    # Extract header
    header_match = re.search(r'(<div class="sidebar-header">.*?</div>)', nav_html, re.DOTALL)
    header_html = header_match.group(1)

    # Extract all nav-sections
    sections = re.findall(r'(<div class="nav-section">.*?</ul>\s*</div>)', nav_html, re.DOTALL)
    
    if len(sections) < 8:
        print(f"Expected 8 sections, found {len(sections)}")
        return

    s_khoi_dong = sections[0]
    s_co_ban = sections[1]
    s_nang_cao = sections[2]
    s_chuyen_gia = sections[3]
    s_nghe_thuat = sections[4]
    s_tot_nghiep = sections[5]
    s_van_de = sections[6]
    s_tai_lieu = sections[7]

    tab_buttons = """
        <div class="sidebar-tabs">
            <button class="tab-btn active" onclick="switchTab('tab-duan', this)">Dự Án</button>
            <button class="tab-btn" onclick="switchTab('tab-lotrinh', this)">Lộ Trình</button>
            <button class="tab-btn" onclick="switchTab('tab-vande', this)">Vấn Đề</button>
            <button class="tab-btn" onclick="switchTab('tab-tailieu', this)">Tài Liệu</button>
        </div>
"""

    tab_duan = f'<div id="tab-duan" class="tab-content active">\n{s_khoi_dong}\n{s_tot_nghiep}\n</div>'
    tab_lotrinh = f'<div id="tab-lotrinh" class="tab-content">\n{s_co_ban}\n{s_nang_cao}\n{s_chuyen_gia}\n{s_nghe_thuat}\n</div>'
    tab_vande = f'<div id="tab-vande" class="tab-content">\n{s_van_de}\n</div>'
    tab_tailieu = f'<div id="tab-tailieu" class="tab-content">\n{s_tai_lieu}\n</div>'

    new_nav = f"""<nav id="sidebar">
{header_html}
{tab_buttons}
{tab_duan}
{tab_lotrinh}
{tab_vande}
{tab_tailieu}
    </nav>"""

    content = content.replace(nav_html, new_nav)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Update successful!")

update_html('c:/projects/raylib-odin/index.html')
