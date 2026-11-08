#!/usr/bin/env bash
# ==============================================================================
# Algic Keyboard Input Matrix - Modular Cross-Distro Build Engine
# Maintainer: necrose99
# Target Dialects: Miami-Illinois (mia), Potawatomi (pot), Kickapoo (kik), Blackfoot (bla)
# ==============================================================================

set -e # Exit immediately on internal command failures

# 1. Default Configuration & Path Fallbacks (Overrideable by Makefile/Ebuild)
VERSION="${VERSION:-2026.11.08}"
PREFIX="${PREFIX:-/usr}"
DESTDIR="${DESTDIR:-}"

# Deduce standard target distribution filesystem layouts
TABLE_DIR="${DESTDIR}${PREFIX}/share/ibus-table/tables"
INPUTRC_DIR="${DESTDIR}${PREFIX}/share/algic-ibus/inputrc"
DOC_DIR="${DESTDIR}${PREFIX}/share/doc/algic-ibus-${VERSION}"

INPUT_SRC="_inputrc.in"
TABLE_SRC="algic_keys.txt"
DOC_SRC="Readme.md"
BUILD_OUT="build_out"

# Helper for unified logging
log_info() { echo -e "\e[32m[*]\e[0m $1"; }
log_warn() { echo -e "\e[33m[!]\e[0m $1"; }

echo "========================================================================"
echo " 🏗️  Algic Modular Compilation Pipeline Engine"
echo "========================================================================"

# ------------------------------------------------------------------------------
# Phase 1: Clean and Prepare Build Directory Staging Sandbox
# ------------------------------------------------------------------------------
rm -rf "$BUILD_OUT"
mkdir -p "$BUILD_OUT"

# ------------------------------------------------------------------------------
# Phase 2: Execute Splitter Component Engines
# ------------------------------------------------------------------------------
if [ -f "split_algic.py" ]; then
    log_info "Executing Python3 split matrix engine for version ${VERSION}..."
    python3 split_algic.py "$TABLE_SRC" "$INPUT_SRC" "$BUILD_OUT" "$VERSION"
else
    log_warn "split_algic.py script missing. Falling back to monolithic configuration."
    # If python splitter is not used, manually stage items to build directory
    cp "$INPUT_SRC" "$BUILD_OUT/inputrc.all"
    if [ -f "$TABLE_SRC" ]; then
        ibus-table-createdb -n "$BUILD_OUT/algic_keys.db" -s "$TABLE_SRC"
    fi
fi

# ------------------------------------------------------------------------------
# Phase 3: Stage Compiled Assets to Target Image (DestDir Installation)
# ------------------------------------------------------------------------------
# Check if the execution context is an actual install pass or just a local build pass
if [ "$1" == "--install" ]; then
    log_info "Installing layouts into target package image boundaries..."

    # Deploy IBus Engines
    if ls "$BUILD_OUT"/*.db &>/dev/null; then
        mkdir -p "$TABLE_DIR"
        cp "$BUILD_OUT"/*.db "$TABLE_DIR/"
        chmod 644 "$TABLE_DIR"/*.db
        log_info "Staged IBus engine binaries inside: $TABLE_DIR"
    fi

    # Deploy GNU Readline Split Sub-modules
    if ls "$BUILD_OUT"/inputrc.* &>/dev/null; then
        mkdir -p "$INPUTRC_DIR"
        cp "$BUILD_OUT"/inputrc.* "$INPUTRC_DIR/"
        chmod 644 "$INPUTRC_DIR"/*
        log_info "Staged terminal profiles inside: $INPUTRC_DIR"
    fi

    # Deploy Package Documentation
    if [ -f "$DOC_SRC" ]; then
        mkdir -p "$DOC_DIR"
        cp "$DOC_SRC" "$DOC_DIR/README.md"
        chmod 644 "$DOC_DIR/README.md"
        log_info "Staged global package layout blueprints inside: $DOC_DIR"
    fi

    echo "========================================================================"
    log_info "Deployment staging finalized successfully!"
    echo "========================================================================"
else
    log_info "Compilation completed inside local sandbox: ./${BUILD_OUT}/"
    log_info "Run with '--install' or use your 'Makefile' to map to system targets."
fi
