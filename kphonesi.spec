%define fname	kphoneSI

Summary:	KPhoneSI - SIP user agent
Name:		kphonesi
Version:	1.2
Release:	%{mkrel 1}
# All kphone files say LGPLv2+ in their headers, but the app also uses
# trayicon.cpp and trayicon.h that are GPLv2+, and the COPYING file is
# the GPL, not the LGPL - AdamW 2008/12
License:	GPLv2+
Group:		Communications
URL:		http://sourceforge.net/projects/kphone/
BuildRequires:	qt3-devel
BuildRequires:	openssl-devel
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	libxt-devel
BuildRequires:	libxscrnsaver-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	png-devel
BuildRequires:	speex-devel
Provides:	kphone = %{version}-%{release}
Obsoletes:	kphone < 4.2-10
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Source0:	http://downloads.sourceforge.net/kphone/%{fname}_%{version}.tar.gz
Patch0:		kphonesi-1.2-x86_64.patch
Patch1:		kphonesi-1.2-destdir.patch
Patch2:		kphone-4.2.0-fix-compile-po.patch
Patch3:		kphonesi-1.2-packed.patch
Patch4:		kphone-pt_BR-trans.patch
Patch5:		kphonesi-1.2-CVE-2006-2442.patch
Patch6:		kphonesi-1.2-gcc43.patch
Patch7:		kphonesi-1.2-mandir.patch

# Deal with --tag
%define __libtoolize /bin/true

%description
KPhoneSI is a SIP (Session Initiation Protocol) user agent for Linux,
with which you can initiate VoIP (Voice over IP) connections over the
Internet. It is a fork of the original, and now unmaintained, KPhone
project.

%prep 
%setup -q -n %{fname} 
%patch0 -p1 -b .lib64
%patch1 -p1
%patch2 -p1 -b .fix_compile_po
%patch3 -p1 -b .packed
%patch4 -p1 -b .pt_BR
%patch5 -p1 -b .cve-2006-2442
%patch6 -p1 -b .gcc43
%patch7 -p1 -b .mandir

%build
autoconf
QTDIR=%{qt3dir} %configure2_5x \
        --enable-shared \
        --with-gnu-ld \
        --with-pic \
        --enable-mt \
	--enable-lipo \
        --disable-rpath
%make

%install
rm -rf %{buildroot}

%makeinstall_std

# Don't want to patch the Makefile
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m0644 icons/large-phone.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m0644 icons/lo-phone.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m0644 icons/mini-phone.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Kphone
Comment=Kphone SIP user agent
Exec=soundwrapper %{_bindir}/kpsi
Icon=%{name}
Terminal=false
Type=Application
Categories=Qt;Network;Telephony;
EOF

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%files
%doc CHANGES HOWTO-Dialer HOWTO-kphonering HOWTO-Shortcuts README
%defattr(-,root,root,-)
%{_bindir}/kphonering
%{_bindir}/kphoneringsh
%{_bindir}/kpsi
%{_bindir}/kpsidial
%{_mandir}/man1/*.1*
%{_datadir}/KPhoneSI
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

