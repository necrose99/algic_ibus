
# Copyright 2026 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=8

# --- Dynamic 9999 Git-R3 vs Static Tarball Logic ---
if [[ ${PV} == 9999 ]]; then
	inherit git-r3
	EGIT_REPO_URI="https://github.com/necrose99/algic_ibus/"
	# Force no keywords for the live 9999 build to keep it masked by default
	KEYWORDS=""
else
	SRC_URI="https://github.com/necrose99/{PN}/archive/refs/tags/v${PV}.tar.gz -> ${P}.tar.gz"
	KEYWORDS="~amd64 ~x86 ~arm"
fi

DESCRIPTION="Algic language IBus keyboard layout maps and terminal macros"
HOMEPAGE="https://github.com"

LICENSE="GPL-2"
SLOT="0"
IUSE="readline"

# --- Compilation & Runtime Dependencies ---
BDEPEND="
	app-i18n/ibus
	app-i18n/ibus-table
"

RDEPEND="
	app-i18n/ibus
	app-i18n/ibus-table
	readline? ( sys-libs/readline )
"

# Set the source directory depending on whether it came from Git or a Tarball
if [[ ${PV} != 9999 ]]; then
	S="${WORKDIR}/${PN}-${PV}"
fi

src_unpack() {
	if [[ ${PV} == 9999 ]]; then
		# Pull live head directly from the GitHub master/main branch
		git-r3_src_unpack
	else
		# Default standard archive decompression fallback loop
		default
	fi
}

src_compile() {
	einfo "Compiling plain-text layout matrices into active database structure..."
	# Compile text database file explicitly within the sandboxed build environment
	ibus-table-createdb -n algic_keys.db -s algic_keys.txt || die "Database compilation failed"
}

src_install() {
	einfo "Installing IBus table engine data artifacts..."
	insinto /usr/share/ibus-table/tables
	doins algic_keys.db

	if use readline; then
		einfo "Installing global terminal macro configuration profile..."
		insinto /etc/skel
		newins _inputrc.in .inputrc
	fi

	# Deploy global multitenant documentation file structures natively 
	einstalldocs
}

pkg_postinst() {
	elog "========================================================================"
	elog " ⌨️  Algic Keyboard Layout Framework (${PV}) Initialized!"
	elog "========================================================================"
	if [[ ${PV} == 9999 ]]; then
		elog "👉 This is a live development build tracked via git-r3."
		elog "   To update your mappings to latest commit on head, simply run:"
		elog "   # emerge --all-members @live-rebuild"
	fi
	elog "------------------------------------------------------------------------"
	elog "1. Restart your desktop session's active ibus-daemon instance to sync additions:"
	elog "   $ ibus exit && ibus-daemon -drx"
	elog "2. Open your Desktop Environment Keyboard settings panel under 'Input Methods'"
	elog "   and click Add -> select your language -> choose 'Algic_Input_Matrix'."
	elog "========================================================================"
}
