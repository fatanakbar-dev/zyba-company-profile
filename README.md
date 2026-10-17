# zyba-company-profile

Source code website company profile **ZYBA** (modest fashion brand) — https://zyba.ahliwebmurah.my.id/

Single-file Cloudflare Worker (`src/worker.js`, HTML inline) dengan halaman Bahasa Indonesia (`/`) dan Bahasa Inggris (`/en`); pindah bahasa via ikon globe + teks EN/ID di pojok kanan navbar.

## Struktur

- `src/worker.js` — worker + seluruh HTML (versi ID & EN)
- `i18n/` — tooling terjemahan: `zyba_map.py` (kamus ID→EN) + `zyba_build.py` (generate `HTML_EN` dari HTML ID, lengkap dengan verifikasi struktur)
- `logo.jpg` — logo ZYBA (juga di-inline sebagai data URI di dalam worker)
- `public/index.html` — arsip halaman publik
- `deploy.py` — script deploy ke Cloudflare Workers
- `wrangler.toml` — konfigurasi worker (`zyba-demo`)

## Deploy

```bash
python3 deploy.py
```

Meng-upload `src/worker.js` ke worker `zyba-demo` via Cloudflare API (kredensial dibaca via secure surrogate helper — tidak ada secret di repo ini).
