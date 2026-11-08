Name:           algic-ibus
Version:        1.0.0
Release:        1%{?dist}
Summary:        Split layout matrix for Algic language keyboard mapping configurations
License:        MIT
URL:            https://github.com
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  python3, ibus-table
Requires:       ibus-table

%description
Provides split sub-module translation keymaps for Algic linguistic variants.

%prep
%autosetup

%build
# Trigger Makefile compilation phase
%make_build VERSION=%{version}

%install
# Stage output using RPM's buildroot macro mapping to DESTDIR
%make_install PREFIX=%{_prefix} TABLEDIR=%{_datadir}/ibus-table/tables

%files
%{_datadir}/ibus-table/tables/algic_*.db
