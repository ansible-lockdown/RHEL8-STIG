# Changes to RHEL8STIG

## STIG V2R7 - 2026 August - Molecule CI, Repo QA CI and lint hygiene

Ports the CI work from the V2R8 branch onto V2R7. Every item was re-derived against this branch's own content rather than cherry-picked, because the two branches differ enough to change the answers: the noqa split is 9 dead here versus 13 on V2R8, and the QA baseline is 112 findings versus 13.

- added `.github/workflows/molecule.yml`: runs the `default` scenario end to end (create, converge, verify, destroy) on pull requests to `latest` and `benchmark*`, pushes to `latest`, a weekly schedule and manual dispatch. `idempotence` is deliberately not run - a second converge of this role is a known non-zero-change run. Goss audit JSONs upload as a build artifact but do not gate; the gate is converge finishing `failed=0`
- the Molecule workflow pins `ansible-core>=2.16,<2.17` and `molecule>=24,<26` on purpose and must not be raised: the scenario targets `/usr/libexec/platform-python` (3.6), the only interpreter on Rocky 8 / RHEL 8 carrying the `dnf` Python bindings, and Ansible 2.19+ emits an `AnsiballZ` wrapper opening with `from __future__ import annotations`, a `SyntaxError` on 3.6
- added `.github/workflows/repo_qa.yml`: runs the Ansible-Lockdown QA checker as a pass/fail gate on the same triggers, with the checker checked out at a pinned tag rather than pip-installed (several of its checks load unpackaged helpers from its `scripts/` directory at run time) and `--strict` set, without which WARN-severity regressions exit 0 and pass silently
- added `.qa_baseline.json` recording the 112 findings that exist on this branch. 97 of them are the Shell Pipefail Layout check: the `set -o pipefail` plus `args.executable` sweep landed in V2R8, not V2R7. Back-porting it here would diverge the branches for no benefit, so it is recorded rather than fixed. The baseline is keyed per finding on file plus description, so a new finding inside an already-baselined check still fails
- `collections/requirements.yml`: pinned `community.general` to 11.4.0, `community.crypto` to 2.26.0 and `ansible.posix` to 2.2.2. All three previously resolved to git HEAD. This is a run-time fix for real RHEL 8 hosts, not only for CI: `community.general` 12.0.0 and `community.crypto` 3.0.0 rewrote their modules to open with `from __future__ import annotations`, a `SyntaxError` on the target's `/usr/libexec/platform-python` (3.6), so `community.general.pamd`, `ini_file`, `sefcontext` and `community.crypto.openssh_keypair` all fail on the managed node. The same major releases raised `requires_ansible` to `>=2.17`, which this role cannot use for the same Python 3.6 reason, so one version boundary covers both
- added `molecule/default/verify.yml`. The scenario had none, which meant `molecule verify` logged `Executed: Missing playbook` and exited 0 - a pass that asserted nothing. It spot-checks `/etc/login.defs` SHA512 hashing, a populated `/etc/issue`, and the RHEL-08-040172 Ctrl-Alt-Del drop-in. The drop-in assertion is deliberately the inverse of the V2R8 branch's: V2R7 writes `55-CtrlAltDel-BurstAction`, V2R8 renames it to `...BurstAction.conf`
- `molecule/default/molecule.yml`: the container platform is now `${MOLECULE_DOCKER_PLATFORM:-linux/arm64}` instead of a hardcoded `linux/arm64`, so the same scenario runs unchanged on an Apple Silicon workstation and on amd64 CI runners
- `molecule/default/molecule.yml` and `converge.yml`: removed the inert `audit_git_version: benchmark_v2r7` pins. `tasks/prelim.yml` include_vars-es `vars/audit.yml`, which derives the value from `benchmark_version` and outranks play and host vars, so these entries never had any effect. Replaced with the `--extra-vars` form that does work
- removed 9 `# noqa` directives that suppress nothing (32 -> 23). Each was verified empirically, not by inspection: every directive was stripped, ansible-lint re-run, and only directives whose rule actually fires in that task block restored. ansible-lint output is byte-identical before and after, exit code 0. Removed: `no-changed-when` x2 (handlers/main.yml), `template-instead-of-copy` x2 and `jinja[invalid]` x1 (tasks/Cat_2/RHEL-08-010xxx.yml), `yaml[line-length]` x1 (tasks/post_remediation_audit.yml), `name[template]` x2 and `yaml[line-length]` x1 (tasks/pre_remediation_audit.yml)
- `molecule/default/README_Molecule+Ansible216.md`: the override table listed `audit_git_version` as a settable host var, which it is not; the scenario summary row still named that host var and the hardcoded platform; `verify.yml` had no entry; and the Ansible 2.16 rationale did not mention that pinning `ansible-core` alone is insufficient because the collections carry the same Python 3.6 barrier
- `CHANGELOG.md`: the V2R7 molecule entry pointed at `molecule/default/README.md`, which has never existed in this repo. Corrected to `README_Molecule+Ansible216.md`

## STIG V2R7 - 2026 May QA updates

- meta/main.yml: set author to `Ansible-Lockdown Team`; bumped `min_ansible_version` to `2.16.1`
- CONTRIBUTING.rst: rebranded to "Ansible-Lockdown Projects"
- README: refreshed requirements list (`Python 3.10+`, `Ansible 2.16+`, `python3-dnf`, `python3-libselinux`); migrated Twitter badge to X; tidied banner date
- Renamed `Changelog.md` to canonical `CHANGELOG.md`
- defaults/main.yml: documented category toggles (`rhel8stig_cat1`/`cat2`/`cat3`)
- Workflows: dropped dead schedule clause from `export_badges_private`; aligned indent in `devel_pipeline_validation`
- handlers/main.yml: cleaned `Restart auditd` name (moved `noqa` off the name to fix notify matching); removed duplicate AIDE listen block (six handlers were defined twice); corrected `warn_control_id` for AIDE check warning from a RHEL-9 ID to `RHEL-08-010360`
- templates/resolv.conf.j2: guarded `rhel8stig_resolv_domain` against null to avoid Ansible 2.19+ trap
- defaults/main.yml: set `rhel8stig_boot_superuser` default to `root` to match audit baseline
- defaults/main.yml: header documentation improvements - WARNING block on variable precedence, expanded comments for CAT toggles / disruption_high / skip_reboot / setup_audit / run_audit / get_audit_binary_method / audit_content; reorganized audit section (audit_max_concurrent grouped with run_audit); exposed `audit_bin_validate_certs` and commented `audit_bin_url_username`/`audit_bin_url_password` placeholders for self-hosted Goss
- Task naming format fixes: RHEL-08-010015 + 010455 had no PATCH segment; 040200 had doubled `HIGH | HIGH |` prefix. All restored to canonical `<SEV> | RHEL-08-NNNNNN | PATCH|AUDIT | <title>` format.
- Register-order canonicalization: moved `register:` to last position (after changed_when/failed_when/check_mode/no_log) per Lockdown convention in 8 task blocks - tasks/prelim.yml:289, tasks/Cat_2/RHEL-08-030xxx.yml:52/157/1411, tasks/Cat_2/RHEL-08-010xxx.yml:2346, tasks/Cat_2/RHEL-08-040xxx.yml:139/386/1974.
- Task name titles aligned verbatim to V2R7 XCCDF for 10 controls where the title shortened the XCCDF syscall list or used outdated wording (16 task-name occurrences total): 030200 (lremovexattr -> setxattr/fsetxattr/lsetxattr/removexattr/fremovexattr/lremovexattr), 030361 (rename -> rename/unlink/rmdir/renameat/unlinkat), 030420 (truncate -> truncate/ftruncate/creat/open/openat/...), 030480 (chown -> chown/fchown/fchownat/lchown), 030490 (chmod -> chmod/fchmod/fchmodat), 030610 (file permissions -> ISSM verification), 020014 (added "until released by admin"), 020080 (generic GUI settings -> session lock-delay override), 010201 (timeout interval -> 10-minute unresponsive), 010291 (DoD encryption -> DOD-approved encryption ciphers).
- Added molecule/default scenario (rockylinux/rockylinux:8-ubi-init, arm64) with `setup_audit: true` + `run_audit: true` + container var preset. Targets `/usr/libexec/platform-python` (the only Python on Rocky 8 / RHEL 8 with `dnf` Python bindings) and requires the `ansible216` venv (Ansible 2.16 is the last release that supports Python 3.6 as a managed-node interpreter). See `molecule/default/README_Molecule+Ansible216.md`.
- vars/is_container.yml: extended container exclusions with 31 controls that cannot work in a Docker container (kernel sysctls 010372/010375/010376/010430/010671/040281/040282/040283; net sysctls 040209-040286; kdump service 010670; interactive-user home-dir family 010720/010730/010731/010740/010741/010750). Closes container-environment failures during molecule converge.
- handlers/main.yml: `Restart_systemd_login` handler now gated by `when: not system_is_container` (systemd-logind is masked in containers).
- Molecule full converge verified: ok=199 changed=75 failed=0 on first pass; ok=191 changed=5 failed=0 on idempotency pass; goss audit pass rate 63.3% PRE -> 83.0% POST (60 controls remediated); zero audit regressions between converges.
- vars/is_container.yml: extended exclusions with 11 more controls that fundamentally can't be remediated/audited in containers: 010030 (LUKS/cryptsetup), 010420 (dmesg NX kernel buffer), 030655 (auditctl - audit kernel subsystem), 040101 (firewalld runtime), 040110 (NetworkManager wifi), 040160 (sshd service runtime state), 010385 (state:absent on /etc/pam.d/sudo - minimal images lack the file), 020270/020320/040090/040400 (manual-check controls). Audit POST pass rate now 87.1% (was 83.0% pre-fix).
- Final verification QA findings: fixed 5-digit ID typo `RHEL-08-20150` -> `RHEL-08-020150` in tasks/Cat_2/RHEL-08-020xxx.yml task name (tag and toggle were already correct); removed 9 stale toggle entries from vars/is_container.yml (020039/020040/020041/020070/010560/030210/030220/030230/030240 - none exist in V2R7 XCCDF or defaults/main.yml); added `when: not system_is_container` gate to `Restart firewalld` handler (matches pattern used by Restart_systemd_login, Restart auditd, etc.).
- tasks/prelim.yml `PRELIM | Find all sudoers files` task: added `rhel8stig_010455` to the `when:` clause (was gated only on `rhel8stig_010380 or rhel8stig_010381`). When `disruption_high: true` is set and 010455 fires but the prelim was skipped, the downstream `loop: prelim_sudoers_files.stdout_lines` errored with `'dict object' has no attribute 'stdout_lines'`. Surfaced only when molecule was run with `disruption_high: true` and 010380/010381's `using_password_auth` gate was false. Audit pass rate +0.3pp (010455 SELinux sudo sub-test now passes).
- molecule/default/molecule.yml + converge.yml: replaced hardcoded user-specific `audit_output_destination` path (`/Users/frederickw/...`) with portable `{{ lookup('env', 'MOLECULE_PROJECT_DIRECTORY') }}/../_temp_fetched_audits/`; aligned `rhel8stig_disruption_high: true` in converge.yml vars to match molecule.yml host_vars; added `fetch_audit_output` + `audit_output_destination` to converge.yml so direct-run (`ansible-playbook converge.yml`) behaves the same as molecule-driven runs.
- molecule/default: flipped `audit_git_version: 2026_MAY_QA_V2R7` -> `benchmark_v2r7` in both molecule.yml and converge.yml, removed POST-MERGE TODO comments (RHEL8-STIG-Audit PR #65 merged the QA branch into benchmark_v2r7). Molecule converge against the merged audit branch verified identical to pre-merge QA branch: ok=185 changed=72 failed=0 on converge 1, ok=181 changed=6 failed=0 on idempotency, audit POST pass rate 87.4%, zero C1->C2 regressions.
- Fixed 3 AUDIT-named tasks that violated the read-only contract by actually modifying state (renamed AUDIT->PATCH): 010370 "Dnf Default" sub-task (uses lineinfile to write gpgcheck=1), 010700 "Set permissions" sub-task (uses file: to set owner on world-writable dirs), 040209 "Remove conflicting instances" sub-task (uses lineinfile state:absent to strip conflicting sysctl entries). Naming bugs only; behavior unchanged.
- defaults/main.yml: reverted `rhel8stig_boot_superuser` default `root` -> `bootloader_admin`. The recent change to `root` made the role hard-fail on real RHEL 8 hosts because the assertion at `tasks/main.yml:60-74` requires the value NOT match any existing `/etc/passwd` entry; `root` always exists on real systems. Container test wasn't catching it because `is_container.yml` gates `rhel8stig_010141`/`010149` off, skipping the assertion. Audit-side default flipped to match (see RHEL8-STIG-Audit commit afe5bbf).

## STIG v2r7

### Benchmark upgrade V2R7 (01 Apr 2026)

- Updated benchmark_version to v2r7 in defaults/main.yml
- Updated README to reference V2R7 release
- Updated SV-* revision tags for 26 rules with new revision numbers
- Promoted 6 rules from CAT2 to CAT1 (medium -> high severity):
  - RHEL-08-010275 (SV-279931) - DOD-approved encryption in bind package
  - RHEL-08-010280 (SV-279930) - IP tunnels FIPS 140-3 cryptographic algorithms
  - RHEL-08-010290 (SV-230251) - SSH server MACs FIPS 140-2 validated algorithms
  - RHEL-08-010291 (SV-230252) - SSH server DOD-approved encryption ciphers
  - RHEL-08-010296 (SV-272482) - SSH client MACs FIPS 140-3 validated algorithms
  - RHEL-08-010297 (SV-272483) - SSH client ciphers FIPS 140-3 validated algorithms
- Demoted 1 rule from CAT1 to CAT2 (high -> medium severity):
  - RHEL-08-040010 (SV-230492) - EPEL repository packages

## STIG v2r6

### May26 Alignment
- fixed meta references
- added check mode
- removed old unused items
- no log added
- company naming aligned
- var naming aligned
- aide logic
- audit improvements
- linting
- removed vars not required

### Feb 2026 QA

- Updated benchmark version
- Lic Year update
- Branding update on .j2's
- Updated discovered vars tasks naming to be unique
- Updated .github workflows to standard
- Fixed handler typo `rRstart sssd` -> `Restart sssd` in Cat_2/RHEL-08-020xxx (020016)
- Fixed goss audit variable mismatch RHEL_08_010381 mapped to wrong toggle (010380 -> 010381)
- Fixed goss audit variable mismatch RHEL_08_030690 mapped to wrong toggle (030090 -> 030690)
- Removed deprecated `verbosity` option from `.ansible-lint`
- Fixed 8 double-space grammar issues in Cat_2 task names
- Removed unused regex variables from `vars/main.yml` (rhel8stig_regexp_quoted_params, rhel8stig_replace_quoted_params, rhel8stig_service_started)
- Renamed 5 non-standard register variables to `discovered_*` prefix convention in `prelim.yml`
- Verified all 366 rules against V2R6
- Aligned defaults/main.yml and goss template with RHEL8-STIG-Audit vars/STIG.yml
- 010180 - removed from defaults and goss template (no remediation task existed; originally merged into 010700)
- 040060 - removed rule toggle from defaults and goss template (no remediation task existed; rhel8stig_epel_required retained under 040010 where it is used)
- 040342 - removed from defaults, goss template, and remediation task in Cat_2/RHEL-08-040xxx.yml (not in V2R6; KEX handled by crypto-policies); rhel8stig_ssh_kex variable removed

### CAT1
- 010015 - new control - crypto-policies
- 010020 - new requirements - rewrite - Crypto FIPS
- 010270 - new - Crypto FIPS
- 040010 - rsh-server changed to EPEL
- 040172 - updated to drop in file

### CAT2
- 010275 - new - bind - crypto
- 010280 - new - ipsec - crypto
- 010287 - removed
- 010293 - removed
- 010294 - removed
- 010295 - removed
- 010296 - updated
- 010297 - updated
- 010350 - changed to root owner
- 010455
- 010572 - ignore vfat
- 010580 - ignore vfat
- 010630
- 010640
- 010660 - removed
- 010670
- 010671 - dropin file
- 010672 - not required if kdump disabled
- 010673 - not required if kdump disabled
- 010674 - not required if kdump disabled
- 010675 - not required if kdump disabled
- 020000 - removed as duplicate of 020270
- 020060 - 10 min timeout
- 020360 - new - shell session TMOUT 10 min inactivity
- 030655 - new - audit cron scripts/executables (added in v2r4, aligned for v2r6)
- 040282 - dropin file
- 040285 - dropin file

### CAT 3

- 010472 - new - rng-tools package installed
- 020340 - removed

## 5.0.0 STIG v2r4

RuleIDs updated for listed controls after changes

- RHEL-08-010330, RHEL-08-010340, RHEL-08-010350
- Added “/usr/lib64” to Check and Fix Text paths.
- RHEL-08-010380 - Updated sudoers “NOPASSWD” Check Text command.
- RHEL-08-010381 - Updated Check Text command to split the search for “NOPASSWD” and “!authenticate”
- RHEL-08-010382 - Updated sudoers “ALL” Check Text command.
- RHEL-08-010741 - Updated finding text.
- RHEL-08-030610 - Adjusted to change rules.d file thanks to @platymatt
- RHEL-08-030655 - Added requirement to audit any script or executable called by cron as root or by any privileged user.
- RHEL-08-040030 - Updated Check command.
- RHEL-08-040310 - Updated the Discussion to include “aide.conf” monitoring explanation and updated the Check to require the SA to review the “aide.conf” manually.
- QA Linting Fixes
- Revamp 08-01010
- Removed boot_partition premlim var

## STIG v2r3

Complete lint update
Updated handlers to start with upper case
separated controls to group numbers
removed conditionals if pkg - to give OK instead of skipped
separated many control to their own task
Added warning list to end of play
Renamed control variables to correct format
auditd logic updated
sssd prelim warning now added to warning summary
bootloader - 010020 UUID logic updated
010423 fixed and 010660 updated
audit alignment
mount logic rewrite
- RHEL-08-101030 - Moved to CAT1
- RHEL-08-010296 - Added Client ssh MACs control.
- RHEL-08-010297 - Added Client ssh Cipher control.
- RHEL-08-010455 - Added requirement.
- RHEL-08-020103 - removed
- RHEL-08-020104 - removed

## STIG v2r2

RuleIDs updated for listed controls after changes in control

- RHEL-08-010030 - moved from CAT2 to CAT1 control
- RHEL-08-010130 - hashing round increase min from 5000 to 100000
- RHEL-08-010290 - MAC reordered
- RHEL-08-010291 - Ciphers reordered
- RHEL-08-010292 - RuleID
- RHEL-08-010680 - RuleID

## 4.0.0 STIG v2r1

RuleIDs updated for all controls
Nist Control ID associations added

- RHEL-08-010350 - command updated
- RHEL-08-010472 - Not Applicable if fips
- RHEL-08-020035 - version 8.7+
- RHEL-08-020039 RHEL-08-020040 RHEL-08-020041 RHEL-08-020042, RHEL-08-020070 - TMUX removed
- RHEL-08-020220, RHEL-08-020221 - remember not required for PAM
- RHEL-08-020320 - Updated Check and Fix
- RHEL-08-030603, RHEL-08-040139, RHEL-08-040140, RHEL-08-040141 - Rules updated Ok if no USB peripherals
- RHEL-08-040284
- RHEL-08-040370
- RHEL-08-010001 - removed as not a NIST value

Min OS version updated to 2.10

workflow updates

## 3.3 STIG V1R14

- #232 - thanks to  @eday87 @BJSmithIEEE
- #298 thanks to @mikefrompsu
- #299 thanks to @cpu010100
- thanks to @dglinder
  - #301
  - #302
- ansible config update

- Added gui discovery option
updated ruleids

- CAT I
  - RHEL-08-020330 - cat1
- CAT II
  - RHEL-08-010040
  - RHEL-08-010070
  - RHEL-08-010200
  - RHEL-08-010201
  - RHEL-08-010423
  - RHEL-08-010520
  - RHEL-08-010521
  - RHEL-08-010522
  - RHEL-08-010550
  - RHEL-08-010830
  - RHEL-08-020350
  - RHEL-08-040161
  - RHEL-08-040340
  - RHEL-08-040341

## 3.3 - STIG V1R13 - 24th Jan 2024

- updated audit variables
- workflow updates
- #277 thanks to @BJSmithIEEE
- #278 thanks to @prestonSeaman2
- #299 thanks to @derekbentson
- removed dependency on jmespath
- updated 010120 prelim and idempotency

## 3.2 - STIG V1R13 - 24th Jan 2024

- Audit updated
  - moved audit into prelim
  - updates to audit logic for copy and archive options

ruleid updated

- 010001
- 020250
- 020290
- 040090

CAT II

- 020035 - updated rule and added handler for logind restart
- 040020 - /bin/false update and ruleid update
- 040080 - /bin/false and ruleid
- 040111 - /bin/false and ruleid

CAT III

- 040021 - /bin/false and ruleid
- 040022 - /bin/false and ruleid
- 040023 - /bin/false and ruleid
- 040024 - /bin/false and ruleid
- 040025 - /bin/false and ruleid
- 040026 - /bin/false and ruleid

## 3.1 - STIG V1R12 - 25th Oct 2023

ruleid updated

- 010020
- 010471
- 030741
- 030742
- 040400

- added SSH validation
- added ansible_facts for variable usage

- AUDIT
  - Audit_only ability now added to run standalone audit
    - audit_only: true
  - Related Audit repo updated to improve tests audit binary(goss updated to latest version)

## 3.0.3 - Stig V1R11 - 26th July 2023

- updates to collections since galaxy updated
- updates to audit

- #229 thanks to @JacobBuskirk

## 3.0.2 - Stig V1R11 - 26th July 2023

- workflow and pipeline updates
- links updates in documentation
- #222 thanks to @BJSmithIEEE
- #226 thanks to @jmalpede
- lint config updates
- lint updates
- precommit added and configured

### 3.0.1 - Stig V1R11 - 26th July 2023

Issues:

- [#207](https://github.com/ansible-lockdown/RHEL8-STIG/issues/207)
- [#208](https://github.com/ansible-lockdown/RHEL8-STIG/issues/208)
- [#209](https://github.com/ansible-lockdown/RHEL8-STIG/issues/209)
- [#210](https://github.com/ansible-lockdown/RHEL8-STIG/issues/210)
- [#211](https://github.com/ansible-lockdown/RHEL8-STIG/issues/211)
- [#212](https://github.com/ansible-lockdown/RHEL8-STIG/issues/212)

### 3.0.0

Controls updated

- CAT2:
  - 010030 - ruleid
  - 010200 - ruleid
  - 010201 - ruleid
  - 010290 - ruleid and SSH MACS updated
  - 010291 - ruleid and SSH Ciphers updated
  - 010770 - ruleid
  - 020035 - new control idlesession timeout new var idlesessiontimeout
  - 020041 - ruleid and tmux script update
  - 030690 - ruleid and protocol options added
  - 040159 - ruleid
  - 040160 - ruleid
  - 040342 - ruleid and SSH KEX algorithms updated

- CAT3
  - 010471 - ruleid

- audit variables updated, new version
- tidied up the end of the playbook ordering with reboot taking place(if set and enabled) prior to audit now.

## 2.9.2

- #216 check that sudo user has a password check improvement
  - thanks to manish on discord for highlighting this

## 2.9.1

- Issue #204 address
  - tidy up of prelim
- update to allow against container
  - vars/is_container.yml updated and aligned
- prelim fqcn

## 2.9.0 Stig V1R10 27th April 2023

- Added new controls
  - RHEL-08-10019
  - RHEL-08-10358
- updated control IDs
  - RHEL-08-10360
  - RHEL-08-10540
  - RHEL-08-10541
  - RHEL-08-10544
  - RHEL-08-10800
  - RHEL-08-20040
  - RHEL-08-20100
  - RHEL-08-20101
  - RHEL-08-20102
  - RHEL-08-20103
  - RHEL-08-20220
  - RHEL-08-20221
  - RHEL-08-20270
  - RHEL-08-30070
  - RHEL-08-40150

- OracleLinux tested and added

## Release 2.8.6

- [#194](https://github.com/ansible-lockdown/RHEL8-STIG/issues/194) thanks to @JacobBuskirk
- [#196](https://github.com/ansible-lockdown/RHEL8-STIG/issues/196) thanks to @jmalpede

- [#195](https://github.com/ansible-lockdown/RHEL8-STIG/pull/195) thanks to PoundsOfFlesh
- [#197](https://github.com/ansible-lockdown/RHEL8-STIG/pull/197) thanks to PoundsOfFlesh

## Release 2.8.5

- updated to /var/log mount check
- added commnets for /mnt and removeable media on Azure systems

## Release 2.8.4

- ansible version updated to 2.10.1 minimum
- updated to ansible user check for passwd rule 010380
  - thanks to discord community member PoundsOfFlesh
- update readme layout and latest audit example
- changed disruptive back to false to allow users to control the settings

## Release 2.8.3

- improvements to openssh configs and seperated tasks

## Release 2.8.2

- updates to pamd logic thanks to @JacobBuskirk for highlighting

 Also following issues/PRs

- #168
- #169
- #170
- #171
- #172
- #177
- #178
- #179
- #180
- #181

## Release 2.8.0

- updates to workflow
  - ami
  - update to actions to latest versions
  - update_galaxy workflow added
- README alignment
- ansible.cfg added showing how tested
- audit template updated
- moved warnihg statements arounf for reboot

- RULEID reference updated
- 010510 rule no longer required
- 010671 improvement
- 020040 loop added
- 040090 - var typo fixed
- 040342 new control for FIP_KEX Algorithms
  - new FIPS_KEX_ALGO variable

## Release 2.7.0

- lint updates
- Benchmark 1.8 Updates
  - New RULEID for the following, plus additional notes if needed
    - CAT1
      - RHEL-08-010000
    - CAT2
      - RHEL-08-010040
      - RHEL-08-010090
      - RHEL-08-010200 - Updated keep alive count max to 1
      - RHEL-08-010201
      - RHEL-08-010360
      - RHEL-08-010372 - Updated to include find and remove for conflicting parameters
      - RHEL-08-010373 - Updated to include find and remove for conflicting parameters
      - RHEL-08-010373 - Updated to include find and remove for conflicting parameters
      - RHEL-08-010374 - Updated to include find and remove for conflicting parameters
      - RHEL-08-010375 - Updated to include find and remove for conflicting parameters
      - RHEL-08-010376 - Updated to include find and remove for conflicting parameters
      - RHEL-08-010383
      - RHEL-08-010384
      - RHEL-08-010430 - Updated to include find and remove for conflicting parameters
      - RHEL-08-010400
      - RHEL-08-010500
      - RHEL-08-010510
      - RHEL-08-010520
      - RHEL-08-010521
      - RHEL-08-010522
      - RHEL-08-010550
      - RHEL-08-010671
      - RHEL-08-010830
      - RHEL-08-020330
      - RHEL-08-020090
      - RHEL-08-020104
      - RHEL-08-020110
      - RHEL-08-020120
      - RHEL-08-020130
      - RHEL-08-020140
      - RHEL-08-020150
      - RHEL-08-020160
      - RHEL-08-020170
      - RHEL-08-020190
      - RHEL-08-020221
      - RHEL-08-020230
      - RHEL-08-010280
      - RHEL-08-020300
      - RHEL-08-020350 - Updated CCI
      - RHEL-08-020352
      - RHEL-08-040127 - Added tasks to deal with different versions of RHEL8
      - RHEL-08-040161
      - RHEL-08-040209 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040210 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040220 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040230 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040239 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040240 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040249 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040250 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040259 - Updated to included find and remove for conflicting parameters
      - RHEL-08-040260 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040261 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040262 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040270 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040279 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040280 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040281 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040282 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040283 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040284 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040285 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040286 - Updated to include find and remove for conflicting parameters
      - RHEL-08-040340
      - RHEL-08-040341
      - RHEL-08-040400 - New control
    - CAT3
      - RHEL-08-020340 - Updated CCI
