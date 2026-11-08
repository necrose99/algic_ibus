# Makefile for algic_ibus module distribution pipeline
VERSION  ?= 1.0.0
PREFIX   ?= /usr
DATADIR  ?= $(PREFIX)/share
TABLEDIR ?= $(DATADIR)/ibus-table/tables
DESTDIR  ?=

SRC_TXT  := algic_keys.txt
BUILD_DIR:= build_out

.PHONY: all split clean install

all: split

split:
	@echo "[+] Splitting and compiling engines for Version $(VERSION)..."
	python3 split_algic.py "$(SRC_TXT)" "$(BUILD_DIR)" "$(VERSION)"

install: all
	@echo "[+] Staging compiled layout tables inside target payload system..."
	install -d "$(DESTDIR)$(TABLEDIR)"
	install -m 0644 $(BUILD_DIR)/*.db "$(DESTDIR)$(TABLEDIR)/"

clean:
	@echo "[+] Purging intermediate build files..."
	rm -rf $(BUILD_DIR)
