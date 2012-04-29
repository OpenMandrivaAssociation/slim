Summary:	Simple login manager
Name:		slim
Version:	1.3.3
Release:	%mkrel 2
Group:		System/X11
License:	GPLv2+
URL:		http://slim.berlios.de
Source0:	http://download.berlios.de/slim/%{name}-%{version}.tar.bz2
Source1:	%{name}.pam
Source2:	25%{name}.conf
Source3:	slim.logrotate
Patch1:		%{name}-1.3.3-config.patch
Patch3:		15287-fix-pam-authentication-with-pam_unix2.patch
Patch4:		405579-fix-numlock.patch
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
Requires:	pam >= 0.80
Requires:	mandriva-theme
Provides:	dm
BuildRoot:	%{_tmppath}/%{name}-%{version}--buildroot

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
%patch3 -p1 -b .ck
%patch4 -p0 -b .numlock

%build
%cmake \
    -DUSE_PAM=yes \
    -DUSE_CONSOLEKIT=yes

%make

%install
rm -rf %{buildroot}

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

popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README THEMES TODO
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_datadir}/X11/dm.d/25%{name}.conf
%dir %{_datadir}/slim
%{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/slim*
%{_datadir}/slim/themes/
%{_mandir}/man1/*
