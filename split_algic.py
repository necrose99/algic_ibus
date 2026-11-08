#!/usr/bin/env python3
import os
import sys
import subprocess

# Define the dialect modules and their associated language tags matching your repo spec
DIALECTS = {
    "central": {
        "NAME": "Algic (Central - alg/sac/shw/kik)",
        "UUID": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
        "TAGS": ["alg", "sac", "shw", "kik"]
    },
    "myaamia": {
        "NAME": "Algic (Myaamia & Potawatomi - mia/pot)",
        "UUID": "b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
        "TAGS": ["mia",]
    },
    "california": {
        "NAME": "Algic (California Isolates - yur/wiy)",
        "UUID": "c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f",
        "TAGS": ["yur", "wiy"]
    }
}
# Add this directly to your DIALECTS mapping dictionary
"potawatomi": {
    "NAME": "Bodéwadminwen (Potawatomi - pot)",
    "UUID": "d4e5f6a7-8b9c-0d1e-2f3a-4b5c6d7e8f9a",
    "TAGS": ["pot", "bodewadmi"],
    # Ensure the engine explicitly permits the accented characters and glottal markers
    "ALLOWED_CHARS": "abcdefg'hijklmnopstwyzžšéÉ·-" 
}

def generate_header(name, uuid, version):
    return f"""### IMKTable source file
### Dynamically generated splitter engine
BEGIN_GE_P_AMB
END_GE_P_AMB
BEGIN_CHAR_PROMPTS
END_CHAR_PROMPTS
BEGIN_TABLE
STATUS_PROMPT = ALG
NAME = {name}
NAME.en = {name}
UUID = {uuid}
SERIAL_NUMBER = {version}
VERSION = {version}
AUTHOR = necrose99
MAX_KEY_LENGTH = 12
ALLOWED_CHARS = abcdefghijklmnopqrstuvwxyz'·-
"""

def split_and_compile(source_txt, dest_dir, version):
    if not os.path.exists(source_txt):
        print(f"[-] Source file {source_txt} not found.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(dest_dir, exist_ok=True)
    
    # Initialize isolated row collections
    dialect_rows = {k: [] for k in DIALECTS.keys()}
    
    print("[+] Sorting dictionary matrices into sub-modules...")
    with open(source_txt, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            # Match layout mapping to target sub-modules by checking inline comments or designators
            matched = False
            for key, config in DIALECTS.items():
                if any(tag in stripped.lower() for tag in config["TAGS"]):
                    dialect_rows[key].append(stripped)
                    matched = True
                    break
            
            # Fallback to Central group if no distinct tags match
            if not matched:
                dialect_rows["central"].append(stripped)

    # Compile each submodule independently
    for key, config in DIALECTS.items():
        if not dialect_rows[key]:
            print(f"[!] Skipping {key}: No matching mapping constraints found.")
            continue
            
        staging_txt = os.path.join(dest_dir, f"algic_{key}.txt")
        compiled_db = os.path.join(dest_dir, f"algic_{key}.db")
        
        # Write temporary compilation matrix
        with open(staging_txt, 'w', encoding='utf-8') as out:
            out.write(generate_header(config["NAME"], config["UUID"], version))
            out.write("BEGIN_TABLE\n")
            out.write("\n".join(dialect_rows[key]))
            out.write("\nEND_TABLE\n")
            
        print(f"[+] Compiling sub-module sub-system: {compiled_db}")
        try:
            subprocess.run(
                ['ibus-table-createdb', '-n', compiled_db, '-s', staging_txt],
                check=True, stdout=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError as e:
            print(f"[-] Failed compiling database layout matrix for {key}: {e}", file=sys.stderr)
        finally:
            if os.path.exists(staging_txt):
                os.remove(staging_txt)

if __name__ == "__main__":
    # Expects format: script.py <input_file> <output_directory> <version>
    src = sys.argv[1] if len(sys.argv) > 1 else "algic_keys.txt"
    dest = sys.argv[2] if len(sys.argv) > 2 else "./build_output"
    ver = sys.argv[3] if len(sys.argv) > 3 else "20261108"
    
    split_and_compile(src, dest, ver)
