# Copyright 2026 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=8

if [[ ${PV} == 9999 ]]; then
	inherit git-r3
	EGIT_REPO_URI="https://github.com"
	KEYWORDS=""
else
	SRC_URI="https://github.com{PN}/archive/refs/tags/v${PV}.tar.gz -> ${P}.tar.gz"
	KEYWORDS="~*"
fi

DESCRIPTION="Algic language IBus keyboard layout maps and terminal macros"
HOMEPAGE="https://github.com"

LICENSE="GPL-2"
SLOT="0"
IUSE="readline"

BDEPEND="
	app-i18n/ibus
	app-i18n/ibus-table
"
RDEPEND="
	app-i18n/ibus
	app-i18n/ibus-table
	readline? ( sys-libs/readline )
"

if [[ ${PV} != 9999 ]]; then
	S="${WORKDIR}/${PN}-${PV}"
fi

src_unpack() {
	if [[ ${PV} == 9999 ]]; then
		git-r3_src_unpack
	else
		default
	fi
}

src_compile() {
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

	# Deploy standard Readme.md documentation natively
	einstalldocs

	einfo "Deploying repository deployment engine for manual home space fallback..."
	# Keeps install.sh executable (755) and targets a safe system directory
	exeinto /usr/share/algic-ibus
	doexe install.sh
	
	# Also copy the required input sources alongside it so install.sh can find them if invoked manually
	insinto /usr/share/algic-ibus
	doins _inputrc.in algic_keys.txt algic_keys.db
}

pkg_postinst() {
	elog "========================================================================"
	elog " ⌨️  Algic Keyboard Layout Framework (${PV}) Initialized!"
	elog "========================================================================"
	elog "🛠️  USER ACCESSIBILITY & FALLBACK PATHS:"
	elog "If IBus configurations break, or if other/existing users need to deploy"
	elog "the layout matrices and terminal macros directly to their /home directories,"
	elog "they can run the pre-bundled installer directly from the system share:"
	elog "   $ cd /usr/share/algic-ibus && ./install.sh"
	elog "========================================================================"
}
