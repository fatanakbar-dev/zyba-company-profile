# Zyba i18n — English page generator

Halaman /en dibuat dari HTML bahasa Indonesia via script ini (bukan duplikat manual).

- `zyba_map.py` — kamus terjemahan ID -> EN (tambah entri baru di sini kalau ada teks Indonesia baru).
- `zyba_build.py` — memasukkan language switcher (globe + EN) ke navbar, menerapkan kamus,
  lalu menulis `src/worker.js` dengan `const HTML` (ID) + `const HTML_EN` + routing /en.

Cara pakai setelah edit teks Indonesia di `src/worker.js`:
  python3 i18n/zyba_build.py   # regenerate + verifikasi otomatis
  node --check src/worker.js   # cek sintaks
  python3 deploy.py            # deploy ke Cloudflare

Verifikasi otomatis di build: urutan tag HTML ID vs EN identik, tidak ada kata Indonesia
tersisa di EN, spot-check switcher + routing.
