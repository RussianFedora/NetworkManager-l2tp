%define nm_version          1:0.8.1
%define dbus_version        1.1
%define gtk2_version        2.10.0
%define ppp_version         2.4.5
%define shared_mime_version 0.16-3

%define snapshot %{nil}
%define realversion 0.1

Summary:   NetworkManager VPN plugin for l2tp
Name:      NetworkManager-l2tp
Version:   0.1
Release:   1%{snapshot}%{?dist}
License:   GPLv2+
Group:     System Environment/Base
URL:       https://github.com/atorkhov/NetworkManager-l2tp
Source:    https://github.com/downloads/atorkhov/NetworkManager-l2tp/%{name}-%{realversion}%{snapshot}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-root


BuildRequires: gtk2-devel             >= %{gtk2_version}
BuildRequires: dbus-devel             >= %{dbus_version}
BuildRequires: dbus-glib-devel        >= 0.74
BuildRequires: NetworkManager-devel   >= %{nm_version}
BuildRequires: NetworkManager-glib-devel >= %{nm_version}
BuildRequires: GConf2-devel
BuildRequires: gnome-keyring-devel
BuildRequires: libglade2-devel
BuildRequires: intltool gettext
BuildRequires: ppp-devel = %{ppp_version}

Requires: gtk2             >= %{gtk2_version}
Requires: dbus             >= %{dbus_version}
Requires: NetworkManager   >= %{nm_version}
Requires: ppp              = %{ppp_version}
Requires: shared-mime-info >= %{shared_mime_version}
Requires: xl2tpd
Requires: GConf2
Requires: gnome-keyring
Requires(post):   /sbin/ldconfig desktop-file-utils
Requires(postun): /sbin/ldconfig desktop-file-utils


%description
This package contains software for integrating L2TP VPN support with
the NetworkManager and the GNOME desktop.

%prep
%setup -q -n NetworkManager-l2tp-%{realversion}


%build
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


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files -f %{name}.lang
%defattr(-, root, root)

%doc AUTHORS
%{_libdir}/NetworkManager/lib*.so*
%{_libexecdir}/nm-l2tp-auth-dialog
%{_sysconfdir}/dbus-1/system.d/nm-l2tp-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-l2tp-service.name
%{_libexecdir}/nm-l2tp-service
%{_libdir}/pppd/2.*/nm-l2tp-pppd-plugin.so
%{_datadir}/gnome-vpn-properties/l2tp/nm-l2tp-dialog.glade
#%{_datadir}/applications/nm-l2tp.desktop
#%{_datadir}/icons/hicolor/48x48/apps/gnome-mime-application-x-l2tp-settings.png
%dir %{_datadir}/gnome-vpn-properties/l2tp

%changelog
* Sun Jan 16 2011 Alexey Torkhov <atorkhov@gmail.com> - 0.1-1%{nil}
- Initial package based on NetworkManager-pptp

