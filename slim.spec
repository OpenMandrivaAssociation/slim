Summary:	Simple login manager
Name:		slim
Version:	1.3.0
Release:	%mkrel 1
Group:		System/X11
License:	GPL
URL:		http://slim.berlios.de
Source0:	http://download.berlios.de/slim/%{name}-%{version}.tar.bz2
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

%build
%make USE_PAM=1

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README THEMES TODO
%dir %{_datadir}/slim
%{_bindir}/slim*
%{_datadir}/slim/themes/
%{_mandir}/man1/*
