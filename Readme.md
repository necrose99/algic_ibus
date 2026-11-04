# ⌨️ Algic Input Configuration Layout Matrix

This directory hosts localized keyboard layout configurations and terminal bindings optimized for entering Algic language orthographies, historical reconstructions, and isolate branches. 

These utilities map custom key stroke combinations natively to specialized unicode glyphs across the entire linguistic continuum:
*   **Myaamia & Potawatomi (`mia`, `pot`):** Supporting `š`, `ž`, `č`, acute vowels (`é`, `É`), and long-vowel macrons (`ā`, `ē`, `ī`, `ō`).
*   **Proto-Algonquian & Central Dialects (`alg`, `sac`, `shw`, `kik`):** Supporting historical reconstructions (`*p`, `*t`, `*k`), the voiceless lateral fricative (`ɬ`), theta (`θ`), and glottal stops (`ʔ`).
*   **California Isolates (`yur`, `wiy`):** Supporting Yurok and Wiyot unique structural markers like soft gamma (`ɣ`), barred-l (`ł`), and postalveolar approximants (`ɹ`).

---

## 🏗️ Repository Architecture

The project splits layout injection rules into two decoupled files to prevent system environment syntax errors:
1.  **`_inputrc.in`**: Contains native GNU Readline configuration bindings mapped to `Alt` (Meta) and sequential chords for terminal environments (e.g., `bash`).
2.  **`algic_keys.txt`**: The plain-text source dictionary dictionary compiled directly into binary databases for graphical desktop interface integration.

---

## ⚙️ Installation Instructions

### 1. Unified Graphical Environment Setup (IBus Table Engine)

Compiling and registering your custom language input engine database allows system-wide desktop accessibility across graphical applications, browsers, and text editors.

Execute these commands from inside your repository root:

```bash
# 1. Compile the plaintext layout script mapping table into an active database structure
# (Ensure columns in algic_keys.txt are strictly separated by literal Tab characters)
ibus-table-createdb -n algic_keys.db -s algic_keys.txt

# 2. Relocate the compiled table asset directly to your engine registry folder
# Choose ONE of the paths below based on your permission constraints:

# Option A: Global System-Wide Installation (Requires Root)
sudo cp algic_keys.db /usr/share/ibus-table/tables/

# Option B: Local User-Space Isolation Sandbox (Recommended)
mkdir -p ~/.local/share/ibus-table/tables/
cp algic_keys.db ~/.local/share/ibus-table/tables/

# 3. Clear the active layout cache and recycle the background IBus daemon pipeline
ibus exit || true
rm -f ~/.cache/ibus/bus/*
ibus-daemon -drx
```

*Note: Once reloaded, open your OS Desktop Settings Control Panel under **Keyboard -> Input Methods**, click "Add", select your language target, and append the newly compiled `Algic_Input_Matrix` profile.*

### 2. Terminal Macro Integration (`~/.inputrc`)

To bake direct keystroke mapping transformations smoothly inside your Command Line Interface shell environments without graphical IME overlays:

```bash
# Append your repository mapping rules securely to your user home profile
# (The sequence forces a trailing newline to prevent existing binding collisions)
[ -f "\$HOME/.inputrc" ] && sed -i -e '\(a\' "\)HOME/.inputrc"
cat _inputrc.in >> "\$HOME/.inputrc"

# Instantly reload your current active terminal session's readline definitions
bind -f "\$HOME/.inputrc"
```

---

## 🚀 Generic Linux Release Tarballs

If you are deploying onto a lean target framework (such as Alpine Linux) or distributed user clients without a local toolchain environment, this repository features an automated GitHub Actions pipeline that builds a self-contained release package.

When you download a compiled `algic_ibus-linux-generic.tar.gz` distribution bundle, you do not need compiler packages (`ibus-table-createdb`). Simply untar the pre-baked asset tree and run the bundled deployment runtime script:

```bash
# Unpack the pre-compiled distribution release bundle
tar -xzvf algic_ibus-linux-generic.tar.gz
cd algic_ibus-linux-generic/

# Run the automated user-space deployment script
./install.sh
```
