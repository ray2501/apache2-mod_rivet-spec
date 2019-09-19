# apache2-mod_rivet-spec
openSUSE RPM spec for Apache Rivet

Source files is from Apache Rivet [Download](http://ftp.tc.edu.tw/pub/Apache/tcl/rivet/).

openSUSE RPM spec and related files is from
[openSUSE](https://build.opensuse.org/package/show/Apache:Modules/apache2-mod_rivet).

* Notice: now I don't know how to pass the check test, so I remove the check.

[Rivet](https://tcl.apache.org/rivet/) 3.0 ships with a major rewriting of mod_rivet, whose code has been
redesigned into a modular architecture with the purpose to preserve the basic
features of the 2.x series of modules but also to provide support for both non
threaded Apache MPMs (Multi Process Module), such as mod_mpm_prefork, and
threaded MPMs such as mod_mpm_worker, mod_mpm_event and mod_mpm_winnt.

