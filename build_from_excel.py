import sys, re, os, math
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

def slugify(text):
    text = str(text).lower()
    text = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", text)
    text = re.sub(r"[èéẹẻẽêềếệểễ]", "e", text)
    text = re.sub(r"[ìíịỉĩ]", "i", text)
    text = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", text)
    text = re.sub(r"[ùúụủũưừứựửữ]", "u", text)
    text = re.sub(r"[ỳýỵỷỹ]", "y", text)
    text = re.sub(r"[đ]", "d", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    return text

def write_sitemap(urls, path, priority="0.8", changefreq="weekly"):
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    now = datetime.utcnow().strftime("%Y-%m-%d")
    for u in urls:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = u
        ET.SubElement(url, "lastmod").text = now
        ET.SubElement(url, "changefreq").text = changefreq
        ET.SubElement(url, "priority").text = priority
    tree = ET.ElementTree(urlset)
    tree.write(path, encoding="utf-8", xml_declaration=True)

def write_index(parts, path):
    root = ET.Element("sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    now = datetime.utcnow().strftime("%Y-%m-%d")
    for p in parts:
        sm = ET.SubElement(root, "sitemap")
        ET.SubElement(sm, "loc").text = p
        ET.SubElement(sm, "lastmod").text = now
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/build_from_excel.py <excel_file>")
        sys.exit(1)
    excel = sys.argv[1]
    df = pd.read_excel(excel)

    products = []
    for _, r in df.iterrows():
        if pd.notna(r.get("Tên hàng")) and pd.notna(r.get("Mã hàng")):
            slug = slugify(r["Tên hàng"])
            products.append(f"https://gifthaus.vn/products/{slug}-{r['Mã hàng']}")
    cats = sorted(set([x for x in df.get("Nhóm hàng(3 Cấp)", []) if pd.notna(x)]))
    categories = [f"https://gifthaus.vn/c/{slugify(c)}" for c in cats]

    # Chunking if needed (<=50k per file)
    chunk = 45000
    product_files = []
    for i in range(0, len(products), chunk):
        name = "sitemap-products{}.xml".format("" if i==0 else f"-{i//chunk+1}")
        write_sitemap(products[i:i+chunk], name)
        product_files.append(name)

    write_sitemap(categories, "sitemap-categories.xml", priority="0.6", changefreq="weekly")

    # Index
    index_parts = [f"https://sitemaps.gifthaus.vn/{f}" for f in product_files + ["sitemap-categories.xml"]]
    write_index(index_parts, "sitemap.xml")
    print("Done. Files updated:", ", ".join(product_files + ["sitemap-categories.xml", "sitemap.xml"]))

if __name__ == "__main__":
    main()
