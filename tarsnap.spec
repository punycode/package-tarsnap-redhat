Summary:            Online backups for the truly paranoid
Name:               tarsnap
Version:            1.0.36.1
Release:            1%{?dist}
License:            AS-IS
Group:              Applications/Archiving
Source:             https://www.tarsnap.com/download/%{name}-autoconf-%{version}.tgz
URL:                https://www.tarsnap.com
BuildRequires:      glibc-devel
BuildRequires:      openssl-devel
BuildRequires:      zlib-devel
BuildRequires:      e2fsprogs-devel

%description
Tarsnap is a secure online backup service for BSD, Linux, OS X, Minix, OpenIndiana, Cygwin, and probably many other
UNIX-like operating systems. The Tarsnap client code provides a flexible and powerful command-line interface which can
be used directly or via shell scripts.

At the present time, Tarsnap does not support Windows (except via Cygwin) and does not have a graphical user interface.

%prep
%autosetup -n %{name}-autoconf-%{version}

%build
%configure --with-bash-completion-dir=%{_sysconfdir}/bash_completion.d
make %{?_smp_mflags}

%install
%make_install
%__mv $RPM_BUILD_ROOT/%{_sysconfdir}/tarsnap.conf.sample $RPM_BUILD_ROOT/%{_sysconfdir}/tarsnap.conf
%__sed -i'' \
  -e 's=^cachedir .*=cachedir %{_localstatedir}/cache/%{name}=g' \
  -e 's=^keyfile .*=keyfile %{_sysconfdir}/tarsnap.key=g' $RPM_BUILD_ROOT/%{_sysconfdir}/tarsnap.conf
%__mkdir_p $RPM_BUILD_ROOT/%{_localstatedir}/cache/%{name}

%files
%defattr(-,root,root)
%doc COPYING
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%config %{_sysconfdir}/bash_completion.d/*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/tarsnap.conf
%attr(0700,root,root) %dir %{_localstatedir}/cache/%{name}
