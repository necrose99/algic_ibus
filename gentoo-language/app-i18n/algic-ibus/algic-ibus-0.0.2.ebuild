EAPI=8

PYTHON_COMPAT=( python3_{10..13} )
inherit python-any-r1

DESCRIPTION="Hierarchical split layout matrix for Algic language keyboard configurations"
HOMEPAGE="https://github.com"
SRC_URI="https://github.com/archive/v${PV}.tar.gz -> ${P}.tar.gz"

LICENSE="MIT"
SLOT="0"
KEYWORDS="~amd64 ~x86 ~arm64" # Readily tracks lean ARM deployment boards

BDEPEND="${PYTHON_DEPS}
	app-i18n/ibus-table"
RDEPEND="app-i18n/ibus-table"

src_compile() {
	# Run the standard make rule directly inside the Portage sandbox image
	emake VERSION="${PV}" all
}

src_install() {
	# Safely push compiled DB structures out into the system layer image boundary
	emake DESTDIR="${D}" PREFIX="/usr" install
	dodoc Readme.md
}
