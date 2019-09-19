#!/usr/bin/tclsh

set arch "x86_64"
set fileurl "https://www-us.apache.org/dist/tcl/rivet/rivet-3.1.1.tar.gz"
set base "libapache2-mod-rivet-3.1.1"

set var [list wget $fileurl -O $base.tar.gz]
exec >@stdout 2>@stderr {*}$var

set var [list tar xzvf $base.tar.gz]
exec >@stdout 2>@stderr {*}$var

set var [list mv rivet-3.1.1 $base]
exec >@stdout 2>@stderr {*}$var

set var [list tar cjvf $base.tar.bz2 $base]
exec >@stdout 2>@stderr {*}$var

if {[file exists build]} {
    file delete -force build
}

file mkdir build/BUILD build/RPMS build/SOURCES build/SPECS build/SRPMS
file copy -force $base.tar.bz2 build/SOURCES

set buildit [list rpmbuild --target $arch --define "_topdir [pwd]/build" -bb apache2-mod_rivet.spec]
exec >@stdout 2>@stderr {*}$buildit

file delete -force $base
file delete $base.tar.gz
file delete $base.tar.bz2

