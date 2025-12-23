![Jhopan](https://img.shields.io/badge/JHOPAN-v3.2-blue?style=for-the-badge&logo=probot&logoColor=white)
![Version](https://img.shields.io/badge/Version-3.2--CrossPlatform-blue?style=for-the-badge&logo=git&logoColor=white)
![Xray-core](https://img.shields.io/badge/Xray--core-v25.12.8-orange?style=for-the-badge&logo=windowsterminal&logoColor=white)

# Jhopan - Cross Platform Bug Checker

Tool untuk mengecek website/IP address yang bisa digunakan untuk injeksi kuota dengan dukungan Xray-core 25.12.8 dan SSH Websocket. Support Android (Termux), Windows, Linux, dan macOS!

## 🚀 Fitur Utama

- ✅ **Multi-Platform**: Android (Termux), Windows, Linux, macOS
- ✅ **8 Mode Scan**: Address, Wildcard, SNI, Onering, SSH, Subdomain, Reverse IP, SNI v2
- ✅ **Account Management**: Simpan & load URL VPN untuk testing cepat
- ✅ **Dual Network Support**: Pilih interface spesifik (Linux dual WiFi/network)
- ✅ **Multiple List Files**: wa.txt, ig.txt, tiktok.txt, line.txt, music.txt, dll
- ✅ **Separate Results**: Hasil tersimpan terpisah per list
- ✅ **Multi Protocol**: VMess, VLess, Trojan
- ✅ **Complete List**: List lengkap IP + Domain untuk WhatsApp, Instagram, TikTok, LINE, Music

## 📦 Quick Install

### Android (Termux)

```bash
pkg update && pkg upgrade -y
pkg install python git wget unzip -y
git clone https://github.com/jhopan/CheckBugByJhopan.git
cd CheckBugByJhopan
pip install -r requirements.txt
bash install.sh
python jhopan.py
```

### Windows

```cmd
git clone https://github.com/jhopan/CheckBugByJhopan.git
cd CheckBugByJhopan
pip install -r requirements.txt
python jhopan.py
```

_Note: Download xray.exe dari [Xray-core releases](https://github.com/XTLS/Xray-core/releases)_

### Linux

```bash
git clone https://github.com/jhopan/CheckBugByJhopan.git
cd CheckBugByJhopan
pip3 install -r requirements.txt
python3 jhopan.py
```

### macOS

```bash
git clone https://github.com/jhopan/CheckBugByJhopan.git
cd CheckBugByJhopan
pip3 install -r requirements.txt
python3 jhopan.py
```

## 🎯 Cara Pakai

```bash
python jhopan.py
```

**Pilih Mode:**

- [1] Address - Test IP/server berbeda
- [2] Wildcard - Test wildcard domain
- [3] SNI - Test SNI/servername
- [4] Onering - Wildcard tanpa pointing
- [5] SSH Websocket
- [6] Subdomain Scanner
- [7] Reverse IP Address
- [8] **SNI v2** - Test SNI + Host sekaligus (untuk Clash)
- [9] **Manage Accounts** - Kelola URL VPN tersimpan

**Input:**

1. Pilih metode (1-9)
2. Pilih/masukkan URL VPN (tersimpan atau baru)
3. Masukkan file list (wa.txt, ig.txt, dll)
4. (Linux dual network) Pilih interface untuk testing

**Output:**

- Hasil tersimpan di `{nama_list}_result.txt`
- Contoh: `wa.txt` → `wa_result.txt`

## 💾 Account Management

**Simpan URL untuk testing cepat:**

```bash
python jhopan.py
Mode: 1
URL: vless://...
List: wa.txt

[?] Save this URL? (y/n): y
[*] Account name: MyVPN

# Next time:
python jhopan.py
Mode: 1

[*] Saved Accounts
[1] MyVPN      - vless
[0] Enter new URL
[?] Select: 1  # ← Quick select!
```

**Manage saved accounts:**
- Option [9] di menu utama
- List semua akun tersimpan
- Hapus akun yang tidak diperlukan

## 🌐 Dual Network Mode (Linux)

**Untuk setup dual WiFi/network:**

```bash
# Setup:
# - WiFi USB (wlan0) → Internet normal
# - WiFi Laptop (wlan1) → Kuota provider

sudo python3 jhopan.py
Mode: 1
URL: vless://...
List: wa.txt

# Auto detect dual network:
[*] Network Mode Selection
[1] Auto (recommended) - Use default routing
[2] Advanced - Select specific interface
[?] Choose: 2

[*] Available Network Interfaces
[1] wlan0    - 192.168.1.5    # Internet normal
[2] wlan1    - 192.168.43.10  # Kuota provider
[?] Select: 2

[+] Using interface: wlan1
# Testing via kuota, operations via internet!
```

**Catatan:**
- Auto mode: Windows, Termux, Linux single network
- Advanced mode: Linux dengan 2+ network interface
- Butuh `sudo` untuk bind interface
- Traffic xray via interface pilihan
- HTTP requests tetap via default route

## 📝 List Files Lengkap

### WhatsApp (wa.txt)

**30+ domain & IP** termasuk:

- Main: web.whatsapp.com, v.whatsapp.net, media.whatsapp.net
- CDN: media-ams3-1.cdn.whatsapp.net, cdn.whatsapp.net
- IPs: 157.240.x.x, 31.13.x.x

### Instagram (ig.txt)

**40+ domain & IP** termasuk:

- Main: www.instagram.com, api.instagram.com, graph.instagram.com
- CDN: scontent.cdninstagram.com, video.cdninstagram.com
- Facebook CDN: instagram.fsin6-1.fna.fbcdn.net
- IPs: 157.240.x.x, 31.13.x.x

### TikTok (tiktok.txt)

**35+ domain & IP** termasuk:

- Main: www.tiktok.com, api.tiktok.com
- API: api16.tiktok.com, api19.tiktok.com, api21.tiktok.com
- Video: v16.tiktok.com, v19.tiktok.com, v21.tiktok.com
- CDN: sf16-sg.tiktokcdn.com, p16-sign-sg.tiktokcdn.com
- IPs: 104.244.x.x, 104.18.x.x, 172.67.x.x

### LINE & Naver (line.txt)

**50+ domain & IP** termasuk:

- LINE Main: line.me, api.line.me, talk.line.me
- LINE CDN: static.line-scdn.net, obs.line-scdn.net
- Naver: www.naver.com, api.naver.com, search.naver.com
- Naver CDN: ssl.pstatic.net, phinf.pstatic.net
- IPs: 125.209.x.x, 147.92.x.x, 203.104.x.x, 211.249.x.x

### Music Streaming (music.txt)

**40+ domain & IP** termasuk:

- JOOX: www.joox.com, api.joox.com, stream.joox.com
- Spotify: www.spotify.com, api.spotify.com, audio-ak-spotify-com.akamaized.net
- YouTube Music: music.youtube.com
- Apple Music: music.apple.com
- Deezer, SoundCloud, Tidal
- IPs: 157.240.x.x, 35.186.x.x, 172.217.x.x

### Facebook (fb.txt)

**30+ domain & IP** untuk Facebook & Instagram gabungan

### SNI Domains (sni.txt)

Domain CDN populer untuk mode SNI v2

## 🆕 Mode SNI v2 (Mode 8)

Mode khusus untuk Clash/v2ray config dimana SNI dan Host header harus sama:

```yaml
proxies:
  - name: "VPN"
    server: 104.18.1.196
    type: vless
    port: 443
    uuid: your-uuid
    tls: true
    servername: cdn.cloudflare.net # ← Hasil scan
    network: ws
    ws-opts:
      path: /vless
      headers:
        Host: cdn.cloudflare.net # ← Sama!
```

**Cara pakai:**

```bash
python jhopan.py
[*] Pilih metode: 8
[*] URL akun: vless://...
[*] List: sni.txt
# Hasil di sni_result.txt bisa langsung dipakai!
```

## 📊 Contoh Workflow

### Scan WhatsApp Bug

```bash
python jhopan.py
Mode: 1 (Address)
URL: vmess://...
List: wa.txt
→ Hasil: wa_result.txt
```

### Scan Instagram Bug

```bash
python jhopan.py
Mode: 3 (SNI)
URL: vless://...
List: ig.txt
→ Hasil: ig_result.txt
```

### Scan TikTok Bug

```bash
python jhopan.py
Mode: 2 (Wildcard)
URL: trojan://...
List: tiktok.txt
→ Hasil: tiktok_result.txt
```

### Buat Config Clash

```bash
python jhopan.py
Mode: 8 (SNI v2)
URL: vless://...
List: sni.txt
→ Hasil: sni_result.txt (ready untuk servername + Host!)
```

## 🔍 Mode Detail

| Mode           | Fungsi                  | Use Case               |
| -------------- | ----------------------- | ---------------------- |
| 1 - Address    | Test server/IP          | Cari IP bug            |
| 2 - Wildcard   | Test wildcard domain    | Domain dengan wildcard |
| 3 - SNI        | Test SNI saja           | Bug SNI                |
| 4 - Onering    | Wildcard tanpa pointing | Advanced wildcard      |
| 5 - SSH WS     | SSH Websocket           | Alternative method     |
| 6 - Subdomain  | Scan subdomain          | Cari subdomain         |
| 7 - Reverse IP | Reverse IP lookup       | Cari domain dari IP    |
| 8 - SNI v2     | SNI + Host              | Config Clash/v2ray     |

## 💡 Tips

- ✅ Gunakan list yang sesuai dengan kuota (wa.txt untuk kuota WA, dll)
- ✅ Test dengan beberapa mode untuk hasil optimal
- ✅ Hasil scan bisa langsung dipakai di config VPN
- ✅ Scan ulang beberapa kali untuk akurasi lebih baik
- ✅ Gunakan SSH dan Xray untuk hasil lebih pasti

## ⚠️ Perhatian

- Pastikan akun VPN stabil
- Gunakan akun yang tidak sedang dipakai injeksi
- Hanya ada kuota yang mau di-scan (no kuota reguler)
- Tool ini memiliki akurasi ~90%

## 📁 File Management

**Edit/Buat List:**

```bash
nano wa.txt
```

**Hapus List:**

```bash
rm wa.txt
```

**Copy ke Storage (Android):**

```bash
cp wa_result.txt /sdcard/
```

## 🔧 Troubleshooting

**Error "xray not found":**

- Windows: Download xray.exe
- Linux: `sudo apt install xray`
- Termux: `bash install.sh`

**Error "Module not found":**

```bash
pip install -r requirements.txt
```

**All targets failed:**

- Check internet connection
- Verify VPN account
- Try different list file

## 📞 Support

- 💻 GitHub: [jhopan/CheckBugByJhopan](https://github.com/jhopan/CheckBugByJhopan)

## 🙏 Credits

- **Developer**: Jhopan
- **Xray-core**: [XTLS/Xray-core](https://github.com/XTLS/Xray-core)
- **Onering**: [dharak36/xray-onering](https://github.com/dharak36/xray-onering)

---

## 📄 License

Pengguna setuju mematuhi semua hukum yang berlaku dan melepas tanggung jawab pengembang dari klaim apa pun.

**Jhopan v3.2 - Happy Bug Hunting! 🚀**
