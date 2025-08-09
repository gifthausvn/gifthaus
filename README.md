# Gifthaus Sitemaps

Static sitemaps for `gifthaus.vn`, hosted on Cloudflare Pages via subdomain `sitemaps.gifthaus.vn`.

## Files
- `sitemap.xml` — sitemap index
- `sitemap-products.xml` — product URLs
- `sitemap-categories.xml` — category URLs

## Regenerate sitemaps from Excel
If you export a new Excel from KiotViet, use the Python script in `tools/`:

```bash
python tools/build_from_excel.py /path/to/DanhSachSanPham.xlsx
```

The script will update the 3 XML files at repo root. Commit & push to trigger a new deploy on Cloudflare Pages.

## Notes
- All `<loc>` are absolute URLs of `https://gifthaus.vn/...`
- `lastmod` is set to the script execution date.
- Keep each sitemap under 50,000 URLs; the script will automatically chunk if exceeded.
```