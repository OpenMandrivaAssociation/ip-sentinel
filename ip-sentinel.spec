%define name ip-sentinel
%define version 0.12
%define release %mkrel 2

Summary: A network ip guardian
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: GPL
Group: Networking/Other
Url: http://enrico-scholz.de/ip-sentinel/
PreReq: rpm-helper

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
# IPS_CHROOT=%_localstatedir/%name
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
mkdir -p %buildroot{%_localstatedir/%name,%_var/log}
touch %buildroot%_var/log/%name.out
touch %buildroot%_var/log/%name.err


%pre
  %_pre_useradd %name %_localstatedir/%name /bin/true

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
%dir %_localstatedir/%name
%config(noreplace) %_sysconfdir/sysconfig/%name
%config(noreplace) %_initrddir/%name
%config(noreplace) %_sysconfdir/logrotate.d/%name
%ghost %_var/log/%name.out
%ghost %_var/log/%name.err


