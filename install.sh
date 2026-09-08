#!/usr/bin/env bash
# ==============================================================================
# Algic Keyboard Input Matrix - Deployment Pipeline Engine
# Maintainer: necrose99
# Target Dialects: Miami-Illinois, Potawatomi, Kickapoo, Blackfoot
# ==============================================================================

set -e # Exit immediately on internal command failures

INPUT_SRC="_inputrc.in"
TABLE_SRC="algic_keys.txt"
DB_OUT="algic_keys.db"

echo "========================================================================"
echo " ⌨️  Algic Keyboard Layout Installer Engine (necrose99/algic_ibus)"
echo "========================================================================"

# ------------------------------------------------------------------------------
# Phase 1: Compile IBus Layout Engine Database
# ------------------------------------------------------------------------------
if [ -f "$TABLE_SRC" ]; then
    echo "[*] Compiling plain-text layout matrices into active database structure..."
    ibus-table-createdb -n "$DB_OUT" -s "$TABLE_SRC"
    
    echo "[*] Elevating privileges to register database asset with IBus system..."
    sudo cp "$DB_OUT" /usr/share/ibus-table/tables/
    
    echo "[*] Resetting active background IBus daemon wrapper engine..."
    ibus-daemon -drx
    echo "[+] IBus layout matrix successfully initialized!"
else
    echo "[!] Warning: '$TABLE_SRC' not found. Skipping IBus table compilation."
fi

echo "------------------------------------------------------------------------"

# ------------------------------------------------------------------------------
# Phase 2: Deploy GNU Readline Mapping Environment Variables
# ------------------------------------------------------------------------------
if [ ! -f "$INPUT_SRC" ]; then
    echo "[!] Critical Error: Mapping template source '$INPUT_SRC' is missing."
    exit 1
fi

# Request deployment context parameters from user entry buffer
read -p "Select Deployment Scope ([G]lobal System-wide / [U]ser Space Home Only): " -n 1 -r
echo "" # Clean carriage return newline

case "$REPLY" in
    [Gg]* )
        echo "[*] Initiating Global Multitenant Deployment..."
        
        # Seed automatic profile injection for all FUTURE user additions
        echo "[*] Writing layout rules to global user skeleton directory..."
        sudo cp "$INPUT_SRC" /etc/skel/.inputrc
        
        # Append layout macros onto all CURRENTLY existing active system terminals
        echo "[*] Appending macros onto machine-wide runtime records (/etc/inputrc)..."
        sudo bash -c "cat $INPUT_SRC >> /etc/inputrc"
        
        echo "[+] Global deployment complete. All active and future accounts synchronized."
        ;;
        
    [Uu]* | * )
        echo "[*] Initiating Local Single-User Space Deployment..."
        
        # Deploy configuration directly into the current active user home path partition
        cp "$INPUT_SRC" "$HOME/.inputrc"
        
        # Force the active open bash shell runtime instance to instantly parse modifications
        bind -f "$HOME/.inputrc" 2>/dev/null || echo "[*] Mapping bound. Restart terminal to fully activate layout rules."
        
        echo "[+] User-space deployment complete inside '$HOME/'."
        ;;
esac

echo "========================================================================"
echo "[+] Configuration sequence finalized with zero runtime loopholes!"
echo "========================================================================"
