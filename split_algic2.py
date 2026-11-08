# Upgraded Linguistic Matrix matching necrose99/algic_ibus layout map specs
DIALECTS = {
    "plains": {
        "NAME": "Algic (Plains Branch - bla/arp/ats/chy)",
        "UUID": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
        "TAGS": ["bla", "blackfoot", "arp", "arapaho", "ats", "gros ventre", "chy", "cheyenne"]
    },
    "central": {
        "NAME": "Algic (Central / Great Lakes - pot/mia/oji/kic/cre...)",
        "UUID": "b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
        "TAGS": [
            "mez", "menominee", "cre", "csw", "crj", "atj", "atikamekw",
            "pot", "potawatomi", "oji", "ojibwe", "otw", "ottawa", "ciw", "chippewa",
            "mia", "miami", "sac", "fox", "meskwaki", "kic", "kickapoo", "sjw", "shawnee"
        ]
    },
    "eastern": {
        "NAME": "Algic (Eastern Algonquian - mic/abe/umu/unm...)",
        "UUID": "c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f",
        "TAGS": [
            "pim", "powhatan", "crr", "lumbee", "qyp", "quiripi", "naugatuck", "unquachog",
            "mic", "mi'kmaq", "abe", "abenaki", "aaq", "pqm", "maliseet", "xpq", "mohegan",
            "pequot", "umu", "munsee", "unm", "unami", "xlb", "loup"
        ]
    },
    "proto": {
        "NAME": "Algic (Proto-Algonquian Reconstructions - alg-pro)",
        "UUID": "d4e5f6a7-8b9c-0d1e-2f3a-4b5c6d7e8f9a",
        "TAGS": ["alg-pro", "proto-algonquian", "alg-x-pro"]
    },
    "western": {
        "NAME": "Algic (Western / California Isolates - yur/wiy)",
        "UUID": "e5f6a7b8-9c0d-1e2f-3a4b-5c6d7e8f9a0b",
        "TAGS": ["yur", "yurok", "wiy", "wiyot"]
    },
    "remnants": {
        "NAME": "Algic (Remnant / Uncertain / Extinct - bue/etc/xlo)",
        "UUID": "f6a7b89c-0d1e-2f3a-4b5c-6d7e8f9a0b1c",
        "TAGS": ["bue", "beothuk", "beot1247", "etc", "etchemin", "xlo"]
    }
}
def get_target_branch(line_text):
    clean_line = line_text.lower().strip()
    
    # Strategy A: Check explicit trailing or leading comment tag bounds (Highly Recommended)
    # e.g., "e	é  # pot" or "e	é  # [pot]"
    if '#' in clean_line:
        comment_part = clean_line.split('#')[-1]
        for branch, config in DIALECTS.items():
            if any(f"{tag}" in comment_part for tag in config["TAGS"]):
                return branch

    # Strategy B: Fallback to scanning tokens in the full row mapping sequence
    for branch, config in DIALECTS.items():
        for tag in config["TAGS"]:
            # Match if the tag is wrapped by spaces, brackets, colons, or punctuation
            if any(wrapper in clean_line for wrapper in [f" {tag}", f"[{tag}]", f"({tag})", f"{tag}:"]):
                return branch
                
    return None # Fallback default can catch unmapped rows safely

