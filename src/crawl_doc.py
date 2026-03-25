import os
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import html2text  # 需要安装: pip install html2text

# --- 配置 ---
# BASE_URL = "https://triton-lang.org/main/index.html"
# TARGET_DOMAIN = "triton-lang.org"
# OUTPUT_DIR = "triton_docs_markdown"

BASE_URL = "https://tilelang.com/index.html"
TARGET_DOMAIN = "tilelang.com"
OUTPUT_DIR = "tilelang_docs_markdown"

MAX_PAGES = 200

# 初始化 HTML 转 Markdown 工具
h2t = html2text.HTML2Text()
h2t.ignore_links = False
h2t.ignore_images = False
h2t.body_width = 0  # 不自动换行

def safe_filename(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path or path == "index.html":
        path = "index"
    path = path.replace("/", "_").replace(".html", "")
    return f"{path}.md"

def fetch_url(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    print(f"正在抓取: {url}")
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text

def extract_clean_content(html: str) -> str:
    """提取正文并转换为 Markdown"""
    soup = BeautifulSoup(html, "html.parser")
    
    # 1. 尝试定位 Sphinx/Docusaurus 常见的正文标签
    # Triton 文档通常在 <div role="main"> 或 <div class="body"> 中
    main_content = soup.find("div", {"role": "main"}) or \
                   soup.find("article") or \
                   soup.find("div", class_="document")
    
    if main_content:
        # 移除不必要的元素（如“编辑页面”按钮、导航链接）
        for extra in main_content.find_all(["script", "style", "nav", "header", "footer"]):
            extra.decompose()
        content_html = str(main_content)
    else:
        # 如果找不到正文容器，回退到 body
        content_html = str(soup.body)

    # 2. 转换为 Markdown
    markdown_text = h2t.handle(content_html)
    return markdown_text

def parse_links(html: str, base_url: str) -> set:
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        full = urljoin(base_url, a["href"]).split('#')[0].split('?')[0]
        if TARGET_DOMAIN in urlparse(full).netloc and full.endswith((".html", "/")):
            links.add(full)
    return links

def save_file(content: str, filename: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def crawl(start_url: str):
    visited = set()
    to_visit = [start_url]

    while to_visit and len(visited) < MAX_PAGES:
        url = to_visit.pop(0)
        if url in visited: continue
        
        try:
            html = fetch_url(url)
            # 提取干净的内容
            markdown_content = extract_clean_content(html)
            
            # 保存为 .md
            fname = safe_filename(url)
            save_file(markdown_content, fname)
            
            visited.add(url)

            # 解析后续链接
            for link in parse_links(html, url):
                if link not in visited and link not in to_visit:
                    to_visit.append(link)
            
            time.sleep(0.8) # 礼貌爬取
        except Exception as e:
            print(f"处理失败 {url}: {e}")
            visited.add(url)

if __name__ == "__main__":
    crawl(BASE_URL)