%global _hardened_build 1
%global username guacd

Name:           guacamole-server
Version:        0.9.2
Release:        2%{?dist}
Summary:        Server-side native components that form the Guacamole proxy

License:        MPLv1.1 or GPLv2+
URL:            http://guac-dev.org/
Source0:        http://downloads.sourceforge.net/guacamole/%{name}-%{version}.tar.gz
Source1:        %{name}.sysconfig
Source2:        %{name}.service
Source3:        %{name}.init

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  doxygen
BuildRequires:  libtool
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(freerdp) >= 1.0.2
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libssh2)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(libtelnet)
BuildRequires:  pkgconfig(ossp-uuid)
%if 0%{?rhel} == 6
BuildRequires:  libvncserver-devel
%else
BuildRequires:  pkgconfig(libvncserver)
%endif
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(vorbis)

%description
Guacamole is an HTML5 remote desktop gateway.

Guacamole provides access to desktop environments using remote desktop protocols
like VNC and RDP. A centralized server acts as a tunnel and proxy, allowing
access to multiple desktops through a web browser.

No browser plugins are needed, and no client software needs to be installed. The
client requires nothing more than a web browser supporting HTML5 and AJAX.

The main web application is provided by the "guacamole-client" package.

%package -n libguac
Summary:        The common library used by all C components of Guacamole

%description -n libguac
libguac is the core library for guacd (the Guacamole proxy) and any protocol
support plugins for guacd. libguac provides efficient buffered I/O of text and
base64 data, as well as somewhat abstracted functions for sending Guacamole
instructions.

%package -n libguac-devel
Summary:        Development files for %{name}
Requires:       libguac%{?_isa} = %{version}-%{release}

%description -n libguac-devel
The libguac-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n libguac-client-rdp
Summary:        RDP support for guacd
Requires:       libguac%{?_isa} = %{version}-%{release}

%description -n libguac-client-rdp
libguac-client-rdp is a protocol support plugin for the Guacamole proxy (guacd)
which provides support for RDP, the proprietary remote desktop protocol used by
Windows Remote Deskop / Terminal Services, via the libfreerdp library.

%package -n libguac-client-ssh
Requires:       libguac%{?_isa} = %{version}-%{release}
Summary:        SSH support for guacd

%description -n libguac-client-ssh
libguac-client-ssh is a protocol support plugin for the Guacamole proxy (guacd)
which provides support for SSH, the secure shell.

%package -n libguac-client-vnc
Requires:       libguac%{?_isa} = %{version}-%{release}
Summary:        VNC support for guacd

%description -n libguac-client-vnc
libguac-client-vnc is a protocol support plugin for the Guacamole proxy (guacd)
which provides support for VNC via the libvncclient library (part of
libvncserver).

%package -n libguac-client-telnet
Requires:       libguac%{?_isa} = %{version}-%{release}
Summary:        Telnet support for guacd

%description -n libguac-client-telnet
libguac-client-telnet is a protocol support plugin for the Guacamole proxy
(guacd) which provides support for Telnet via the libtelnet library.

%package -n guacd
Summary:        Proxy daemon for Guacamole
Requires(pre):  shadow-utils
Requires:       libguac%{?_isa} = %{version}-%{release}

%if 0%{?fedora} || 0%{?rhel} >= 7
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%endif

%if 0%{?rhel} == 6
Requires(post):    /sbin/chkconfig
Requires(preun):   /sbin/chkconfig
Requires(preun):   /sbin/service
Requires(postun):  /sbin/service
%endif

%description -n guacd
guacd is the Guacamole proxy daemon used by the Guacamole web application and
framework to translate between arbitrary protocols and the Guacamole protocol.

%prep
%setup -q

%build
autoreconf -vif
%configure --disable-static

make %{?_smp_mflags}
cd doc/
doxygen Doxyfile

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete
cp -fr doc/doxygen-output/html .
%if 0%{?rhel} == 6
rm -f html/installdox
%endif

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/guacd
mkdir -p %{buildroot}%{_sharedstatedir}/guacd

%if 0%{?fedora} || 0%{?rhel} >= 7

# Systemd unit files
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_unitdir}/guacd.service

%else

# Initscripts
mkdir -p %{buildroot}%{_initrddir}
install -p -m 755 -D %{SOURCE3} %{buildroot}%{_initrddir}/guacd

%endif

%pre -n guacd
getent group %username >/dev/null || groupadd -r %username &>/dev/null || :
getent passwd %username >/dev/null || useradd -r -s /sbin/nologin \
    -d %{_sharedstatedir}/guacd -M -c 'Guacamole proxy daemon' -g %username %username &>/dev/null || :
exit 0

%if 0%{?fedora} || 0%{?rhel} >= 7

%post -n guacd
%systemd_post guacd.service

%preun -n guacd
%systemd_preun guacd.service

%postun -n guacd
%systemd_postun_with_restart guacd.service

%endif

%if 0%{?rhel} == 6

%post -n guacd
/sbin/chkconfig --add guacd

%preun -n guacd
if [ "$1" = 0 ]; then
        /sbin/service guacd stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del guacd
fi

%postun -n guacd
if [ "$1" -ge "1" ]; then
        /sbin/service guacd condrestart >/dev/null 2>&1 || :
fi

%endif

%post -n libguac -p /sbin/ldconfig

%postun -n libguac -p /sbin/ldconfig

%post -n libguac-client-rdp -p /sbin/ldconfig

%postun -n libguac-client-rdp -p /sbin/ldconfig

%post -n libguac-client-ssh -p /sbin/ldconfig

%postun -n libguac-client-ssh -p /sbin/ldconfig

%post -n libguac-client-vnc -p /sbin/ldconfig

%postun -n libguac-client-vnc -p /sbin/ldconfig

%post -n libguac-client-telnet -p /sbin/ldconfig

%postun -n libguac-client-telnet -p /sbin/ldconfig

%files -n libguac
%doc AUTHORS LICENSE README
%{_libdir}/libguac.so.*

%files -n libguac-devel
%doc html
%{_includedir}/*
%{_libdir}/libguac.so

# The libguac source code dlopen's these plugins, and they are named without
# the version in the shared object; i.e. "libguac-client-$(PROTOCOL).so".

%files -n libguac-client-rdp
%{_libdir}/libguac-client-rdp.so
%{_libdir}/libguac-client-rdp.so.*
%{_libdir}/freerdp/*.so

%files -n libguac-client-ssh
%{_libdir}/libguac-client-ssh.so
%{_libdir}/libguac-client-ssh.so.*

%files -n libguac-client-vnc
%{_libdir}/libguac-client-vnc.so
%{_libdir}/libguac-client-vnc.so.*

%files -n libguac-client-telnet
%{_libdir}/libguac-client-telnet.so
%{_libdir}/libguac-client-telnet.so.*

%files -n guacd
%config(noreplace) %{_sysconfdir}/sysconfig/guacd
%{_mandir}/man8/guacd.8.*
%{_sbindir}/guacd
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/guacd.service
%else
%{_initrddir}/guacd
%endif
%attr(750,%{username},%{username}) %{_sharedstatedir}/guacd

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Simone Caronni <negativo17@gmail.com> - 0.9.2-1
- Update to 0.9.2.
- Add OOSP UUID library build requirement.

* Mon Jul 21 2014 Simone Caronni <negativo17@gmail.com> - 0.9.1-6
- Update environment in service file.

* Mon Jul 21 2014 Simone Caronni <negativo17@gmail.com> - 0.9.1-5
- Add patch for FreeRDP 1.2.0 beta 1 support.
- Use automatic dependency logic for FreeRDP libraries.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Simone Caronni <negativo17@gmail.com> - 0.9.1-3
- There is now VNC support (libvncserver) in all EPEL 7 arches.

* Mon May 26 2014 Simone Caronni <negativo17@gmail.com> - 0.9.1-2
- There is no VNC support (libvncserver) in EPEL 7 ppc/ppc64.

* Mon May 26 2014 Simone Caronni <negativo17@gmail.com> - 0.9.1-1
- Update to 0.9.1.
- Removed upstreamed patch.
- Enable new telnet plugin.

* Fri Apr 18 2014 Simone Caronni <negativo17@gmail.com> - 0.9.0-1
- Update to 0.9.0.
- Removed upstreamed patch.
- Backport fixes from 0.9.1 to fix build.

* Mon Nov 18 2013 Simone Caronni <negativo17@gmail.com> - 0.8.3-5
- Update patch for new autoconf.

* Mon Nov 18 2013 Simone Caronni <negativo17@gmail.com> - 0.8.3-4
- Require FreeRDP version >= 1.0.2 to avoid RDP refresh problems.

* Thu Sep 05 2013 Simone Caronni <negativo17@gmail.com> - 0.8.3-3
- Add autoconf patch for RHEL autconf compatibility.

* Mon Sep 02 2013 Simone Caronni <negativo17@gmail.com> - 0.8.3-2
- Add specific EPEL 6 workaround for really old autoconf version.

* Wed Aug 28 2013 Simone Caronni <negativo17@gmail.com> - 0.8.3-1
- Update to 0.8.3.
- Drop upstreamed patch.

* Tue Jul 30 2013 Simone Caronni <negativo17@gmail.com> - 0.8.2-2
- SysV init script was overwritten by mistake in SCM.

* Tue Jul 16 2013 Simone Caronni <negativo17@gmail.com> - 0.8.2-1
- First build.
