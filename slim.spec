Summary:	Simple login manager
Name:		slim
Version:	1.3.6
Release:	11
Group:		System/X11
License:	GPLv2+
URL:		http://slim.berlios.de
Source0:	http://download.berlios.de/slim/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
Source2:	25%{name}.conf
Source3:	slim.logrotate
Source4:	slim.rpmlintrc
Source5:	slim-tmpfiles.conf
Patch1:		%{name}-1.3.3-config.patch
Patch7:		slim-1.3.6-fix-CMakeLists.patch
Patch8:		slim-1.3.5-fix-service-file.patch
Patch9:		slim-1.3.6-systemd-session.patch
BuildRequires:	cmake
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	gettext
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(libpng16) >= 1.6
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libsystemd-login)
Requires:	pam >= 0.80
Requires:	distro-theme
Provides:	dm
Requires(post,postun,preun):	rpm-helper
Obsoletes:	%{mklibname slim 1} < 1.3.6-9

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
%apply_patches

%build
%global optflags %{optflags} -I/usr/include/freetype2

%cmake \
    -DBUILD_SHARED_LIBS=Off \
    -DUSE_PAM=yes \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_LIBDIR:PATH="%{_lib}" \
    -DUSE_CONSOLEKIT=no

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}

mkdir -p %{buildroot}%{_datadir}/X11/dm.d
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/X11/dm.d/25%{name}.conf

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# (tpg) use background distro-theme
rm -f %{buildroot}%{_datadir}/slim/themes/default/background.jpg
ln -s ../../../mdk/backgrounds/default.png %{buildroot}%{_datadir}/slim/themes/default/background.jpg

install -p -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

%files
%doc ChangeLog README THEMES TODO
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_datadir}/X11/dm.d/25%{name}.conf
%dir %{_datadir}/slim
%{_unitdir}/slim.service
%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/tmpfiles.d/slim.conf
%{_bindir}/slim*
%{_datadir}/slim/themes/
%{_mandir}/man1/*
