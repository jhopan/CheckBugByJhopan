# Advanced Features Guide - Jhopan v3.3

## ⚙️ Custom Settings

Configure sesuai kebutuhan dengan defaults yang sudah optimal.

### Access Settings
```bash
python jhopan.py
[10] Settings
```

### Available Settings:

**Performance:**
- **Timeout**: 1-30s (default: 5s)
- **Parallel Jobs**: 1-10 (default: 1)  
- **Auto Retry**: ON/OFF (default: ON)
- **Retry Count**: 1-5x (default: 2)

**Features:**
- **Show Progress Bar**: ON/OFF (default: ON)
- **Speed Test**: ON/OFF (default: OFF)

**Telegram:**
- **Bot Token**: Your bot token
- **Chat ID**: Your Telegram chat ID

### Parallel Jobs Speed Boost

**Sequential (default = 1):**
```
100 targets × 5s = 500s (8+ minutes)
```

**Parallel (jobs = 5):**
```
100 targets ÷ 5 × 5s = 100s (2 minutes)
⚡ 5x faster!
```

**Note**: Terlalu banyak parallel bisa trigger rate limiting!

---

## 📦 Batch Mode

Scan multiple lists dalam satu run.

### Usage:
```bash
python jhopan.py
[12] Batch Mode

[*] List files: wa.txt,ig.txt,tiktok.txt
[*] Mode: 1 (Address)
[*] URL: vless://...
```

### Output:
```
Processing wa.txt [████████] 100%
✅ 8/30 (26.7%) - 142.5s

Processing ig.txt [████████] 100%
✅ 12/40 (30.0%) - 198.2s

Processing tiktok.txt [████████] 100%
✅ 5/35 (14.3%) - 156.8s

━━━━━━━━━━━━━━━━━━━━
📦 Total: 3 lists
✅ Connected: 25/105
⏱️  Duration: 497.5s
━━━━━━━━━━━━━━━━━━━━
```

---

## 🔄 Auto Retry

Automatically retry failed targets to handle network glitches.

### How it works:
1. First pass: Test all targets
2. If Auto Retry ON: Retry failed targets
3. Retry count times (default 2x)
4. Combine results

### Example:
```
First pass: 8/30 connected, 22 failed

Retry 1/2: Testing 22 failed targets...
✅ Recovered 3 targets!

Retry 2/2: Testing 19 failed targets...
✅ Recovered 2 targets!

Final: 13/30 connected (43.3%)
```

**Success rate meningkat significantly!**

---

## 📱 Telegram Bot

Get notifications via Telegram Bot.

### Setup (One Time):

**1. Create Bot:**
```
1. Open Telegram, search @BotFather
2. Send: /newbot
3. Follow instructions
4. Copy bot token: 123456789:ABCdef...
```

**2. Get Chat ID:**
```
1. Send message to your bot
2. Visit: https://api.telegram.org/bot<TOKEN>/getUpdates
3. Find "chat":{"id":987654321}
4. Copy chat ID
```

**3. Configure in Jhopan:**
```bash
python jhopan.py
[10] Settings
[7] Telegram

[*] Bot Token: 123456789:ABCdef...
[*] Chat ID: 987654321

[+] Telegram enabled!
```

### Notifications:

**Scan Start:**
```
🚀 Scan Started
📋 Mode: Address
📁 List: wa.txt
🎯 Targets: 30
⏳ Testing in progress...
```

**Scan Complete:**
```
✅ Scan Complete
📋 Mode: Address
📁 List: wa.txt
⏱️  Duration: 142.5s

━━━━━━━━━━━━━━━━━━
📊 Results:
✅ Connected: 8/30 (26.7%)
❌ Failed: 22/30
━━━━━━━━━━━━━━━━━━

✅ Connected Targets:
  • web.whatsapp.com
  • v.whatsapp.net
  • media.whatsapp.net
  • cdn.whatsapp.net
  ... and 4 more

💾 Result: wa_result.txt
```

**Batch Complete:**
```
🎊 Batch Scan Complete

📦 Total Lists: 3
⏱️  Total Duration: 497.5s
✅ Total Connected: 25/105

━━━━━━━━━━━━━━━━━━
🎉 wa.txt
   8/30 (26.7%) - 142.5s

✅ ig.txt
   12/40 (30.0%) - 198.2s

⚠️  tiktok.txt
   5/35 (14.3%) - 156.8s
```

### Dual Network Safe ⚠️

**PENTING untuk Linux dual network:**

- **Telegram bot** → Pakai WiFi USB (wlan0 - internet)
- **Xray testing** → Pakai WiFi Laptop (wlan1 - kuota)

Bot menggunakan default routing (internet), tidak terikat ke interface testing!

---

## 📚 Scan History

Track all your scans with detailed results.

### View History:
```bash
python jhopan.py
[11] View History

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    Date/Time            List      Mode      Result        Time
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1]  2024-12-24 14:30     wa.txt    Address   8/30 (26.7%)  142.5s
[2]  2024-12-24 13:15     ig.txt    SNI       12/40 (30%)   198.2s
[3]  2024-12-23 20:00     tiktok    Wildcard  5/35 (14.3%)  156.8s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### View Details:
```bash
[?] Select: 1

Scan Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date/Time: 2024-12-24 14:30
Mode: Address
List File: wa.txt
Duration: 142.5s
Success Rate: 26.7% (8/30)

✅ Connected (8):
  ✅ web.whatsapp.com
  ✅ v.whatsapp.net
  ✅ media.whatsapp.net
  ✅ cdn.whatsapp.net
  ... and 4 more

❌ Failed (22):
  ❌ static.whatsapp.net
  ❌ graph.whatsapp.net
  ... and 20 more
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Features:
- Auto save setiap scan
- Simpan connected & failed targets
- Keep last 50 scans
- Delete all history option

---

## 📊 Live Progress Bar

Real-time feedback saat scanning.

### Example:
```
[████████░░] 80% (40/50) ✅ 12  ❌ 28  | web.whatsapp.com
```

**Shows:**
- Progress bar dengan warna
- Success rate real-time
- Current target being tested
- Success/failed count

**Colors:**
- 🟢 Green: >50% success
- 🟡 Yellow: 20-50% success
- 🔴 Red: <20% success

**Disable:**
```bash
[10] Settings
[5] Show Progress Bar: OFF
```

---

## 🎯 Workflow Examples

### Example 1: Quick Scan
```bash
python jhopan.py
[1] Address
[1] MyVPN  # Quick select
wa.txt

# Uses defaults: timeout 5s, sequential, auto retry 2x
# Shows live progress
# Saves to wa_result.txt
# Telegram notification ✓
# History saved ✓
```

### Example 2: Fast Parallel Scan
```bash
# First, configure:
[10] Settings
[2] Parallel Jobs: 5

# Then scan:
[1] Address
[1] MyVPN
ig.txt

# 5x faster!
```

### Example 3: Batch All Lists
```bash
[12] Batch Mode
wa.txt,ig.txt,tiktok.txt,line.txt,music.txt
[1] Address
[1] MyVPN

# Scans all lists automatically
# Telegram summary at end
```

### Example 4: Dual Network Testing
```bash
sudo python3 jhopan.py
[1] Address
[1] MyVPN
wa.txt

[*] Network Mode: [2] Advanced
[2] wlan1 (kuota provider)

# Testing via kuota
# Telegram via internet
# Perfect isolation!
```

---

## 📂 Files Created

**Settings:**
- `jhopan_settings.json` - Your configuration

**History:**
- `jhopan_history.json` - Scan history (last 50)

**Accounts:**
- `accounts.json` - Saved VPN URLs

**Results:**
- `<list>_result.txt` - Connected targets per list

---

## 🔧 Troubleshooting

**Telegram not working?**
- Check token & chat ID
- Test: Send message to bot first
- Firewall blocking?

**Parallel too fast = errors?**
- Reduce parallel jobs
- Provider rate limiting

**Auto retry not working?**
- Check settings: Auto Retry ON
- Network too unstable? Increase retry count

**History not showing?**
- File: `jhopan_history.json`
- Delete if corrupted, will recreate

**Dual network - Telegram fails?**
- Telegram uses default route automatically
- Check wlan0 has internet
- Bot doesn't bind to testing interface

---

Jhopan v3.3 - Happy Bug Hunting! 🚀
