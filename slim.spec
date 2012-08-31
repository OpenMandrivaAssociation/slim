Summary:	Simple login manager
Name:		slim
Version:	1.3.4
Release:	4
Group:		System/X11
License:	GPLv2+
URL:		http://slim.berlios.de
Source0:	http://download.berlios.de/slim/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
Source2:	25%{name}.conf
Source3:	slim.logrotate
Source4:	slim.service
Patch1:		%{name}-1.3.3-config.patch
Patch5:		slim-1.3.4-libpng.patch
Patch7:		slim-1.3.4-link-against-Xmu.patch
BuildRequires:	cmake
BuildRequires:	libxmu-devel
BuildRequires:	libxft-devel
BuildRequires:	libxrender-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig
BuildRequires:	gettext
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(libpng15) >= 1.5
BuildRequires:	pkgconfig(zlib)
BuildRequires:	consolekit-devel
BuildRequires:	systemd
Requires:	pam >= 0.80
Requires:	mandriva-theme
Provides:	dm

%description
SLiM (Simple Login Manager) is a Desktop-independent graphical 
login manager for X11.

It aims to be light and simple, although completely configurable 
through themes and an option file; is suitable for machines on which 
remote login functionalities are not needed.

Features included:

* PNG and XFT support for alpha transparency and antialiased fonts
* External themes support
* Configurable runtime options: X server, login / shutdown / reboot commands
* Single (GDM-like) or double (XDM-like) input control
* Can load predefined user at startup
* Configurable welcome / shutdown messages
* Random theme selection

%prep
%setup -q

%patch1 -p1 -b .config
%patch5 -p1 -b .libpng
%patch7 -p1 -b .xmu

%build

%cmake \
    -DUSE_PAM=yes \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_CONSOLEKIT=yes

%install
pushd build
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}

mkdir -p %{buildroot}%{_datadir}/X11/dm.d
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/X11/dm.d/25%{name}.conf

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# (tpg) use background from mandriva-theme
rm -f %{buildroot}%{_datadir}/slim/themes/default/background.jpg
ln -s ../../../mdk/backgrounds/default.jpg %{buildroot}%{_datadir}/slim/themes/default/background.jpg

mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/slim.service

popd

%files
%doc ChangeLog README THEMES TODO
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_datadir}/X11/dm.d/25%{name}.conf
%dir %{_datadir}/slim
%{_unitdir}/slim.service
%{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/slim*
%{_datadir}/slim/themes/
%{_mandir}/man1/*
