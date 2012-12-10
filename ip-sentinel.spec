%define name ip-sentinel
%define version 0.12
%define release %mkrel 6

Summary: A network ip guardian
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: GPL
Group: Networking/Other
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url: http://enrico-scholz.de/ip-sentinel/
Requires(post,preun):	rpm-helper

%description
This program tries to prevent unauthorized usage of IPs within
the local ethernet broadcastdomain by giving an answer to
ARP-requests. After receiving such a faked reply, the requesting
party stores the told MAC in its ARP-table and will send future
packets to this MAC. Because this MAC is invalid, the host with
the invalid IP can not be reached.

Features
- non-root execution in a chroot jail
- freely customizable IPs (netmasks, negations, ranges)

%prep
%setup -q

%build
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# Config
mkdir -p %buildroot{%_sysconfdir/sysconfig,%_initrddir,%_sysconfdir/logrotate.d}

perl -pi -e 's/^# chkconfig:.*/# chkconfig: 345 95 05/' contrib/ip-sentinel.init
cp contrib/ip-sentinel.init %buildroot%_initrddir/%name
cat > %buildroot%_sysconfdir/sysconfig/%name <<EOF
IPS_USER=ip-sentinel
IPS_GROUP=ip-sentinel
# IPS_CHROOT=%_localstatedir/lib/%name
# IPS_IPFILE=ips.cfg
# IPS_LOGFILE=/var/log/ip-sentinel.out
# IPS_ERRFILE=/var/log/ip-sentinel.err
# IPS_OPTIONS=
# IPS_DEVICE=eth0

## Assign to yes if running a dietlibc-compiled version of ip-sentinel
## on a system using remote NSS for passwd-lookups (e.g. LDAP, NIS).
##
## When using a group which is not the effective group of the user,
## you will have to assign the numeric gid of this group to GROUP.
# IPS_NEEDS_NUMERIC_UID=
EOF

cat > %buildroot%_sysconfdir/logrotate.d/%name << EOF
/var/log/%name.err /var/log/%name.out {
    missingok
    notifempty
    postrotate
        /bin/kill -HUP `/bin/cat /var/run/%name.pid`
    endscript
}
EOF

# Data
mkdir -p %buildroot{%_localstatedir/lib/%name,%_var/log}
touch %buildroot%_var/log/%name.out
touch %buildroot%_var/log/%name.err


%pre
  %_pre_useradd %name %_localstatedir/lib/%name /bin/true

%post
  touch %_var/log/%name.out
  touch %_var/log/%name.err
  %_post_service %{name}

%postun
  %_postun_userdel %name

%preun
  %_preun_service %{name}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%_sbindir/%name
%_mandir/man8/%{name}*
%dir %_localstatedir/lib/%name
%config(noreplace) %_sysconfdir/sysconfig/%name
%config(noreplace) %_initrddir/%name
%config(noreplace) %_sysconfdir/logrotate.d/%name
%ghost %_var/log/%name.out
%ghost %_var/log/%name.err




%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.12-6mdv2011.0
+ Revision: 619676
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0.12-5mdv2010.0
+ Revision: 429520
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.12-4mdv2009.0
+ Revision: 247257
- rebuild
- fix no-buildroot-tag

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Tue Dec 18 2007 Thierry Vignaud <tv@mandriva.org> 0.12-2mdv2008.1
+ Revision: 131783
- fix prereq on rpm-helper
- kill re-definition of %%buildroot on Pixel's request
- kill changelog left by repsys


* Sat Jul 15 2006 Olivier Thauvin <nanardon@mandriva.org>
+2006-07-15 18:06:19 (41315)
- rebuild
- fix url

* Sat Jul 15 2006 Olivier Thauvin <nanardon@mandriva.org>
+2006-07-15 18:04:23 (41314)
Import ip-sentinel

* Mon Apr 25 2005 Olivier Thauvin <nanardon@mandriva.org> 0.12-1mdk
- 0.12

* Sun Jan 30 2005 Sylvie Terjan <erinmargault@mandrake.org> 0.11-1mdk
- Change version to 0.11

* Tue Dec 16 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.9-1mdk
- Make a specfile

