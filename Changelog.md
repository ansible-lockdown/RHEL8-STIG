# Changes to RHEL8STIG

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
  - 020035 - new control idlesession timeout new var rhel_08_020035_idlesessiontimeout
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
      - RHEL-08-040283 - Updated to include find adn remove for conflicting parameters
      - RHEL-08-040284 - Updated to include find adn remove for conflicting parameters
      - RHEL-08-040285 - Updated to include find adn remove for conflicting parameters
      - RHEL-08-040286 - Updated to include find adn remove for conflicting parameters
      - RHEL-08-040340
      - RHEL-08-040341
      - RHEL-08-040400 - New control
    - CAT3
      - RHEL-08-020340 - Updated CCI
