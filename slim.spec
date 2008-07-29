Summary:	Simple login manager
Name:		slim
Version:	1.3.0
Release:	%mkrel 8
Group:		System/X11
License:	GPLv2+
URL:		http://slim.berlios.de
Source0:	http://download.berlios.de/slim/%{name}-%{version}.tar.bz2
Source1:	%{name}.pam
Source2:	25%{name}.conf
Patch0:		%{name}-1.3.0-makefile.patch
Patch1:		%{name}-1.3.0-config.patch
Patch2:		%{name}-1.3.0-libgen.patch
BuildRequires:	libxmu-devel
BuildRequires:	libxft-devel
BuildRequires:	libxrender-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	freetype-devel
BuildRequires:	fontconfig-devel
BuildRequires:	pkgconfig
BuildRequires:	gettext
BuildRequires:	pam-devel
Requires:	xterm
Requires:	pam >= 0.80
Requires:	mandriva-theme
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
%patch0 -p1 -b .makefile
%patch1 -p1 -b .config
%patch2 -p1 -b .libgen

%build
%make USE_PAM=1

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/X11/dm.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/X11/dm.d/25%{name}.conf

# (tpg) use background from mandriva-theme
rm -f %{buildroot}%{_datadir}/slim/themes/default/background.jpg
ln -s ../../../mdk/backgrounds/default.jpg %{buildroot}%{_datadir}/slim/themes/default/background.jpg

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog README THEMES TODO
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/X11/slim/%{name}.conf
%config(noreplace) %{_sysconfdir}/X11/dm.d/25%{name}.conf
%dir %{_datadir}/slim
%{_bindir}/slim*
%{_datadir}/slim/themes/
%{_mandir}/man1/*
