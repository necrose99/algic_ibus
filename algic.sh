# /etc/profile.d/algic.sh - Transient terminal input runtime mapper for Algic IBus
# Dynamically configures GNU Readline mappings for the active terminal session.

if [ -n "$BASH_VERSION" ] || [ -n "$ZSH_VERSION" ]; then
    # 1. Determine active dialect context (Explicit variable override wins first)
    local active_dialect="${ALGIC_DIALECT}"
    
    if [ -z "$active_dialect" ]; then
        # Automatically fallback by checking POSIX ISO language identifiers
        case "${LANG:-$LC_CTYPE}" in
            pot* | *pot_*)  active_dialect="potawatomi" ;;
            mia* | *mia_*)  active_dialect="myaamia"    ;;
            kik* | *kik_*)  active_dialect="kickapoo"   ;;
            bla* | *bla_*)  active_dialect="blackfoot"  ;;
            yur* | *yur_*)  active_dialect="california" ;;
            wiy* | *wiy_*)  active_dialect="california" ;;
            sac* | *sac_*)  active_dialect="central"    ;;
            shw* | *shw_*)  active_dialect="central"    ;;
            *)              active_dialect=""           ;; # Default safety boundary
        esac
    fi

    # 2. Inject target dialect layout profile into active terminal workspace
    if [ -n "$active_dialect" ]; then
        local target_rc="/usr/share/algic-ibus/inputrc/inputrc.${active_dialect}"
        
        if [ -f "$target_rc" ] && [ -r "$target_rc" ]; then
            # Bind the specified layout map definitions natively without subshell leakage
            if type bind &>/dev/null; then
                bind -f "$target_rc" 2>/dev/null || true
            fi
        fi
    fi
fi
