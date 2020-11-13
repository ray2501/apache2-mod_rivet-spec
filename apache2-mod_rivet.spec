#
# spec file for package apache2-mod_rivet
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


########################################
# apache macros
########################################
# apache2 auto include config folder
%define ap2sysconfautodir %{apache_sysconfdir}/conf.d
# full path to rivet apache2 config file
%define ap2rivetconffile %{ap2sysconfautodir}/mod_rivet.conf
########################################
# tcl macros
########################################
# On SUSE, this macro is available by BuildRequires tcl-devel
# on other platforms, create it
%{!?tcl_archdir: %define tcl_archdir %(echo 'puts [file normalize [lindex $tcl_pkgPath 0]]'|tclsh)}
%define sourcedir libapache2-mod-rivet-%{version}
%define rivetdir %{tcl_archdir}/%{name}%{version}
Name:           apache2-mod_rivet
Version:        3.2.0
Release:        0
Summary:        Apache module containing TCL servlet engine
License:        Apache-2.0
Group:          Productivity/Networking/Web/Servers
Url:            http://tcl.apache.org/rivet/
Source0:        %{sourcedir}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  apache-rpm-macros
%if 0%{?suse_version}
BuildRequires:  apache2-devel
BuildRequires:  curl
BuildRequires:  tcl-devel
Requires:       apache2
Requires:       %{apache_mmn}
Requires:       %{apache_suse_maintenance_mmn}
%else
BuildRequires:  httpd
BuildRequires:  httpd-devel
BuildRequires:  tcl-devel
#Requires:       httpd
%endif

%description
Apache2 module for TCL script language.
- Servelet: use TCL inline in html files.
- CGI-like: TCL script to generate HTML page.

See: http://tcl.apache.org/rivet

%prep
%setup -q -n %{sourcedir}

%build
# Error on CentOS, RH: libtool: link: only absolute run-paths are allowed
# -> set APACHE_LIBEXECDIR to "apxs -q libexecdir"
# (all macros in comments are made inactive by doubelling the %%)
# export APACHE_LIBEXECDIR=%%apache2_libexecdir
%configure \
        --with-tcl=%{_libdir} \
        --with-tclsh=%{_bindir}/tclsh \
        --with-apache=/usr \
        --with-rivet-target-dir=%{rivetdir} \
        --with-apxs=%{apache_apxs} \
        --with-pic \
        --disable-rpath

#        --disable-debug

		if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
# %%{__make} %%{?_smp_mflags} doc

%install
make DESTDIR=%{buildroot} install
# Create configuration file mod_rivet.conf to /etc/apache2/conf.d
mkdir -p %{buildroot}%{ap2sysconfautodir}
cat <<EOT >%{buildroot}%{ap2rivetconffile}
# Apache2 module rivet configuration file

EOT

# If there is no a2enmod, load rivet by the configuration file
if [ ! -x %{_sbindir}/a2enmod ]
then
    cat <<EOT >>%{buildroot}%{ap2rivetconffile}
# Loads the module.
LoadModule rivet_module modules/mod_rivet.so

EOT

fi

    cat <<EOT >>%{buildroot}%{ap2rivetconffile}
# Let the module handle .rvt and .tcl files.
AddType application/x-httpd-rivet  rvt
AddType application/x-rivet-tcl    tcl

# The default charset can be specified in the configuration
AddType "application/x-httpd-rivet; charset=utf-8" rvt

# Add index.rvt to the list of files that will be served
DirectoryIndex index.rvt

EOT

%post
if [ -x %{_sbindir}/a2enmod ]
then
        if ! a2enmod -q rivet; then
                a2enmod rivet
        fi
fi

%preun
# only if uninstalled
if [ "$1" = "0" ]
then
        if [ -x %{_sbindir}/a2enmod ]
        then
        if a2enmod -q rivet; then
                a2dismod rivet
        fi
        fi
fi

%postun
%restart_on_update apache2

%files
%defattr(-,root,root, 0755)
%doc LICENSE NOTICE contrib doc/html doc/examples ChangeLog BUGS README* TODO
%{rivetdir}
%{apache_libexecdir}/*.so
%config(noreplace) %{ap2rivetconffile}

%changelog
* Thu Nov 13 2020 ray2501@gmail.com
- Update to Rivet release 3.2.0
* Thu Jan 10 2019 ray2501@gmail.com
- Update to Rivet release 3.1.1
* Wed Nov 28 2018 ray2501@gmail.com
- Update to Rivet release 3.1.0
* Mon Nov 19 2018 ray2501@gmail.com
- Update to Rivet release 3.0.3
* Mon Jul 9 2018 ray2501@gmail.com
- Update to Rivet release 3.0.2
* Sat Feb 10 2018 ray2501@gmail.com
- Update to Rivet release 3.0.1
* Thu Jan 1 2018 ray2501@gmail.com
- Update to Rivet release 3.0.0
- Remove check test (for spec test)
* Thu Sep 7 2017 oehhar@users.sourceforge.net
- Update to Rivet release 2.3.4
* Thu Sep 22 2016 oehhar@users.sourceforge.net
- Update to Rivet release 2.3.2
* Wed Mar 30 2016 oehhar@users.sourceforge.net
- Update to Rivet release 2.3.0
* Mon Dec 07 2015 oehhar@users.sourceforge.net
- Update to Rivet release 2.2.4
* Fri Sep 25 2015 pgajdos@suse.com
- apache-rpm-macros now know basic macros also for other
  rpm based distros
* Wed Sep 16 2015 oehhar@users.sourceforge.net
- Added support for RHEL 7 and friends by switching apxs path
* Tue Sep 15 2015 pgajdos@suse.com
- test module with %apache_test_module_curl
* Thu Jul 16 2015 pgajdos@suse.com
- Requries: %{apache_suse_maintenance_mmn}
  This will pull this module to the update (in released distribution)
  when apache maintainer thinks it is good (due api/abi changes).
* Wed Jul 15 2015 oehhar@users.sourceforge.net
- Update to Rivet release 2.2.3
* Tue Nov 11 2014 pgajdos@suse.cz
- no parallel install, it fails randomly
* Mon Nov 3 2014 pgajdos@suse.cz
- call spec-cleaner
- use apache rpm macros
* Thu Jun 26 2014 oehhar@users.sourceforge.net
- Update to Rivet release 2.2.0
* Tue Mar 18 2014 oehhar@users.sourceforge.net
- Update to Rivet release 2.1.4
* Wed Oct 2 2013 oehhar@users.sourceforge.net
- Update to Rivet release 2.1.3 
- Removed make install-packages
* Mon Jul 15 2013 oehhar@users.sourceforge.net
- Added make install-packages to also install packages
* Mon Jul 1 2013 oehhar@users.sourceforge.net
- Update to Rivet release 2.1.2
* Mon Feb 25 2013 oehhar@users.sourceforge.net
- Update to Rivet release 2.1.1
* Thu Dec 6 2012 oehhar@users.sourceforge.net
- Update to Rivet release 2.1.0
* Thu Dec 6 2012 oehhar@users.sourceforge.net
- Update to Rivet release 2.0.6
* Wed Jul 4 2012 oehhar@users.sourceforge.net
- Fedora requires httpd-devel instead apache2-devel.
  Inserted conditional code inspiered from apache2-mod_bmx.spec
- Added "file normalize" to macro tcl_archdir
* Fri Jun 29 2012 oehhar@users.sourceforge.net
- Update to Rivet release 2.0.5
* Mon Sep 26 2011 oehhar@users.sourceforge.net
- Update to Rivet release 2.0.4
- Removed own deletion of .la files - is now done by rivet makefile
* Sat Jul 16 2011 oehhar@users.sourceforge.net
- Update to Rivet release 2.0.3
* Mon Nov 1 2010 oehhar@users.sourceforge.net
- Use apxs2-prefork instead apxs2 because rivet only works with prefork.
* Sun Oct 31 2010 oehhar@users.sourceforge.net
- Update to Rivet release 2.0.2
* Sat Jul 17 2010 oehhar@users.sourceforge.net
- Update to Rivet release 2.0.1
* Fri May 14 2010 oehhar@users.sourceforge.net
- Incorporated ideas from rpmforge make file at
  http://svn.rpmforge.net/viewvc/rpmforge/trunk/rpms/mod_rivet/
* Wed May 12 2010 oehhar@users.sourceforge.net
- Initial version (well mainly written by Reinhard Max from SuSE)
* Tue May 11 2010 oehhar@users.sourceforge.net
- Renamed to apache2-mod_rivet
- Use /etc/apache2/conf.d for config auto include

