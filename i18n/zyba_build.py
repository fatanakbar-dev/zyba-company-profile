# -*- coding: utf-8 -*-
"""Build the EN version of the Zyba page and write the new worker.js.

- Inserts the globe+EN language switcher into the ID navbar.
- Applies the ID->EN translation map (whitespace-insensitive, longest-first).
- Verifies: identical HTML tag sequence ID vs EN; no leftover Indonesian words.
- Writes worker.js with `const HTML` (ID), `const HTML_EN`, and /en routing.
"""
import re
import sys

sys.path.insert(0, "/tmp")
from zyba_map import PAIRS

SRC = "/home/hatch/workspace/zyba-worker/src/worker.js"
OUT = "/home/hatch/workspace/zyba-worker/src/worker.js"

SWITCHER = """          <!-- Language Switcher -->
          <a href="/en" aria-label="Switch to English version"
            class="flex items-center gap-1.5 px-3.5 py-2.5 rounded-full border border-gold/40 text-espresso text-xs font-bold tracking-wider hover:bg-blush/40 hover:text-burgundy transition-colors">
            <i data-lucide="globe" class="w-4 h-4 text-burgundy"></i><span>EN</span>
          </a>
"""

ANCHOR = ('        <!-- Right Side CTA & Mobile Hamburger -->\n'
          '        <div class="flex-1 flex justify-end items-center gap-3">\n')

src = open(SRC).read()

# --- extract the HTML const (robust: end is the `; right before export default) ---
m = re.search(r"const HTML = `", src)
assert m, "HTML const not found"
start = m.end()
end_marker = "`;\n\nexport default"
end = src.find(end_marker, start)
assert end > start, "HTML const end not found"
html_id = src[start:end]
print("ID html chars:", len(html_id))
assert html_id.rstrip().endswith("</html>"), "HTML does not end with </html>!"

# --- 1. insert language switcher into ID html ---
assert html_id.count(ANCHOR) == 1, f"navbar anchor count = {html_id.count(ANCHOR)}"
html_id = html_id.replace(ANCHOR, ANCHOR + SWITCHER)
assert "data-lucide=\"globe\"" in html_id
print("switcher inserted into ID html")

# --- 2. apply translation map (longest first, whitespace-insensitive) ---
pairs = sorted(PAIRS, key=lambda p: len(p[0]), reverse=True)
html_en = html_id
def rx(key):
    """Build a whitespace-insensitive regex for a key.
    Leading '>' / trailing '<' anchors tolerate surrounding whitespace/newlines."""
    core = key
    pre = ""
    post = ""
    if core.startswith(">"):
        pre = r">\s*"
        core = core[1:]
    if core.endswith("<"):
        post = r"\s*<"
        core = core[:-1]
    return re.compile(pre + r"\s+".join(re.escape(p) for p in core.split()) + post)


pairs = sorted(PAIRS, key=lambda p: len(p[0]), reverse=True)
html_en = html_id
for id_text, en_text in pairs:
    html_en, n = rx(id_text).subn(lambda _m: en_text, html_en)
    if n == 0:
        print(f"  WARNING: no match for key: {id_text[:70]!r}")
print("EN html chars:", len(html_en))

# --- 3a. verify identical tag-name sequence (attributes like lang may differ) ---
def tag_seq(h):
    return re.findall(r"</?([a-zA-Z][a-zA-Z0-9]*)", h)
seq_id, seq_en = tag_seq(html_id), tag_seq(html_en)
assert seq_id == seq_en, (
    "TAG SEQUENCE MISMATCH: "
    f"id={len(seq_id)} en={len(seq_en)} "
    + str(next(((i, seq_id[i], seq_en[i]) for i in range(min(len(seq_id), len(seq_en)))
                 if seq_id[i] != seq_en[i]), None)))
print("tag sequence identical:", len(seq_id), "tags")

# --- 3b. verify no leftover Indonesian words (word boundaries) ---
ID_WORDS = ("adalah ialah yang dan untuk dengan dari kami kita anda kamu mereka beliau "
            "perempuan laki laki bisnis produk desain layanan koleksi kontak beranda tentang "
            "cerita setiap juga tidak bukan lebih dapat secara melalui hingga maupun dalam "
            "pada sebagai oleh telah akan sudah ini itu apa bagaimana mengapa kapan dimana "
            "siapa berapa milik punya belum pernah serta agar supaya yaitu yakni adalah "
            "merupakan antara lain kah lah tak jangan bisa harus perlu boleh "
            "ingin mau tahu lihat cari buat jadi kalau jika karena saat ketika sambil "
            "sambil lalu kemudian kini nanti tadi kemarin besok hari ini itu sangat amat "
            "cukup kurang lebih paling banyak sedikit semua seluruh tiap berbagai macam "
            "jenis bagian cara hal masa waktu tempat orang dunia hidup mati besar kecil "
            "baru lama baik buruk benar salah mudah sulit cepat lambat dekat jauh tinggi "
            "rendah panjang pendek lebar luas sempit penuh kosong bersih kotor terang "
            "gelap hangat dingin manis pahit asin asam pedas empuk keras lembut kasar "
            "halus tebal tipis berat ringan kuat lemah sehat sakit kaya miskin muda tua "
            "cantik tampan jelek bagus indah nyaman aman bahaya penting perlu butuh ingin "
            "mau suka cinta benci marah sedih senang gembira tertawa menangis bicara diam "
            "dengar lihat rasa cium sentuh pegang bawa ambil beri terima beli jual pakai "
            "gunakan buat bikin kerja usaha dagang tani ajar belajar tulis baca hitung "
            "gambar nyanyi tari main lari jalan duduk berdiri tidur bangun mandi makan "
            "minum masak cuci sapu pel jemur setrika jahit potong rebus goreng bakar kukus "
            "tumbuh kembang mekar layu hidup mati lahir wafat kawin cerai punya milik sewa "
            "kontrak pinjam hutang bayar tagih untung rugi modal laba omzet pajak gaji upah "
            "lembur cuti pensiun lamar terima tolak setuju sepakat janji sumpah doa harap "
            "cita impian angan hayal nyata palsu asli tiruan contoh teladan panutan idola "
            "penggemar penonton pendengar pembaca penulis wartawan artis selebriti pejabat "
            "pemimpin rakyat warga masyarakat bangsa negara kota desa kampung jalan gang "
            "rumah gedung kantor sekolah kampus masjid gereja pasar mal toko warung restoran "
            "kafe hotel losmen kos kontrakan apartemen vila wisma graha plaza menara gapura "
            "tugu monumen museum galeri studio arena stadion sirkuit terminal stasiun bandara "
            "pelabuhan halte pos gardu menara mercusuar jembatan jalan tol rel kereta bus "
            "mobil motor sepeda becak delman andong ojek taksi bajaj angkot kereta api kapal "
            "perahu sampan rakit pesawat helikopter balon udara layang parasut terjun payung "
            "selam renang dayung kano kayak arung jeram rafting panjat tebing hiking camping "
            "piknik tamasya wisata ziarah umroh haji mudik pulang pergi datang berangkat tiba "
            "singgah mampir lewat lintas seberang belok putar balik mundur maju naik turun "
            "terbang melayang tenggelam hanyut apung renang selam menyelam timbul timbul "
            "tenggelam").split()
text_only = re.sub(r"<[^>]+>", " ", html_en)
text_only = re.sub(r"data:image/jpeg;base64,[A-Za-z0-9+/=]+", " ", text_only)
leftovers = sorted({w for w in ID_WORDS if re.search(rf"(?i)(?<![a-z]){re.escape(w)}(?![a-z])", text_only)})
if leftovers:
    print("LEFTOVER Indonesian words:", leftovers)
    # show context for each
    for w in leftovers[:10]:
        mm = re.search(rf"(?i)(?<![a-z]){re.escape(w)}(?![a-z])", text_only)
        s = max(0, mm.start() - 60)
        print("  ...", text_only[s:mm.end() + 60].replace("\n", " "), "...")
    sys.exit("leftover check failed")
print("no leftover Indonesian words")

# --- 3c. spot checks ---
for needle in ['<html lang="en"', '>Home<', '>About Zyba<',
               'Empowered Through Style', '>Contact Us<', 'aria-label="Open Menu"',
               'aria-label="Previous slide"', '>Explore Zyba Design<',
               'href="/" aria-label="Ganti ke versi Bahasa Indonesia"',
               '<span>ID</span>']:
    assert needle in html_en, f"missing in EN: {needle}"
for needle in ['>Beranda<', '>Tentang Zyba<', 'Berdaya Lewat Gaya', 'aria-label="Buka Menu"',
               'Terima kasih,']:
    assert needle not in html_en, f"untranslated leftover in EN: {needle}"
# ID page keeps its switcher + Indonesian copy
assert 'href="/en"' in html_id and '>Beranda<' in html_id
print("spot checks OK")

# --- 4. write new worker.js ---
head = src[:start]  # up to and including "const HTML = `"
tail = src[end:]    # from "`;" onward
assert tail.startswith("`;"), tail[:10]

new_fetch = """`;

const HTML_EN = `""" + html_en + """`;

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const path = url.pathname;
    const headers = { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "public, max-age=3600" };
    if (path === "/" || path === "/index.html") {
      return new Response(HTML, { headers });
    }
    if (path === "/en" || path === "/en/" || path === "/en/index.html") {
      return new Response(HTML_EN, { headers });
    }
    const notFound = path.startsWith("/en") ? "Page not found" : "Halaman tidak ditemukan";
    return new Response(notFound, { status: 404 });
  },
};
"""

# tail currently starts with "`;" then the old export default block; drop the old fetch block
old_fetch_start = tail.find("export default")
assert old_fetch_start > 0
new_src = head + html_id + new_fetch

open(OUT, "w").write(new_src)
print("written", OUT, len(new_src), "chars")
