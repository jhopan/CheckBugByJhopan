# Changelog v3.3.1 - Telegram Interface Selection

## 🆕 New Feature: Telegram Interface Selection

### What's New?

Telegram bot sekarang bisa dikonfigurasi untuk menggunakan interface jaringan spesifik! 

Perfect untuk setup **dual network/dual WiFi** di Linux:
- **wlan0** (WiFi USB) → Internet access → Untuk Telegram
- **wlan1** (WiFi Laptop) → Kuota only → Untuk Xray testing

### Changes:

#### 1. Settings Enhancement
- **New Setting**: `telegram_interface` (default: "auto")
- **New Menu**: [8] Telegram Interface Selection
- **New Button**: [T] Test Telegram Connection

#### 2. Auto Default Mode
- Default: "auto" (uses default routing)
- Recommended untuk single network setup
- No configuration needed

#### 3. Manual Interface Selection
- List all available network interfaces
- Select specific interface for Telegram
- Warning: Interface must have internet!

#### 4. Socket Binding Implementation
- Telegram API calls bind to specific interface IP
- Fallback to default route if binding fails
- Cross-platform compatible

### Technical Details:

**Files Modified:**
1. `utils/settings.py`
   - Added `telegram_interface` to DEFAULT_SETTINGS
   - Added menu option [8] for interface selection
   - Added [T] for testing connection
   - Import telegram_bot for test function

2. `utils/telegram_bot.py`
   - Added `interface` parameter to all functions
   - Implemented `get_interface_ip()` helper
   - Socket binding in `send_telegram_message()`
   - Updated all notification functions

3. `jhopan.py`
   - Pass `telegram_interface` from settings to bot functions
   - Updated 3 Telegram notification calls
   - Version bump to v3.3.1

4. Documentation
   - Updated `README.md` (v3.3.1)
   - Enhanced `ADVANCED_FEATURES.md` with interface guide
   - Added usage examples and warnings

### Usage Example:

```bash
python jhopan.py
[10] Settings
[8] Telegram Interface

[1] Auto (default route) - Recommended
[2] wlan0 - 192.168.1.100
[3] wlan1 - 192.168.43.1

[?] Select (1-3): 2
[+] Telegram: wlan0 (192.168.1.100)
[!] Warning: Interface must have internet!

# Test connection
[T] Test Telegram Connection
🤖 Bot Test
✅ Bot configured successfully!
🌐 Using interface: wlan0
```

### Benefits:

✅ **Dual Network Support**: Perfect untuk Linux dual WiFi setup  
✅ **Auto Default**: Works out of the box, no config needed  
✅ **Manual Override**: Full control when needed  
✅ **Safe Fallback**: Auto falls back if binding fails  
✅ **Easy Testing**: Test button untuk verify connection  
✅ **Clear Warnings**: User diperingatkan tentang internet requirement  

### Backward Compatibility:

✅ Existing settings tetap work (auto default)  
✅ No breaking changes  
✅ Optional feature  

---

**Version**: 3.3.1  
**Date**: 2024  
**Author**: Jhopan  
