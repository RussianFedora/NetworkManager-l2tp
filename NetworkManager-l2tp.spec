%define nm_version          1:0.9.2
%define dbus_version        1.1
%define gtk3_version        3.0
%define ppp_version         2.4.5
%define shared_mime_version 0.16-3

Summary:   NetworkManager VPN plugin for l2tp
Name:      NetworkManager-l2tp
Version:   0.9.6
Release:   1%{?dist}
License:   GPLv2+
Group:     System Environment/Base
URL:       https://launchpad.net/~seriy-pr/+archive/network-manager-l2tp
Source:    %{name}-%{version}.tar.gz

BuildRequires: libtool
BuildRequires: gtk3-devel             >= %{gtk3_version}
BuildRequires: dbus-devel             >= %{dbus_version}
BuildRequires: dbus-glib-devel        >= 0.74
BuildRequires: NetworkManager-devel   >= %{nm_version}
BuildRequires: NetworkManager-glib-devel >= %{nm_version}
%if 0%{?fedora} > 16
BuildRequires: libgnome-keyring-devel
%else
BuildRequires: gnome-keyring-devel
%endif
BuildRequires: intltool gettext
BuildRequires: ppp-devel = %{ppp_version}

Requires: dbus             >= %{dbus_version}
Requires: NetworkManager   >= %{nm_version}
Requires: ppp              = %{ppp_version}
Requires: shared-mime-info >= %{shared_mime_version}
Requires: pptp
Requires: gnome-keyring
Requires: xl2tpd
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils

%description
This package contains software for integrating L2TP VPN support with
the NetworkManager and the GNOME desktop.

%prep
%setup -q


%build
./autogen.sh
%configure \
	--disable-static \
	--enable-more-warnings=yes \
	--with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version}

make %{?_smp_mflags}

%install

make install DESTDIR=$RPM_BUILD_ROOT

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a

rm -f %{buildroot}%{_libdir}/pppd/2.*/nm-l2tp-pppd-plugin.la
rm -f %{buildroot}%{_libdir}/pppd/2.*/nm-l2tp-pppd-plugin.a

%find_lang %{name}


%post
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%{_libdir}/NetworkManager/lib*.so*
%{_libexecdir}/nm-l2tp-auth-dialog
%{_sysconfdir}/dbus-1/system.d/nm-l2tp-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-l2tp-service.name
%{_libexecdir}/nm-l2tp-service
%{_libdir}/pppd/2.*/nm-l2tp-pppd-plugin.so
#%{_datadir}/applications/nm-pptp.desktop
#%{_datadir}/icons/hicolor/48x48/apps/gnome-mime-application-x-pptp-settings.png
%dir %{_datadir}/gnome-vpn-properties/l2tp
%{_datadir}/gnome-vpn-properties/l2tp/nm-l2tp-dialog.ui

%changelog
* Mon Nov 19 2012  <drizt@land.ru> - 0.9.6-1.R
- initial version based on NetworkManager-pptp 1:0.9.3.997-3

