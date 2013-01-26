Summary:	Simple login manager
Name:		slim
Version:	1.3.5
Release:	1
Group:		System/X11
License:	GPLv2+
URL:		http://slim.berlios.de
Source0:	http://download.berlios.de/slim/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
Source2:	25%{name}.conf
Source3:	slim.logrotate
Source5:	slim-tmpfiles.conf
Patch1:		%{name}-1.3.3-config.patch
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
%if %mdvver < 201300
BuildRequires:	consolekit-devel
%endif
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
%patch7 -p1 -b .xmu

%build
# fix installation path of slim.service
sed -i 's|usr/lib/systemd/system|/&|' CMakeLists.txt

%cmake \
    -DUSE_PAM=yes \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_BUILD_TYPE=Release \
%if %mdvver >= 201300
    -DUSE_CONSOLEKIT=no
%else
    -DUSE_CONSOLEKIT=yes
%endif

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

install -p -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

popd

%post
systemd-tmpfiles --create slim.conf

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


%changelog
* Fri Aug 31 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.4-4
+ Revision: 816156
- set default restart timeout to 5 seconds for slim service
- fix requires for slim.service

* Sun Aug 26 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.4-2
+ Revision: 815759
- drop patch 6, rely on %%sessiondir in config file
- provide a systemd service file

* Tue Aug 21 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.4-1
+ Revision: 815569
- Patch6: get next session name
- Patch7: link against Xmu
- spec file clean

  + Jon Dill <dillj@mandriva.org>
    - fixed linking in build
    - correct filename
    - update to 1.3.4
    - drop pam and numlock patch
    - include libpng patch(gentoo)

* Sun Apr 29 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.3-2
+ Revision: 794458
- add pam_gnome_keyrin to pam file

* Mon Mar 26 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.3-1
+ Revision: 787062
- update to new version 1.3.3
- drop patches 0 and 2
- rediff patch 1
- Patch3: fix consolekit support (from gentoo)
- Patch4: fix numlock support (from gentoo)
- add logrotate config
- enable PAM nad ConsoleKit support
- update buildrequires

* Sat Aug 07 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.2-1mdv2011.0
+ Revision: 567439
- update to new version 1.3.2
- rediff patches 0 and 1
- drop patch 3

* Sat Aug 22 2009 Funda Wang <fwang@mandriva.org> 1.3.1-2mdv2010.0
+ Revision: 419589
- fix build with gcc 4.4

* Thu Feb 19 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.1-2mdv2009.1
+ Revision: 343001
- Patch1: rediff, add xserver arguments, like start on vt7 etc.
- add provides on dm

* Sat Nov 15 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.1-1mdv2009.1
+ Revision: 303601
- Patch0: use xvt instead of xterm
- update to new version 1.3.1
- rediff patches 0 and 1
- drop patch 3 and 4 as they were merged by upstream
- remove requires on xterm

* Fri Sep 05 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.0-9mdv2009.0
+ Revision: 281215
- Patch4: add autologin feature
- Patch3: fix compiling with gcc43
- compile with %%{optflags}
- adjust X11 dm path

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild

* Tue Mar 18 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.0-6mdv2008.1
+ Revision: 188496
- mandriva-theme uses jpeg compression for wallpapers
- do not package COPYING file

* Sat Jan 26 2008 Funda Wang <fwang@mandriva.org> 1.3.0-5mdv2008.1
+ Revision: 158298
- fix conf file

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Nov 12 2007 Funda Wang <fwang@mandriva.org> 1.3.0-4mdv2008.1
+ Revision: 108176
- rebuild for new lzma

* Fri Nov 02 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.0-3mdv2008.1
+ Revision: 105219
- rework patch 1 one more time
- add missing header (patch 2)

* Thu Nov 01 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.0-2mdv2008.1
+ Revision: 104462
- new license policy
- rediff both patches
- add initial support for the drakedm and dm script, rest hast to be done in initscripts file (/etc/X11/prefdm)

* Tue Oct 02 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.0-1mdv2008.1
+ Revision: 94462
- use background from mandriva-theme
- mark slim.conf as a configuration file
- provide patch 1 (configuration)
- provide patch 0 (makefile patch)
- add pam rules
- import slim


