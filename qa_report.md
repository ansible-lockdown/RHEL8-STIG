# QA Report: Private-RHEL8-STIG

**Date:** 2026-02-24 15:48:54  
**Branch:** benchmark_v2r6  
**Tool Version:** 2.4.2  
**Benchmark Prefix:** rhel8stig

---

## Summary

| Metric | Count |
|--------|-------|
| Total Checks | 11 |
| Passed | 9 |
| Failed | 0 |
| Warnings | 2 |
| Skipped | 0 |

---

## [PASS] YAML Lint

**Status:** PASS  
**Summary:** 0 issue(s)


---

## [PASS] Ansible Lint

**Status:** PASS  
**Summary:** 0 issue(s)


---

## [PASS] Spell Check

**Status:** PASS  
**Summary:** 0 issue(s)


---

## [PASS] Grammar Check

**Status:** PASS  
**Summary:** 0 issue(s)


---

## [WARN] Unused Variables

**Status:** WARN  
**Summary:** 19 issue(s)


| Severity | File | Line | Description |
|----------|------|------|-------------|
| warning | `tasks/Cat_2/RHEL-08-010xxx.yml` | 432 | Referenced but not defined: 'rhel8stig_010161_keytab_files' |
| warning | `tasks/Cat_2/RHEL-08-010xxx.yml` | 1094 | Referenced but not defined: 'rhel8stig_aide_cron_minute' |
| warning | `tasks/Cat_2/RHEL-08-010xxx.yml` | 1095 | Referenced but not defined: 'rhel8stig_aide_cron_hour' |
| warning | `tasks/Cat_2/RHEL-08-010xxx.yml` | 1096 | Referenced but not defined: 'rhel8stig_aide_cron_weekday' |
| warning | `tasks/Cat_2/RHEL-08-010xxx.yml` | 1097 | Referenced but not defined: 'rhel8stig_aide_cron_day' |
| warning | `tasks/Cat_2/RHEL-08-010xxx.yml` | 2427 | Referenced but not defined: 'rhel8stig_010680_nameserver_count' |
| warning | `tasks/Cat_2/RHEL-08-010xxx.yml` | 2469 | Referenced but not defined: 'rhel8stig_010690_user_path' |
| warning | `tasks/Cat_2/RHEL-08-020xxx.yml` | 618 | Referenced but not defined: 'rhel8stig_020030_lock_enabled' |
| warning | `templates/ansible_vars_goss.yml.j2` | 5 | Referenced but not defined: 'rhel8stig_os_distribution' |
| warning | `templates/ansible_vars_goss.yml.j2` | 12 | Referenced but not defined: 'rhel8stig_os_version_pre_8_2' |
| warning | `templates/ansible_vars_goss.yml.j2` | 45 | Referenced but not defined: 'rhel8stig_bootloader_path' |
| warning | `templates/ansible_vars_goss.yml.j2` | 427 | Referenced but not defined: 'rhel8stig_password_hash' |
| warning | `templates/ansible_vars_goss.yml.j2` | 436 | Referenced but not defined: 'rhel8stig_banner_file' |
| warning | `templates/ansible_vars_goss.yml.j2` | 447 | Referenced but not defined: 'rhel8stig_uses_dns' |
| warning | `templates/ansible_vars_goss.yml.j2` | 450 | Referenced but not defined: 'rhel8stig_aide_cron_file' |
| warning | `templates/ansible_vars_goss.yml.j2` | 466 | Referenced but not defined: 'rhel8stig_remotelog_port' |
| warning | `templates/ansible_vars_goss.yml.j2` | 467 | Referenced but not defined: 'rhel8stig_remotelog_protocol' |
| warning | `handlers/main.yml` | 234 | Referenced but not defined: 'rhel8stig_aide_temp_db_file' |
| warning | `handlers/main.yml` | 244 | Referenced but not defined: 'rhel8stig_overwrite_aide_db' |

---

## [WARN] Variable Naming

**Status:** WARN  
**Summary:** 7 issue(s)


| Severity | File | Line | Description |
|----------|------|------|-------------|
| warning | `tasks/Cat_1/RHEL-08-010xxx.yml` | 205 | Duplicate register variable 'discovered_crypto_policies_status' (first seen in tasks/Cat_1/RHEL-08-010xxx.yml:54) |
| warning | `tasks/Cat_2/RHEL-08-010xxx.yml` | 2515 | Duplicate register variable 'discovered_world_writable_directories' (first seen in tasks/Cat_2/RHEL-08-010xxx.yml:2488) |
| warning | `tasks/Cat_2/RHEL-08-030xxx.yml` | 271 | Duplicate register variable 'discovered_audit_log_dir' (first seen in tasks/Cat_2/RHEL-08-030xxx.yml:240) |
| warning | `tasks/Cat_2/RHEL-08-030xxx.yml` | 301 | Duplicate register variable 'discovered_audit_log_dir' (first seen in tasks/Cat_2/RHEL-08-030xxx.yml:240) |
| warning | `tasks/main.yml` | 68 | Duplicate register variable 'discovered_user_list' (first seen in tasks/Cat_2/RHEL-08-010xxx.yml:2549) |
| warning | `tasks/post_remediation_audit.yml` | 38 | Duplicate register variable 'post_audit_summary' (first seen in tasks/post_remediation_audit.yml:26) |
| warning | `tasks/pre_remediation_audit.yml` | 102 | Duplicate register variable 'pre_audit_summary' (first seen in tasks/pre_remediation_audit.yml:90) |

---

## [PASS] File Mode Quoting

**Status:** PASS  
**Summary:** 0 issue(s)


---

## [PASS] Company Naming

**Status:** PASS  
**Summary:** 0 issue(s)


---

## [PASS] Audit Template

**Status:** PASS  
**Summary:** 0 issue(s)


---

## [PASS] FQCN Usage

**Status:** PASS  
**Summary:** 0 issue(s)


---

## [PASS] Rule Coverage

**Status:** PASS  
**Summary:** 0 issue(s)


---

