# ⌨️ Algic Input Configuration Layout Matrix

This directory hosts localized keyboard layout configurations and terminal bindings optimized for entering Algic language orthographies (including Myaamia, Potawatomi, Kickapoo, Blackfoot). These utilities map custom modified combinations natively to output specialized unicode glyphs like `š`, `ž`, `č`, and macrons (`ā`, `ē`, `ī`, `ō`).

## ⚙️ Installation Instructions

### 1. IBus Table Layout Engine Setup
Compiling and registering your custom language input engine database allows system-wide desktop accessibility across your native desktop environments.

Execute these commands from inside your terminal instance:
```bash
# Compile the plaintext layout script mapping table into an active database structure
ibus-table-createdb -n algic_keys.db -s algic_keys.txt

# Relocate the compiled table asset directly to the global engine registry folder
sudo cp algic_keys.db /usr/share/ibus-table/tables/

# Restart the active background IBus daemon wrapper engine to sync additions dynamically
ibus-daemon -drx
```
*Note: Once reloaded, open your OS settings panel under Keyboard/Input Methods and manually append the newly compiled `Algic_Input_Matrix` profile.*

---