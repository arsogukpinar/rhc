%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemversion %(echo %{version} | cut -d'.' -f1-3)

Summary:       OpenShift client management tools
Name:          rhc
Version: 1.18.1
Release:       1%{?dist}
Group:         Network/Daemons
License:       ASL 2.0
URL:           http://openshift.redhat.com
Source0:       rhc-%{version}.tar.gz

BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: ruby >= 1.8.5
BuildRequires: rubygems
BuildRequires: rubygem-rdoc
BuildRequires: ruby-irb
Requires:      ruby >= 1.8.5
Requires:      rubygem-parseconfig
Requires:      rubygem-httpclient
Requires:      rubygem-test-unit
Requires:      rubygem-net-ssh
Requires:      rubygem-net-ssh-multi
Requires:      rubygem-archive-tar-minitar
Requires:      rubygem-commander
Requires:      rubygem-open4
Requires:      git
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
Requires:      rubygem-net-ssh-multi
%endif
Obsoletes:     rhc-rest
Provides:      rubygem-rhc

BuildArch:     noarch

%description
Provides OpenShift client libraries.

%prep
%setup -q

%build
for f in bin/rhc*
do
  ruby -c $f
done

for f in lib/*.rb
do
  ruby -c $f
done

%install
pwd
rm -rf $RPM_BUILD_ROOT

mkdir -p "$RPM_BUILD_ROOT/usr/share/man/man1/"
mkdir -p "$RPM_BUILD_ROOT/usr/share/man/man5/"

for f in man/*
do
  len=`expr length $f`
  manSection=`expr substr $f $len $len`
  cp $f "$RPM_BUILD_ROOT/usr/share/man/man${manSection}/"
done

mkdir -p $RPM_BUILD_ROOT/etc/openshift
if [ ! -f "$RPM_BUILD_ROOT/etc/openshift/express.conf" ]
then
  cp "conf/express.conf" $RPM_BUILD_ROOT/etc/openshift/
fi

LC_ALL=en_US.UTF-8

# Package the gem
gem build rhc.gemspec

mkdir -p .%{gemdir}
# Ignore dependencies here because these will be handled by rpm 
gem install --install-dir $RPM_BUILD_ROOT/%{gemdir} --bindir $RPM_BUILD_ROOT/%{_bindir} --local -V --force --rdoc --ignore-dependencies \
     rhc-%{version}.gem

# Copy the bash autocompletion script
mkdir -p "$RPM_BUILD_ROOT/etc/bash_completion.d/"
cp autocomplete/rhc_bash $RPM_BUILD_ROOT/etc/bash_completion.d/rhc

cp LICENSE $RPM_BUILD_ROOT/%{gemdir}/gems/rhc-%{version}/LICENSE
cp COPYRIGHT $RPM_BUILD_ROOT/%{gemdir}/gems/rhc-%{version}/COPYRIGHT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE
%doc COPYRIGHT
%{_bindir}/rhc
%{_mandir}/man1/rhc*
%{_mandir}/man5/express*
%{gemdir}/gems/rhc-%{version}/
%{gemdir}/cache/rhc-%{version}.gem
%{gemdir}/doc/rhc-%{version}
%{gemdir}/specifications/rhc-%{version}.gemspec
%config(noreplace) %{_sysconfdir}/openshift/express.conf
%attr(0644,-,-) /etc/bash_completion.d/rhc

%changelog
* Wed Dec 04 2013 Adam Miller <admiller@redhat.com> 1.18.1-1
- Merge pull request #518 from liggitt/sztsian-master
  (dmcphers+openshiftbot@redhat.com)
- Update spec test (jliggitt@redhat.com)
- Bug 1033348  Display OpenShift instance name when requesting password
  https://bugzilla.redhat.com/show_bug.cgi?id=1033348 Added openshift_server
  name in Line 77 to show the server info. (zsun@fedoraproject.org)
- Add spec tests (jliggitt@redhat.com)
- Fix bug 1035157: Test for git (jliggitt@redhat.com)
- Fix bug 1006154: app create indent (jliggitt@redhat.com)
- bump_minor_versions for sprint 37 (admiller@redhat.com)

* Tue Nov 19 2013 Adam Miller <admiller@redhat.com> 1.17.6-1
- Correctly clean up scalable test (jliggitt@redhat.com)

* Wed Nov 13 2013 Adam Miller <admiller@redhat.com> 1.17.5-1
- Fix bug 1018077: Regex-breaking cartridge name search (jliggitt@redhat.com)
- Merge pull request #510 from liggitt/bug_1025241_typo
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #509 from
  liggitt/bug_1010939_improve_no_allowed_gear_sizes
  (dmcphers+openshiftbot@redhat.com)
- Bug 1025241: Fix typo (jliggitt@redhat.com)
- Bug 1010939: Improve no allowed gear sizes (jliggitt@redhat.com)

* Tue Nov 12 2013 Adam Miller <admiller@redhat.com> 1.17.4-1
- Merge pull request #508 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #507 from
  liggitt/bug_1029166_improve_domain_configure_error
  (dmcphers+openshiftbot@redhat.com)
- Fixes origin tests - list cartridges and randomly pick one for testing
  (contact@fabianofranz.com)
- Fix bug 1029166: Improve error message on domain configure
  (jliggitt@redhat.com)
- Fix bug 1029169 - improve rhc domain configure gear size help
  (jliggitt@redhat.com)

* Mon Nov 11 2013 Adam Miller <admiller@redhat.com> 1.17.3-1
- Merge pull request #504 from liggitt/bug_1028963_force_delete_domain
  (dmcphers+openshiftbot@redhat.com)
- Update spec test (jliggitt@redhat.com)
- Bug 1026275 - will fail in the client when trying to deploy an artifact
  incompatible with the app deployment type (contact@fabianofranz.com)
- Bug 1028963: Add --force option to delete-domain (jliggitt@redhat.com)

* Fri Nov 08 2013 Adam Miller <admiller@redhat.com> 1.17.2-1
- Merge pull request #502 from liggitt/fix_scalable_test
  (dmcphers+openshiftbot@redhat.com)
- Fix scalable test (jliggitt@redhat.com)

* Thu Nov 07 2013 Adam Miller <admiller@redhat.com> 1.17.1-1
- Merge pull request #501 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Allows specifying gear size when adding cartridge to an app
  (contact@fabianofranz.com)
- remove a dot from help (mmahut@redhat.com)
- Bug 1024741 (contact@fabianofranz.com)
- bump_minor_versions for sprint 36 (admiller@redhat.com)

* Thu Oct 31 2013 Adam Miller <admiller@redhat.com> 1.16.8-1
- Merge pull request #496 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Bug 1024741 (contact@fabianofranz.com)

* Thu Oct 31 2013 Adam Miller <admiller@redhat.com> 1.16.7-1
- Merge pull request #495 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Improved performance and wording in deployment activations list
  (contact@fabianofranz.com)
- Fixes Bug 1024741 (contact@fabianofranz.com)
- Improved output format of the deployments list (contact@fabianofranz.com)

* Wed Oct 30 2013 Adam Miller <admiller@redhat.com> 1.16.6-1
- Fix oo-register-user invocation for Origin on RHEL. (kraman@gmail.com)
- Merge pull request #493 from smarterclayton/color_error_message
  (dmcphers+openshiftbot@redhat.com)
- Color error message from SSH (ccoleman@redhat.com)

* Tue Oct 29 2013 Adam Miller <admiller@redhat.com> 1.16.5-1
- Bug 1022444 - Should also print warnings when an error occurs
  (ccoleman@redhat.com)

* Fri Oct 25 2013 Adam Miller <admiller@redhat.com> 1.16.4-1
- Merge pull request #491 from liggitt/krb5 (dmcphers+openshiftbot@redhat.com)
- Add feature test for kerberos key add (jliggitt@redhat.com)

* Thu Oct 24 2013 Adam Miller <admiller@redhat.com> 1.16.3-1
- Allow passing key type and content via command line (jliggitt@redhat.com)
- krb5 work (jliggitt@redhat.com)
- Bug 1019294 - ssh_helpers now handle authentication failures
  (contact@fabianofranz.com)

* Tue Oct 22 2013 Adam Miller <admiller@redhat.com> 1.16.2-1
- Merge pull request #489 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Bug 1021365 - fixed handling server without deployment support
  (contact@fabianofranz.com)

* Mon Oct 21 2013 Adam Miller <admiller@redhat.com> 1.16.1-1
- Fixes Bug 1019646 and Bug 1020473 (contact@fabianofranz.com)
- Respect proxy config when deploying from binary file url
  (contact@fabianofranz.com)
- Fix ssh key test (jliggitt@redhat.com)
- Merge pull request #482 from
  smarterclayton/bug_1019980_test_cases_for_key_distribution
  (dmcphers+openshiftbot@redhat.com)
- Bug 1019980 - Add test cases for SSH access across multiple users
  (ccoleman@redhat.com)
- Deploy - display when configure-app provided with no options, other minor
  improvements (contact@fabianofranz.com)
- Deploy - better handling of errors form stderr (contact@fabianofranz.com)
- Deploy - grammar fixes (contact@fabianofranz.com)
- Deploy - better handling of errors form stderr (contact@fabianofranz.com)
- Bug 1018729 - fixed deploy binary from url (contact@fabianofranz.com)
- Deploy (contact@fabianofranz.com)
- Fix test cases to run on F19/Origin (kraman@gmail.com)
- Merge pull request #475 from brenton/spec_fixes1
  (dmcphers+openshiftbot@redhat.com)
- Remove old unnecessary test case for domains (ccoleman@redhat.com)
- Adding BuildRequires (bleanhar@redhat.com)
- Adding ose-2.0 releaser (jdetiber@redhat.com)
- bump_minor_versions for sprint 35 (admiller@redhat.com)

* Fri Oct 04 2013 Adam Miller <admiller@redhat.com> 1.15.6-1
- Merge pull request #473 from smarterclayton/depend_on_net_ssh_multi
  (dmcphers+openshiftbot@redhat.com)
- Depend on net-ssh-multi (ccoleman@redhat.com)

* Thu Oct 03 2013 Adam Miller <admiller@redhat.com> 1.15.5-1
- Merge pull request #471 from
  smarterclayton/bug_1013321_handle_implicit_arguments_correctly
  (dmcphers+openshiftbot@redhat.com)
- Review comments, add more tests and fix a few edge cases
  (ccoleman@redhat.com)
- Bug 1014692 - rhc authorization -h should display help page
  (ccoleman@redhat.com)
- domain.feature fails because rhc domain changes (ccoleman@redhat.com)
- Bug 1013321 - Handle implicit arguments more accurately (ccoleman@redhat.com)

* Tue Oct 01 2013 Adam Miller <admiller@redhat.com> 1.15.4-1
- Merge pull request #469 from smarterclayton/mongo_rhc_test_fails
  (dmcphers+openshiftbot@redhat.com)
- Bug 1013292 - Tolerate OSE1.2 attributes (ccoleman@redhat.com)
- Names of carts changed (ccoleman@redhat.com)

* Fri Sep 27 2013 Troy Dawson <tdawson@redhat.com> 1.15.3-1
- Merge pull request #468 from smarterclayton/origin_ui_72_membership
  (dmcphers+openshiftbot@redhat.com)
- Origin UI 72 - Memberhip (ccoleman@redhat.com)

* Thu Sep 26 2013 Troy Dawson <tdawson@redhat.com> 1.15.2-1
- 

* Thu Sep 26 2013 Troy Dawson <tdawson@redhat.com> 1.15.1-1
- flatten than compact ssh cmd (mateus@caruccio.com)
- stub has_ssh? (mateus@caruccio.com)
- add --ssh to snapshot (mateus@caruccio.com)
- bump_minor_versions for sprint 34 (admiller@redhat.com)

* Thu Sep 12 2013 Adam Miller <admiller@redhat.com> 1.14.7-1
- Bug 1006031 - rhc restore with spaces in filename (jdetiber@redhat.com)
- Merge pull request #463 from liggitt/gssapi_failure
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #462 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Catch gssapi exception, fall back to basic (jliggitt@redhat.com)
- Bug 999868 - improved order for messages (contact@fabianofranz.com)
- Bug 999868 - encapsulated check for env vars support
  (contact@fabianofranz.com)
- Bug 999868 - cleanup (contact@fabianofranz.com)
- Bug 999868 - warns when create-app and add-cartridge and server does not
  support env vars (contact@fabianofranz.com)

* Wed Sep 11 2013 Adam Miller <admiller@redhat.com> 1.14.6-1
- Update testcase support info for phpmyadmin version (jforrest@redhat.com)
- Merge pull request #457 from
  jwforres/bug_1006255_match_cart_descrip_by_whole_word
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #458 from
  smarterclayton/bug_1005763_use_ssh_url_to_check_login
  (dmcphers+openshiftbot@redhat.com)
- Bug 1006255 - cartridges should only match description on whole words
  (jforrest@redhat.com)
- Bug 1005763 - Need to use the ssh_url (not uuid) to generate SSH
  (ccoleman@redhat.com)

* Tue Sep 10 2013 Adam Miller <admiller@redhat.com> 1.14.5-1
- Merge pull request #456 from markllama/test/env_feature_init
  (dmcphers+openshiftbot@redhat.com)
- create an app for each env set/clear scenario (markllama@gmail.com)

* Mon Sep 09 2013 Adam Miller <admiller@redhat.com> 1.14.4-1
- Merge pull request #454 from smarterclayton/update_domain_text
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #445 from smarterclayton/bug_990484_too_many_attempts_fail
  (dmcphers+openshiftbot@redhat.com)
- Clarify namespace on create (ccoleman@redhat.com)
- Update domain messages and text to be more domain centric (rather than
  namespace) (ccoleman@redhat.com)
- Add test case for retry to the max, also fix bad constant overrides
  (ccoleman@redhat.com)
- Bug 990484 - Error when hitting max retries (ccoleman@redhat.com)

* Fri Sep 06 2013 Adam Miller <admiller@redhat.com> 1.14.3-1
- Merge pull request #446 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Fixing RHC tests for Origin (kraman@gmail.com)
- Added cucumber tests for rhc env (contact@fabianofranz.com)
- Added cucumber tests for rhc env (contact@fabianofranz.com)
- Create app with env vars as arguments (contact@fabianofranz.com)
- Will not display env vars info on the end of create-app process
  (contact@fabianofranz.com)
- Added spec test for option being provided twice, other minor stuff
  (contact@fabianofranz.com)
- Introduces :option_type => :list (contact@fabianofranz.com)
- Readded support to option as array on commander, rhc env spec tests for
  multiple -e|--env items (contact@fabianofranz.com)

* Thu Sep 05 2013 Adam Miller <admiller@redhat.com> 1.14.2-1
- Bug 1002269 - trim leading newlines and trailing whitespace in client
  messages (jforrest@redhat.com)

* Thu Aug 29 2013 Adam Miller <admiller@redhat.com> 1.14.1-1
- Update phpmyadmin-3 to phpmyadmin-4 (mfojtik@redhat.com)
- Merge pull request #450 from jwforres/bug_999637_rhc_tests_fail_with_seed
  (dmcphers+openshiftbot@redhat.com)
- Bug 999637 - rhc tests fail with seed 48203 (jforrest@redhat.com)
- Bug 999791 - uninitialized constant RHC::Rest::Client::Set
  (jforrest@redhat.com)
- bump_minor_versions for sprint 33 (admiller@redhat.com)

* Wed Aug 21 2013 Adam Miller <admiller@redhat.com> 1.13.5-1
- Merge pull request #444 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #443 from Miciah/bug-999602-RHC-CommandHelpBindings-sort-
  commands (dmcphers+openshiftbot@redhat.com)
- Merge pull request #440 from Miciah/lib-rhc-commands-base.rb-whitespace
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #442 from
  jwforres/bug_994174_rhc_client_messages_not_displayed
  (dmcphers+openshiftbot@redhat.com)
- Added spec tests for env vars with whitespaces (contact@fabianofranz.com)
- RHC::CommandHelpBindings: Sort commands (miciah.masters@gmail.com)
- More spec tests for env vars parser (contact@fabianofranz.com)
- Bug 994174 - rhc not displaying CLIENT_MESSAGE returned by broker
  (jforrest@redhat.com)
- Improved error message for invalid env var names (contact@fabianofranz.com)
- Added spec test cases for invalid env var names (contact@fabianofranz.com)
- Validates env var names according to IEEE Std 1003.1-2001
  (contact@fabianofranz.com)
- rhc/commands/base.rb: Fix whitespace (miciah.masters@gmail.com)

* Wed Aug 21 2013 Adam Miller <admiller@redhat.com> 1.13.4-1
- Merge pull request #441 from
  smarterclayton/bug_994986_remove_old_cartridge_alias
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #439 from Miciah/delete-RHC-Commands-Base-inherited
  (dmcphers+openshiftbot@redhat.com)
- Bug 997763 - raise error if server does not provide a Jenkins cartridge
  (contact@fabianofranz.com)
- Bug 997763 - encapsulated fetch of jenkins cartridges names
  (contact@fabianofranz.com)
- Bug 997763 - find jenkins cartridges by tag and base name
  (contact@fabianofranz.com)
- Bug 994986 - Remove 'rhc cartridge' because it conflicts with other aliases
  (ccoleman@redhat.com)
- Delete RHC::Commands::Base::inherited (miciah.masters@gmail.com)

* Tue Aug 20 2013 Adam Miller <admiller@redhat.com> 1.13.3-1
- Merge pull request #436 from fabianofranz/dev/ffranz/env-vars
  (dmcphers+openshiftbot@redhat.com)
- Adds support to user-defined environment variables through 'rhc env'
  (ffranz@redhat.com)
- Added "rhc env-var [list|add|remove]" commands to handle user settable
  environment variables (kraman@gmail.com)

* Mon Aug 19 2013 Adam Miller <admiller@redhat.com> 1.13.2-1
- <cartridge versions> origin_runtime_219, fix up references to renamed carts
  https://trello.com/c/evcTYKdn/219-3-adjust-out-of-date-cartridge-versions
  (jolamb@redhat.com)

* Thu Aug 08 2013 Adam Miller <admiller@redhat.com> 1.13.1-1
- Review comments (ccoleman@redhat.com)
- Merge pull request #434 from
  smarterclayton/to_stage_bug_992942_rhc_misreporting_disk_usage
  (dmcphers+openshiftbot@redhat.com)
- Bug 992942 - RHC is reporting block counts, not bytes (ccoleman@redhat.com)
- bump_minor_versions for sprint 32 (admiller@redhat.com)

* Wed Jul 31 2013 Adam Miller <admiller@redhat.com> 1.12.4-1
- Update spec test to check new client against old server (jliggitt@redhat.com)
- Fix bug 989307 - remove version accept header on initial negotiation
  (jliggitt@redhat.com)

* Fri Jul 26 2013 Adam Miller <admiller@redhat.com> 1.12.3-1
- Fix rhc domain spec tests for default list action (jliggitt@redhat.com)
- Merge pull request #428 from smarterclayton/support_rhc_domain_list
  (dmcphers+openshiftbot@redhat.com)
- Should not require things from commands (ccoleman@redhat.com)
- Support LIST_APPLICATIONS in API 1.5 (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into support_rhc_domain_list
  (ccoleman@redhat.com)
- Include autocompletes (ccoleman@redhat.com)
- Switch to LIST_DOMAINS_BY_OWNER (ccoleman@redhat.com)
- Handle nil values in header array (ccoleman@redhat.com)
- Fix review comments (ccoleman@redhat.com)
- Dangling commas not allowed on Ruby 2.0 (ccoleman@redhat.com)
- Support distinguishing between domains the user owns and all domains he has
  acces to (ccoleman@redhat.com)
- Support listing domains from RHC (ccoleman@redhat.com)

* Wed Jul 24 2013 Adam Miller <admiller@redhat.com> 1.12.2-1
- Merge pull request #430 from liggitt/bug_987336_deprecate_sshkey_delete
  (dmcphers+openshiftbot@redhat.com)
- Fix bug 987336 - deprecate `sshkey delete` (jliggitt@redhat.com)
- Fix bug 987219 - incorrect help for `rhc cartridge-list`
  (jliggitt@redhat.com)
- Merge remote-tracking branch 'origin/master' into use_http_client_auth
  (ccoleman@redhat.com)
- reset_challenge should do nothing (ccoleman@redhat.com)
- Review comment test case and fix @passwd reference (ccoleman@redhat.com)
- If the number of columns is zero, do not wrap. (jpazdziora@redhat.com)
- RSpec 2.14 is a bit of a nazi about deprecations - make them disappear
  (ccoleman@redhat.com)
- Tests 100%% passing (ccoleman@redhat.com)
- Use HTTPClient auth (ccoleman@redhat.com)

* Fri Jul 12 2013 Adam Miller <admiller@redhat.com> 1.12.1-1
- bump_minor_versions for sprint 31 (admiller@redhat.com)

* Wed Jul 10 2013 Adam Miller <admiller@redhat.com> 1.11.4-1
- Bug 979963 - Log and trace errors for interrupts during rhc setup
  (ccoleman@redhat.com)
- Merge pull request #425 from
  smarterclayton/bug_979992_fix_stty_handling_for_non_interactive
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #420 from pravisankar/dev/ravi/bug980804
  (dmcphers+openshiftbot@redhat.com)
- Bug 979992 - Only respond to 'y', 'yes', 'n', and 'no' (ccoleman@redhat.com)
- Bug 980804 - Alias name need to be in lower case while comparing with
  existing app aliases (rpenta@redhat.com)

* Tue Jul 09 2013 Adam Miller <admiller@redhat.com> 1.11.3-1
- Merge pull request #421 from smarterclayton/bug_981780_better_responses
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #423 from
  smarterclayton/bug_982135_fix_namespace_optional_message
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #424 from
  smarterclayton/bug_981274_forgot_to_update_autocomplete
  (dmcphers+openshiftbot@redhat.com)
- Bug 981274 - Update autocomplete script (ccoleman@redhat.com)
- Bug 982135 - Namespace optional should affect the message displayed
  (ccoleman@redhat.com)
- Bug 980413 - Options that are nil should default to true
  (ccoleman@redhat.com)
- Bug 981780 - Filter broker results more effectively, and display results on
  cartridge actions (ccoleman@redhat.com)

* Tue Jul 02 2013 Adam Miller <admiller@redhat.com> 1.11.2-1
- Add net-ssh-multi as dependency on F19+ (kraman@gmail.com)
- Bug 978837 - Don't show stack trace if --ssh executable not found
  (andy.goldstein@redhat.com)
- Webmock 1.12 breaks query parameter compatibility, can't dupe Symbol/Fixnum
  when it tries to match a request signature.  Lock to < 1.12 for now.
  (ccoleman@redhat.com)
- fix typos (dmcphers@redhat.com)

* Tue Jun 25 2013 Adam Miller <admiller@redhat.com> 1.11.1-1
- bump_minor_versions for sprint 30 (admiller@redhat.com)

* Mon Jun 24 2013 Adam Miller <admiller@redhat.com> 1.10.6-1
- Merge pull request #411 from
  smarterclayton/bug_976682_overly_aggressive_check_in_rhc
  (dmcphers+openshiftbot@redhat.com)
- Display empty lines with prefix from ssh (ccoleman@redhat.com)
- Bug 976682 - Check for web carts was too aggressive (ccoleman@redhat.com)

* Thu Jun 20 2013 Adam Miller <admiller@redhat.com> 1.10.5-1
- Merge pull request #408 from anthonyfok/ask_password_chomp
  (dmcphers+openshiftbot@redhat.com)
- Prevent ask_password from stripping whitespace (Take 2)
  (anthony.t.fok@gmail.com)

* Wed Jun 19 2013 Adam Miller <admiller@redhat.com> 1.10.4-1
- Modify rhc ssh command to reject --limit values of < 1 (hripps@redhat.com)
- Merge pull request #407 from
  smarterclayton/bug_965804_display_results_from_remove_cart
  (dmcphers+openshiftbot@redhat.com)
- Bug 965804 - Display results when a cartridge or application is removed
  (ccoleman@redhat.com)

* Tue Jun 18 2013 Adam Miller <admiller@redhat.com> 1.10.3-1
- Bug 975410 - rhc ssh limit option failing (jforrest@redhat.com)

* Mon Jun 17 2013 Adam Miller <admiller@redhat.com> 1.10.2-1
- Merge pull request #404 from smarterclayton/parallel_commands
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #401 from liggitt/bug_971328_results_messages
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #402 from jwforres/bug_974439_rhc_subcommand_with_dash
  (dmcphers+openshiftbot@redhat.com)
- Review comments (ccoleman@redhat.com)
- Run in order on Ruby 1.8.7 (ccoleman@redhat.com)
- Merge pull request #405 from
  jwforres/bug_974381_cartlist_verbose_missing_asterisk
  (dmcphers+openshiftbot@redhat.com)
- Add spec test for various results messages formats (jliggitt@redhat.com)
- Bug 974439 - add testcase (jforrest@redhat.com)
- Bug 974381 - review feedback (jforrest@redhat.com)
- Bug 974381 - cartridge list -v missing asterisk on carts with usage cost
  (jforrest@redhat.com)
- Bug 974439 - review feedback (jforrest@redhat.com)
- Missing coverage, better output handling (ccoleman@redhat.com)
- Bug 969390 - Only full stop triggers message (ccoleman@redhat.com)
- Implement a parallel SSH command helper 'rhc ssh --gears' which executes a
  command against all gears of an app. Implement a quota display for 'rhc show-
  app --gears quota' (ccoleman@redhat.com)
- When rounded, certain table cells can get extra whitespace
  (ccoleman@redhat.com)
- Bug 974439 - fix rhc help issues (jforrest@redhat.com)
- Fix bug 971328 - new results message format (jliggitt@redhat.com)
- Merge pull request #400 from
  smarterclayton/bug_963985_overhaul_rhc_app_create_output
  (dmcphers+openshiftbot@redhat.com)
- Allow RHC extended to run. (ccoleman@redhat.com)
- Review feedback (ccoleman@redhat.com)
- Merge pull request #399 from smarterclayton/issue_390_handle_no_proxy
  (dmcphers+openshiftbot@redhat.com)
- Ensure the return value is correct in Ruby 1.8.7 (ccoleman@redhat.com)
- Fix Ruby 1.8.7, test equality of strings (ccoleman@redhat.com)
- Bug 963985 - Overhaul how RHC app-create generates output
  (ccoleman@redhat.com)
- Support NO_PROXY by defaulting to httpclient's support.  This means non-
  qualified URIs are no longer supported. (ccoleman@redhat.com)
- Added optional command argument to 'rhc app ssh' so you can run a command,
  for example: (andy.goldstein@gmail.com)
- Updating RHC tests to work with F19 cartridge versions. Add psych as optional
  gem dependency used only on F19 systems (kraman@gmail.com)
- Merge pull request #396 from smarterclayton/allow_direct_scale_value
  (dmcphers+openshiftbot@redhat.com)
- Allow users to specify a direct scale value with rhc scale-cartridge php 5
  (sets min and max) (ccoleman@redhat.com)
- Bug 970028 - Handle empty rows (ccoleman@redhat.com)
- Give users a warning about scaling being a long running operation, and an
  additional bit of info on receive timeouts from set scale Handle ECONNRESET
  Suppress incorrect warning about downloaded cart on post-install operations
  (ccoleman@redhat.com)

* Thu May 30 2013 Adam Miller <admiller@redhat.com> 1.10.1-1
- bump_minor_versions for sprint 29 (admiller@redhat.com)

* Wed May 29 2013 Adam Miller <admiller@redhat.com> 1.9.6-1
- Merge pull request #393 from liggitt/bug_965923_trap_supported_signals
  (dmcphers+openshiftbot@redhat.com)
- Fix bug 965923 - only trap PIPE if supported (jordan@liggitt.net)
- Merge pull request #392 from
  liggitt/bug_967683_delete_domain_is_case_sensitive
  (dmcphers+openshiftbot@redhat.com)
- Fix bug 967683 - make domain id matching case-insensitive
  (jliggitt@redhat.com)

* Tue May 28 2013 Adam Miller <admiller@redhat.com> 1.9.5-1
- Fix bug 965923 - only trap supported signals (jliggitt@redhat.com)

* Thu May 23 2013 Adam Miller <admiller@redhat.com> 1.9.4-1
- Handle empty http proxy (ccoleman@redhat.com)

* Mon May 20 2013 Dan McPherson <dmcphers@redhat.com> 1.9.3-1
- Check for ENV presence (ccoleman@redhat.com)
- Support OPENSHIFT_CONFIG, which is the name of a file in the config directory
  to load. Switch to using a centralized debug output mechanism vs. individual
  classes caring. (ccoleman@redhat.com)
- Merge pull request #387 from
  smarterclayton/string_format_cant_align_ansi_sequences
  (dmcphers+openshiftbot@redhat.com)
- String ansi sequences aren't properly aligned by string format - revert to
  doing it ourselves (ccoleman@redhat.com)
- Add downloadable cart info to RHC (ccoleman@redhat.com)

* Thu May 16 2013 Adam Miller <admiller@redhat.com> 1.9.2-1
- Bug 963419 - Don't check API versions, check client links
  (ccoleman@redhat.com)
- Support for initial_git_url and downloadable cartridges should be tested
  against the presence of an optional parameter on the link relation.
  (ccoleman@redhat.com)
- Merge pull request #383 from jtharris/bugs/BZ958683
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #380 from smarterclayton/bug_960926_handle_pipe_closure
  (dmcphers+openshiftbot@redhat.com)
- Use --exclude-remote when targeting a single gear. (jharris@redhat.com)
- Bug 960926 - Handle EPIPE gracefully with exit (ccoleman@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.9.1-1
- bump_minor_versions for sprint 28 (admiller@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.8.9-1
- Merge pull request #382 from jtharris/bugs/BZ958675
  (dmcphers+openshiftbot@redhat.com)
- Wording change when no ports can be forwarded. (jharris@redhat.com)

* Wed May 08 2013 Adam Miller <admiller@redhat.com> 1.8.8-1
- Merge pull request #381 from smarterclayton/bug_960808_spelling_errors
  (dmcphers+openshiftbot@redhat.com)
- Bug 960808 - Mispelling in command help (ccoleman@redhat.com)
- Fix personal cart up to match latest (ccoleman@redhat.com)

* Mon May 06 2013 Adam Miller <admiller@redhat.com> 1.8.7-1
- Cannot add cart to app (missing tests) (ccoleman@redhat.com)
- Merge pull request #376 from
  smarterclayton/bug_959542_handle_empty_tables_better
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #375 from
  smarterclayton/bug_959144_respect_disable_authorization_tokens_in_setup
  (dmcphers+openshiftbot@redhat.com)
- Bug 959542 - Handle empty tables cleanly (ccoleman@redhat.com)
- Bug 959144 - Respect use_authorization_tokens=false in rhc setup
  (ccoleman@redhat.com)

* Fri May 03 2013 Adam Miller <admiller@redhat.com> 1.8.6-1
- Merge pull request #374 from jtharris/bugs/BZ958668
  (dmcphers+openshiftbot@redhat.com)
- Tail the correct log dir for db carts (jharris@redhat.com)

* Thu May 02 2013 Adam Miller <admiller@redhat.com> 1.8.5-1
- Merge pull request #370 from smarterclayton/support_external_cartridges
  (dmcphers+openshiftbot@redhat.com)
- Rename "external cartridge" to "downloaded cartridge".  UI should call them
  "personal" cartridges (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into support_external_cartridges
  (ccoleman@redhat.com)
- Allow URLs to be passed to app creation and cartridge addition.  Clean up a
  few minor visual bugs, use the <verb>-<noun> form when referring to other
  commands (ccoleman@redhat.com)
- Support custom cartridge URLs (ccoleman@redhat.com)

* Wed May 01 2013 Adam Miller <admiller@redhat.com> 1.8.4-1
- Merge pull request #371 from jtharris/features/Card39
  (dmcphers+openshiftbot@redhat.com)
- Expand gear ssh url to handle gear not found. (jharris@redhat.com)
- --gear option for tail (jharris@redhat.com)
- --gear option for port-forward (jharris@redhat.com)

* Tue Apr 30 2013 Adam Miller <admiller@redhat.com> 1.8.3-1
- Merge pull request #373 from smarterclayton/test_enterprise_server
  (dmcphers+openshiftbot@redhat.com)
- Support running test cases without certain users (ccoleman@redhat.com)

* Mon Apr 29 2013 Adam Miller <admiller@redhat.com> 1.8.2-1
- Bug 957105 - Should remove the useless info in the result message when domain
  updated successfully (jforrest@redhat.com)

* Thu Apr 25 2013 Adam Miller <admiller@redhat.com> 1.8.1-1
- rhc show app --gear includes gear id and header (jharris@redhat.com)
- Gear info shows profile, status, carts, ssh (jharris@redhat.com)
- Merge pull request #367 from smarterclayton/bug_953802_change_community_url
  (dmcphers+openshiftbot@redhat.com)
- Bug 953802 - Change community url to be correct (ccoleman@redhat.com)
- Bug 953767 - Arguments that are arrays should set the options to an array
  (ccoleman@redhat.com)
- Nicer error message on invalid server URI. (jharris@redhat.com)
- Merge pull request #362 from smarterclayton/bug_952985_contextual_args_broken
  (dmcphers+openshiftbot@redhat.com)
- Bug 952985 - Context arguments broken due to optional list changes
  (ccoleman@redhat.com)
- bump_minor_versions for sprint 2.0.26 (tdawson@redhat.com)

* Tue Apr 16 2013 Troy Dawson <tdawson@redhat.com> 1.7.7-1
- Merge pull request #361 from jtharris/bugs/BZ928297
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #360 from smarterclayton/skip_nested_alias_load
  (dmcphers@redhat.com)
- Merge pull request #359 from smarterclayton/bug_952047_header_mutates_string
  (dmcphers+openshiftbot@redhat.com)
- API mismatch wording tweak (jharris@redhat.com)
- min_api is specified in rest_client call (jharris@redhat.com)
- Optional api version check for rest calls. (jharris@redhat.com)
- Aliases are being lazily executed on app list view, even though they don't
  have to be.  Clean up aliases retrieval to be based on capability, rather
  than version. (ccoleman@redhat.com)
- Bug 952047 - SSH key doesn't detect duplicate because name is changed
  (ccoleman@redhat.com)

* Mon Apr 15 2013 Adam Miller <admiller@redhat.com> 1.7.6-1
- Merge remote-tracking branch 'origin/master' into better_app_create_flow
  (ccoleman@redhat.com)
- Fix tests, reorganize wizard slightly (ccoleman@redhat.com)
- During app create, try more aggressively to set the user up.  Includes
  setting up the base config, domain, and keys.  Changes behavior of argument
  parsing for app to be optional. (ccoleman@redhat.com)

* Sat Apr 13 2013 Krishna Raman <kraman@gmail.com> 1.7.5-1
- Merge pull request #358 from
  smarterclayton/bug_951352_should_retry_key_on_bad_name
  (dmcphers+openshiftbot@redhat.com)
- Bug 951352 - Retry the key name during the wizard flow (ccoleman@redhat.com)
- Merge pull request #355 from fabianofranz/master (dmcphers@redhat.com)
- Bug 951436 - handling Windows platform on paging (ffranz@redhat.com)
- Bug 951369 (ffranz@redhat.com)
- tito releasers update (bleanhar@redhat.com)

* Thu Apr 11 2013 Adam Miller <admiller@redhat.com> 1.7.4-1
- Merge pull request #352 from
  smarterclayton/origin_ui_13_autocomplete_and_wrapping
  (dmcphers+openshiftbot@redhat.com)
- Bug 949910 - Mark alter and destroy as deprecated aliases
  (ccoleman@redhat.com)
- Generate separate switches for --[no-]-<...> switches in autocomplete
  (ccoleman@redhat.com)
- Review fixes (ccoleman@redhat.com)
- Require 'delegate' for HighLine extensions (ccoleman@redhat.com)
- Add help search capability and 'rhc help commands' (ccoleman@redhat.com)
- Support HighLine 1.5.1 for now for RHEL (ccoleman@redhat.com)
- Failing test case (ccoleman@redhat.com)
- Add alias from 'authorization' to 'authorizations' (ccoleman@redhat.com)
- Reopen ansi escape sequences after wrapping (ccoleman@redhat.com)
- Cleanup option values for --app and --namespace, minor syntax tweaks
  (ccoleman@redhat.com)
- Add Linux pager support for cartridges list and help (ccoleman@redhat.com)
- Tablify help output, add vastly improved root level help for commands.  Fix
  minor bugs in wrapping. (ccoleman@redhat.com)
- Autocomplete was not added to built gem (ccoleman@redhat.com)
- Disable paging for now (ccoleman@redhat.com)
- Separate HighLine extensions into their own class, use extension rather than
  injection.  Fix unit tests to properly isolate $terminal.
  (ccoleman@redhat.com)
- Copy autocomplete into the home directory to ensure it's not lost
  (ccoleman@redhat.com)
- Properly reset formatter after execution (ccoleman@redhat.com)
- Let RHEL/Fedora tests be run deliberately, fix ruby 1.8.7 test failure
  (ccoleman@redhat.com)
- Fix help for aliases and secondary commands, change core help page to use
  more readable forms (ccoleman@redhat.com)
- Move logout to root level (ccoleman@redhat.com)
- Add autocompletion instructions and a revised script to RHC.  Expose 'rake
  autocomplete' to generate a new version of the script. (ccoleman@redhat.com)
- Rogue puts used in error (ccoleman@redhat.com)
- All commands default to using dashes instead of spaces to separate them.
  Help now displays dashed versions in preference to spaces form.  Also
  supports a reversed "verb-noun" construct for commands. (ccoleman@redhat.com)

* Wed Apr 10 2013 Adam Miller <admiller@redhat.com> 1.7.3-1
- Fix broken rhc_extended tests (ccoleman@redhat.com)
- Ruby 1.8 treats Integer(nil) as 0, and 1.9 treats it as nil.  Switch to
  default gracefully. (ccoleman@redhat.com)

* Mon Apr 08 2013 Adam Miller <admiller@redhat.com> 1.7.2-1
- Replace expect{}.should with expect{}.to in remaining spots, depend on
  webmock 1.8 (ccoleman@redhat.com)
- Upgrade spec tests to passing, fix RSpec2 syntax errors, ensure randomized
  tests pass correctly (ccoleman@redhat.com)
- Merge pull request #347 from smarterclayton/delete_unused_files
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #348 from smarterclayton/bug_928240_prevent_from_code
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #346 from
  smarterclayton/bug_927425_use_authorization_tokens_not_strict_enough
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #345 from fabianofranz/master
  (dmcphers+openshiftbot@redhat.com)
- Remove doc files from spec (ccoleman@redhat.com)
- Bug 928240 - --from-code is not supported on clients where the latest API
  version is < 1.3 (ccoleman@redhat.com)
- Delete unused files (ccoleman@redhat.com)
- Bug 927425 - The use_authorization_tokens flag should be strict
  (ccoleman@redhat.com)
- Merge pull request #344 from jtharris/bugs/BZ928357 (dmcphers@redhat.com)
- Bug 928210 - fixed remove alias for API <= 1.3 (ffranz@redhat.com)
- Tests allow multiple DB cartridges to be added. (jharris@redhat.com)
- Bug 928357 - rhc_extended tests (jharris@redhat.com)

* Thu Mar 28 2013 Adam Miller <admiller@redhat.com> 1.7.1-1
- bump_minor_versions for sprint 26 (admiller@redhat.com)
- removing old API doc (dmcphers@redhat.com)

* Wed Mar 27 2013 Adam Miller <admiller@redhat.com> 1.6.7-1
- Bug 924633 - now dealing with empty certificate and private key files
  (ffranz@redhat.com)
- Bug 928210 - now handling server with no support to SSL certificates
  (ffranz@redhat.com)
- Fixed tests (ffranz@redhat.com)
- REST API version is now 1.4 (ffranz@redhat.com)
- Small wording improvement (ffranz@redhat.com)
- Merge pull request #339 from smarterclayton/bug_924142_should_safe_read_file
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #337 from smarterclayton/update_to_new_plan_values
  (dmcphers+openshiftbot@redhat.com)
- Wizard spec should be on FakeFS (ccoleman@redhat.com)
- Bug 924142 - Safely handle empty sshkey files (ccoleman@redhat.com)
- Merge pull request #340 from BanzaiMan/dev/hasari/bz920059
  (dmcphers+openshiftbot@redhat.com)
- Fix Bug 920059 (asari.ruby@gmail.com)
- Merge pull request #338 from
  smarterclayton/bug_924594_help_shouldnt_trigger_wizard
  (dmcphers+openshiftbot@redhat.com)
- Bug 924594 - Any combination of help should never trigger wizard behavior
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into update_to_new_plan_values
  (ccoleman@redhat.com)
- Rename 'MegaShift' to 'Silver' (ccoleman@redhat.com)

* Tue Mar 26 2013 Adam Miller <admiller@redhat.com> 1.6.6-1
- Merge pull request #336 from jtharris/bugs/BZ924863 (dmcphers@redhat.com)
- http_proxy ENV variable does not have to set protocol. (jharris@redhat.com)

* Mon Mar 25 2013 Adam Miller <admiller@redhat.com> 1.6.5-1
- Minor bug fixes (ffranz@redhat.com)
- Minor bug fixes and typos (ffranz@redhat.com)
- Minor bug fixes and typos (ffranz@redhat.com)
- Card #239: Added support to alias creation and deletion and SSL certificate
  upload to the CLI (ffranz@redhat.com)

* Thu Mar 21 2013 Adam Miller <admiller@redhat.com> 1.6.4-1
- Updates to enable RHC extended tests to run on Fedora 18 (kraman@gmail.com)

* Mon Mar 18 2013 Adam Miller <admiller@redhat.com> 1.6.3-1
- Display the duration of http requests in the debug output
  (ccoleman@redhat.com)

* Thu Mar 14 2013 Adam Miller <admiller@redhat.com> 1.6.2-1
- Merge pull request #332 from jtharris/highline_fix (dmcphers@redhat.com)
- Merge pull request #331 from BanzaiMan/dev/hasari/bz920028
  (dmcphers@redhat.com)
- Always use color for mock highline. (jharris@redhat.com)
- This spec now passes. (asari.ruby@gmail.com)
- Bug 920028. (asari.ruby@gmail.com)
- Merge pull request #328 from
  smarterclayton/unable_to_auth_when_tokens_missing
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #327 from jtharris/features/US2627
  (dmcphers+openshiftbot@redhat.com)
- When user is contacting a non auth service with use_authorization_tokens
  true, their credentials aren't passed to the server.  Instead, they get in a
  loop prompt. (ccoleman@redhat.com)
- Mark the failing spec as pending. (asari.ruby@gmail.com)
- Add spec for Bug 920028. (asari.ruby@gmail.com)
- Bug 918667 (jharris@redhat.com)
- Adding usage rate reminders. (jharris@redhat.com)

* Thu Mar 07 2013 Adam Miller <admiller@redhat.com> 1.6.1-1
- bump_minor_versions for sprint 25 (admiller@redhat.com)

* Wed Mar 06 2013 Adam Miller <admiller@redhat.com> 1.5.12-1
- Merge pull request #326 from smarterclayton/add_rhc_gears_call
  (dmcphers@redhat.com)
- Add rhc app show --gears to display info about the gears
  (ccoleman@redhat.com)

* Wed Mar 06 2013 Adam Miller <admiller@redhat.com> 1.5.11-1
- Wrap it up in paragraph (asari.ruby@gmail.com)
- Bug 917605 (asari.ruby@gmail.com)
- Bug 917457 (asari.ruby@gmail.com)
- Merge pull request #323 from smarterclayton/bug_915255_recreate_token
  (dmcphers+openshiftbot@redhat.com)
- Bug 915255 - Correctly regenerate token when use_authorization_tokens is true
  (ccoleman@redhat.com)
- Don't retry infinitely when in a loop (ccoleman@redhat.com)

* Tue Mar 05 2013 Adam Miller <admiller@redhat.com> 1.5.10-1
- Merge pull request #322 from
  smarterclayton/bug_917728_rhc_should_invoke_setup_with_no_args
  (dmcphers@redhat.com)
- Merge pull request #313 from smarterclayton/client_is_too_lazy
  (dmcphers@redhat.com)
- Merge pull request #321 from BanzaiMan/dev/feature/add_commit_script
  (dmcphers@redhat.com)
- Bug 917728 - rhc with no args should invoke setup if the express.conf file
  does not exist (ccoleman@redhat.com)
- Extra debugging was breaking output (ccoleman@redhat.com)
- Get around FakeFS bug (defunkt/fakefs#177) (asari.ruby@gmail.com)
- httpclient is too lazy for auth, sending double the number of necessary
  requests (ccoleman@redhat.com)
- add rspec test, but not working for now (misc@zarb.org)
- automatically deploy git hooks upon clone (misc@zarb.org)

* Mon Mar 04 2013 Adam Miller <admiller@redhat.com> 1.5.9-1
- Merge pull request #320 from
  smarterclayton/bug_917721_catch_exceptions_in_ssh_key_parse
  (dmcphers+openshiftbot@redhat.com)
- Bug 917721 - Don't let exceptions get raised from fingerprint tests
  (ccoleman@redhat.com)

* Mon Mar 04 2013 Adam Miller <admiller@redhat.com> 1.5.8-1
- Merge pull request #319 from
  smarterclayton/bug_917514_require_one_argument_to_authorization
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #318 from
  smarterclayton/bug_915255_track_user_preference_for_auth
  (dmcphers+openshiftbot@redhat.com)
- Bug 917514 - 'authorization delete' should require at least one token
  (ccoleman@redhat.com)
- Bug 915255 - Track auth preference in the config (ccoleman@redhat.com)
- Update reference to rubygems.org to avoid warning (asari.ruby@gmail.com)

* Fri Mar 01 2013 Adam Miller <admiller@redhat.com> 1.5.7-1
- During output, defend against exceptions caused by bad apps
  (ccoleman@redhat.com)
- Merge pull request #315 from BanzaiMan/dev/hasari/bz916122
  (dmcphers+openshiftbot@redhat.com)
- Bug 916122: Avoid misleading port-forwarding specification for MySQL.
  (asari.ruby@gmail.com)
- rhc_extended: Fixed find_application in rhc_helper (fotios@redhat.com)

* Thu Feb 28 2013 Adam Miller <admiller@redhat.com> 1.5.6-1
- Bug 916058 - Show error when auth token operation not supported
  (ccoleman@redhat.com)

* Tue Feb 26 2013 Adam Miller <admiller@redhat.com> 1.5.5-1
- Bug 913375 - Tail should be logging all carts in the head gear
  (ccoleman@redhat.com)
- Merge pull request #310 from smarterclayton/session_auth_support_2
  (dmcphers+openshiftbot@redhat.com)
- Bug 915203 - Create token directory lazily (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into session_auth_support_2
  (ccoleman@redhat.com)
- Add authorization management commands and unit tests (ccoleman@redhat.com)
- Set a better client string on new tokens (ccoleman@redhat.com)
- Merge branch 'rhc_not_sending_version' into session_auth_support_2
  (ccoleman@redhat.com)
- Bug 912606 - Guard against bad file input, fix bad md5sums
  (ccoleman@redhat.com)
- Missed coverage of token loading in clean environment (ccoleman@redhat.com)
- Bug 910442 - Write config file without quotes (ccoleman@redhat.com)
- Bug 910630 - rhc app create broken against older servers
  (ccoleman@redhat.com)
- Print out missed lines when the number is relatively low
  (ccoleman@redhat.com)
- Allow tests to be run in reverse order by fixing cleanup problems
  (ccoleman@redhat.com)
- Negotiate token auth with server and support logout (ccoleman@redhat.com)

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 1.5.4-2
- bump Release for fixed build target rebuild (admiller@redhat.com)

* Mon Feb 25 2013 Adam Miller <admiller@redhat.com> 1.5.4-1
- Add support for ruby 2.0.0-p0, needed to preferentially use zlib
  (ccoleman@redhat.com)
- Merge pull request #298 from BanzaiMan/dev/hasari/bz907742
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #308 from maxamillion/dev/admiller/new_brew_tags
  (dmcphers+openshiftbot@redhat.com)
- new brew tag (admiller@redhat.com)
- Merge pull request #303 from kraman/origin_rhel_fixes
  (dmcphers+openshiftbot@redhat.com)
- updates for rhel6.4 (admiller@redhat.com)
- Merge pull request #300 from fotioslindiakos/find_application
  (dmcphers+openshiftbot@redhat.com)
- Using stub_one_application (fotios@redhat.com)
- Converted RHC::ApplicationNotFound exception to
  RHC::Rest::ApplicationNotFound (fotios@redhat.com)
- Fix error messages to bring them in line with old values (fotios@redhat.com)
- Added options to find_application (fotios@redhat.com)
- Raise errors based on exit code (fotios@redhat.com)
- Fixed spacing for find_application calls (fotios@redhat.com)
- Changed function name and proper URI creation (fotios@redhat.com)
- Modified spec tests to use new client.find_application Added rest_spec tests
  to ensure the client is using the proper find_application (fotios@redhat.com)
- Added find_application to rest_client (fotios@redhat.com)
- Fix name of oo-register-user (kraman@gmail.com)
- Use 'localhost' exclusively for local port forwarding. (asari.ruby@gmail.com)

* Wed Feb 20 2013 Adam Miller <admiller@redhat.com> 1.5.3-1
- RHC is not sending the API version after negotiation (ccoleman@redhat.com)

* Tue Feb 19 2013 Adam Miller <admiller@redhat.com> 1.5.2-1
- Fixed spec tests for checking colors (fotios@redhat.com)

* Thu Feb 07 2013 Adam Miller <admiller@redhat.com> 1.5.1-1
- bump_minor_versions for sprint 24 (admiller@redhat.com)

* Wed Feb 06 2013 Adam Miller <admiller@redhat.com> 1.4.7-1
- Merge pull request #297 from BanzaiMan/dev/hasari/bz907742
  (dmcphers+openshiftbot@redhat.com)
- Bug 907742 (asari.ruby@gmail.com)
- Merge pull request #295 from BanzaiMan/bz903403 (dmcphers@redhat.com)
- Clean up (asari.ruby@gmail.com)
- Specs for RHC::Helpers.hosts_file_contains? (asari.ruby@gmail.com)
- Spec for Bug 903403. (asari.ruby@gmail.com)
- Tweak error message. (asari.ruby@gmail.com)
- Bug 903403 (asari.ruby@gmail.com)

* Tue Feb 05 2013 Adam Miller <admiller@redhat.com> 1.4.6-1
- Merge pull request #296 from
  smarterclayton/bug_903057_use_system_path_for_errors
  (dmcphers+openshiftbot@redhat.com)
- Bug 903057 - Use system_path for files (ccoleman@redhat.com)

* Mon Feb 04 2013 Adam Miller <admiller@redhat.com> 1.4.5-1
- Some stylistic tweaks - you don't need --dryrun because you can stub
  themethods directly.  Also fail fast on invalid arguments.
  (ccoleman@redhat.com)
- fixing tests and code so that tests will pass using dryrun
  (cdaley1981+github@gmail.com)
- making updates and writing tests for new rhc app ssh command
  (cdaley1981+github@gmail.com)
- updating rhc app ssh command code (cdaley1981+github@gmail.com)
- added rhc app ssh <app> command to ssh into application
  (cdaley1981+github@gmail.com)
- Fix cartridge steps broken by my commit (ccoleman@redhat.com)

* Fri Feb 01 2013 Adam Miller <admiller@redhat.com> 1.4.4-1
- Merge pull request #291 from
  smarterclayton/search_cartridge_names_consistently
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #290 from jtharris/jenkins_fix
  (dmcphers+openshiftbot@redhat.com)
- Allow more flexible searching (ccoleman@redhat.com)
- Search cartridge names more consistently across all commands
  (ccoleman@redhat.com)
- Removing test-unit as a dependency. (jharris@redhat.com)

* Thu Jan 31 2013 Adam Miller <admiller@redhat.com> 1.4.3-1
- Merge pull request #287 from jtharris/features/US3159
  (dmcphers+openshiftbot@redhat.com)
- Fixing infinite loop in cuke namespace check. (jharris@redhat.com)
- Removing rhc-* commands from spec. (jharris@redhat.com)
- Clearing out DNS and coverage for legacy commands. (jharris@redhat.com)
- Removing legacy rhc-* man pages. (jharris@redhat.com)
- Removing deprecated rhc- commands. (jharris@redhat.com)

* Tue Jan 29 2013 Adam Miller <admiller@redhat.com> 1.4.2-1
- Merge pull request #286 from BanzaiMan/dev/hasari/fix_rhc_extended
  (dmcphers+openshiftbot@redhat.com)
- Fix RHC Extended test failures. (asari.ruby@gmail.com)
- Match the new min for scaled php cartridge (asari.ruby@gmail.com)
- Adding back cartridge storage functionality. (jharris@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.4.1-1
- bump_minor_versions for sprint 23 (admiller@redhat.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.3.8-1
- Merge pull request #284 from BanzaiMan/bz903071
  (dmcphers+openshiftbot@redhat.com)
- Put code where they belong. (asari.ruby@gmail.com)
- Fix up specs. (asari.ruby@gmail.com)
- Don't say anything, since user expressly told us not to upload the key.
  (asari.ruby@gmail.com)
- Bug 903071: bypass test_ssh_connectivity if ssh key is not uploaded
  (asari.ruby@gmail.com)

* Wed Jan 23 2013 Adam Miller <admiller@redhat.com> 1.3.7-1
- Merge pull request #283 from smarterclayton/bug_903164_take_args_correctly
  (dmcphers+openshiftbot@redhat.com)
- Bug 903164 - Arguments with an app_context not being pulled off the stack
  (ccoleman@redhat.com)
- Bug 903071: 'rhc setup' can show unexpected error message
  (asari.ruby@gmail.com)
- Merge pull request #281 from
  smarterclayton/exit_codes_in_rhc_integration_changed
  (dmcphers+openshiftbot@redhat.com)
- Merge pull request #280 from
  smarterclayton/bug_903057_display_platform_paths_in_setup
  (dmcphers+openshiftbot@redhat.com)
- Exit code for RHC on certain errors is now 128 - update RHC integration tests
  (ccoleman@redhat.com)
- Bug 903071 - Exceptions in ssh connectivity should be caught by the server
  (ccoleman@redhat.com)
- Remove tests that are already being run implicitly, add better test coverage
  (ccoleman@redhat.com)
- Indicate which sshkeys in the list are local by color and attribute
  (ccoleman@redhat.com)
- Set a 2 minute connect timeout, and no receive/send timeouts.  Validated that
  it tolerates long delays better. (ccoleman@redhat.com)
- Ensure that FakeFS has ALT_SEPARATOR set to empty (ccoleman@redhat.com)
- Bug 895411 - Fixed improper arguments for help options (ccoleman@redhat.com)
- Bug 903057 - Show windows specific paths in the wizard (ccoleman@redhat.com)
- Merge pull request #278 from BanzaiMan/dev/hasari/us2410_followup
  (dmcphers+openshiftbot@redhat.com)
- Include coverage for the case where a test_* method raises an exception
  (asari.ruby@gmail.com)
- Tests are not fatal. (asari.ruby@gmail.com)

* Tue Jan 22 2013 Adam Miller <admiller@redhat.com> 1.3.6-1
- Merge pull request #277 from smarterclayton/us2410_move_rhc_chk
  (dmcphers+openshiftbot@redhat.com)
- Review: minor tweaks to output to clean up overall look (ccoleman@redhat.com)
- Force alphabetical order on tests to make specs pass on both 1.8 and 1.9.
  (asari.ruby@gmail.com)
- Make use of cache here (asari.ruby@gmail.com)
- Actually loop through the applications (asari.ruby@gmail.com)
- Cache applications to avoid making unnecessary API calls
  (asari.ruby@gmail.com)
- Discover tests, rather than hard coding them. (asari.ruby@gmail.com)
- Clear SSH key cache when new key is uploaded (asari.ruby@gmail.com)
- Missed this occurrence in the last commit (asari.ruby@gmail.com)
- Provide a single method to provide the cached SSH keys from the REST client
  (asari.ruby@gmail.com)
- Specs pass now (asari.ruby@gmail.com)
- Use the new REST client calls. (asari.ruby@gmail.com)
- No point in testing deprecated command. (asari.ruby@gmail.com)
- No point in covering a deprecated command with no spec.
  (asari.ruby@gmail.com)
- Deprecate 'rhc domain status' (asari.ruby@gmail.com)
- Match 'rhc-chk' output (asari.ruby@gmail.com)
- Add deprecation warning. (asari.ruby@gmail.com)
- US2410 roll 'rhc-chk checks into "rhc setup"' (asari.ruby@gmail.com)

* Mon Jan 21 2013 Adam Miller <admiller@redhat.com> 1.3.5-1
- Add support for the --from-code=<URL> parameter on application create. Show a
  default message if the broker returns a message with no text.
  (ccoleman@redhat.com)
- Merge pull request #274 from smarterclayton/use_nahi_httpclient_instead
  (dmcphers+openshiftbot@redhat.com)
- Allow app name to exist in git config, and evaluate some context helpers for
  argument positions (ccoleman@redhat.com)
- Fix remaining integration test failure (ccoleman@redhat.com)
- Bug 895000 - Ambiguous parse options should be properly displayed to users
  (ccoleman@redhat.com)
- Bug 894291 - Configuration values should be processed the same way as options
  (ccoleman@redhat.com)
- Merge branch 'master' of github.com:openshift/rhc into
  use_nahi_httpclient_instead (ccoleman@redhat.com)
- Bug 895000 - Handle configuration file path errors gracefully
  (ccoleman@redhat.com)
- Add information about the gears being used in the app in the CLI
  (ccoleman@redhat.com)
- Remove request/response debugging (use env HTTP_DEBUG=1 for that), merge
  client.spec build changes (ccoleman@redhat.com)
- Support multiple cartridges on app creation (ccoleman@redhat.com)
- tty? should be mocked true (ccoleman@redhat.com)
- Disable color if stdout is not a tty, disable paging if either stdin or
  stdout is not a tty (ccoleman@redhat.com)
- Print the client output id, replace app show --state with app show
  (ccoleman@redhat.com)
- Update mode of sshkey (ccoleman@redhat.com)
- rhc server should be lazy auth (ccoleman@redhat.com)
- Add more detail to cartridge listing, add a verbose mode, --version no longer
  responds to -v (ccoleman@redhat.com)
- Minor whitespace tweak (ccoleman@redhat.com)
- Standarize better confirmation behavior, make --noprompt fail most operations
  that require confirmation (ccoleman@redhat.com)
- Display gear count and gear sizes available during rhc setup
  (ccoleman@redhat.com)
- Add 'rhc account' If user specifies password on CLI, don't prompt again just
  display error (no interactive input) (ccoleman@redhat.com)
- Tolerate HTTPClient 2.2.1 not supporting --ssl-version by warning the user
  they cannot use that option unless they upgrade (ccoleman@redhat.com)
- Add a 'help options' command to show all global options, and improve the
  setup documentation. (ccoleman@redhat.com)
- Fetch cartridges with apps list (ccoleman@redhat.com)
- Httpclient 2.2 raises 502/401, Httpclient 2.3 does not. (ccoleman@redhat.com)
- Begin fixing spec tests, fix various real world problems as we go
  (ccoleman@redhat.com)
- Return all spec tests to passing, dramatically simplify wizard spec tests.
  (ccoleman@redhat.com)
- Premerge with master (ccoleman@redhat.com)
- Get tests back to passing, remove all old code (ccoleman@redhat.com)
- An initial httpclient implementation (ccoleman@redhat.com)
- Merge branch 'master' of github.com:openshift/rhc into
  refactor_rhc_rest_client (ccoleman@redhat.com)
- Ruby 1.8 does not appear to set a default cert store, and rest-client doesn't
  allow setting a cert_store directly.  Work around it until we investigate
  nahi/httpclient more. (ccoleman@redhat.com)
- Move arguments validation and fill to RHC::Commands (ccoleman@redhat.com)
- Serialization of config options should go through RHC::Config#save!, simplify
  wizard spec tests to depend slightly less on state, add comments around spec
  intentions, make Commander::Command::Options have a bit cleaner behavior.
  (ccoleman@redhat.com)
- Restore spec tests to 100%% coverage, remove some unused methods
  (ccoleman@redhat.com)
- Handle lambda context parameters (for lazy evaluation), reach 100%% spec
  coverage again (ccoleman@redhat.com)
- Provide a specific message for invalid protocols (ccoleman@redhat.com)
- Support client certs and ca_file being passed on command line
  (ccoleman@redhat.com)
- Remove some unused crap from base.rb (ccoleman@redhat.com)
- Allow --ssl-version to be passed on the command line, which will allow Mac
  users to bypass cert issues on some servers (ccoleman@redhat.com)
- More cleanup of client creation, remove need for globals, start simplifying
  wizard client creation, prepare for delayed auth (ccoleman@redhat.com)
- Clean up timeouts and DRY up specs (ccoleman@redhat.com)
- TarGz not autoloaded (ccoleman@redhat.com)
- Spec tests pass (ccoleman@redhat.com)
- Make auth abstractable, separate client and api, and use less poor behavior
  (ccoleman@redhat.com)

* Fri Jan 18 2013 Dan McPherson <dmcphers@redhat.com> 1.3.4-1
- Encrypt again with '-r' flag, for use with openshift/rhc
  (asari.ruby@gmail.com)
- Set up Travis uploads if spec fails (asari.ruby@gmail.com)

* Thu Jan 10 2013 Adam Miller <admiller@redhat.com> 1.3.3-1
- Update build.sh (ccoleman@redhat.com)
- Add rubygems as a build requires for gem (ccoleman@redhat.com)
- Remove rake references (ccoleman@redhat.com)
- Removing the cucumber dependency from the RPM builds (bleanhar@redhat.com)
- Merge pull request #269 from Coolhand/dev/niharvey/bug/880511
  (dmcphers+openshiftbot@redhat.com)
- fixed line 98 in lib/rhc/rest/application.rb to replace add_alias with
  remove_alias in debug output (niharvey@redhat.com)
- We should select applications and cartridges case-incensitively.
  (asari.ruby@gmail.com)
- Merge pull request #266 from
  smarterclayton/bug_889090_print_password_on_cart_addition
  (dmcphers+openshiftbot@redhat.com)
- Time.new is new for 1.9.3, use Time.local (ccoleman@redhat.com)
- Date calculation for test case has a fencepost coverage error
  (ccoleman@redhat.com)
- Styling changes per clayton's comments (fotios@redhat.com)
- Nest cartridges into applications (fotios@redhat.com)
- Time.new is new for 1.9.3, use Time.local (ccoleman@redhat.com)
- Add some spacing around the cartridge output (ccoleman@redhat.com)
- Bug 889090 - Password and other cart options should be displayed to the user
  on cart creation and on cart show. (ccoleman@redhat.com)
- Date calculation for test case has a fencepost coverage error
  (ccoleman@redhat.com)
- Don't give away the password length. (asari.ruby@gmail.com)
- Merge pull request #261 from BanzaiMan/dev/hasari/bz888100
  (openshift+bot@redhat.com)
- TarGz not autoloaded (ccoleman@redhat.com)
- Conceal password entirely. (asari.ruby@gmail.com)
- Iterate over Array as well. (asari.ruby@gmail.com)
- Fixes BZ888100. (asari.ruby@gmail.com)
- Remove debug statements from cucumber tests (ccoleman@redhat.com)
- Remove rhc-common, fix extended failure introduced by us3117
  (ccoleman@redhat.com)

* Tue Dec 18 2012 Adam Miller <admiller@redhat.com> 1.3.2-1
- Merge pull request #259 from smarterclayton/us3117_refactor_help_and_cleanup
  (openshift+bot@redhat.com)
- Merge pull request #250 from BanzaiMan/dev/hasari/bz865746
  (openshift+bot@redhat.com)
- Scaling string changes (ccoleman@redhat.com)
- Fix failing cucumber test (string change in missing cart)
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into
  us3117_refactor_help_and_cleanup (ccoleman@redhat.com)
- Merge pull request #257 from BanzaiMan/dev/hasari/bz887136
  (openshift+bot@redhat.com)
- Changing wording in cart not found exception. (jharris@redhat.com)
- In 'rhc domain', detect '--debug' and finesse args so that 'rhc-chk' can run
  in debug mode. (asari.ruby@gmail.com)
- Merge pull request #256 from fotioslindiakos/US2438_cleanup_master
  (openshift+bot@redhat.com)
- Temporarily remove cartridge storage commands from CLI (fotios@redhat.com)
- Merge pull request #247 from fotioslindiakos/BZ884636
  (openshift+bot@redhat.com)
- Fix help texts on CLI, as reported by
  https://bugzilla.redhat.com/show_bug.cgi?id=865746 (asari.ruby@gmail.com)
- Fix for BZ884636 (fotios@redhat.com)
- Bug 883725 - Allow 'jenkins' to be used as the application name
  (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into
  us3117_refactor_help_and_cleanup (ccoleman@redhat.com)
- Normalize exit trapping across commands, move up to bin/rhc level for it
  (ccoleman@redhat.com)
- Bug 883303 - Simplify how we handle SIGINT (ccoleman@redhat.com)
- Additional cleanup steps for cucumber tests (ccoleman@redhat.com)
- --debug should not --trace (ccoleman@redhat.com)
- Add back check for env (ccoleman@redhat.com)
- Tests are running again, hide --help, don't show duplicate options in help
  (ccoleman@redhat.com)
- SSHKey wizard cleanup, verify key setup works during app create
  (ccoleman@redhat.com)
- * Remove references to rhc-common from within the new CLI commands * Allow a
  global --server option * Reduce complexity in config and allow for better
  mocking * More test case simplification (ccoleman@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.3.1-1
- bump_minor_versions for sprint 22 (admiller@redhat.com)

* Wed Dec 12 2012 Adam Miller <admiller@redhat.com> 1.2.6-1
- Merge pull request #249 from jtharris/bz883725 (dmcphers@redhat.com)
- Merge pull request #248 from brenton/spec1 (openshift+bot@redhat.com)
- Removing webmock build require (bleanhar@redhat.com)
- Bug 883725 - Allow 'jenkins' to be used as the application name
  (ccoleman@redhat.com)
- Reverted 'if debug?' logic (nhr@redhat.com)
- Updated based on review feedback (nhr@redhat.com)
- Additional corrections to sshkey cucumber tests (nhr@redhat.com)
- Added keyed_user test to ensure that rhc is properly configured for snapshot
  operations (nhr@redhat.com)
- Updated test case to expect correct error code (nhr@redhat.com)
- Rebased to collect all recent cucumber work (nhr@redhat.com)
- Don't track previous namespace, just look it up the next time
  (ccoleman@redhat.com)
- Stop writing namespace to file (ccoleman@redhat.com)
- Reset $namespace when switching users, clean_application should do the same,
  better debug output (ccoleman@redhat.com)

* Fri Dec 07 2012 Adam Miller <admiller@redhat.com> 1.2.5-1
- Merge pull request #244 from jtharris/BZ_880856 (dmcphers@redhat.com)
- Merge pull request #245 from BanzaiMan/dev/hasari/bz880924
  (openshift+bot@redhat.com)
- Cleaning out version.rb rewrite in package.rake (jharris@redhat.com)
- Setting  for cucumber @cartridge_storage_user_required context
  (nhr@redhat.com)
- Added cartridge storage capability and testing to rhc (jharris@redhat.com)
- Update help text for 'port-forward' to include '<application>'.
  (asari.ruby@gmail.com)

* Thu Dec 06 2012 Adam Miller <admiller@redhat.com> 1.2.4-1
- More tweaks to extended tests (ccoleman@redhat.com)

* Wed Dec 05 2012 Adam Miller <admiller@redhat.com> 1.2.3-1
- Merge pull request #243 from maxamillion/dev/admiller/bundle_gem_build
  (ccoleman@redhat.com)
- Back to 100%% tests (ccoleman@redhat.com)
- Make env clean used keys, reset keys correctly for users
  (ccoleman@redhat.com)
- added bundle exec to build.sh (admiller@redhat.com)
- Cucumber tasks should run setup again for geared users (ccoleman@redhat.com)
- On GET requests, retry 502 proxy error exactly once (ccoleman@redhat.com)
- Loading errors and ordering (ccoleman@redhat.com)
- Error code 103 is used (ccoleman@redhat.com)
- Use a different log file so other tests don't clobber us
  (ccoleman@redhat.com)
- Merge pull request #239 from BanzaiMan/resolv_with_host_file
  (openshift+bot@redhat.com)
- Merge pull request #240 from smarterclayton/bug_883204_fix_rhc_extended_more
  (openshift+bot@redhat.com)
- Merge pull request #238 from brevilo/fix_timeout_msg
  (openshift+bot@redhat.com)
- Use Resolv::Hosts to resolve hostnames when dns is not used.
  (asari.ruby@gmail.com)
- Merge pull request #237 from anthonyfok/ask_password_chomp
  (openshift+bot@redhat.com)
- Merge pull request #209 from BanzaiMan/dev/hasari/us2773
  (openshift+bot@redhat.com)
- Bug 883204 - Fix RHC Extended actual tests (ccoleman@redhat.com)
- Update message since 'rhc app status' is deprecated (code@obock.de)
- Prevent ask_password from stripping whitespace (anthony.t.fok@gmail.com)
- Update the man page (asari.ruby@gmail.com)
- Magic data. (I mean, a missing period/full stop.) (asari.ruby@gmail.com)
- Use #bound? for more descriptive method name to check if the connection is
  bound. Instance variable name remains the same. (asari.ruby@gmail.com)
- When the application is down, the server does not return any port information
  for us to use. Detect this situation (even though we have to make another API
  call), and advise to users if the application is indeed down.
  (asari.ruby@gmail.com)
- Yeah, I removed this method. (asari.ruby@gmail.com)
- Tweak the command output slightly. (asari.ruby@gmail.com)
- Probably we should rescue problems with REST client. (asari.ruby@gmail.com)
- Clean up error messages for the failed forwarding attempts.
  (asari.ruby@gmail.com)
- No reasonable use case for @remote_host and @port_to to change.
  (asari.ruby@gmail.com)
- Be less noisy. The same information is printed above. (asari.ruby@gmail.com)
- Reformat so that indentation-based code folding works correctly.
  (asari.ruby@gmail.com)
- Refactor common code in RSpec examples. (asari.ruby@gmail.com)
- Cosmetic changes. (asari.ruby@gmail.com)
- Remove dead code and replace it with the appropriate message emitted at the
  right time. (asari.ruby@gmail.com)
- English is hard™. (asari.ruby@gmail.com)
- Set up mocks correctly to simulate an unreachable host. This caused a spec
  run to prompt for password on the Mac. (asari.ruby@gmail.com)
- Passing "self" is kludgy. (asari.ruby@gmail.com)
- I forgot to restore the "ssh" command message (asari.ruby@gmail.com)
- clean up messages somewhat (asari.ruby@gmail.com)
- Remove comments resulted from dead code (asari.ruby@gmail.com)
- Ooops. Gotta avoid infinite loop. (asari.ruby@gmail.com)
- On a second thought, we should not raise Exception here, since we are just
  iterating over port forwarding specifications, not all of them failing.
  (asari.ruby@gmail.com)
- Exit with error code, yes. (asari.ruby@gmail.com)
- Fix the expected message on non-Macs (asari.ruby@gmail.com)
- Almost 100%% code coverage (asari.ruby@gmail.com)
- Not using this to build the error messages (asari.ruby@gmail.com)
- We no longer need this exception (asari.ruby@gmail.com)
- Remove specs we do not need (asari.ruby@gmail.com)
- All specs pass now. (asari.ruby@gmail.com)
- Use info on STDERR to build port forwarding specs. (asari.ruby@gmail.com)
- Fix description (asari.ruby@gmail.com)
- Change colors so messages stand out. (asari.ruby@gmail.com)
- Tweak messages on non-Mac platforms (asari.ruby@gmail.com)
- #inspect already contains the text "forwarding" (asari.ruby@gmail.com)
- These port forwarding specs need to be rewritten. (asari.ruby@gmail.com)
- Provide means of grouping ForwardingSpecs easily. Currently, bound ones sort
  before unbounded one, and then sorted according to the service name, remote
  host name, and port. (asari.ruby@gmail.com)
- Introduce RHC::Commands::ForwardingSpec to simply port forwarding handling.
  If a local port is bound already (which is the case for a scaled app), try a
  different port. * Old code is still left behind, and some cleanup is
  necessary. (asari.ruby@gmail.com)
- Move 'mac?' to Helpers. (asari.ruby@gmail.com)
- On the Mac, port forwarding is not allowed on local machine except for the
  loopback address. https://access.redhat.com/knowledge/docs/en-
  US/OpenShift/2.0/html/User_Guide/sect-OpenShift-User_Guide-
  Application_Maintenance_Monitoring_and_Troubleshooting-
  Performing_Application_Maintenance_from_Your_Workstation.html#sect-OpenShift-
  User_Guide-Port_Forwarding (asari.ruby@gmail.com)
- Suppress warnings for unbalanced right brace '}'. (asari.ruby@gmail.com)
- While it is highly unlikely that 'list-ports' will return a line that yields
  a false positive, it is probably a good idea to defend against that
  possibility. (asari.ruby@gmail.com)
- Suspend throwing the exception while working on US2773.
  (asari.ruby@gmail.com)

* Thu Nov 29 2012 Adam Miller <admiller@redhat.com> 1.2.2-1
- Merge pull request #233 from fabianofranz/master (openshift+bot@redhat.com)
- Merge pull request #235 from
  smarterclayton/bug_876714_remove_wizard_from_general_user
  (openshift+bot@redhat.com)
- Minor tweak to output (ccoleman@redhat.com)
- explicitly seperating rake target from rake arguments as rake --trace takes
  an optional argument depending on version. (kraman@gmail.com)
- Fixing spec test (fotios@redhat.com)
- Modified warning as per Hiro's comments (fotios@redhat.com)
- Added comment related to gem commander 4.0.x issue (ffranz@redhat.com)
- Fixes BZ878407 (ffranz@redhat.com)
- Fixes for clayton's comments (fotios@redhat.com)
- Created STDERR helper to match new error messages (fotios@redhat.com)
- Made wizard not run by default, but show a message instead
  (fotios@redhat.com)
- Bug 877526 - Update message to be correct (ccoleman@redhat.com)
- When a command with a default action is shown in help, the default subcommand
  should be listed.  When a command has no default action, it should raise an
  ArgumentError showing the list of actions.  Global options should not be
  displayed when displaying a bulk command help (ccoleman@redhat.com)
- Commander 4.0.3 returns an array for all 'program :symbol' calls
  (ccoleman@redhat.com)
- Simplifications to wizard that will reduce wording (ccoleman@redhat.com)
- Merge pull request #225 from BanzaiMan/dev/hasari/bz877532
  (ccoleman@redhat.com)
- Bug 876715 - Users don't know what cart types to add. (ccoleman@redhat.com)
- Fixing message typo pointed out by BZ877532 (and then some).
  (asari.ruby@gmail.com)

* Sat Nov 17 2012 Adam Miller <admiller@redhat.com> 1.2.1-1
- bump_minor_versions for sprint 21 (admiller@redhat.com)

* Fri Nov 16 2012 Adam Miller <admiller@redhat.com> 1.1.9-1
- Merge pull request #226 from fotioslindiakos/BZ840938 (dmcphers@redhat.com)
- Fixed spec test for dns lookup (fotios@redhat.com)
- Moved host_exists to helpers and made deprecated rhc-common use it
  (fotios@redhat.com)
- Bug 876715 - Remove the additional_cartridges help which is wrong
  (ccoleman@redhat.com)
- Merge pull request #222 from fotioslindiakos/BZ874848
  (openshift+bot@redhat.com)
- Change the way the custom test runner is loaded for rhc-chk
  (fotios@redhat.com)

* Thu Nov 15 2012 Adam Miller <admiller@redhat.com> 1.1.8-1
- Address BZ868451: Display what we think are superfluous arguments. Detecting
  what the user meant as an action may be too difficult. (asari.ruby@gmail.com)
- Merge pull request #220 from fotioslindiakos/BZ840938
  (openshift+bot@redhat.com)
- Merge pull request #217 from BanzaiMan/dev/hasari/bz874027
  (openshift+bot@redhat.com)
- Merge pull request #219 from BanzaiMan/dev/hasari/bz861030
  (dmcphers@redhat.com)
- Fixing DNS resolution for hostexist? (fotios@redhat.com)
- Long overdue spec (asari.ruby@gmail.com)
- Fix BZ861030 for good. #debug is actually looked up via #method_missing, so
  #respond_to? returns nil (asari.ruby@gmail.com)
- We should not support API version 1.0 going forward. (asari.ruby@gmail.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.7-1
- Merge pull request #216 from BanzaiMan/dev/hasari/bz870891
  (openshift+bot@redhat.com)
- With Ruby19 as the default, the UTF-8 characters in the client.spec cause an
  issue with building and loading cucumber. (ccoleman@redhat.com)
- Fix Bug 870891 - User should not be prompted for authentication when running
  'rhc cartridge list' (asari.ruby@gmail.com)
- Fixes BZ876126 (ffranz@redhat.com)

* Wed Nov 14 2012 Adam Miller <admiller@redhat.com> 1.1.6-1
- Merge pull request #214 from abhgupta/agupta-dev (openshift+bot@redhat.com)
- Merge pull request #213 from fabianofranz/master (openshift+bot@redhat.com)
- specifying rake gem version range (abhgupta@redhat.com)
- Fixes BZ875373 (ffranz@redhat.com)

* Tue Nov 13 2012 Adam Miller <admiller@redhat.com> 1.1.5-1
- Add a Cucumber test to cover cartridge list (ccoleman@redhat.com)
- Bug 875878 - Show a more complete cartridge list (ccoleman@redhat.com)

* Mon Nov 12 2012 Adam Miller <admiller@redhat.com> 1.1.4-1
- Merge pull request #211 from fabianofranz/master (openshift+bot@redhat.com)
- Fixes BZ869973 (ffranz@redhat.com)

* Mon Nov 12 2012 Adam Miller <admiller@redhat.com> 1.1.3-1
- Bug 874829 - Client doesn't report a very coherent error when the server is
  dead. (ccoleman@redhat.com)

* Thu Nov 08 2012 Adam Miller <admiller@redhat.com> 1.1.2-1
- Allow specs to be run individually.  Stub sleep for jenkins so spec tests are
  fast again. (ccoleman@redhat.com)
- Spec failure when run from stdinput and without tty (ccoleman@redhat.com)
- Spec failure when running as root - user has access to all files.  Use mock
  instead. (ccoleman@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.1.1-1
- bump_minor_versions for sprint 20 (admiller@redhat.com)

* Thu Nov 01 2012 Adam Miller <admiller@redhat.com> 1.0.4-1
- Merge pull request #206 from fabianofranz/master (openshift+bot@redhat.com)
- Increased the timeout to add jenkins cartridge to app (now the same as when
  creating scaling apps) (ffranz@redhat.com)
- Increased the timeout to add jenkins cartridge to app (now the same as when
  creating scaling apps) (ffranz@redhat.com)
- Increased the timeout to add jenkins cartridge to app (now the same as when
  creating scaling apps) (ffranz@redhat.com)
- Checking for specific exit_code = 157 when adding jenkins cartridge to the
  app being created (ffranz@redhat.com)
- Checking for specific exit_code = 157 when adding jenkins cartridge to the
  app being created (ffranz@redhat.com)
- Bug 872084 - URL value lookup is not safe (ccoleman@redhat.com)
- Will display jenkins creds when jenkins cartridge is created through app
  creation (with --enable-jenkins) (ffranz@redhat.com)
- Will retry when adding the jenkins cartridge to apps created with --enable-
  jenkins (ffranz@redhat.com)
- Fixes BZ870258 (ffranz@redhat.com)

* Wed Oct 31 2012 Adam Miller <admiller@redhat.com> 1.0.3-1
- Merge pull request #203 from BanzaiMan/master (openshift+bot@redhat.com)
- Look at the Right Stuff™ to set the debug flag (asari.ruby@gmail.com)
- rhc_extended is failing because cucumber is not loading through bundler
  (ccoleman@redhat.com)
- Revert "Eradicate the class variable @@headers from the RHC::Rest::Base"
  (ccoleman@redhat.com)
- Revert "Pass @api_version, a String, here, not an Array."
  (ccoleman@redhat.com)
- Revert "Replace unsightly #set_auth_header with appropriate #merge! and
  #auth_header calls." (ccoleman@redhat.com)

* Tue Oct 30 2012 Adam Miller <admiller@redhat.com> 1.0.2-1
- Merge pull request #204 from smarterclayton/reach_100_percent_coverage
  (ccoleman@redhat.com)
- Regression in test coverage, fixing by adding tests (ccoleman@redhat.com)

* Tue Oct 30 2012 Adam Miller <admiller@redhat.com> 1.0.1-1
- bumping spec to 1.0.0 (dmcphers@redhat.com)
- BZ870334: Fixing output when adding cartridge (fotios@redhat.com)
- Merge pull request #197 from BanzaiMan/dev/hasari/bug/no_headers_class_var
  (openshift+bot@redhat.com)
- Replace unsightly #set_auth_header with appropriate #merge! and #auth_header
  calls. (asari.ruby@gmail.com)
- Pass @api_version, a String, here, not an Array. (asari.ruby@gmail.com)
- Eradicate the class variable @@headers from the RHC::Rest::Base hierarchy.
  (asari.ruby@gmail.com)

* Mon Oct 29 2012 Adam Miller <admiller@redhat.com> 0.99.14-1
- Merge pull request #196 from J5/commands-merge-master (ccoleman@redhat.com)
- add arch document (johnp@redhat.com)

* Fri Oct 26 2012 Adam Miller <admiller@redhat.com> 0.99.13-1
- Don't cleanup applications if NO_CLEAN is specified (fotios@redhat.com)
- Fixed spec syntax problem for Ruby 1.8 (fotios@redhat.com)
- Clean up applications before scenarios with @clean tag (fotios@redhat.com)
- Added more explicit output to failed app creation (fotios@redhat.com)
- Better debug output for failed app creation (fotios@redhat.com)
- Fixed parsing of cartridge show (fotios@redhat.com)
- Added cucumber tests for US2615 and fixed some errors (fotios@redhat.com)
- Added spec tests for US2615 (fotios@redhat.com)
- Added scaling support for US2615 (fotios@redhat.com)

* Wed Oct 24 2012 Adam Miller <admiller@redhat.com> 0.99.12-1
- Fixed line wrapping, will not insert a new line if last line ends with
  space(s) (ffranz@redhat.com)
- Fixed a missing require in the rest client (ffranz@redhat.com)
- Merge pull request #194 from J5/bugfix2 (openshift+bot@redhat.com)
- use length index on strings so ruby 1.8 returns a string (johnp@redhat.com)
- some wrapping fixes (johnp@redhat.com)
- Fixed spec tests for rhc snapshot restore (ffranz@redhat.com)
- Merge remote-tracking branch 'upstream/master' (ffranz@redhat.com)
- Fixes BZ 847947 (ffranz@redhat.com)
- Merge remote-tracking branch 'upstream/master' (ffranz@redhat.com)

* Mon Oct 22 2012 Adam Miller <admiller@redhat.com> 0.99.11-1
- Merge pull request #192 from calfonso/master (openshift+bot@redhat.com)
- Merge pull request #187 from
  smarterclayton/avoid_creating_conf_file_during_spec_tests
  (openshift+bot@redhat.com)
- Merge pull request #188 from BanzaiMan/dev/hasari/bz867708
  (dmcphers@redhat.com)
- BZ868119 - Need to add jbossews in the description of rhc threaddump -h
  (calfonso@redhat.com)
- Merge pull request #190 from J5/bugfix2 (openshift+bot@redhat.com)
- Merge remote-tracking branch 'origin/master' into
  avoid_creating_conf_file_during_spec_tests (ccoleman@redhat.com)
- Match the change in warning output. (asari.ruby@gmail.com)
- Invert API fetching logic so that we issue network request at most twice.
  (asari.ruby@gmail.com)
- When the versions supported by the REST Client is completely out of date,
  suggest updating and exit with error status. (asari.ruby@gmail.com)
- Fix debug command specs by looking at the correct IO object.
  (asari.ruby@gmail.com)
- Debug message should go to $stderr. (asari.ruby@gmail.com)
- Add gear size and scalable to app show output (johnp@redhat.com)
- add gear test (johnp@redhat.com)
- Ensure various configuration/filesystem resets are called
  (ccoleman@redhat.com)
- Replace FakeFS.activate! with FakeFS &block wherever possible, move
  Filesystem clear to before rather than after, delete common_spec, use a more
  predictable exit code stubbing mechanism for snapshot tests, and make sure
  wizard is using the default config when it starts. (ccoleman@redhat.com)
- setup_spec.rb was unintentionally creating config files (ccoleman@redhat.com)

* Fri Oct 19 2012 Adam Miller <admiller@redhat.com> 0.99.10-1
- Merge pull request #184 from fabianofranz/master (openshift+bot@redhat.com)
- Fixed BZ841170 (ffranz@redhat.com)
- Merge pull request #172 from fotioslindiakos/origin_cucumber
  (dmcphers@redhat.com)
- Merge pull request #189 from J5/bugfix (dmcphers@redhat.com)
- Merge pull request #185 from BanzaiMan/dev/hasari/bz861030
  (dmcphers@redhat.com)
- Updated cucumber tests to register user for origin (fotios@redhat.com)
- Fixed line wrap for single words larger than the terminal size
  (ffranz@redhat.com)
- Merge remote-tracking branch 'upstream/master' (ffranz@redhat.com)
- make sure all deprecated keys are symbols (johnp@redhat.com)
- Pass debug option to the REST client as well. (asari.ruby@gmail.com)
- Decreased the range of the string to match for a color code, improves
  performance (ffranz@redhat.com)
- Other minor readability improvements (ffranz@redhat.com)
- Fixed match method call for Ruby 1.8 (ffranz@redhat.com)
- Merge remote-tracking branch 'upstream/master' (ffranz@redhat.com)
- Improved Highline monkey patch to allow inline color codes
  (ffranz@redhat.com)
- Rebase the master branch (asari.ruby@gmail.com)
- Merge remote-tracking branch 'upstream/master' (ffranz@redhat.com)
- Fixes BZ 866530 (ffranz@redhat.com)

* Thu Oct 18 2012 Adam Miller <admiller@redhat.com> 0.99.9-1
- Merge pull request #186 from
  smarterclayton/bug_821107_allow_unknown_ssh_keys_to_be_uploaded
  (openshift+bot@redhat.com)
- Bug 821107 - Allow an unrecognizable SSH key to be uploaded
  (ccoleman@redhat.com)

* Thu Oct 18 2012 Adam Miller <admiller@redhat.com> 0.99.8-1
- These superfluous 'Accept' headers were throwing off specs on Linux.
  (asari.ruby@gmail.com)
- Tweak debug messages based on feedback. (asari.ruby@gmail.com)
- Addresses US2853. Allows REST Client to negotiate with OpenShift server which
  API version to use in order to communicate. (asari.ruby@gmail.com)
- Looks like #179 needs specs to cover the added lines. (asari.ruby@gmail.com)

* Tue Oct 16 2012 Adam Miller <admiller@redhat.com> 0.99.7-1
- Merge pull request #179 from J5/bugfix (openshift+bot@redhat.com)
- Merge pull request #180 from J5/bugfix2 (dmcphers@redhat.com)
- s/a error/an error (johnp@redhat.com)
- deprecate app cartridge alias (johnp@redhat.com)
- [bug #865909] process --version before running command (johnp@redhat.com)

* Mon Oct 15 2012 Adam Miller <admiller@redhat.com> 0.99.6-1
- BZ863937  Need update rhc app tail to rhc tail for output of rhc threaddump
  command (calfonso@redhat.com)
- Merge pull request #176 from jwhonce/dev/bz863962 (openshift+bot@redhat.com)
- Merge pull request #177 from fabianofranz/master (openshift+bot@redhat.com)
- Fixed spec tests for /openshift/rhc/pull/176 (ffranz@redhat.com)
- Fix for Bug 863962 (jhonce@redhat.com)
- Fix BZ829919: Look up defined OpenShift user name before prompting the user
  for it. (asari.ruby@gmail.com)
- Merge pull request #169 from J5/commands-merge-master
  (openshift+bot@redhat.com)
- Fixed spec tests for cartridge status (ffranz@redhat.com)
- Fixes BZ861556 (ffranz@redhat.com)
- fix geargroups mock (johnp@redhat.com)
- Change description for --state flag (johnp@redhat.com)
- switch --apache to be --state and fix output to show geargroups
  (johnp@redhat.com)
- Fixes BZ861556 (ffranz@redhat.com)
- Merge pull request #30 from BanzaiMan/dev/hasari/bz829929 (johnp@redhat.com)
- Adding tito releaser for onprem (calfonso@redhat.com)
- Fixes BZ864770 (ffranz@redhat.com)
- Spec for BZ829929. (asari.ruby@gmail.com)
- Come up with a unique name for the key name. (asari.ruby@gmail.com)
- Remove known illegal characters from the default key name we present.
  (asari.ruby@gmail.com)
- Fix BZ829929. SSH key name to be a bit more decipherable than a stripped key
  fingerprint. Leaving the fingerprint code for now, to verify that the key is
  usable. (asari.ruby@gmail.com)
- BZ863963 Unable to tail app logs via rhc tail (calfonso@redhat.com)
- Cucumber feature to confirm BZ844246. (asari.ruby@gmail.com)
- add --scaling to app man page (johnp@redhat.com)
- make noprompt help clearer and disallow using noprompt with rhc setup
  (johnp@redhat.com)
- simplify wizard by pulling proof of concept packagekit installer
  (johnp@redhat.com)
- Use the new flag-less syntax for 'rhc app create' (asari.ruby@gmail.com)
- [Bug 863915] Fix some typos in the app commands docs (johnp@redhat.com)
- Address BZ830307: suggest running 'rhc app create' when no application is
  found. (asari.ruby@gmail.com)
- Address the unclear error message pointed out by
  https://bugzilla.redhat.com/show_bug.cgi?id=860922#c3 (asari.ruby@gmail.com)
- remove some debug output (johnp@redhat.com)
- fix typos (johnp@redhat.com)
- Defaults to help action in rhc snapshot (ffranz@redhat.com)
- seperate out scaled tests and add hooks (johnp@redhat.com)
- raise a useful error when user tries to create app without a domain
  (johnp@redhat.com)
- Test the output for the case when no valid cartridges exist for the user
  (asari.ruby@gmail.com)
- Display helpful message when the app has no cartridge. (asari.ruby@gmail.com)
- fixes for cucumber tests (should now pass) (johnp@redhat.com)
- Fixes BZ861533 (ffranz@redhat.com)
- only show embedded carts in rhc (johnp@redhat.com)
- add --confirm option and deprecate -b option for app delete
  (johnp@redhat.com)
- update domain update test (johnp@redhat.com)
- update the domain man file (johnp@redhat.com)
- spec file fixes for rhc domain update (johnp@redhat.com)
- change domain update to require specifying the old domain (johnp@redhat.com)
- some small test fixes (johnp@redhat.com)
- cover rhc help invalidcommand code path (johnp@redhat.com)
- simplify tail and get 100%% spec coverage (johnp@redhat.com)
- use the new status command not the legacy in cart tests (johnp@redhat.com)
- Fix the message in spec. (asari.ruby@gmail.com)
- update tests to new api (johnp@redhat.com)
- Match spec's expectation with the REST client's message.
  (asari.ruby@gmail.com)
- Stub the default key (asari.ruby@gmail.com)
- remove some debugs puts (johnp@redhat.com)
- s/rhc-app/rhc app (johnp@redhat.com)
- remove legacy man pages (johnp@redhat.com)
- add new cartridge man file and update app man file (johnp@redhat.com)
- [bug 861540] fix listing carts by type (johnp@redhat.com)
- remove a duplicate alias (johnp@redhat.com)
- [bug 861556] special case windows exec for git clone (johnp@redhat.com)
- BZ860976 Have not the list of action in rhc alias --help
  (calfonso@redhat.com)
- US2814 Refactor RHC alias commands (calfonso@redhat.com)
- US2816 Refactor RHC tail command (calfonso@redhat.com)
- add a help method that prints out help for the active command
  (johnp@redhat.com)
- fix timeout (johnp@redhat.com)
- we don't parse globals seperatly from command options anymore
  (johnp@redhat.com)
- special case --trace option parsing (johnp@redhat.com)
- Fixes BZ 861305 (ffranz@redhat.com)
- [bug 860978] remove clash from --rhlogin option and -r on app create
  (johnp@redhat.com)
- move open4 from being a development dep to a runtime one (johnp@redhat.com)
- [Bug 861330] Fix for detecting git errors under ruby 1.8 (johnp@redhat.com)
- allow switches to be a different name from the argument they fill
  (johnp@redhat.com)
- override commander's parse_global_options to catch AmbiguousOption
  (johnp@redhat.com)
- remove another local timeout option (johnp@redhat.com)
- implement timeout as a global option (johnp@redhat.com)
- remove -t for global option --trace because it clashes with local options
  (johnp@redhat.com)
- implement reload in rest app model (johnp@redhat.com)
- implement tidy on rest app model (johnp@redhat.com)
- remove unused code (johnp@redhat.com)
- remove app from help template as it is autogenerated now (johnp@redhat.com)
- don't iterate over nil (johnp@redhat.com)
- Fixes BZ860913 (ffranz@redhat.com)
- 100%% code coverage in Wizard, to accompany the previous change.
  (asari.ruby@gmail.com)
- During 'setup', update the existing key on the account via
  RHC::Rest::Key#update. (asari.ruby@gmail.com)
- use the mocking facilities of rest_spec_helper to set up tests
  (johnp@redhat.com)
- add a way to deprecate a method, not just an alias (johnp@redhat.com)
- add status to cartridges (johnp@redhat.com)
- 100%% code coverage on Wizard. (asari.ruby@gmail.com)
- initial gear group coverage (johnp@redhat.com)
- add getting applicaiton status (johnp@redhat.com)
- add new gear_group model (johnp@redhat.com)
- pass the rest_client to the SSHWizard not the user and password
  (johnp@redhat.com)
- US2817: 100%% code coverage (ffranz@redhat.com)
- add spec test for app show (johnp@redhat.com)
- US2817: minor spec tests improvements (ffranz@redhat.com)
- US2817: better handling of snapshot sample files while running spec tests
  (ffranz@redhat.com)
- US2817: spec tests and coverage, now stubbing exit status (ffranz@redhat.com)
- US2817: spec tests and coverage (ffranz@redhat.com)
- US2817: spec tests and coverage (ffranz@redhat.com)
- Remove #stub_user_info from the Wizard mock. (asari.ruby@gmail.com)
- DRY up namespace definitions. (asari.ruby@gmail.com)
- Rather than testing the procedure to set up the SSH keys locally in the RSpec
  execution environment, assume that the key exists already, so that the output
  is accurately compared. (asari.ruby@gmail.com)
- Fix up what Highline should get to get the spec to pass.
  (asari.ruby@gmail.com)
- Tweak the stubbing method to allow stubbing of applications that have no
  public URLs. (asari.ruby@gmail.com)
- Stub a domain and applications simultaneously. (asari.ruby@gmail.com)
- Set up mock RHC::Rest::Domain object through REST client.
  (asari.ruby@gmail.com)
- make output look nicer for rhc app create (johnp@redhat.com)
- Modified proxy parsing in rhc-common.rb (fotios@redhat.com)
- deprecate rhc-app and related binaries (johnp@redhat.com)
- Stub Wizard#get_preferred_key_name here. I'm actually having a hard time
  actually stubbing a minimally appropriate method here; the subsequent
  "$terminal.write_line" 'yes' in this situation should result in accepting
  'default' as the key name, so stub that instead as a compromise.
  (asari.ruby@gmail.com)
- Stub REST client call. (asari.ruby@gmail.com)
- Somehow stubbing here is not working. Changed the output to match, since the
  existing matchers test what the stub should return, but the output from the
  wizard. (asari.ruby@gmail.com)
- Stub REST client (asari.ruby@gmail.com)
- Stub correct object. (asari.ruby@gmail.com)
- add app show and use the app output helper in domain (johnp@redhat.com)
- add an output helper for shared output (johnp@redhat.com)
- Fixed variable used for creating scaled apps (fotios@redhat.com)
- test deprecated options (johnp@redhat.com)
- 100%% app command spec coverage (johnp@redhat.com)
- test jenkins enablement under various conditions (johnp@redhat.com)
- be more specific which error we are looking for in spec tests
  (johnp@redhat.com)
- use Kernel.sleep instead of sleep so we can stub it out to speed tests
  (johnp@redhat.com)
- add application create spec tests (johnp@redhat.com)
- US2817: minor adjustments (ffranz@redhat.com)
- US2817: improved wording (ffranz@redhat.com)
- US2817: added basic structure for rhc app snapshot spec tests
  (ffranz@redhat.com)
- US2817: refactored rhc snapshot restore (ffranz@redhat.com)
- US2817: refactored rhc snapshot save (ffranz@redhat.com)
- US2817: deprecated rhc-snapshot, created basic refactoring structure
  (ffranz@redhat.com)
- fix some spec tests failing due to internal changes (johnp@redhat.com)
- add mock user class and have wizard spec use the rest_spec_helper mock
  classes (johnp@redhat.com)
- some cleanup for option deprecation (johnp@redhat.com)
- DRY up #find_key between RHC::Rest::Client and RHC::Rest::User.
  (asari.ruby@gmail.com)
- Removing intermediate local variable and avoiding shadowing outer-scope
  variable with the block-local one. (asari.ruby@gmail.com)
- Rename fingerprint_for helper as fingerprint_for_local_key.
  (asari.ruby@gmail.com)
- Created deprecated context for command line options (fotios@redhat.com)
- DRYed up functionality for alerting users of deprecated commands and optoins
  (fotios@redhat.com)
- Eradicate remaining non-REST calls. (asari.ruby@gmail.com)
- split up the windows dns fallback methods for testing purposes
  (johnp@redhat.com)
- set config.password when getting the password from user input
  (johnp@redhat.com)
- print out the messages from the server when creating app (johnp@redhat.com)
- add rhc app tidy (johnp@redhat.com)
- contain server messages in rest models instead of passing as a seperate hash
  (johnp@redhat.com)
- enable code coverage here (asari.ruby@gmail.com)
- Move SSH key file loading and fingerprint computation to ssh_key_helpers.
  (asari.ruby@gmail.com)
- Revert "Move #find_key closer to other SSH key methods."
  (asari.ruby@gmail.com)
- No local variable is necessary. (asari.ruby@gmail.com)
- Raise these exceptions here, so that refactoring (in the future) can work
  better. (asari.ruby@gmail.com)
- 100%% code coverage in wizard.rb. (asari.ruby@gmail.com)
- Move SSH key display format to a single location. (asari.ruby@gmail.com)
- This spec needs fingerprints. (asari.ruby@gmail.com)
- Revert "Under some circumstances, RestClient may fail to connect to the
  OpenShift server. (I observed this with MRI 1.9.3 on Mac OS X 10.8.1.)"
  (asari.ruby@gmail.com)
- #set_expected_key_name_and_action was used for differentiating 'update' and
  'add' for SSH key management during the workflow. This is no longer
  supported. (asari.ruby@gmail.com)
- Move #find_key closer to other SSH key methods. (asari.ruby@gmail.com)
- Shortcut the spec logic by returning 'true'. (asari.ruby@gmail.com)
- One more usage of RHC.get_ssh_keys to be removed. (asari.ruby@gmail.com)
- RHC::Wizard#ssh_key_upload? no longer triggers #ssh_keygen_fallback unless
  keys exist for the REST client. (asari.ruby@gmail.com)
- Under some circumstances, RestClient may fail to connect to the OpenShift
  server. (I observed this with MRI 1.9.3 on Mac OS X 10.8.1.)
  (asari.ruby@gmail.com)
- In Wizard#ssh_keygen_fallback, return correct value. (asari.ruby@gmail.com)
- More fixes in Specs. (asari.ruby@gmail.com)
- Starting work on US2872. Streamline 'rhc setup' workflow using the new REST
  API. (asari.ruby@gmail.com)
- initial app tests (johnp@redhat.com)
- update mock classes for rhc app tests (johnp@redhat.com)
- make sure commands return 0 (johnp@redhat.com)
- add ability to send input with spec_helper run command (johnp@redhat.com)
- add tests for app uuid context (johnp@redhat.com)
- dry and othewise cleanup the rest modules (johnp@redhat.com)
- add context helper spec tests (johnp@redhat.com)
- spec test fixes (johnp@redhat.com)
- more spec test fixes (johnp@redhat.com)
- fix tests for methods with underscore as underscore now turns into dash
  (johnp@redhat.com)
- add app start, stop, force-stop, restart, reload (johnp@redhat.com)
- cartridge - switch to using the cartridge helper (johnp@redhat.com)
- apps - use cartridge helper to find cartridges based on regex
  (johnp@redhat.com)
- properly handle types in the rest_client find_cartridges method
  (johnp@redhat.com)
- move find_cartridge to a helper so the app command can use it
  (johnp@redhat.com)
- add cartridge show command for showing properties of a cartridge
  (johnp@redhat.com)
- dry up cartridge regex search and add display for cartridge properties
  (johnp@redhat.com)
- add a multiple cartridge exception (johnp@redhat.com)
- add regex matching for application cartridges (johnp@redhat.com)
- dry up some of teh cartridge commands (johnp@redhat.com)
- remove legacy command code path from rhc binary (johnp@redhat.com)
- add app delete command (johnp@redhat.com)
- minor fixups and nicer output for app commands (johnp@redhat.com)
- move git code into a git helper (johnp@redhat.com)
- fixed some typos and add debug spew to app context (johnp@redhat.com)
- use the uuid in the git config to fill in the app context (johnp@redhat.com)
- add git-clone action; configure git repo and ssh keys (johnp@redhat.com)
- get host from rest application model (johnp@redhat.com)
- allow multiline descriptions (johnp@redhat.com)
- when adding command transform underscores in method names to dashes
  (johnp@redhat.com)
- provide the host from the rest model (johnp@redhat.com)
- almost complete first pass implementation of rhc app create
  (johnp@redhat.com)
- modify the find_application method to search based on cartridge
  (johnp@redhat.com)
- add GitException class (johnp@redhat.com)
- add constants to the helper (johnp@redhat.com)
- fix syntax (johnp@redhat.com)
- we really need a debug output helper so people don't use if @debug
  (johnp@redhat.com)
- framework for app create command (johnp@redhat.com)
- remove noprompt from config since we just use the option (johnp@redhat.com)
- fixes missed in merge (johnp@redhat.com)
- add back noprompt which was lost in merge (johnp@redhat.com)
- have integration tests test the new cartridge api (johnp@redhat.com)
- 100%% spec coverage for cartridge command (johnp@redhat.com)
- spec test cartridge start, stop, restart and reload (johnp@redhat.com)
- add the ability to deprecate interfaces (johnp@redhat.com)
- implemented cartridge start, stop, restart, reload, remove (johnp@redhat.com)
- implement find_cartridge for the rest application model (johnp@redhat.com)
- stub out cartridge commands with metadata and add deprecated to aliases
  (johnp@redhat.com)
- Revert "remove cartridge spec so we can merge with master" (johnp@redhat.com)
- Revert "remove cartridge for now so that the infrastructure can be marged"
  (johnp@redhat.com)

* Thu Oct 04 2012 Adam Miller <admiller@redhat.com> 0.99.5-1
- Merge pull request #171 from mrunalp/dev/typeless (dmcphers@redhat.com)
- Fix for BZ 861067. (mpatel@redhat.com)
- Fix for BZ 861047. (mpatel@redhat.com)

* Wed Oct 03 2012 Adam Miller <admiller@redhat.com> 0.99.4-1
- Merge pull request #167 from J5/bugfix (openshift+bot@redhat.com)
- Merge pull request #165 from BanzaiMan/fix-commit-6dffb48
  (openshift+bot@redhat.com)
- seperate out scaled tests and add hooks (johnp@redhat.com)
- add cucumber tests for scalable apps (johnp@redhat.com)
- contain server messages in rest models instead of passing as a seperate hash
  (johnp@redhat.com)
- Ensure that there is at least one SSH key exists for the account before
  running "rhc sshkey list". (asari.ruby@gmail.com)
- Avoid bombing on systems that do not have /root. (asari.ruby@gmail.com)

* Wed Sep 26 2012 Adam Miller <admiller@redhat.com> 0.99.3-1
- BZ858144 Lost threaddump help doc in man rhc (calfonso@redhat.com)

* Thu Sep 20 2012 Adam Miller <admiller@redhat.com> 0.99.2-1
- Updated rhc cucumber tests (fotios@redhat.com)
- Merge pull request #161 from calfonso/master (openshift+bot@redhat.com)
- Fix Bug 856876 - Caught unexpected error messages when adding an sshkey with
  private key (asari.ruby@gmail.com)
- US2815: Refactor RHC threaddump command (calfonso@redhat.com)

* Wed Sep 12 2012 Adam Miller <admiller@redhat.com> 0.99.1-1
- bump_minor_versions for sprint 18 (admiller@redhat.com)
- Merge pull request #160 from BanzaiMan/us2600_followup
  (openshift+bot@redhat.com)
- Remove "rhc sshkey update" altogether. (asari.ruby@gmail.com)
- "sshkey update" is "removed", not "deprecated". (asari.ruby@gmail.com)
- Also catch Net::SSH::Exception (asari.ruby@gmail.com)
- Remove mention of "update" from rhc-sshkey(1). (asari.ruby@gmail.com)
- Remove mention of "rhc sshkey update" from "rhc sshkey help".
  (asari.ruby@gmail.com)
- Add Cucumber test for the case where an invalid SSH public key is added.
  (asari.ruby@gmail.com)
- Add spec for the case for the invalid key addition. We validate before
  sending it to the server. (asari.ruby@gmail.com)

* Wed Sep 12 2012 Adam Miller <admiller@redhat.com> 0.98.15-1
- Avoid warnings when these steps run. (asari.ruby@gmail.com)
- Merge pull request #156 from nhr/BZ856038 (openshift+bot@redhat.com)
- Capture stderr output from git clone (jhonce@redhat.com)
- Merge pull request #157 from J5/bugfix-port-forward
  (openshift+bot@redhat.com)
- [Bug #856202] catch Errno::EADDRINUSE and Errno::EADDRNOTAVAIL
  (johnp@redhat.com)
- BZ856038 - Updated gemspec to require earliest compatible version of Net::SSH
  (hripps@redhat.com)

* Tue Sep 11 2012 Troy Dawson <tdawson@redhat.com> 0.98.14-1
- Merge pull request #155 from J5/bugfix (openshift+bot@redhat.com)
- Merge pull request #153 from BanzaiMan/rhc-sshkey-cucumber-features
  (openshift+bot@redhat.com)
- move set_terminal to bin/rhc and add FIXME comment (johnp@redhat.com)
- [Bug #856056] make sure set_terminal is called and disable color for windows
  (johnp@redhat.com)
- Merge pull request #154 from J5/bugfix (openshift+bot@redhat.com)
- Block args handling is slightly different in MRI 1.9.3; *args are wrapped in
  an Array, so that #to_s ends up with something weird under some
  circumstances. (asari.ruby@gmail.com)
- another spot where we weren't catching the sshkey error (johnp@redhat.com)
- Cucumber features for "rhc sshkey" (asari.ruby@gmail.com)

* Mon Sep 10 2012 Dan McPherson <dmcphers@redhat.com> 0.98.13-1
- Merge pull request #149 from fabianofranz/dev/ffranz/refactor/port-forward
  (openshift+bot@redhat.com)
- Fixed rhc sshkey to use the new command lookup defaults (ffranz@redhat.com)
- Changed --app from option to argument in rhc port-forward (ffranz@redhat.com)
- Styling fixes to the rhc port-forward command, as suggested
  (ffranz@redhat.com)
- US2833: added rspec tests to fix coverage (ffranz@redhat.com)
- US2833: deprecated rhc-port-forward command (ffranz@redhat.com)
- US2833 - added spec tests for port forward, new default object_name for
  commands, improved wording (ffranz@redhat.com)
- US2833: moved port-forward to new command structure (ffranz@redhat.com)

* Mon Sep 10 2012 Troy Dawson <tdawson@redhat.com> 0.98.12-1
- 

* Mon Sep 10 2012 Troy Dawson <tdawson@redhat.com> 0.98.11-1
- US2600: [Debt] Refactor RHC key commands (asari.ruby@gmail.com)

* Fri Sep 07 2012 Adam Miller <admiller@redhat.com> 0.98.10-1
- Merge pull request #151 from J5/bugfix (openshift+bot@redhat.com)
- Merge pull request #150 from J5/add_deprecated_aliases
  (openshift+bot@redhat.com)
- use encode64().delete("\n") since b64encode prints to stdout
  (johnp@redhat.com)
- rhc version.rb bump (admiller@redhat.com)
- some cleanups for deprecated aliases (johnp@redhat.com)
- spec test to test deprecation framework (johnp@redhat.com)
- add the ability to deprecate interfaces (johnp@redhat.com)

* Thu Sep 06 2012 Adam Miller <admiller@redhat.com> 0.98.9-1
- Merge pull request #148 from J5/bugfix (openshift+bot@redhat.com)
- ruby 1.8 still requires us to strip off the last \n for b64encode
  (johnp@redhat.com)
- fix tests by setting the correct user agent (johnp@redhat.com)
- use version paths to call the correct base64 method (johnp@redhat.com)
- rhc version.rb bump (admiller@redhat.com)
- [bug 854152] make sure we don't have newlines in base64 auth encoding
  (johnp@redhat.com)

* Tue Sep 04 2012 Adam Miller <admiller@redhat.com> 0.98.8-1
- rhc version.rb bump (admiller@redhat.com)

* Tue Sep 04 2012 Adam Miller <admiller@redhat.com> 0.98.7-1
- Merge pull request #144 from
  smarterclayton/us2819_cleanup_layout_and_refactor (openshift+bot@redhat.com)
- Version loading won't work for old commands (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into
  us2819_cleanup_layout_and_refactor (ccoleman@redhat.com)
- Modified output message to reflect the config file name that was actually
  created. (hripps@redhat.com)
- Remove --noprompt from ARGV for legacy commands (ccoleman@redhat.com)
- Make the application layout more consistent with the console
  (ccoleman@redhat.com)
- Removed extra line from README (fotios@redhat.com)
- Updated features/README.md (fotios@redhat.com)
- Update features/README.md (fotioslindiakos@gmail.com)
- Updated README (fotios@redhat.com)
- Modified support/env.rb to automatically try to reuse values stored in
  /tmp/rhc if NO_CLEAN is set (fotios@redhat.com)
- Modified features/support/env.rb to take care of setting up required
  environment (fotios@redhat.com)
- Fixing hooks and assumptions (fotios@redhat.com)
- Fixed background/hooks for applications (fotios@redhat.com)
- Added QUIET env variable to suppress initialization output during Jenkins
  tests (fotios@redhat.com)
- Moved constant declarations to rhc_helper to prevent duplicates
  (fotios@redhat.com)
- Commented out some unimplemented features (fotios@redhat.com)
- Changed background for multiple cartridges features (fotios@redhat.com)
- Moved searching options to persitable (fotios@redhat.com)
- DRY up accessible checks for multiple apps (fotios@redhat.com)
- DRYed up cartridge steps (fotios@redhat.com)
- Rearranged application scenario steps to be more logical, but also run
  individually (fotios@redhat.com)
- Modified application steps to use transform for expectations
  (fotios@redhat.com)
- Fixing some hooks (fotios@redhat.com)
- Refactored features to re-run @init code if run independently
  (fotios@redhat.com)
- Refactoring cucumber tests (fotios@redhat.com)
- rhc version.rb bump (admiller@redhat.com)

* Thu Aug 30 2012 Adam Miller <admiller@redhat.com> 0.98.6-1
- rhc version bump (admiller@redhat.com)
- remove autocomplete rake task for now (johnp@redhat.com)

* Thu Aug 30 2012 Adam Miller <admiller@redhat.com> 0.98.5-1
- version bump for rhc (admiller@redhat.com)

* Tue Aug 28 2012 Adam Miller <admiller@redhat.com> 0.98.4-1
- Merge pull request #137 from BanzaiMan/dev/hasari/feature-color-spec-output
  (openshift+bot@redhat.com)
- Merge pull request #140 from J5/command-refactor (openshift+bot@redhat.com)
- Merge pull request #138 from fotioslindiakos/jenkins_rhc_tests
  (openshift+bot@redhat.com)
- add spec test for deleting a domain with applications (johnp@redhat.com)
- Minor spec bug (ccoleman@redhat.com)
- Readd nocov, J5 to add it separately (ccoleman@redhat.com)
- Fix puts in ssh_key_helpers (ccoleman@redhat.com)
- Merge remote-tracking branch 'origin/master' into integration
  (ccoleman@redhat.com)
- Fix refactor spec tests (ccoleman@redhat.com)
- Merge pull request #133 from smarterclayton/move_rhc_rest_to_proper_namespace
  (ccoleman@redhat.com)
- Merge pull request #120 from J5/command-refactor (ccoleman@redhat.com)
- 100%% spec coverage (johnp@redhat.com)
- assign config and options outside the constructor (johnp@redhat.com)
- remove spec changes for domain update to reflect the revert
  (johnp@redhat.com)
- remove cartridge spec so we can merge with master (johnp@redhat.com)
- Revert "update 'domain update' to use old_domain as a context arg"
  (johnp@redhat.com)
- remove cartridge for now so that the infrastructure can be marged
  (johnp@redhat.com)
- Changed begin/retry to use loop to satisfy changes for 1.9 Moved redirect
  logic outside of timeout to prevent original timeout from killing recursion
  Added redirect depth check (fotios@redhat.com)
- Update features/README.md (fotioslindiakos@gmail.com)
- Added information for bypassing SSH to the README (fotios@redhat.com)
- Fixed Domain create step (fotios@redhat.com)
- Modified HTTP request code (fotios@redhat.com)
- Modified test for deleted applications (fotios@redhat.com)
- Require ActiveSupport::OrderedHash for cucumber (fotios@redhat.com)
- Added SSH wrapper so we can ignore host authenticity checking during Jenkins
  tests (fotios@redhat.com)
- Create ~/.openshift directory before tests if it doesn't exist
  (fotios@redhat.com)
- rhc version bump (admiller@redhat.com)
- Move "--color" option to a file that is read by "(r)spec". This will allow
  "bundle exec spec …" to pick up "--color" without having to type it every
  time. (asari.ruby@gmail.com)
- Leave FIXME on domain.destroy catch exception (ccoleman@redhat.com)
- Remove command_runner.rb, should be in another branch (ccoleman@redhat.com)
- Move Rhc::Rest to proper RHC::Rest package (ccoleman@redhat.com)
- fix spec issues from rebase (johnp@redhat.com)
- revert overzealous code removal (johnp@redhat.com)
- remove spec tests since we removed contextual args (johnp@redhat.com)
- commit rake task that runs the autocomplete generator (johnp@redhat.com)
- refactor autocomplete as a script generation tool (johnp@redhat.com)
- readd requires which got lost in rebase (johnp@redhat.com)
- remove rhc and autocommit from args list in autocomplete (johnp@redhat.com)
- move autocomplete out of stream of the regular commands (johnp@redhat.com)
- improvements to autocomplete (johnp@redhat.com)
- initial commit of the hidden autocomplete command (johnp@redhat.com)
- hide any commands which don't have a summary (johnp@redhat.com)
- refactor context arguments as options and implement lists (johnp@redhat.com)
- indent fix (johnp@redhat.com)
- clean up arg fill loop by using reverse.each_with_index (johnp@redhat.com)
- add the actual cartridge tests to get 100%% spec test coverage
  (johnp@redhat.com)
- 100%% spec coverage on carts (johnp@redhat.com)
- add spec tests for argument fill and validation (johnp@redhat.com)
- fix broken spec tests (johnp@redhat.com)
- rename find_cartridge to find_cartridges since it returns an array
  (johnp@redhat.com)
- add new cartridge command (johnp@redhat.com)
- update 'domain update' to use old_domain as a context arg (johnp@redhat.com)
- add context argument processing (johnp@redhat.com)
- enable finding cartridges via a regex (johnp@redhat.com)
- add the ability to alias a command as a root command (johnp@redhat.com)

* Thu Aug 23 2012 Adam Miller <admiller@redhat.com> 0.98.3-1
- rhc version bump (admiller@redhat.com)

* Thu Aug 23 2012 Adam Miller <admiller@redhat.com> 0.98.2-1
- version bump for rhc (admiller@redhat.com)

* Wed Aug 22 2012 Adam Miller <admiller@redhat.com> 0.98.1-1
- bump_minor_versions for sprint 17 (admiller@redhat.com)
- rhc version bump (admiller@redhat.com)
- Merge pull request #136 from BanzaiMan/dev/hasari/tar_output_devnull
  (openshift+bot@redhat.com)
- Add a missing space (asari.ruby@gmail.com)
- Further cleanup of targz.rb. (asari.ruby@gmail.com)

* Wed Aug 22 2012 Adam Miller <admiller@redhat.com> 0.97.16-1
- bump rhc version (admiller@redhat.com)
- Merge pull request #134 from rmillner/dev/rmillner/BZ850544
  (openshift+bot@redhat.com)
- Merge pull request #135 from J5/bugfix (dmcphers@redhat.com)
- Merge pull request #132 from fabianofranz/master (dmcphers@redhat.com)
- [Bug 850697] catch another exception that may result from an invalid key
  (johnp@redhat.com)
- Merge pull request #130 from BanzaiMan/dev/hasari/tar_output_devnull
  (openshift+bot@redhat.com)
- Include monitoring URL in list of printed entities. (rmillner@redhat.com)
- Fixes BZ 849769 (ffranz@redhat.com)
- Send only STDERR to /dev/null. (asari.ruby@gmail.com)
- When calling "(gnu)tar" via shell, send output to /dev/null, so that when the
  tar file doesn not contain the file we are looking for, the error message
  does not seep through to the output. (asari.ruby@gmail.com)
- General cleanup. Replace hard tabs with spaces, and replace "smart" quotes.
  (asari.ruby@gmail.com)
- Fixes BZ 849769 (ffranz@redhat.com)

* Tue Aug 21 2012 Adam Miller <admiller@redhat.com> 0.97.15-1
- Merge pull request #128 from nhr/BZ844025 (openshift+bot@redhat.com)
- Modified regex for searching the embedded hash (nhr@redhat.com)
- BZ844025 - Temporary fix for missing functionality in rhc-port-forward
  (nhr@redhat.com)

* Tue Aug 21 2012 Adam Miller <admiller@redhat.com> 0.97.14-1
- Merge pull request #126 from J5/bugfix (openshift+bot@redhat.com)
- rhc version bump (admiller@redhat.com)
- [Bug 847685] seperate connection errors from timeouts (johnp@redhat.com)
- [Bug 847723] Get jenkins url (johnp@redhat.com)

* Mon Aug 20 2012 Adam Miller <admiller@redhat.com> 0.97.13-1
- rhc version bump wasn't pushed ... need to figure out why
  (admiller@redhat.com)

* Fri Aug 17 2012 Adam Miller <admiller@redhat.com> 0.97.12-1
- bump rhc version (admiller@redhat.com)
- Merge pull request #125 from J5/bugfix (openshift+bot@redhat.com)
- fix spec test mock rest classes so they inherit from actual classes
  (johnp@redhat.com)
- [bug 847723] have cartridge model handle propery access better
  (johnp@redhat.com)
- Bug 848262 - Alias are not shown when using rhc domain show
  (lnader@redhat.com)

* Thu Aug 16 2012 Adam Miller <admiller@redhat.com> 0.97.11-1
- bump version for rhc (admiller@redhat.com)
- [Bug 848619] Let user know they need to update configs (johnp@redhat.com)
- suggest rhc domain 'update' instead of 'alter' (johnp@redhat.com)
- [Bug 848611] check for cartridge_url is not nil (johnp@redhat.com)

* Wed Aug 15 2012 Adam Miller <admiller@redhat.com> 0.97.10-1
- 

* Wed Aug 15 2012 Adam Miller <admiller@redhat.com> 0.97.9-1
- Merge branch 'master' of github.com:openshift/rhc (admiller@redhat.com)
- Correct punctuation in client.spec (ccoleman@redhat.com)

* Wed Aug 15 2012 Adam Miller <admiller@redhat.com> 0.97.8-1
- 

* Wed Aug 15 2012 Adam Miller <admiller@redhat.com>
- 

* Wed Aug 15 2012 Adam Miller <admiller@redhat.com> 0.97.7-1
- regex fix from git - match on word boundry (johnp@redhat.com)
- Clean up error strings (johnp@redhat.com)
- update adding commands doc (johnp@redhat.com)
- add results formatting block so results are alway consistent
  (johnp@redhat.com)
- [Bug 847685] Raise default timeout for domain update and implement --timeout
  (johnp@redhat.com)
- [Bug 847719] Remove the suggestion to use --force from domain delete output
  (johnp@redhat.com)
- [Bug 847723] - show connection url for carts in domain show
  (johnp@redhat.com)

* Mon Aug 13 2012 Adam Miller <admiller@redhat.com> 0.97.6-1
- 

* Fri Aug 10 2012 Adam Miller <admiller@redhat.com> 0.97.5-1
- micro version bump, should have been auto-committed. will follow up
  (admiller@redhat.com)
- Refactor find methods to either return one value or raise an exception
  (johnp@redhat.com)
- some feature test fixes (johnp@redhat.com)
- fix tests as RESULTS: became RESULT: in output (johnp@redhat.com)
- make output more consistent umong commands (johnp@redhat.com)
- output a RESULTS: block like other commands (johnp@redhat.com)
- switch to raising an excpetion instead of exiting in config
  (johnp@redhat.com)
- rename as domains since it is an array (johnp@redhat.com)
- scope the exitcode correctly (johnp@redhat.com)
- some fixes to merge errors (johnp@redhat.com)
- correct logic for when we need to install bigdecimal gem (johnp@redhat.com)
- make gemfile work with ruby 1.8 (johnp@redhat.com)
- global options argument format change missed in rebase (johnp@redhat.com)
- fix the error code where the issue is and revert the last change
  (johnp@redhat.com)
- fix expected error code (johnp@redhat.com)
- add feature tests (johnp@redhat.com)
- if callback is present have it handle the return code (johnp@redhat.com)
- make rhc domain destroy an alias to rhc domain delete (johnp@redhat.com)
- suppress aliases from help output (johnp@redhat.com)
- add a test for the alter alias (johnp@redhat.com)
- add aliasing functionality and alias domain alter to domain update
  (johnp@redhat.com)
- remove exceptions handled by rest api and add DomainNotFoundException
  (johnp@redhat.com)
- move config code to commander.rb instead of in the individual commands
  (johnp@redhat.com)
- add rhc domain and rhc domain show checks (johnp@redhat.com)
- fix up cucumber tests and add domain alter steps (johnp@redhat.com)
- reset config before tests (johnp@redhat.com)
- use internal config (johnp@redhat.com)
- add doc section on using default_action (johnp@redhat.com)
- refactor wizard to take a config object (johnp@redhat.com)
- add default_action class method to allow aliasing methods as default
  (johnp@redhat.com)
- deprecate domain binaries as rhc domain is the one true interface now
  (johnp@redhat.com)
- refactor when we run the first run wizard (johnp@redhat.com)
- 100%% spec coverage (johnp@redhat.com)
- handle generic exceptions (johnp@redhat.com)
- correctly handle help on error and run with our Runner instance on tests
  (johnp@redhat.com)
- use correct help formatter when error occures (johnp@redhat.com)
- remove another usage of command_success (johnp@redhat.com)
- fix spec tests to reflect string changes (johnp@redhat.com)
- small fixes (johnp@redhat.com)
- remove use of command_success and just return 0 (johnp@redhat.com)
- if help is passed in run as if --help was passed in (johnp@redhat.com)
- refactor override Runner.run! for handling error conditions
  (johnp@redhat.com)
- let commander handle rhc help (johnp@redhat.com)
- clean up domain command a bit (johnp@redhat.com)
- fix documentation to be linked from toplevel README.md and renamed
  (johnp@redhat.com)
- cleanups (johnp@redhat.com)
- use headline style in section output (johnp@redhat.com)
- simplify code block (johnp@redhat.com)
- style fix (johnp@redhat.com)
- simplify metadata identifiers (johnp@redhat.com)
- Only flatten 1 level since OptionParser syntax allows for lists
  (johnp@redhat.com)
- fix options to take a list of switches for future functionality
  (johnp@redhat.com)
- add a readme on how to add commands (johnp@redhat.com)
- check length because diffent ruby versions order options differently
  (johnp@redhat.com)
- run true without a path as different test systems may install it elsewhere
  (johnp@redhat.com)
- remove some spaces before parens to supress warnings (johnp@redhat.com)
- add the domain spec tests (missed this) (johnp@redhat.com)
- fix the application model to expose git and app url (johnp@redhat.com)
- get spec tests at 100%% for new commander domain code (johnp@redhat.com)
- make sure wizard is either suppresed or mocked (johnp@redhat.com)
- add new tests to check error conditions (johnp@redhat.com)
- don't filter out help formatter in coverage test anymore (johnp@redhat.com)
- check that objects are accessable when printing out help (johnp@redhat.com)
- fix error reporting (johnp@redhat.com)
- correctly pass in params as *args (johnp@redhat.com)
- remove some whitespace (johnp@redhat.com)
- suppress wizard and other little test fixes (johnp@redhat.com)
- add global options output to help (johnp@redhat.com)
- rename success to command_success so it doesn't clash with the highline
  helper (johnp@redhat.com)
- send it correct default options object and add noprompt global option
  (johnp@redhat.com)
- handle outputting traces better (johnp@redhat.com)
- fix race in tests where auth is not yet set up correctly (johnp@redhat.com)
- suppress wizard for rhc server since you don't need a login
  (johnp@redhat.com)
- default to show for rhc domain (johnp@redhat.com)
- add debug option and fix domain creation (johnp@redhat.com)
- fix test to reflect fixed cart status output when cart is not added
  (johnp@redhat.com)
- revert modification that mistakenly got checked in (johnp@redhat.com)
- port rhc domain destroy to rest api (johnp@redhat.com)
- hook rhc domain status back up (johnp@redhat.com)
- minor string fixups (johnp@redhat.com)
- fix error invokation (johnp@redhat.com)
- port rhc domain create to the rest api (johnp@redhat.com)
- port rhc domain alter to rest (johnp@redhat.com)
- remove help handler in setup command as we handle it generically now
  (johnp@redhat.com)
- hook up domain show to rest apis (johnp@redhat.com)
- handle errors gracefully (johnp@redhat.com)
- fix typo (johnp@redhat.com)
- improve the help output for commands (johnp@redhat.com)
- handle help for all commands (johnp@redhat.com)
- refactor metadata vars to be more descriptive (johnp@redhat.com)
- remove -c global option for config since legacy uses that for cartridge
  (johnp@redhat.com)
- Stub out domain command and handle argument and options processing
  (johnp@redhat.com)
- only show rhc usage for top level commands (johnp@redhat.com)
- initial stub of the domain command (johnp@redhat.com)
- run wizard on initialize not on run (johnp@redhat.com)
- run setup wizard if needed also allow commands to suppress the wizard
  (johnp@redhat.com)
- handle invalid commands via commander's help formatter (johnp@redhat.com)
- make sure the erb files get installed (johnp@redhat.com)
- add help templates for usage (johnp@redhat.com)

* Wed Aug 08 2012 Adam Miller <admiller@redhat.com> 0.97.4-1
- 

* Tue Aug 07 2012 Adam Miller <admiller@redhat.com> 0.97.3-1
- Bug 845171 - Was returning too aggressively, output not produced.
  (ccoleman@redhat.com)

* Sat Aug 04 2012 Dan McPherson <dmcphers@redhat.com> 0.97.2-1
- Bug 845171 (lnader@redhat.com)
- Merge pull request #113 from lnader/master (ccoleman@redhat.com)
- Bug 845171 (lnader@redhat.com)
- Loop and test roughly the same amount of time as before (ccoleman@redhat.com)
- Bug 845154 - When the CLI creates an app, it should check the health check
  URL first (if available), then check the root page.  If either are available
  we consider the app to have been loaded. (ccoleman@redhat.com)

* Thu Aug 02 2012 Adam Miller <admiller@redhat.com> 0.97.1-1
- bump_minor_versions for sprint 16 (admiller@redhat.com)

* Wed Aug 01 2012 Adam Miller <admiller@redhat.com> 0.96.7-1
- Merge pull request #110 from lnader/master (ccoleman@redhat.com)
- Merge pull request #111 from fabianofranz/master (ccoleman@redhat.com)
- Fixes #823851 and #841170 (ffranz@redhat.com)
- Bug 839889, Bug 841430 and use health_check_path returned by API
  (lnader@redhat.com)

* Tue Jul 31 2012 Adam Miller <admiller@redhat.com> 0.96.6-1
- Merge pull request #109 from smarterclayton/send_user_agent
  (ccoleman@redhat.com)
- Fix require bug with helpers and non-standard rhc load order
  (ccoleman@redhat.com)
- Merge pull request #106 from smarterclayton/send_user_agent
  (ccoleman@redhat.com)
- Ensure that the gem version is always < 4 numbers (ccoleman@redhat.com)
- Send user agent on all requests, add spec test coverage for user agent, and
  simplify api request stubs (ccoleman@redhat.com)

* Mon Jul 30 2012 Dan McPherson <dmcphers@redhat.com> 0.96.5-1
- Merge pull request #103 from smarterclayton/us2531_expose_version_info_in_gem
  (ccoleman@redhat.com)
- build.sh should invoke rake version, rake version should default to the
  client spec. (ccoleman@redhat.com)
- US2531 - Update gem version during RPM build, and use RHC::VERSION::STRING
  when accessing the current version. (ccoleman@redhat.com)

* Thu Jul 26 2012 Dan McPherson <dmcphers@redhat.com> 0.96.4-1
- added zend health_check.php (lnader@redhat.com)

* Thu Jul 19 2012 Adam Miller <admiller@redhat.com> 0.96.3-1
- Update README with changes to repository name. (ccoleman@redhat.com)
- Tidied up some redundancies in the shared examples setup. (hripps@redhat.com)
- Rhc::Rest#send was colliding with Ruby core send() method. This has been
  renamed to resolve the collision. Changes have been made throughout the REST
  API to accound fort this correction. Additionally, removed evals in
  rest_application_spec.rb to use the newly liberated ruby send() method
  instead. (hripps@redhat.com)
- Changed the way that class expectations are evaluated (hripps@redhat.com)
- DRYed up the Rhc::Rest::Aplication tests. (hripps@redhat.com)
- Added coverage for Rhc::Rest::Application; also added a filter to coverage
  config for a file that was blocking 100%% coverage. (hripps@redhat.com)

* Fri Jul 13 2012 Adam Miller <admiller@redhat.com> 0.96.2-1
- Merge pull request #97 from fotioslindiakos/BZ836483 (johnp@redhat.com)
- Merge pull request #99 from J5/master (ccoleman@redhat.com)
- some fixes to setup command and checking the spec test (johnp@redhat.com)
- Added tests to ensure a domain exists (fotios@redhat.com)
- Fixed error_for to ensure the sprintf won't fail (fotios@redhat.com)
- Ensuring we don't fail if broker sends nil HTTP response (fotios@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 0.96.1-1
- bump_minor_versions for sprint 15 (admiller@redhat.com)

* Wed Jul 11 2012 Adam Miller <admiller@redhat.com> 0.95.13-1
- [rspec] get to 100%% coverage with new wizard command change
  (johnp@redhat.com)
- add a better help formatter (johnp@redhat.com)
- make wizard run from Commander and setup default command line args
  (johnp@redhat.com)
- Merge pull request #94 from fabianofranz/master (ccoleman@redhat.com)
- Added coverage to File ext (chunks) (contact@fabianofranz.com)
- Moved File chunk extension to core_ext.rb (contact@fabianofranz.com)
- Changed tar.gz file check from client to server side when on Windows
  (contact@fabianofranz.com)
- Added a rescue to handle server errors when attempting to create new scaling
  applications (nhr@redhat.com)
- Removed debug code (contact@fabianofranz.com)
- Merge branch 'master' of github.com:openshift/os-client-tools
  (contact@fabianofranz.com)
- Fixes BZ 836097 (contact@fabianofranz.com)

* Tue Jul 10 2012 Adam Miller <admiller@redhat.com> 0.95.12-1
- Merge pull request #92 from J5/master (ccoleman@redhat.com)
- add Config value as default because it correctly evaluates when called
  (johnp@redhat.com)
- [bug #837189] Normalize on generating ssh keys using the wizard
  (johnp@redhat.com)

* Mon Jul 09 2012 Adam Miller <admiller@redhat.com> 0.95.11-1
- Merge pull request #90 from J5/master (contact@fabianofranz.com)
- [bug #816813] fix it so debug=true in conf works with rhc app
  (johnp@redhat.com)
- [spec] add test for ssh helper (johnp@redhat.com)
- bump the key generation to 2048 bits (johnp@redhat.com)
- [bug #837189] call ssh-add when writing out ssh key (johnp@redhat.com)

* Mon Jul 09 2012 Dan McPherson <dmcphers@redhat.com> 0.95.10-1
- Removed debug comments (contact@fabianofranz.com)
- Fixes BZ 837464 (contact@fabianofranz.com)
- Fixes BZ 837191, not parsing \n on windows anymore (using .lines instead)
  (contact@fabianofranz.com)

* Mon Jul 09 2012 Dan McPherson <dmcphers@redhat.com> 0.95.9-1
- Merge pull request #89 from nhr/BZ836177 (ccoleman@redhat.com)
- Merge pull request #87 from J5/master (ccoleman@redhat.com)
- Fixed BZ836177 -  error message is not clear when using invalid domain name
  in rhc setup wizard (nhr@redhat.com)
- Added rspec coverage for Rhc::Rest::Client (nhr@redhat.com)
- [cucumber] add tests for cartridge creation and stub out other tests
  (johnp@redhat.com)
- [cucumber] Suppress simplecov output for rhc scripts (johnp@redhat.com)
- [cucumber] revert debug comments which were mistakenly checked in
  (johnp@redhat.com)

* Thu Jul 05 2012 Adam Miller <admiller@redhat.com> 0.95.8-1
- Added rsepc testing for Rhc::Rest. Made minor fixes to Rhc::Rest base module.
  (nhr@redhat.com)

* Tue Jul 03 2012 Adam Miller <admiller@redhat.com> 0.95.7-1
- added buildrequires rubygem-cucumber because tests are running at rpm build
  time (admiller@redhat.com)

* Mon Jul 02 2012 Adam Miller <admiller@redhat.com> 0.95.6-1
- add comment to the top of coverage_helper (johnp@redhat.com)
- make coverage helper module more ruby'esk (johnp@redhat.com)
- [rake] make a cucumber_local task that runs on the local bundle
  (johnp@redhat.com)
- [rake] clean up tasks (johnp@redhat.com)
- [rake] add cucumber task and allow specifying RHC_SERVER (johnp@redhat.com)
- [cucumber coverage] use a helper to start simplecov (johnp@redhat.com)
- add simplecov to cucumber tests (johnp@redhat.com)
- [simplecov] Seperated simplecov output for spec tests (nhr@redhat.com)
- Fixes BZ 829833, Yard warnings when gem install rhc (ffranz@redhat.com)

* Wed Jun 27 2012 Adam Miller <admiller@redhat.com> 0.95.5-1
- add thor developer dependency so we can run cucumber tests (johnp@redhat.com)
- fix tito build due to move to root directory (johnp@redhat.com)
- Merge pull request #77 from smarterclayton/add_help_information_to_framework
  (johnp@redhat.com)
- Fixes BZ 834813, error while creating scaled apps on Ruby 1.9+
  (ffranz@redhat.com)
- DateTime on Ruby 1.8.7 can't be converted because of timezones
  (ccoleman@redhat.com)
- Ruby 1.8.7 doesn't support to_time (ccoleman@redhat.com)
- Add simple help info to the framework Improve the spec tests so that they
  pass when an openshift config file already exists Get 100%% coverage of
  helpers in helpers_spec.rb Add a way to create global options cleanly from
  the helper (ccoleman@redhat.com)
- Move everything in express/ into the root (ccoleman@redhat.com)
- Add contributing guidelines (ccoleman@redhat.com)
- Merge pull request #75 from smarterclayton/finish_up_cuc_tests
  (ccoleman@redhat.com)
- Ruby 1.8.7 does not support URI#hostname (ccoleman@redhat.com)
- Integrate cucumber into rake, simplify coverage reporting, allow optional
  execution of coverage during cucumber (ccoleman@redhat.com)
- Fix ActiveSupport override in both Ruby 1.8 and 1.9 (ccoleman@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 0.95.4-1
- Merge pull request #67 from matthicksj/add-cuc-tests (ccoleman@redhat.com)
- Switching cucumber to exit on any failure (mhicks@redhat.com)
- Adding rhc app show test (mhicks@redhat.com)
- Better OpenShift Origin instance support and docs (mhicks@redhat.com)
- No need to exclude these fields anymore (mhicks@redhat.com)
- Refactoring, fixes and additional functionality (mhicks@redhat.com)
- Minor fixes, handling rhc setup and configuration (mhicks@redhat.com)
- Adds end to end cucumber integration tests (mhicks@redhat.com)

* Sat Jun 23 2012 Dan McPherson <dmcphers@redhat.com> 0.95.3-1
- Merge pull request #73 from J5/master (ccoleman@redhat.com)
- [rspec] finish up the odds and ends to get Config to 100%% coverage
  (johnp@redhat.com)
- [rspec] break up Config to make it easier for testsing (johnp@redhat.com)
- [rspec] add RHC::Config tests (johnp@redhat.com)
- [rspec] fix home dir switching code to correctly reload config
  (johnp@redhat.com)
- [rspec] move fakefs bits into spec_helper so other tests can benifit
  (johnp@redhat.com)

* Thu Jun 21 2012 Adam Miller <admiller@redhat.com> 0.95.2-1
- Merge pull request #72 from J5/master (ccoleman@redhat.com)
- [simplecov] simpler coverage fix (johnp@redhat.com)
- Merge pull request #69 from J5/master (ccoleman@redhat.com)
- [simplecov] use the same regex for nocov as simplecov uses (johnp@redhat.com)
- Merge pull request #71 from xiy/master (ccoleman@redhat.com)
- Make line enumeration in rhc-port-forward compatible with both ruby 1.8 and
  1.9. (xiy3x0@gmail.com)
- [simplecov] monkey patch to correctly ignore :nocov: lines (johnp@redhat.com)
- [rspec] make stub methods less generic (johnp@redhat.com)
- [rspec] make sure we our internal ssh fingerprint methods match out fallback
  (johnp@redhat.com)
- [rspec] stub out ssh_keygen_fallback instead of exe_cmd (johnp@redhat.com)
- [rspec] silence output during tests by using highline's "say" instead of
  "puts" (johnp@redhat.com)
- remove debug output (johnp@redhat.com)
- [rspec] 100%% wizard coverage (johnp@redhat.com)
- [rspec] get coverage for ssh-keygen fallback (johnp@redhat.com)
- [rspec] more package kit code path coverage (johnp@redhat.com)
- [rspec] cover has_git? error condition (johnp@redhat.com)
- [rcov] cover the dbus_send_session_method method (johnp@redhat.com)
- [rspec wizard] add windows codepath check (johnp@redhat.com)
- [rspec] mock package kit (johnp@redhat.com)
- [rspec] small changes to get better test coverage (johnp@redhat.com)
- [rspec] add a test that runs through the whole wizard in one go
  (johnp@redhat.com)

* Wed Jun 20 2012 Adam Miller <admiller@redhat.com> 0.95.1-1
- bump_minor_versions for sprint 14 (admiller@redhat.com)
- Removing --noprompt from ARGV after we're done with it since the other
  commands complain about it not being a valid option (fotios@redhat.com)

* Wed Jun 20 2012 Adam Miller <admiller@redhat.com> 0.94.8-1
- Improved style (ffranz@redhat.com)
- Minor message improvements (ffranz@redhat.com)
- Fixed wrong forum URL everywhere (ffranz@redhat.com)
- Fixes BZ 826769 - will not fail app create and will show a message when the
  Windows Winsock bug is detected (ffranz@redhat.com)

* Tue Jun 19 2012 Adam Miller <admiller@redhat.com> 0.94.7-1
- Merge pull request #68 from J5/master (ccoleman@redhat.com)
- [bug 831771] require highline 1.5.1 (johnp@redhat.com)
- Merge pull request #66 from smarterclayton/handle_interrupts_gracefully
  (johnp@redhat.com)
- Bug 825766 - Catch any interrupts that have escaped all command execution
  (ccoleman@redhat.com)
- [bug 826472] namespace isn't in config file, don't update when altering
  namespace (johnp@redhat.com)
- update wizard spec tests (johnp@redhat.com)
- [bug 828324]exit 0 on success for rhc app cartridge list (johnp@redhat.com)

* Tue Jun 19 2012 Adam Miller <admiller@redhat.com> 0.94.6-1
- Fixup RHC requires so that only one module is requiring Rubygems, also ensure
  requires are not circular (ccoleman@redhat.com)

* Mon Jun 18 2012 Adam Miller <admiller@redhat.com> 0.94.5-1
- Merge pull request #65 from J5/master (ccoleman@redhat.com)
- add missing parseconfig.rb (johnp@redhat.com)
- Merge pull request #64 from J5/master (ccoleman@redhat.com)
- vendor parseconfig and remove monkey patches (johnp@redhat.com)
- remove some more unused parseconfig code (johnp@redhat.com)
- remove some stale code that must have crept back in from a merge
  (johnp@redhat.com)
- monkey patch parseconfig to remove deprication warnings (johnp@redhat.com)
- only run wizard if a valid command is issued (johnp@redhat.com)
- Improved SSH checks (fotios@redhat.com)
- Bug 831459 - Use the correct RbConfig version depending on Ruby version
  (ccoleman@redhat.com)

* Fri Jun 15 2012 Adam Miller <admiller@redhat.com> 0.94.4-1
- parseconfig 1.0.2 breaks our config module so specify < 1.0
  (johnp@redhat.com)
- fix traceback when checking for git and it is not installed
  (johnp@redhat.com)
- Do fast check for git (path) before slow check (package_kit)
  (ccoleman@redhat.com)
- Bug 831682 - Remove rake from core dependencies (ccoleman@redhat.com)
- add an accessor to config for default_rhlogin (johnp@redhat.com)
- Provide rubygem-rhc so we don't clash with f17 packages (johnp@redhat.com)
- [fix bug 830260] defaults to previously entered username in setup
  (johnp@redhat.com)

* Fri Jun 08 2012 Adam Miller <admiller@redhat.com> 0.94.3-1
- Merge pull request #61 from J5/master (ccoleman@redhat.com)
- fix traceback when checking for git and it is not installed
  (johnp@redhat.com)
- Bug fixes for 790459 and 808440 (abhgupta@redhat.com)
- change wordage for key read warning (johnp@redhat.com)
- Fix dealing with invalid ssh keys (indicate the key can not be read)
  (johnp@redhat.com)
- use the vendor version of SSHKey (johnp@redhat.com)
- fix typo s/message/display (johnp@redhat.com)
- [fix bug 829858] we don't need to check for a .ssh/config file
  (johnp@redhat.com)
- [fix bug 829903] Don't run setup when --help is specified (johnp@redhat.com)

* Fri Jun 08 2012 Adam Miller <admiller@redhat.com> 0.94.2-1
- fix another merge issue (johnp@redhat.com)
- fix merge issue by adding back Requires: rubygem-test-unit (johnp@redhat.com)
- move sshkey into the vendor module (johnp@redhat.com)
- use FileUtils as it works for all versions of ruby >= 1.8.7
  (johnp@redhat.com)
- Pull sshkey module into the source tree since it is small (johnp@redhat.com)
- Update client spec to require rubygem-test-unit, and relax version
  requirements (ccoleman@redhat.com)
- Off by one bug in simplecov, temporarily reduce percentage by 1 because
  coverage report is 100%% green (ccoleman@redhat.com)
- Allow users with bigdecimal as a system gem to run tests (crack requires
  bigdecimal implicitly) (ccoleman@redhat.com)
- Fix to_a bugs in Ruby 1.9 (behavior change, code was not forward compatible)
  (ccoleman@redhat.com)
- Bug 829764 - Add test-unit 1.2.3 as a firm dependency by the gem
  (ccoleman@redhat.com)

* Fri Jun 01 2012 Adam Miller <admiller@redhat.com> 0.94.1-1
- bumping spec versions (admiller@redhat.com)
- Fixed code coverage (:nocov:) (ffranz@redhat.com)
- fix bug #827582 - Wizard's git check returns a false negitive on RHEL6
  (johnp@redhat.com)

* Thu May 31 2012 Adam Miller <admiller@redhat.com> 0.93.18-1
- 

* Thu May 31 2012 Adam Miller <admiller@redhat.com> 0.93.17-1
- Added a fallback for ssh keys fingerprint handling to the setup wizard
  (related to BZ 824318) (ffranz@redhat.com)
- Merge pull request #53 from J5/master (contact@fabianofranz.com)
- extra space caused line continuation to fail (johnp@redhat.com)
- bug #826788, 826814 - fix wording (johnp@redhat.com)
- Merge pull request #51 from fabianofranz/master (johnp@redhat.com)
- Fixes BZ 824318, workaround for older net/ssh versions (usually Mac platform)
  (ffranz@redhat.com)
- fixes bz 826853 - del old config file to make sure new one gets created
  (johnp@redhat.com)
- make spec tests pass again (johnp@redhat.com)
- add ENV['LIBRA_SERVER'] to config options (johnp@redhat.com)
- bz 822833 - make commands read from correct configs (johnp@redhat.com)
- Totally reverted snapshot create and restore to native when not on windows
  (ffranz@redhat.com)

* Wed May 30 2012 Adam Miller <admiller@redhat.com> 0.93.16-1
- Merge pull request #49 from fabianofranz/master (contact@fabianofranz.com)
- Removed warning on Mac platform (ffranz@redhat.com)
- use SSH::Net to load public ssh fingerprint (johnp@redhat.com)
- Fixes BZ 824741 (ffranz@redhat.com)
- Fixed coverage (ffranz@redhat.com)
- Fixed coverage tests (ffranz@redhat.com)
- Fixes BZ 824312, back to native tar if not on windows (ffranz@redhat.com)

* Tue May 29 2012 Adam Miller <admiller@redhat.com> 0.93.15-1
- 

* Tue May 29 2012 Adam Miller <admiller@redhat.com> 0.93.14-1
- Merge pull request #44 from fabianofranz/master (johnp@redhat.com)
- Explanatory comment (ffranz@redhat.com)
- Fixes BZ 823854 (ffranz@redhat.com)

* Tue May 29 2012 Adam Miller <admiller@redhat.com> 0.93.13-1
- fix cmp typo (s/=/==) (johnp@redhat.com)
- make sure we check for uncaught signals if retcode is nil (johnp@redhat.com)
- remove generation of .ssh/config since we default to id_rsa now
  (johnp@redhat.com)
- add the server option to the rhc manpage (johnp@redhat.com)
- autocomplete rhc server and rhc setup (johnp@redhat.com)
- Removed duplicated code for rhc app tail and rhc-tail-files
  (ffranz@redhat.com)
- Fixed BZ 823448 (ffranz@redhat.com)
- Merge pull request #40 from fabianofranz/master (contact@fabianofranz.com)
- Fixes BZ 823441 (ffranz@redhat.com)

* Fri May 25 2012 Adam Miller <admiller@redhat.com> 0.93.12-1
- Removed vendored libs from coverage reports (ffranz@redhat.com)
- Merge pull request #37 from fabianofranz/master (ccoleman@redhat.com)
- workaround for bug #816338 - no longer get redefine warning
  (johnp@redhat.com)
- Vendored libs reorganized (ffranz@redhat.com)
- Fixes BZ 823853 and 824312 (ffranz@redhat.com)
- catch NotImplementedError which is raised for invalid key types
  (johnp@redhat.com)
- typo fix s/FileUtil/FileUtils (johnp@redhat.com)
- [wizard] some more scoping issues (johnp@redhat.com)
- 30 threads testing tar.gz file reads (ffranz@redhat.com)
- Removed pr-zlib in favour of zliby to solve pr-zlib multithreading bug, added
  more rspec tests (ffranz@redhat.com)

* Thu May 24 2012 Adam Miller <admiller@redhat.com> 0.93.11-1
- Merge pull request #34 from J5/master (ccoleman@redhat.com)
- add rhc setup to help docs (johnp@redhat.com)
- [wizard] fix scoping issue uncovered in tests (johnp@redhat.com)
- [tests] add ssh_key upload stage tests (johnp@redhat.com)
- [tests] implement create ssh key tests (johnp@redhat.com)
- [tests] implement File.chmod as a noop for FakeFS (johnp@redhat.com)
- allow home_dir to be set in the configs so it can be set for tests
  (johnp@redhat.com)
- use FileUtil instead of Dir so it works with FakeFS (johnp@redhat.com)
- [tests] implement the write config stage checks (johnp@redhat.com)
- [tests] stub out some http requests in wizard tests (johnp@redhat.com)
- [tests] use the more reliable terminal IO api (johnp@redhat.com)
- [tests] utilize the new mock terminal IO api (johnp@redhat.com)
- [tests] move libra_server def up (johnp@redhat.com)
- [tests] require fakefs (johnp@redhat.com)
- [tests] make it easier to read and write the mock terminal streams
  (johnp@redhat.com)
- make WizardDriver a mixin and allow it to access the stages array
  (johnp@redhat.com)
- [tests] stub out wizzard tests (johnp@redhat.com)

* Thu May 24 2012 Adam Miller <admiller@redhat.com> 0.93.10-1
- 

* Thu May 24 2012 Adam Miller <admiller@redhat.com> 0.93.9-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (ffranz@redhat.com)
- Fixed a helpers bug (ffranz@redhat.com)

* Wed May 23 2012 Adam Miller <admiller@redhat.com> 0.93.8-1
- Improved coverage (ffranz@redhat.com)

* Wed May 23 2012 Adam Miller <admiller@redhat.com> 0.93.7-1
- Improved rspec syntax (ffranz@redhat.com)
- Removed deprecated herpers, added specific .rb for json and targz helpers,
  json and targz tests (ffranz@redhat.com)
- Merge pull request #29 from J5/master (ccoleman@redhat.com)
- Merge pull request #31 from bdecoste/master (contact@fabianofranz.com)
- US2307 (bdecoste@gmail.com)
- fix (johnp@redhat.com)
- Merge remote-tracking branch 'origin/master' into j5 (johnp@redhat.com)
- [tests] check for section(:bottom => -1) senario (johnp@redhat.com)
- [wizard] test coverage for formatter helpers (johnp@redhat.com)
- Add RHC::Helpers test for environment variables (ccoleman@redhat.com)
- [wizard] add formatting helpers to get rid of \n (johnp@redhat.com)
- [wizard] change git test (johnp@redhat.com)
- [wizard] use File.open do end blocks (johnp@redhat.com)
- [wizard] use @libra_server instead of hardcoding urls (johnp@redhat.com)
- [wizard] output formatting fixes (johnp@redhat.com)
- [wizard] add an application info stage (johnp@redhat.com)
- [wizard] namespace creation stage added (root@dhcp-100-2-224.bos.redhat.com)
- [wizard] fallback if using PackageKit fails (johnp@redhat.com)
- [wizard] add default name for ssh key based on fingerprint (johnp@redhat.com)
- [wizard] reformat output and add better worded prompts (johnp@redhat.com)

* Tue May 22 2012 Adam Miller <admiller@redhat.com> 0.93.6-1
- Implement simple server status command 'rhc server' and helpers to support it
  (ccoleman@redhat.com)

* Tue May 22 2012 Adam Miller <admiller@redhat.com> 0.93.5-1
- Merge pull request #28 from fabianofranz/master (contact@fabianofranz.com)
- Fixed rspec tests (ffranz@redhat.com)

* Tue May 22 2012 Adam Miller <admiller@redhat.com> 0.93.4-1
- Fixes an issue related to leaving a file open when reading snapshot files
  (ffranz@redhat.com)
- Merge remote-tracking branch 'upstream/master' (ffranz@redhat.com)
- Fixed tar and gzip bugs on windows, fixed port forwarding bugs on windows
  (ffranz@redhat.com)
- [wizard] all stages must return true to continue processing
  (johnp@redhat.com)
- [wizard] handle case where the user has no ssh keys, even 'default'
  (johnp@redhat.com)
- [wizard] add ability to rerun by calling rhc setup (johnp@redhat.com)
- [wizard] fix print out of command (johnp@redhat.com)
- [wizard] add windows stage which prints out client tool info
  (johnp@redhat.com)
- [wizard] add the package check and install phase (johnp@redhat.com)

* Fri May 18 2012 Adam Miller <admiller@redhat.com> 0.93.3-1
- [wizard] use highline say and ask for input and output (johnp@redhat.com)

* Thu May 17 2012 Adam Miller <admiller@redhat.com> 0.93.2-1
- [wizard] check if sshkey is uploaded and if not upload it (johnp@redhat.com)
- remove merge artifact (johnp@redhat.com)
- caught some more places to convert to the Config module (johnp@redhat.com)
- Merges Windows bug fixes (ffranz@redhat.com)
- Back to highline for user input, use * echo on password input
  (ffranz@redhat.com)
- Fixes bz 816644 (ffranz@redhat.com)
- get default_proxy from the Config singlton instead of as a magic var
  (johnp@redhat.com)
- break out wizard to its own module (root@dhcp-100-2-224.bos.redhat.com)
- Increased timeout when creating scaled apps (ffranz@redhat.com)
- Fixed port forwarding for scaled apps (bz 816644) (ffranz@redhat.com)
- fixed typo (johnp@redhat.com)
- use new Config module (johnp@redhat.com)
- add new config module (johnp@redhat.com)
- quick fix - add --noprompt switch to bypass first run wizard
  (johnp@redhat.com)
- Temporary commit to build (johnp@redhat.com)
- Remove native extension builds and update the spec with the necessary RPMs
  (ccoleman@redhat.com)
- Newer versions of rspec are loading empty specs (ccoleman@redhat.com)
- Using commander create command infrastructure for registration and a simple
  'status' command With RSpec, ensure 100%% code coverage and make <100%% of
  required code being covered by tests fail build Add an example 'status'
  command that demonstrates registration for simple testing, and add it to
  'rhc' (ccoleman@redhat.com)
- Fixes rhc.gemspec (typo during previous merge) (ffranz@redhat.com)
- Merging windows branch (ffranz@redhat.com)
- Add travis build indicator to express/README.md (ccoleman@redhat.com)
- Exclude Gemfile.lock (ccoleman@redhat.com)
- Use a core gemspec file with the appropriate content Change Rake to default
  to :test over :package Add a simple RHC module Move autocomplete rhc script
  out of lib directory and into autocomplete/ (ccoleman@redhat.com)
- Refactored Rakefile to pull from tasks/*.rake Added more rake test tasks
  (like test:functionals) Added dependencies into Gemfile so Travis will
  install them Added requirement for gem version of test-unit so we can omit
  tests gracefully Added omission code to domain and application tests for now
  Merge changes to remove domain name (fotios@redhat.com)
- Validates the snapshot .tar.gz file locally (ffranz@redhat.com)
- Removed native zlib requirement, added vendored pure Ruby zlib (rbzlib)
  (ffranz@redhat.com)
- Removed highline gem, using our own prompt solution (ffranz@redhat.com)
- Ported rhc app snapshot to pure ruby, unified code with rhc-snapshot
  (ffranz@redhat.com)
- Ported rhc-snapshot to minitar (ffranz@redhat.com)
- Ported tar command to pure ruby using minitar and zlib ruby
  (ffranz@redhat.com)
- Improved error handling and capturing sigint (ffranz@redhat.com)
- Port checking and port forwarding now working with Net::SSH
  (ffranz@redhat.com)
- Forwarding ports through net::ssh (todo: convert list_ports also)
  (ffranz@redhat.com)
- Completely removed json gems in favour of vendored okjson.rb
  (ffranz@redhat.com)
- Added highline dep :( but passwords work properly in windows now
  (mmcgrath@redhat.com)
- removed s.extensions because it caused the gem to get flagged as native this
  causes issues in windows (mmcgrath@redhat.com)
- Added new deps (Mike McGrath)
- replacing libra_id_rsa with standard id_rsa (Mike McGrath)
- remove openssh dep on tail-files and use Net::SSH instead (Mike McGrath)
- Wizard now supports uploading keys (among others, see full commit message)
  (builder@example.com)
- Added initial wizard, still needs work (mmcgrath@redhat.com)
- Startred adding native ruby ssh bindings (mmcgrath@redhat.com)

* Thu May 10 2012 Adam Miller <admiller@redhat.com> 0.93.1-1
- Merge pull request #18 from rmillner/master (ccoleman@redhat.com)
- bumping spec versions (admiller@redhat.com)
- Let the broker dictate what valid gear sizes are for the user.
  (rmillner@redhat.com)

* Wed May 09 2012 Adam Miller <admiller@redhat.com> 0.92.10-1
- Removed large gear size, only small and medium for now (ffranz@redhat.com)

* Tue May 08 2012 Adam Miller <admiller@redhat.com> 0.92.9-1
- Bug 819739 (dmcphers@redhat.com)

* Mon May 07 2012 Adam Miller <admiller@redhat.com> 0.92.8-1
- TA2025 (bdecoste@gmail.com)

* Fri May 04 2012 Dan McPherson <dmcphers@redhat.com> 0.92.7-1
- Revert "Merge pull request #12 from fotioslindiakos/config_file"
  (dmcphers@redhat.com)

* Fri May 04 2012 Adam Miller <admiller@redhat.com> 0.92.6-1
- Fix for BugZ#817985. gear_profile was not being passed for scaled apps
  (kraman@gmail.com)
- Added config file generation (fotios@redhat.com)
- Added tests and renamed REST tests so they don't get executed by rake since
  they rely on a devenv (fotios@redhat.com)
- Fixed checking for debug flag in config file to allow command line to
  override (fotios@redhat.com)

* Thu May 03 2012 Adam Miller <admiller@redhat.com> 0.92.5-1
- 

* Thu May 03 2012 Adam Miller <admiller@redhat.com> 0.92.4-1
- Fix for BugZ#817985. gear_profile was not being passed for scaled apps
  (kraman@gmail.com)

* Tue May 01 2012 Adam Miller <admiller@redhat.com> 0.92.3-1
- Revert "Merge pull request #10 from fotioslindiakos/config_file" - some
  failing tests, will retry.  Be sure to resubmit pull request.
  (ccoleman@redhat.com)
- Merge pull request #10 from fotioslindiakos/config_file
  (smarterclayton@gmail.com)
- remove rhc-rest removal message (dmcphers@redhat.com)
- Renamed REST based tests so they're not run via rake test (fotios@redhat.com)
- Added documentation to the new functions in rhc-common (fotios@redhat.com)
- Added tests for new config files. Also added a pseudo-fixtures file for
  testing and a script to generate that YAML (fotios@redhat.com)
- Broke config file generation down into multiple functions (fotios@redhat.com)
- add rake require and rhc-rest obsolete (dmcphers@redhat.com)
- Improved ~/.openshift/express.conf generation   - allows us to specify a hash
  of config variables, comments, and default values   - checks the users
  current configuration     - preserves modified settings     -
  restores/updates comments (in case we change something)     - adds new
  variables and removes deprecated ones     - saves the user's old config to
  ~/.openshift/express.bak In response to
  https://bugzilla.redhat.com/show_bug.cgi?id=816763 (fotios@redhat.com)
- Improved config file generation for
  https://bugzilla.redhat.com/show_bug.cgi?id=816763 (fotios@redhat.com)

* Fri Apr 27 2012 Adam Miller <admiller@redhat.com> 0.92.2-1
- Fix for Bugz#812308 (kraman@gmail.com)

* Thu Apr 26 2012 Adam Miller <admiller@redhat.com> 0.92.1-1
- bumping spec versions (admiller@redhat.com)

* Wed Apr 25 2012 Adam Miller <admiller@redhat.com> 0.91.10-1
- 

* Wed Apr 25 2012 Adam Miller <admiller@redhat.com> 0.91.9-1
- Removed finding rhc-rest before uninstalling since we can just catch the
  uninstall error. This was causing problems on Ubuntu (fotios@redhat.com)
- Changed JSON library checking for only install json_pure if native json fails
  (fotios@redhat.com)

* Tue Apr 24 2012 Adam Miller <admiller@redhat.com> 0.91.8-1
- Added ability to remove rhc-rest when this gem gets installed This should
  prevent any conflicts between old rhc-rest and new libs/rhc-rest*
  (fotios@redhat.com)
- Added rake as a dependency, so extension building will succeed Added rescue
  around native json installation and fallback to json_pure (fotios@redhat.com)

* Tue Apr 24 2012 Adam Miller <admiller@redhat.com> 0.91.7-1
- update scaling entry to include jenkins-client-1.4 as embedded cartridge
  (davido@redhat.com)

* Mon Apr 23 2012 Adam Miller <admiller@redhat.com> 0.91.6-1
- added --scaling details, fixed some formatting, adding path arg to --config
  (davido@redhat.com)

* Fri Apr 20 2012 Adam Miller <admiller@redhat.com> 0.91.5-1
- exit with exit code 0 is --help is invoked (johnp@redhat.com)
- updated --timeout details, fixed typo, removed 'Express' (davido@redhat.com)

* Thu Apr 19 2012 Adam Miller <admiller@redhat.com> 0.91.4-1
- It was decided that the connect-timeout parameter was extraneous.
  (rmillner@redhat.com)
- Mixed up variable names (rmillner@redhat.com)
- After discussions; it was decided to just have one timeout parameter and a
  connect_timeout config file option which can increase both timeouts from
  their defaults. (rmillner@redhat.com)

* Wed Apr 18 2012 Adam Miller <admiller@redhat.com> 0.91.3-1
- Added logic from fotios to skip gems dep installer steps
  (admiller@redhat.com)
- Ignore gem dep solver, we use rpm for deps (admiller@redhat.com)

* Wed Apr 18 2012 Adam Miller <admiller@redhat.com> 0.91.2-1
- Fixed paths for new combined rhc package (fotios@redhat.com)
- Moved rhc-rest files into express (fotios@redhat.com)
- Make the timeout parameter specific to the session timeout and add a
  connection timeout. (rmillner@redhat.com)
- Following request in bugzilla ticket 813110; further increase the timeout to
  120s. (rmillner@redhat.com)
- The default read timeout is causing build/test failures and user-visible
  bugs.  Increasing the read timeout default to 90s which is 30%% higher than
  our current worst-case non-scalable app creation time. (rmillner@redhat.com)
- Fixing extensions so the build will pass (fotios@redhat.com)
- Update Rakefile with move (ccoleman@redhat.com)
- Merge branch 'master' of github.com:openshift/os-client-tools
  (dmcphers@redhat.com)
- Add links to the getting started guide (ccoleman@redhat.com)
- Update README.md with recent changes. (ccoleman@redhat.com)
- US2145: properly choosing json/json_pure based on installation environment
  (fotios@redhat.com)
- Fixed error output for non-scalable apps (fotios@redhat.com)

* Mon Apr 16 2012 Dan McPherson <dmcphers@redhat.com> 0.91.1-1
- add read timeout (dmcphers@redhat.com)

* Thu Apr 12 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.6-1
- BZ810790: Fixed app scaling payload creation (fotios@redhat.com)

* Wed Apr 11 2012 Mike McGrath <mmcgrath@redhat.com> 0.90.5-1
- Struct::Fakeresponse was not defined in a couple of instances.
  (rmillner@redhat.com)

* Wed Apr 11 2012 Adam Miller <admiller@redhat.com> 0.90.4-1
- error out if archive is not found when restoring a snapshot
  (johnp@redhat.com)

* Wed Apr 11 2012 Adam Miller <admiller@redhat.com> 0.90.3-1
- Merge branch 'master' of https://github.com/openshift/os-client-tools
  (admiller@redhat.com)
- Fixes #807200: added a handler for FakeResponse - error messages related to
  scaling apps (ffranz@redhat.com)

* Tue Apr 10 2012 Adam Miller <admiller@redhat.com> 0.90.2-1
- API change in REST api - use domain.id instead of domain.namespace
  (johnp@redhat.com)
- corrected end_point in rhc client tools (lnader@redhat.com)
- add port-forward to the list of autocomplete verbs for rhc (johnp@redhat.com)
- Renaming gem extension so builder can find it (fotios@redhat.com)
- initialize global $remote_ssh_pubkeys at the very top of first test
  (johnp@redhat.com)
- BZ809335: Added rhc-rest dependency to gemspec and made sure test-unit is
  properly installed in 1.9 (fotios@redhat.com)
- BZ810439: Fixed dependency for client tools to require latest version of rhc-
  rest (fotios@redhat.com)
- if gnutar exists use that (johnp@redhat.com)
- bug fixes (lnader@redhat.com)

* Mon Apr 09 2012 Dan McPherson <dmcphers@redhat.com> 0.90.1-1
- make sure $remote_ssh_pubkeys is an empty list, not nil (johnp@redhat.com)
- Added scaling support to cli tools (fotios@redhat.com)
- bump spec number (dmcphers@redhat.com)

* Mon Apr 02 2012 Mike McGrath <mmcgrath@redhat.com> 0.89.12-1
- create an error response instead of returning false (johnp@redhat.com)

* Sat Mar 31 2012 Dan McPherson <dmcphers@redhat.com> 0.89.11-1
- remove newlines from help text (johnp@redhat.com)
- error out on app create if domain isn't created yet (johnp@redhat.com)

* Fri Mar 30 2012 Dan McPherson <dmcphers@redhat.com> 0.89.10-1
- 

* Thu Mar 29 2012 Dan McPherson <dmcphers@redhat.com> 0.89.9-1
- add Requires dep on rhc-rest (johnp@redhat.com)
- make --info work when there are no domains or multiple domains
  (johnp@redhat.com)
- handle empty domains and multiple domains (johnp@redhat.com)
- Solve undefined method [] error. (rmillner@redhat.com)

* Wed Mar 28 2012 Dan McPherson <dmcphers@redhat.com> 0.89.8-1
- add scaling to rhc-app (rmillner@redhat.com)

* Tue Mar 27 2012 Dan McPherson <dmcphers@redhat.com> 0.89.7-1
- Clean up command help (rmillner@redhat.com)
- Creating scalable apps was causing a timeout.  Needed to setup an exception
  to propagate that back to the end-user. (rmillner@redhat.com)

* Tue Mar 27 2012 Dan McPherson <dmcphers@redhat.com> 0.89.6-1
- 

* Tue Mar 27 2012 Dan McPherson <dmcphers@redhat.com> 0.89.5-1
- 

* Mon Mar 26 2012 Dan McPherson <dmcphers@redhat.com> 0.89.4-1
- 

* Mon Mar 26 2012 Dan McPherson <dmcphers@redhat.com> 0.89.3-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (lnader@redhat.com)
- US1876 (lnader@redhat.com)
- add -g option to rhc-app man page (johnp@redhat.com)
- add rhc-port-forward to the rhc command (rhc port-forward) (johnp@redhat.com)

* Sat Mar 17 2012 Dan McPherson <dmcphers@redhat.com> 0.89.2-1
- 

* Sat Mar 17 2012 Dan McPherson <dmcphers@redhat.com> 0.89.1-1
- bump spec number (dmcphers@redhat.com)
- Changed allowed scalable types (fotios@redhat.com)

* Thu Mar 15 2012 Dan McPherson <dmcphers@redhat.com> 0.88.9-1
- Bug 800742 (dmcphers@redhat.com)

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.8-1
- Merge pull request #7 from jwhonce/master (jwhonce@gmail.com)
- targeting LICENSE and COPYRIGHT (jhonce@redhat.com)

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.7-1
- Merge pull request #6 from jwhonce/master (jwhonce@gmail.com)
- named target files (jhonce@redhat.com)

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.6-1
- Merge pull request #5 from jwhonce/master (jwhonce@gmail.com)
- License and Copyright files targeted for wrong directory (jhonce@redhat.com)

* Wed Mar 14 2012 Dan McPherson <dmcphers@redhat.com> 0.88.5-1
- Updated Copyright and License files (jhonce@redhat.com)
- Add gear-size option. (rmillner@redhat.com)

* Mon Mar 12 2012 Dan McPherson <dmcphers@redhat.com> 0.88.4-1
- Modified flag for scaling (fotios@redhat.com)
- fixing bug 800586 - printing git url in case of -no-git and no-dns option
  (abhgupta@redhat.com)
- The return values from expose and show-port are not being parsed by the API
  and setup behind the scenes as part of scaling.  These commands were exposed
  for testing and aren't needed any more. (rmillner@redhat.com)

* Fri Mar 09 2012 Dan McPherson <dmcphers@redhat.com> 0.88.3-1
- bump api version (dmcphers@redhat.com)

* Thu Mar 08 2012 Dan McPherson <dmcphers@redhat.com> 0.88.2-1
- Change std size to small (rmillner@redhat.com)
- add medium gear size (rmillner@redhat.com)
- Added some new REST API features to app creation (fotios@redhat.com)
- rename raw to diy in the man pages (abhgupta@redhat.com)

* Fri Mar 02 2012 Dan McPherson <dmcphers@redhat.com> 0.88.1-1
- bumping spec version (dmcphers@redhat.com)

* Fri Mar 02 2012 Dan McPherson <dmcphers@redhat.com> 0.87.8-1
- fix case (dmcphers@redhat.com)
- fix for bug 799375 - rhc app show now returns exit code 1 if app does not
  exist (abhgupta@redhat.com)

* Wed Feb 29 2012 Dan McPherson <dmcphers@redhat.com> 0.87.7-1
- fix for bug 798674 - rhc wrapper commands now return the actual exit codes
  (abhgupta@redhat.com)

* Tue Feb 28 2012 Dan McPherson <dmcphers@redhat.com> 0.87.6-1
- Update w/ correct license and export doc (jim@jaguNET.com)

* Sat Feb 25 2012 Dan McPherson <dmcphers@redhat.com> 0.87.5-1
- rename jboss 7.0 to jboss 7 (dmcphers@redhat.com)

* Fri Feb 24 2012 Dan McPherson <dmcphers@redhat.com> 0.87.4-1
- print out error message if invalid gear size is passed (johnp@redhat.com)

* Tue Feb 21 2012 Dan McPherson <dmcphers@redhat.com> 0.87.3-1
- Add show-port call. (rmillner@redhat.com)
- update man page for rhc-create-app to reflect the -g option
  (johnp@redhat.com)
- add a -g option to specify gear size (johnp@redhat.com)

* Mon Feb 20 2012 Dan McPherson <dmcphers@redhat.com> 0.87.2-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- allowing underscores in ssh key names (abhgupta@redhat.com)

* Thu Feb 16 2012 Dan McPherson <dmcphers@redhat.com> 0.87.1-1
- bump spec numbers (dmcphers@redhat.com)
- Bugzilla ticket 768809: The jenkins command line option description breaks up
  the flow too much and line wraps poorly.  Moved to a note below the argument
  description. (rmillner@redhat.com)

* Wed Feb 15 2012 Dan McPherson <dmcphers@redhat.com> 0.86.7-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- fix for bug 790987 (abhgupta@redhat.com)

* Wed Feb 15 2012 Dan McPherson <dmcphers@redhat.com> 0.86.6-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- fix for bug 790795 (abhgupta@redhat.com)
- Merge branch 'patch-1' of https://github.com/Qalthos/os-client-tools
  (abhgupta@redhat.com)
- Fixed some SSH key issues and improved error message specification
  (fotios@redhat.com)
- Fix for BZ786230 when account doesn't exist (fotios@redhat.com)
- Tell tar to use the wildcard instead of looking for a folder called '*'.
  (Qalthos@gmail.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.86.5-1
- Rolling back my changes to expose targetted proxy. Revert "Add '--target'
  option for expose/conceal port options." (rmillner@redhat.com)
- Rolling back my changes to expose targetted proxy. Revert "The target option
  was intended to be optional." (rmillner@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.86.4-1
- fix for bug 789928 (abhgupta@redhat.com)
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- fix for bug 789928 (abhgupta@redhat.com)
- Merge branch 'master' of github.com:openshift/os-client-tools
  (mmcgrath@redhat.com)
- return the json rep so it can be used (mmcgrath@redhat.com)

* Mon Feb 13 2012 Dan McPherson <dmcphers@redhat.com> 0.86.3-1
- The target option was intended to be optional. (rmillner@redhat.com)
- Add '--target' option for expose/conceal port options. (rmillner@redhat.com)
- bug 722828 (bdecoste@gmail.com)

* Wed Feb 08 2012 Dan McPherson <dmcphers@redhat.com> 0.86.2-1
- Adding expose / conceal ports (mmcgrath@redhat.com)
- remove use of broker_version (dmcphers@redhat.com)

* Fri Feb 03 2012 Dan McPherson <dmcphers@redhat.com> 0.86.1-1
- bump spec numbers and remove combo (dmcphers@redhat.com)

* Fri Feb 03 2012 Dan McPherson <dmcphers@redhat.com> 0.85.12-1
- fix for bug 787120 (abhgupta@redhat.com)

* Wed Feb 01 2012 Dan McPherson <dmcphers@redhat.com> 0.85.11-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- fix for bug 786339 - added option -t in the rhc-app man page
  (abhgupta@redhat.com)
- Fix for BZ 690465 - Merge changes originally made by jhonce
  (aboone@redhat.com)
- rhc-create-app man page: wsgi -> python and rack -> ruby (BZ 786356)
  (aboone@redhat.com)

* Tue Jan 31 2012 Dan McPherson <dmcphers@redhat.com> 0.85.10-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- fix for bug 785948 - defaulting to bash auto completion if the rhc auto
  completion does not find any matches (abhgupta@redhat.com)

* Mon Jan 30 2012 Dan McPherson <dmcphers@redhat.com> 0.85.9-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (dmcphers@redhat.com)
- modification to the usage description (abhgupta@redhat.com)

* Mon Jan 30 2012 Dan McPherson <dmcphers@redhat.com> 0.85.8-1
- exiting with 1 instead of 0 in case rhc-domain-info returns an exit code
  other than 0 (abhgupta@redhat.com)
- fix for bug 785647 (abhgupta@redhat.com)
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- fix for bug 785638 (abhgupta@redhat.com)

* Sun Jan 29 2012 Dan McPherson <dmcphers@redhat.com> 0.85.7-1
- 

* Sun Jan 29 2012 Dan McPherson <dmcphers@redhat.com> 0.85.6-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- added man files for the new rhc wrapper commands (abhgupta@redhat.com)

* Fri Jan 27 2012 Dan McPherson <dmcphers@redhat.com> 0.85.5-1
- removing the check for bash completion directory in the spec file
  (abhgupta@redhat.com)
- added man file for top level rhc command (abhgupta@redhat.com)
- corrected the command description in the usage text (abhgupta@redhat.com)

* Fri Jan 27 2012 Dan McPherson <dmcphers@redhat.com> 0.85.4-1
- 

* Fri Jan 27 2012 Dan McPherson <dmcphers@redhat.com> 0.85.3-1
- minor fixe to rhc domain status command (abhgupta@redhat.com)
- fixing self identified bugs as well as those identified by Dan
  (abhgupta@redhat.com)
- changes required due to ssh_key response structure change
  (abhgupta@redhat.com)
- changing message content to reflect new commands (abhgupta@redhat.com)
- more fixes to the new wrapper commands (abhgupta@redhat.com)
- fixing issues identified during self testing (abhgupta@redhat.com)
- fixes to rhc rpm spec file (abhgupta@redhat.com)
- rolling back change to convert application and namespace name to lowercase
  (abhgupta@redhat.com)
- converting application and namespace names to lowercase before passing to the
  server (abhgupta@redhat.com)
- correction in rhc app command usage description (abhgupta@redhat.com)
- minor correction to auto completion bash script (abhgupta@redhat.com)
- added bash completion script and other minor changes (abhgupta@redhat.com)
- using rhc-domain-info consistently (abhgupta@redhat.com)
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- new rhc command structure implemented (abhgupta@redhat.com)

* Tue Jan 17 2012 Dan McPherson <dmcphers@redhat.com> 0.85.2-1
- use rhc-domain-info consistently (dmcphers@redhat.com)
- fix for bug 773144 (abhgupta@redhat.com)

* Fri Jan 13 2012 Dan McPherson <dmcphers@redhat.com> 0.85.1-1
- bump spec numbers (dmcphers@redhat.com)

* Fri Jan 13 2012 Dan McPherson <dmcphers@redhat.com> 0.84.13-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- accounting for change to the response structure for ssh keys
  (abhgupta@redhat.com)

* Thu Jan 12 2012 Dan McPherson <dmcphers@redhat.com> 0.84.12-1
- Bump expected API version to 1.1.2 (key_type required on rhc-create-domain)
  (aboone@redhat.com)

* Wed Jan 11 2012 Dan McPherson <dmcphers@redhat.com> 0.84.11-1
- man page updates (dmcphers@redhat.com)
- man page updates (dmcphers@redhat.com)

* Wed Jan 11 2012 Dan McPherson <dmcphers@redhat.com> 0.84.10-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- adding man files for the newly added CLI commands (abhgupta@redhat.com)
- Remove output about threaddump command, this is handled by the cartridges now
  (aboone@redhat.com)
- Added test-unit dependency for Ruby 1.9 (fotios@redhat.com)

* Tue Jan 10 2012 Dan McPherson <dmcphers@redhat.com> 0.84.9-1
- adding more clarity to the help description for rhc-ctl-domain -a based on
  discussion with docs (abhgupta@redhat.com)
- displaying SSH key type in rhc-domain-info (abhgupta@redhat.com)
- placing validations after checking if --help is requested
  (abhgupta@redhat.com)

* Mon Jan 09 2012 Dan McPherson <dmcphers@redhat.com> 0.84.8-1
- Changing the deprecation warning for rhc-user-info (abhgupta@redhat.com)
- moving comments to debug mode (abhgupta@redhat.com)
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- fixing typo in the script help/usage description (abhgupta@redhat.com)

* Mon Jan 09 2012 Dan McPherson <dmcphers@redhat.com> 0.84.7-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- reflecting changes in rhc spec file (abhgupta@redhat.com)

* Fri Jan 06 2012 Dan McPherson <dmcphers@redhat.com> 0.84.6-1
- adding output comment to highlight command for user ssh key management
  (abhgupta@redhat.com)
- reverting a change that was made for local testing (abhgupta@redhat.com)
- Merge branch 'master' of github.com:openshift/os-client-tools
  (abhgupta@redhat.com)
- ensuring rhc-chk does not fail if issued from a machine using a non-default
  ssh key (abhgupta@redhat.com)

* Fri Jan 06 2012 Dan McPherson <dmcphers@redhat.com> 0.84.5-1
- specifying the ssh key type in the request to the controller
  (abhgupta@redhat.com)
- adding features for namespace deletion and user ssh key (additional keys)
  management (abhgupta@redhat.com)

* Tue Jan 03 2012 Dan McPherson <dmcphers@redhat.com> 0.84.4-1
- better formatting (dmcphers@redhat.com)

* Fri Dec 16 2011 Dan McPherson <dmcphers@redhat.com> 0.84.3-1
- update man page for threaddump (bdecoste@gmail.com)

* Thu Dec 15 2011 Dan McPherson <dmcphers@redhat.com> 0.84.2-1
- use actual app name in note (wdecoste@localhost.localdomain)

* Wed Dec 14 2011 Dan McPherson <dmcphers@redhat.com> 0.84.1-1
- bump spec number (dmcphers@redhat.com)

* Tue Dec 13 2011 Dan McPherson <dmcphers@redhat.com> 0.83.7-1
- added threaddump script doc (wdecoste@localhost.localdomain)
- remove extra message (dmcphers@redhat.com)
- Merge branch 'master' of github.com:openshift/os-client-tools
  (ffranz@redhat.com)
- Updated man pages (ffranz@redhat.com)

* Mon Dec 12 2011 Dan McPherson <dmcphers@redhat.com> 0.83.6-1
- Now using popen3(ssh) for rhc-port-forward instead of Net::SSH - we don't
  want to require additional gems (ffranz@redhat.com)
- US1550: add threaddump command (wdecoste@localhost.localdomain)

* Sun Dec 11 2011 Dan McPherson <dmcphers@redhat.com> 0.83.5-1
- New client tool rhc-port-forward for SSH tunelling (ffranz@redhat.com)

* Wed Dec 07 2011 Matt Hicks <mhicks@redhat.com> 0.83.4-1
- Check for inconsistent client/server API versions, warn user
  (aboone@redhat.com)

* Tue Dec 06 2011 Alex Boone <aboone@redhat.com> 0.83.3-1
- 

* Tue Dec 06 2011 Alex Boone <aboone@redhat.com> 0.83.2-1
- Construct the Git url earlier in case we have to include it in an error
  message (aboone@redhat.com)

* Thu Dec 01 2011 Dan McPherson <dmcphers@redhat.com> 0.83.1-1
- bump spec version (dmcphers@redhat.com)

* Wed Nov 30 2011 Dan McPherson <dmcphers@redhat.com> 0.82.18-1
- Bugzilla ticket 710112 Fix up http_proxy environment variable to allow
  username and password.  Also allow it to specify a full URL for compat with
  other utilities.  All of these should now work:
  http://foo@bar:10.11.12.13:3128/ http://10.11.12.13:3128
  foo@bar:10.11.12.13:3128 10.11.12.13:3128 (rmillner@redhat.com)

* Mon Nov 28 2011 Dan McPherson <dmcphers@redhat.com> 0.82.17-1
- Added global config file support to rhc-chk (fotios@redhat.com)

* Wed Nov 23 2011 Dan McPherson <dmcphers@redhat.com> 0.82.16-1
- further trimming the output of rhc-create-app (abhgupta@redhat.com)

* Tue Nov 22 2011 Dan McPherson <dmcphers@redhat.com> 0.82.15-1
- Added 2 checks to prevent errors if password not specified or kfile does not
  exist (fotios@redhat.com)

* Tue Nov 22 2011 Alex Boone <aboone@redhat.com> 0.82.14-1
- 

* Tue Nov 22 2011 Dan McPherson <dmcphers@redhat.com> 0.82.13-1
- need some output on ctl-app (dmcphers@redhat.com)
- Added test to attempt to SSH into all of the user's apps (fotios@redhat.com)
- Moved YAML from __END__ (fotios@redhat.com)

* Tue Nov 22 2011 Alex Boone <aboone@redhat.com> 0.82.12-1
- Use rubygem-json for RHEL5 (aboone@redhat.com)
- Degrade to Rake::GemPackageTask when Gem::PackageTask is not supported
  (aboone@redhat.com)
- Lower requirement on ruby version to 1.8.5 (aboone@redhat.com)

* Mon Nov 21 2011 Dan McPherson <dmcphers@redhat.com> 0.82.11-1
- reducing the number of messages being output for the rhc-create-app command
  (abhgupta@redhat.com)
- Moved messages to __END__. Added ssh-agent test. Moved message rendering to
  its own function (fotios@redhat.com)

* Mon Nov 21 2011 Dan McPherson <dmcphers@redhat.com>
- reducing the number of messages being output for the rhc-create-app command
  (abhgupta@redhat.com)
- Moved messages to __END__. Added ssh-agent test. Moved message rendering to
  its own function (fotios@redhat.com)

* Mon Nov 21 2011 Dan McPherson <dmcphers@redhat.com>
- reducing the number of messages being output for the rhc-create-app command
  (abhgupta@redhat.com)
- Moved messages to __END__. Added ssh-agent test. Moved message rendering to
  its own function (fotios@redhat.com)

* Sat Nov 19 2011 Dan McPherson <dmcphers@redhat.com> 0.82.8-1
- Refactored rhc-chk to use Test::Unit for tests (fotios@redhat.com)

* Sat Nov 19 2011 Dan McPherson <dmcphers@redhat.com>
- Refactored rhc-chk to use Test::Unit for tests (fotios@redhat.com)

* Thu Nov 17 2011 Dan McPherson <dmcphers@redhat.com> 0.82.6-1
- fail gracefully on ctrl+c from destroy y/n prompt (dmcphers@redhat.com)

* Wed Nov 16 2011 Dan McPherson <dmcphers@redhat.com> 0.82.5-1
- add better command details to man page (dmcphers@redhat.com)

* Tue Nov 15 2011 Dan McPherson <dmcphers@redhat.com> 0.82.4-1
- adding tidy option to rhc-ctl-app (dmcphers@redhat.com)

* Mon Nov 14 2011 Dan McPherson <dmcphers@redhat.com> 0.82.3-1
- match client and server messages (dmcphers@redhat.com)
- error sooner on app already exists (dmcphers@redhat.com)

* Sat Nov 12 2011 Dan McPherson <dmcphers@redhat.com> 0.82.2-1
- doc update (dmcphers@redhat.com)

* Thu Nov 10 2011 Dan McPherson <dmcphers@redhat.com> 0.82.1-1
- bump spec numbers (dmcphers@redhat.com)

* Wed Nov 09 2011 Dan McPherson <dmcphers@redhat.com> 0.81.14-1
- man page fixes (dmcphers@redhat.com)

* Wed Nov 09 2011 Dan McPherson <dmcphers@redhat.com> 0.81.13-1
- Automatic commit of package [rhc] release [0.81.12-1]. (aboone@redhat.com)
- Automatic commit of package [rhc] release [0.81.12-1]. (dmcphers@redhat.com)
- Bug 752341 (dmcphers@redhat.com)
- update man page with alias logic (dmcphers@redhat.com)
- Typo in message (mhicks@redhat.com)
- fix not to throw exception on ctl+c from password (dmcphers@redhat.com)

* Tue Nov 08 2011 Alex Boone <aboone@redhat.com> 0.81.12-1
- cleanup (dmcphers@redhat.com)

* Mon Nov 07 2011 Dan McPherson <dmcphers@redhat.com> 0.81.11-1
- move create app message down and ruby 1.8.6 compatibility
  (dmcphers@redhat.com)

* Sun Nov 06 2011 Dan McPherson <dmcphers@redhat.com> 0.81.10-1
- more error handling (dmcphers@redhat.com)

* Sat Nov 05 2011 Dan McPherson <dmcphers@redhat.com> 0.81.9-1
- missed an if (dmcphers@redhat.com)

* Sat Nov 05 2011 Dan McPherson <dmcphers@redhat.com> 0.81.8-1
- adding auto enable jenkins (dmcphers@redhat.com)
- hide user uuid to avoid confusion (dmcphers@redhat.com)
- rhc-chk needs to default back to id_rsa like create app (dmcphers@redhat.com)

* Fri Nov 04 2011 Dan McPherson <dmcphers@redhat.com> 0.81.7-1
- move messages to a more appropriate place (dmcphers@redhat.com)
- 749758 (dmcphers@redhat.com)
- Merge branch 'master' of github.com:openshift/os-client-tools
  (mmcgrath@redhat.com)
- Added no-dns feature (mmcgrath@redhat.com)

* Fri Nov 04 2011 Dan McPherson <dmcphers@redhat.com> 0.81.6-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (mmcgrath@redhat.com)
- Ignore alias check when no command is specified (mmcgrath@redhat.com)

* Thu Nov 03 2011 Dan McPherson <dmcphers@redhat.com> 0.81.5-1
- Merge branch 'master' of github.com:openshift/os-client-tools
  (mmcgrath@redhat.com)
- Adding alias checks (mmcgrath@redhat.com)

* Thu Nov 03 2011 Dan McPherson <dmcphers@redhat.com> 0.81.4-1
- better error handling around creating git parent (dmcphers@redhat.com)

* Fri Oct 28 2011 Dan McPherson <dmcphers@redhat.com> 0.81.3-1
- single quotes are better (dmcphers@redhat.com)
- allow actual booleans for debug and alter (dmcphers@redhat.com)
- Bug 749737 (dmcphers@redhat.com)

* Thu Oct 27 2011 Dan McPherson <dmcphers@redhat.com> 0.81.2-1
- fix doc (dmcphers@redhat.com)
- update API doc as well (dmcphers@redhat.com)
- stop passing cartridge to server for normal ctl commands (except for
  embedded) (dmcphers@redhat.com)
- Bug 749464 (dmcphers@redhat.com)

* Thu Oct 27 2011 Dan McPherson <dmcphers@redhat.com> 0.81.1-1
- bump spec number (dmcphers@redhat.com)

* Wed Oct 26 2011 Dan McPherson <dmcphers@redhat.com> 0.80.5-1
- Add better messaging around the format of the archive (dmcphers@redhat.com)

* Wed Oct 26 2011 Dan McPherson <dmcphers@redhat.com> 0.80.4-1
- bug 749097 (dmcphers@redhat.com)
- error message correction (dmcphers@redhat.com)

* Fri Oct 21 2011 Dan McPherson <dmcphers@redhat.com> 0.80.3-1
- up app name limit to 32 (dmcphers@redhat.com)

* Wed Oct 19 2011 Dan McPherson <dmcphers@redhat.com> 0.80.2-1
- add force-stop (dmcphers@redhat.com)

* Thu Oct 13 2011 Dan McPherson <dmcphers@redhat.com> 0.80.1-1
- bump spec version (dmcphers@redhat.com)

* Tue Oct 11 2011 Dan McPherson <dmcphers@redhat.com> 0.79.5-1
- Bug 739432 (dmcphers@redhat.com)
- Bug 744493 (dmcphers@redhat.com)

* Mon Oct 10 2011 Dan McPherson <dmcphers@redhat.com> 0.79.4-1
- leave timeout disabled for now (accept default) (dmcphers@redhat.com)
- bug 755660 (dmcphers@redhat.com)

* Sun Oct 09 2011 Dan McPherson <dmcphers@redhat.com> 0.79.3-1
- Bug 744369 (dmcphers@redhat.com)

* Tue Oct 04 2011 Dan McPherson <dmcphers@redhat.com> 0.79.2-1
- debug cleanups... (jim@jaguNET.com)
- Update doccos (jim@jaguNET.com)
- Make the connection timeout user configurable (jim@jaguNET.com)

* Thu Sep 29 2011 Dan McPherson <dmcphers@redhat.com> 0.79.1-1
- cleanup merge (dmcphers@redhat.com)
- add --config to man pages (dmcphers@redhat.com)
- Man pages (jim@jaguNET.com)

* Wed Sep 28 2011 Dan McPherson <dmcphers@redhat.com> 0.77.8-1
- use methods to find key to check for rhc-chk (dmcphers@redhat.com)

* Tue Sep 27 2011 Dan McPherson <dmcphers@redhat.com> 0.77.7-1
- add rhc-chk to executables and add --config option (dmcphers@redhat.com)

* Tue Sep 27 2011 Dan McPherson <dmcphers@redhat.com> 0.77.6-1
- use --config setting for updates as well as reads (dmcphers@redhat.com)

* Tue Sep 27 2011 Dan McPherson <dmcphers@redhat.com> 0.77.5-1
- add pkg to gitignore (dmcphers@redhat.com)

* Tue Sep 27 2011 Dan McPherson <dmcphers@redhat.com> 0.77.4-1
- remove rhlogin length check (dmcphers@redhat.com)
- match working names (jim@jaguNET.com)
- remove old (jim@jaguNET.com)
- and replace (jim@jaguNET.com)
- update (jim@jaguNET.com)
- fold in chcker (jim@jaguNET.com)
- Abtract out the --config path check... reuse (jim@jaguNET.com)
- Allow user to specify config-file directly via --config opt (jim@jaguNET.com)
- updated (jim@jaguNET.com)

* Mon Sep 12 2011 Dan McPherson <dmcphers@redhat.com> 0.77.3-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- Added rhc-chk (mmcgrath@redhat.com)

* Fri Sep 09 2011 Matt Hicks <mhicks@redhat.com> 0.77.2-1
- No more dev here for express client tools (jimjag@redhat.com)

* Thu Sep 01 2011 Dan McPherson <dmcphers@redhat.com> 0.77.1-1
- bump spec numbers (dmcphers@redhat.com)

* Wed Aug 31 2011 Dan McPherson <dmcphers@redhat.com> 0.76.7-1
- bz726646 patch attempt #2 (markllama@redhat.com)

* Mon Aug 29 2011 Dan McPherson <dmcphers@redhat.com> 0.76.6-1
- Revert "Revert "reverse patched to removed commit
  d34abaacc98e5b8f5387eff71064c4616a61f24b"" (markllama@gmail.com)
- Revert "reverse patched to removed commit
  d34abaacc98e5b8f5387eff71064c4616a61f24b" (markllama@redhat.com)

* Mon Aug 29 2011 Dan McPherson <dmcphers@redhat.com> 0.76.5-1
- reverse patched to removed commit d34abaacc98e5b8f5387eff71064c4616a61f24b
  (markllama@redhat.com)

* Mon Aug 29 2011 Dan McPherson <dmcphers@redhat.com> 0.76.4-1
- bz736646 - allow pty for ssh commands (markllama@redhat.com)

* Thu Aug 25 2011 Dan McPherson <dmcphers@redhat.com> 0.76.3-1
- change rsa_key_file to ssh_key_file and change not found to warning
  (dmcphers@redhat.com)

* Wed Aug 24 2011 Dan McPherson <dmcphers@redhat.com> 0.76.2-1
- add to client tools the ability to specify your rsa key file as well as
  default back to id_rsa as a last resort (dmcphers@redhat.com)

* Fri Aug 19 2011 Matt Hicks <mhicks@redhat.com> 0.76.1-1
- bump spec numbers (dmcphers@redhat.com)

* Wed Aug 17 2011 Dan McPherson <dmcphers@redhat.com> 0.75.9-1
- Another message tweak (mhicks@redhat.com)
- change wording from pull to clone (dmcphers@redhat.com)
- Adding some more information to the warning message (mhicks@redhat.com)
- Making DNS timeout non-fatal (mhicks@redhat.com)

* Wed Aug 17 2011 Dan McPherson <dmcphers@redhat.com> 0.75.8-1
- wording change (dmcphers@redhat.com)

* Tue Aug 16 2011 Dan McPherson <dmcphers@redhat.com> 0.75.7-1
- doc update (dmcphers@redhat.com)

* Tue Aug 16 2011 Dan McPherson <dmcphers@redhat.com> 0.75.6-1
- add better message to libra_id_rsa missing on the client
  (dmcphers@redhat.com)

* Tue Aug 16 2011 Dan McPherson <dmcphers@redhat.com> 0.75.5-1
- cleanup how we call snapshot (dmcphers@redhat.com)
- prepping for UUID prefixed backups (mmcgrath@redhat.com)

* Sun Aug 14 2011 Dan McPherson <dmcphers@redhat.com> 0.75.4-1
- doc updates (dmcphers@redhat.com)
- restore error handling (dmcphers@redhat.com)
- functional restore (dmcphers@redhat.com)
- Use \d regex patter for clarity pull broker and server-side api from any/all
  responses if possible protect against parse errors (jimjag@redhat.com)

* Thu Aug 11 2011 Matt Hicks <mhicks@redhat.com> 0.75.3-1
- If broker provides API and broker version, client should display
  (jimjag@redhat.com)

* Tue Aug 09 2011 Dan McPherson <dmcphers@redhat.com> 0.75.2-1
- get restore to a basic functional level (dmcphers@redhat.com)
- pub (jimjag@redhat.com)
- client-side API in req (jimjag@redhat.com)

* Mon Aug 08 2011 Dan McPherson <dmcphers@redhat.com> 0.75.1-1
- restore work in progress (dmcphers@redhat.com)

* Thu Jul 21 2011 Dan McPherson <dmcphers@redhat.com> 0.74.5-1
- doc updates (dmcphers@redhat.com)

* Mon Jul 18 2011 Dan McPherson <dmcphers@redhat.com> 0.74.4-1
- api update (dmcphers@redhat.com)
- Block it (jimjag@redhat.com)
- Adding a script to build the gem with json_pure (mhicks@redhat.com)
- force as block (jimjag@redhat.com)
- Adding the ability to force json_pure dependency (mhicks@redhat.com)

* Fri Jul 15 2011 Dan McPherson <dmcphers@redhat.com> 0.74.3-1
- bug 721296 (dmcphers@redhat.com)
- Bug 721236 (dmcphers@redhat.com)

* Tue Jul 12 2011 Dan McPherson <dmcphers@redhat.com> 0.74.2-1
- Automatic commit of package [rhc] release [0.74.1-1]. (dmcphers@redhat.com)
- bumping spec numbers (dmcphers@redhat.com)
- add options to tail-files (dmcphers@redhat.com)
- Automatic commit of package [rhc] release [0.73.14-1]. (dmcphers@redhat.com)
- add retries to login/logout and doc updates (dmcphers@redhat.com)
- Automatic commit of package [rhc] release [0.73.13-1]. (dmcphers@redhat.com)
- remove embed param passing to broker and doc updates (dmcphers@redhat.com)
- API updates (dmcphers@redhat.com)
- Automatic commit of package [rhc] release [0.73.12-1]. (dmcphers@redhat.com)
- bug 719510 (dmcphers@redhat.com)
- Remove non-tested depende (jimjag@redhat.com)
- Automatic commit of package [rhc] release [0.73.11-1]. (dmcphers@redhat.com)
- Bug 719219 (dmcphers@redhat.com)
- Automatic commit of package [rhc] release [0.73.10-1]. (dmcphers@redhat.com)
- up (jimjag@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (jimjag@redhat.com)
- force spec file to use darwin (jimjag@redhat.com)
- standardize message (dmcphers@redhat.com)
- Automatic commit of package [rhc] release [0.73.9-1]. (dmcphers@redhat.com)
- Allowing rhc-tail-files to operate on the ~/ dir instead of ~/app
  (mmcgrath@redhat.com)
- Automatic commit of package [rhc] release [0.73.8-1]. (edirsh@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- fixing mysql version in example (mmcgrath@redhat.com)
- Automatic commit of package [rhc] release [0.73.7-1]. (dmcphers@redhat.com)
- cart list fixes from embed (dmcphers@redhat.com)
- Automatic commit of package [rhc] release [0.73.6-1]. (dmcphers@redhat.com)
- cleanup (dmcphers@redhat.com)
- perf improvements for how/when we look up the valid cart types on the server
  (dmcphers@redhat.com)
- move health check path to server (dmcphers@redhat.com)
- Automatic commit of package [rhc] release [0.73.5-1]. (dmcphers@redhat.com)
- fixing merge from Dan (mmcgrath@redhat.com)
- fixed formatting and embedded display (mmcgrath@redhat.com)
- Automatic commit of package [rhc] release [0.73.4-1]. (dmcphers@redhat.com)
- handle embed or command not passed (dmcphers@redhat.com)
- Adding embedded list support (mmcgrath@redhat.com)
- Automatic commit of package [rhc] release [0.73.3-1]. (mhicks@redhat.com)
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (mhicks@redhat.com)
- allow messsages from cart to client (dmcphers@redhat.com)
- Updating to new Rake tasks to avoid deprecation warning (mhicks@redhat.com)
- Adding embed support (mmcgrath@redhat.com)
- Added embedded list (mmcgrath@redhat.com)

* Mon Jul 11 2011 Dan McPherson <dmcphers@redhat.com> 0.74.1-1
- bumping spec numbers (dmcphers@redhat.com)
- add options to tail-files (dmcphers@redhat.com)

* Thu Jul 07 2011 Dan McPherson <dmcphers@redhat.com> 0.73.14-1
- add retries to login/logout and doc updates (dmcphers@redhat.com)

* Thu Jul 07 2011 Dan McPherson <dmcphers@redhat.com> 0.73.13-1
- remove embed param passing to broker and doc updates (dmcphers@redhat.com)
- API updates (dmcphers@redhat.com)

* Thu Jul 07 2011 Dan McPherson <dmcphers@redhat.com> 0.73.12-1
- bug 719510 (dmcphers@redhat.com)
- Remove non-tested depende (jimjag@redhat.com)

* Wed Jul 06 2011 Dan McPherson <dmcphers@redhat.com> 0.73.11-1
- Bug 719219 (dmcphers@redhat.com)

* Wed Jul 06 2011 Dan McPherson <dmcphers@redhat.com> 0.73.10-1
- up (jimjag@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (jimjag@redhat.com)
- force spec file to use darwin (jimjag@redhat.com)
- standardize message (dmcphers@redhat.com)

* Tue Jul 06 2011 Jim Jagielski <jimjag@redhat.com> 0.73.10-1
- json_pure dependencies
  (mmcgrath@redhat.com)

* Tue Jul 05 2011 Dan McPherson <dmcphers@redhat.com> 0.73.9-1
- Allowing rhc-tail-files to operate on the ~/ dir instead of ~/app
  (mmcgrath@redhat.com)

* Fri Jul 01 2011 Emily Dirsh <edirsh@redhat.com> 0.73.8-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (mmcgrath@redhat.com)
- fixing mysql version in example (mmcgrath@redhat.com)

* Thu Jun 30 2011 Dan McPherson <dmcphers@redhat.com> 0.73.7-1
- cart list fixes from embed (dmcphers@redhat.com)

* Thu Jun 30 2011 Dan McPherson <dmcphers@redhat.com> 0.73.6-1
- cleanup (dmcphers@redhat.com)
- perf improvements for how/when we look up the valid cart types on the server
  (dmcphers@redhat.com)
- move health check path to server (dmcphers@redhat.com)

* Wed Jun 29 2011 Dan McPherson <dmcphers@redhat.com> 0.73.5-1
- fixing merge from Dan (mmcgrath@redhat.com)
- fixed formatting and embedded display (mmcgrath@redhat.com)
- Adding embedded list support (mmcgrath@redhat.com)

* Wed Jun 29 2011 Dan McPherson <dmcphers@redhat.com> 0.73.4-1
- handle embed or command not passed (dmcphers@redhat.com)

* Tue Jun 28 2011 Matt Hicks <mhicks@redhat.com> 0.73.3-1
- Merge branch 'master' of git1.ops.rhcloud.com:/srv/git/li (mhicks@redhat.com)
- allow messsages from cart to client (dmcphers@redhat.com)
- Updating to new Rake tasks to avoid deprecation warning (mhicks@redhat.com)
- Adding embed support (mmcgrath@redhat.com)
- Added embedded list (mmcgrath@redhat.com)

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.73.2-1
- force evaluation (jimjag@redhat.com)
- better structure... (jimjag@redhat.com)
- adjust for Fed13 and RHEL5 (no elsif?) (jimjag@redhat.com)

* Mon Jun 27 2011 Dan McPherson <dmcphers@redhat.com> 0.73.1-1
- Fed13 and RHEL5 use json_pure
- bump spec numbers (dmcphers@redhat.com)
- json_pure for 1.8.6, Darwin and Windows. Thx mhicks for the pointer!
  (jimjag@redhat.com)
- Note that others may exist... suggest -h (jimjag@redhat.com)
- cleanup for 1.8.6 (jimjag@redhat.com)
- 1.8.6 no have start_with (jimjag@redhat.com)

* Thu Jun 23 2011 Dan McPherson <dmcphers@redhat.com> 0.72.29-1
- no more need Xcode... show how (jimjag@redhat.com)

* Thu Jun 23 2011 Dan McPherson <dmcphers@redhat.com> 0.72.28-1
- 

* Thu Jun 23 2011 Dan McPherson <dmcphers@redhat.com> 0.72.27-1
- switch timeout back to 10s (dmcphers@redhat.com)

* Wed Jun 22 2011 Dan McPherson <dmcphers@redhat.com> 0.72.26-1
- trying a larger timeout (dmcphers@redhat.com)

* Wed Jun 22 2011 Dan McPherson <dmcphers@redhat.com> 0.72.25-1
- API cleanup (dmcphers@redhat.com)

* Tue Jun 21 2011 Dan McPherson <dmcphers@redhat.com> 0.72.24-1
- fix typo (dmcphers@redhat.com)

* Sat Jun 18 2011 Dan McPherson <dmcphers@redhat.com> 0.72.23-1
- test case fix (dmcphers@redhat.com)

* Fri Jun 17 2011 Dan McPherson <dmcphers@redhat.com> 0.72.22-1
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (jimjag@redhat.com)
- wrong commit/revert (jimjag@redhat.com)

* Fri Jun 17 2011 Dan McPherson <dmcphers@redhat.com> 0.72.21-1
- userland info message update... (jimjag@redhat.com)
- Allow the cartridge_post to handle invalid carts for us. (jimjag@redhat.com)

* Thu Jun 16 2011 Dan McPherson <dmcphers@redhat.com> 0.72.20-1
- add error if invalid cart sent to server (dmcphers@redhat.com)

* Wed Jun 15 2011 Dan McPherson <dmcphers@redhat.com> 0.72.19-1
- 

* Wed Jun 15 2011 Dan McPherson <dmcphers@redhat.com> 0.72.18-1
- 

* Wed Jun 15 2011 Dan McPherson <dmcphers@redhat.com> 0.72.17-1
- 

* Wed Jun 15 2011 Dan McPherson <dmcphers@redhat.com> 0.72.16-1
- 

* Wed Jun 15 2011 Dan McPherson <dmcphers@redhat.com> 0.72.15-1
- api doc updates (dmcphers@redhat.com)
- api doc updates (dmcphers@redhat.com)
- add cart_types param to cartlist call (dmcphers@redhat.com)
- No need for roundtrip if they provided cartridge.. the server will let us
  know if not accepted. (jimjag@redhat.com)
- Inform user that we need to contact the RHCloud server Handle errors from
  server in a somewhat more user-friendly way (jimjag@redhat.com)
- simple prettyfication -> ((required)) --> (required) (jimjag@redhat.com)

* Tue Jun 14 2011 Matt Hicks <mhicks@redhat.com> 0.72.14-1
- rename to make more sense... (jimjag@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (jimjag@redhat.com)
- remove pw from deconfigure on error call (dmcphers@redhat.com)
- Use as symbols (jimjag@redhat.com)
- minor fixes (dmcphers@redhat.com)
- Merge branch 'master' of ssh://git1.ops.rhcloud.com/srv/git/li
  (jimjag@redhat.com)
- method name (jimjag@redhat.com)
- minor fixes (dmcphers@redhat.com)
- parse from array (jimjag@redhat.com)
- Pass string (jimjag@redhat.com)
- No more convert (jimjag@redhat.com)
- cart_list factor returns a string now, with cartridges sep by '|'
  (jimjag@redhat.com)
- Adjust for JSON (jimjag@redhat.com)
- past one level (jimjag@redhat.com)
- and not a key (jimjag@redhat.com)
- pull in carts from result (jimjag@redhat.com)
- force debug for now (jimjag@redhat.com)
- use as boolean (jimjag@redhat.com)
- simple name change (jimjag@redhat.com)
- be consistent (jimjag@redhat.com)
- Pass debug flag (jimjag@redhat.com)
- Scoping issues (jimjag@redhat.com)
- pull into client tools cartinfo (jimjag@redhat.com)

* Fri Jun 10 2011 Matt Hicks <mhicks@redhat.com> 0.72.13-1
- give better message when running rhc-create-domain with alter first
  (dmcphers@redhat.com)

* Fri Jun 10 2011 Matt Hicks <mhicks@redhat.com> 0.72.12-1
- bug 712276 (dmcphers@redhat.com)

* Fri Jun 10 2011 Matt Hicks <mhicks@redhat.com> 0.72.11-1
- Added applicatino name (mmcgrath@redhat.com)

* Thu Jun 09 2011 Dan McPherson <dmcphers@redhat.com> 0.72.10-1
- bug 707857 (dmcphers@redhat.com)

* Thu Jun 09 2011 Matt Hicks <mhicks@redhat.com> 0.72.9-1
- Bug 706353 (dmcphers@redhat.com)
- cleanup (dmcphers@redhat.com)
- Bug 707857 (dmcphers@redhat.com)
- Bug 705703 (dmcphers@redhat.com)
- improve terminology with rhlogin in usage and man pages (dmcphers@redhat.com)

* Wed Jun 08 2011 Dan McPherson <dmcphers@redhat.com> 0.72.8-1
- 

* Wed Jun 08 2011 Dan McPherson <dmcphers@redhat.com> 0.72.7-1
- Bug 711685 (dmcphers@redhat.com)
- fix rhc-snapshot (dmcphers@redhat.com)

* Tue Jun 07 2011 Matt Hicks <mhicks@redhat.com> 0.72.6-1
- Added a curl example (mmcgrath@redhat.com)
- Adding more explicit references in API doc (mmcgrath@redhat.com)

* Fri Jun 03 2011 Matt Hicks <mhicks@redhat.com> 0.72.4-1
- fix breakge no mo pure (jimjag@redhat.com)
- revert (jimjag@redhat.com)
- Move to json/pure for client side (jimjag@redhat.com)
- Adding json string (mmcgrath@redhat.com)
- Added API returns (mmcgrath@redhat.com)
- Switching to json_pure for Mac / Windows (mhicks@redhat.com)

* Wed Jun 01 2011 Dan McPherson <dmcphers@redhat.com> 0.72.3-1
- app-uuid patch from dev/markllama/app-uuid
  69b077104e3227a73cbf101def9279fe1131025e (markllama@gmail.com)

* Tue May 31 2011 Matt Hicks <mhicks@redhat.com> 0.72.2-1
- Bug 707488 (dmcphers@redhat.com)
