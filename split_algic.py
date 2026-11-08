#!/usr/bin/env python3
# ==============================================================================
# Algic Keyboard Input Matrix - Hierarchical Glottolog Compiler Engine
# Maintainer: necrose99
# Target Environment: Canada / Alpine Target Sandbox / Generic Cross-Distro
# ==============================================================================

import os
import sys
import subprocess
import re

# ------------------------------------------------------------------------------
# 1. Glottolog-Style Hierarchical Registry Matrix
# ------------------------------------------------------------------------------
REGIONAL_TREE = {
    "plains": {
        "NAME": "Plains Algonquian",
        "ALLOWED_CHARS": "abcdefg'hijklmnopstwyz·-",
        "SUB_REGIONS": {
            "siksika": {"NAME": "Blackfoot", "TAGS": ["bla"]},
            "arapahoan": {"NAME": "Arapaho-Gros Ventre", "TAGS": ["arp", "ats"]},
            "cheyenne": {"NAME": "Cheyenne", "TAGS": ["chy"]}
        }
    },
    "central": {
        "NAME": "Central Algonquian Node",
        "ALLOWED_CHARS": "abcdefg'hijklmnopstwyzžšéÉčČ·-^",
        "SUB_REGIONS": {
            "cree-innu": {"NAME": "Cree-Innu Continuum", "TAGS": ["cre", "csw", "crj", "atj", "crk"]},
            "ca-proper": {"NAME": "Central Algonquian Proper", "TAGS": ["mia", "pot", "sac", "kic", "kic-us", "kic-mx", "sjw", "mez"]},
            "ojibwean": {"NAME": "Ojibwe-Ottawa-Chippewa", "TAGS": ["oji", "otw", "ciw"]}
        }
    },
    "eastern": {
        "NAME": "Eastern Algonquian Core",
        "ALLOWED_CHARS": "abcdefg'hijklmnopstwyz·-",
        "SUB_REGIONS": {
            "maritime": {"NAME": "Maritime / Mi'kmaw-Maliseet", "TAGS": ["mic", "pqm"]},
            "abenakian": {"NAME": "Abenaki", "TAGS": ["abe", "aaq"]},
            "southern-new-england": {"NAME": "Southern New England / Mohegan", "TAGS": ["xpq", "xlb"]},
            "delawarean": {"NAME": "Delaware / Munsee-Unami", "TAGS": ["umu", "unm"]}
        }
    },
    "carolinas": {
        "NAME": "Carolina Algonquian (Southern Eastern)",
        "ALLOWED_CHARS": "abcdefg'hijklmnopstwyz·-",
        "SUB_REGIONS": {
            "powhatan": {"NAME": "Powhatan (Virginia)", "TAGS": ["pim"]},
            "pamlico": {"NAME": "Carolina / Lumbee-Pamlico", "TAGS": ["crr"]}
        }
    },
    "western": {
        "NAME": "Western Algic (California Isolates)",
        "ALLOWED_CHARS": "abcdefg'hijklmnopstwyzłłɣɹ·-",
        "SUB_REGIONS": {
            "yurok": {"NAME": "Yurok", "TAGS": ["yur"]},
            "wiyot": {"NAME": "Wiyot", "TAGS": ["wiy"]}
        }
    },
    "proto": {
        "NAME": "Proto-Algonquian Historical Reconstructions",
        "ALLOWED_CHARS": "abcdefg'hijklmnopstwyz·-ɬθʔç*·^",
        "SUB_REGIONS": {
            "reconstructions": {"NAME": "Proto-Algonquian Core", "TAGS": ["alg-pro", "alg-x-pro"]}
        }
    },
    "remnants": {
        "NAME": "Lost / Extinct / Uncertain Remnants",
        "ALLOWED_CHARS": "abcdefg'hijklmnopstwyz·-",
        "SUB_REGIONS": {
            "beothukan": {"NAME": "Beothuk (Newfoundland Isolate?)", "TAGS": ["bue", "beot1247"]},
            "etchemin": {"NAME": "Etchemin", "TAGS": ["etc"]},
            "loup-a": {"NAME": "Loup A", "TAGS": ["xlo"]}
        }
    }
}

UUID_BASE = "2f9a0b1c-0d1e-2f3a-4b5c-"

# ------------------------------------------------------------------------------
# 2. Dynamic Routing & Mapping Helpers
# ------------------------------------------------------------------------------
def get_iso_metadata(iso_code):
    """Traces an ISO tag down the Glottolog tree hierarchy to extract names and traits."""
    target = iso_code.lower().strip()
    for reg_id, reg_meta in REGIONAL_TREE.items():
        for sub_id, sub_meta in reg_meta["SUB_REGIONS"].items():
            # Support exact matches or expansion keywords like 'ca-proper'
            if target in sub_meta["TAGS"] or target == sub_id:
                return {
                    "region": reg_id,
                    "sub_region": sub_id,
                    "display_name": f"{reg_meta['NAME']} -> {sub_meta['NAME']}",
                    "allowed_chars": reg_meta["ALLOWED_CHARS"]
                }
    return None

def generate_ibus_header(iso_code, meta, version):
    """Generates standard compliant IBus metadata configuration headers."""
    padded_iso = iso_code.ljust(12, '0')[:12]
    derived_uuid = f"{UUID_BASE}{padded_iso[:4]}-{padded_iso[4:12]}"
    return f"""### IMKTable source file
### Dynamically generated via split_algic.py
BEGIN_GE_P_AMB
END_GE_P_AMB
BEGIN_CHAR_PROMPTS
END_CHAR_PROMPTS
BEGIN_TABLE
STATUS_PROMPT = {iso_code.upper()[:3]}
NAME = Algic ({meta['display_name']})
NAME.en = Algic ({meta['display_name']})
UUID = {derived_uuid}
SERIAL_NUMBER = {version}-{iso_code}
VERSION = {version}
AUTHOR = necrose99
MAX_KEY_LENGTH = 12
ALLOWED_CHARS = {meta['allowed_chars']}
"""

# ------------------------------------------------------------------------------
# 3. Core Structural Processing Blocks
# ------------------------------------------------------------------------------
def process_pipeline(source_txt, source_rc, dest_dir, version):
    os.makedirs(dest_dir, exist_ok=True)
    iso_table_rows = {}
    iso_rc_rows = {}

    # Pass A: Parse Graphical Layout Dictionaries (algic_keys.txt)
    if os.path.exists(source_txt):
        print("[+] Processing graphical layout matrices...")
        with open(source_txt, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip() or line.startswith('#'):
                    continue
                
                # Identify explicit tag descriptors (e.g., # tags: mia, pot, ca-proper)
                found_tags = re.findall(r'\b([a-z0-9\-–]+)\b', line.lower())
                
                for tag in found_tags:
                    # Resolve tag expansion rules (e.g., expanding ca-proper list)
                    if tag == "ca-proper":
                        sub_tags = REGIONAL_TREE["central"]["SUB_REGIONS"]["ca-proper"]["TAGS"]
                    else:
                        sub_tags = [tag]
                        
                    for sub_tag in sub_tags:
                        meta = get_iso_metadata(sub_tag)
                        if meta:
                            iso_table_rows.setdefault(sub_tag, []).append(line.strip())

    # Pass B: Parse Terminal Readline Macros (_inputrc.in)
    if os.path.exists(source_rc):
        print("[+] Processing GNU Readline macro files...")
        active_tags = []
        with open(source_rc, 'r', encoding='utf-8') as f:
            for line in f:
                # Catch regional comment boundary context changes
                if 'tags:' in line.lower() or 'module:' in line.lower():
                    raw_tags = re.findall(r'\b([a-z0-9\-–]+)\b', line.lower())
                    active_tags = []
                    for t in raw_tags:
                        if t == "ca-proper":
                            active_tags.extend(REGIONAL_TREE["central"]["SUB_REGIONS"]["ca-proper"]["TAGS"])
                        elif get_iso_metadata(t):
                            active_tags.append(t)
                
                if line.strip() and not line.startswith('#'):
                    for tag in active_tags:
                        iso_rc_rows.setdefault(tag, []).append(line)

    # ------------------------------------------------------------------------------
    # 4. Compilation Execution Block (Situation: Bottom Routing Registry)
    # ------------------------------------------------------------------------------
    all_discovered_keys = set(iso_table_rows.keys()).union(set(iso_rc_rows.keys()))
    
    for iso in sorted(all_discovered_keys):
        meta = get_iso_metadata(iso)
        print(f"[+] Compiling dialect sub-module pipeline: {iso.upper()}")
        
        # Build out targeted graphic database tables
        if iso in iso_table_rows:
            staging_file = os.path.join(dest_dir, f"algic_{iso}.txt")
            final_db = os.path.join(dest_dir, f"algic_{iso}.db")
            
            with open(staging_file, 'w', encoding='utf-8') as out:
                out.write(generate_ibus_header(iso, meta, version))
                out.write("BEGIN_TABLE\n")
                out.write("\n".join(iso_table_rows[iso]))
                out.write("\nEND_TABLE\n")
                
            subprocess.run(['ibus-table-createdb', '-n', final_db, '-s', staging_file], 
                           check=True, stdout=subprocess.DEVNULL)
            os.remove(staging_file)
            print(f"    ↳ Successfully baked asset: {os.path.basename(final_db)}")

        # Build out targeted terminal macro configuration sheets
        if iso in iso_rc_rows:
            output_rc = os.path.join(dest_dir, f"inputrc.{iso}")
            with open(output_rc, 'w', encoding='utf-8') as out:
                out.write(f"# Compiled Terminal Macro Overlays for: {meta['display_name']}\n")
                out.write("".join(iso_rc_rows[iso]))
            print(f"    ↳ Successfully baked profile: {os.path.basename(output_rc)}")

if __name__ == "__main__":
    # Handle inputs passed natively down via build.sh or Makefile targets
    infile_txt = sys.argv[1] if len(sys.argv) > 1 else "algic_keys.txt"
    infile_rc  = sys.argv[2] if len(sys.argv) > 2 else "_inputrc.in"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "./build_out"
    pkg_version = sys.argv[4] if len(sys.argv) > 4 else "2026.11.08"
    
    process_pipeline(infile_txt, infile_rc, output_dir, pkg_version)
    print("========================================================================")
    print("[+] All localized sub-modules processed under target version definitions.")
    print("========================================================================")
