# Molecule Default Scenario - requires pinned Ansible 2.16 venv

## Quick start

```bash
# One-time: create a venv pinned to Ansible 2.16 (last release that supports Python 3.6 managed nodes)
python3.11 -m venv ~/venv/ansible216
source ~/venv/ansible216/bin/activate
pip install 'ansible-core>=2.16,<2.17' 'molecule>=24,<26' 'molecule-plugins[docker]' docker passlib

# Every time: activate the venv, then run molecule
source ~/venv/ansible216/bin/activate
cd /path/to/RHEL8-STIG
molecule destroy && molecule converge && molecule converge   # full role + idempotency pass
deactivate
```

After a converge with `setup_audit: true` + `run_audit: true` + `fetch_audit_output: true` (all set in `molecule.yml` host_vars), goss audit JSONs (`*_pre_scan_*.json` and `*_post_scan_*.json`) are fetched back to the path set in `audit_output_destination` (default in this scenario: `<working-tree>/_temp_fetched_audits/`).

## Why a pinned Ansible 2.16 venv?

Ansible 2.19+ refuses to run modules on Python 3.6 - its generated `AnsiballZ` module wrapper starts with `from __future__ import annotations`, which is a `SyntaxError` on Python 3.6.

Rocky 8 / RHEL 8 ship the `dnf` Python bindings **only** for platform-python 3.6. The `python39` and `python3.11` dnf modules don't include matching `python3X-dnf` packages, and rebuilding them from source for a newer Python ABI is heavyweight.

Ansible 2.16 sidesteps the whole issue by running modules directly on platform-python 3.6, which already has the dnf bindings. This is the cleanest path to get a working molecule scenario for RHEL 8 / Rocky 8 without custom Docker images or source-rebuilt bindings.

If you use a newer Ansible (2.17+) for other roles, that's fine - just activate this scenario's venv only when running molecule for this RHEL 8 role.

## What's in the scenario

| File | Purpose |
|---|---|
| `molecule.yml` | Driver: docker. Image: `rockylinux/rockylinux:8-ubi-init` on `${MOLECULE_DOCKER_PLATFORM:-linux/arm64}`, systemd via `/usr/sbin/init`. Host vars: `ansible_python_interpreter: /usr/libexec/platform-python`, `setup_audit: true`, `run_audit: true`, `system_is_container: true`, `skip_reboot: true`, `rhel8stig_disruption_high: true`, `fetch_audit_output: true`, `audit_output_destination: <path>`. |
| `prepare.yml` | Installs supporting packages (`audit`, `aide`, `crypto-policies`, `firewalld`, `chrony`, etc.), stubs `/etc/default/grub` so GRUB-tag tasks don't fail in the container. |
| `converge.yml` | Sets root password (so PAM tasks don't lock us out), includes the role. |

## Expected results

A clean run on this scenario should produce:

| Phase | Tasks | Failed | Notes |
|---|---|---|---|
| Converge 1 | `ok=~178 changed=~72 skipped=~521` | **0** | Full remediation pass |
| Converge 2 | `ok=~174 changed=~6 skipped=~516` | **0** | Idempotency pass; ~6 changed-on-second-run are all acceptable-by-design (molecule prep, audit shells, facts file, bridge template re-render) |
| Audit POST | 278 tests | ~36 still failing | Pass rate ~87%; remaining failures are environmental (see below), not role bugs |

Zero audit regressions between Converge 1 POST and Converge 2 POST scans.

### Why ~36 failures remain (and why that's correct)

The remaining failures fall into three buckets, all expected by design:

1. **~20 SSH-config controls** (banner, ciphers, KexAlgorithms, MACs, idle timeouts, login grace time, etc.) — these check `/etc/ssh/sshd_config` content, which doesn't exist because `openssh-server` is intentionally not installed in `prepare.yml`. Running sshd inside a Docker container is a well-known anti-pattern: containers use `docker exec` (or `kubectl exec` / `aws ecs execute-command`) for shell access rather than a network-exposed SSH daemon, and bundling sshd bloats the image, increases attack surface, and complicates the PID-1 process model. The role's `when: rhel8stig_ssh_required` gate is the correct primitive; on real RHEL 8 hosts that have sshd, all 20 controls remediate correctly.

2. **~10 user-state controls** (FIPS-hashed passwords, password lifetime, dotfile audit) — these need real interactive users (UID >= 1000) with shadow entries and home-dir init files. Containers are stateless and have only system accounts (`chrony`, `polkitd`, `tss`, etc.), so the role's tasks either no-op (nothing to remediate) or hit the system accounts and partially pass. Audit still shows the controls as failing because the underlying preconditions don't hold.

3. **~6 sub-tests within mixed controls** — a single STIG_ID often has multiple goss sub-tests; some sub-tests pass while others (e.g. SELinux context queries, dmesg kernel-buffer greps) can't succeed in a container with a shared host kernel. The primary sub-test typically passes; the secondary fails on environment-bound checks.

None of these warrant fixing the role or installing more packages into prepare. They're the expected delta between a containerized test environment and a real RHEL 8 host.

## Per-environment overrides

In `molecule.yml` `host_vars`:

| Override | Default | Purpose |
|---|---|---|
| `audit_git_version` | `benchmark_{{ benchmark_version }}` (`benchmark_v2r8`) | The branch name on `RHEL8-STIG-Audit` to pull goss content from. **Not settable here** - `vars/audit.yml` sets it via `include_vars`, which outranks play and host vars, so a `host_vars` entry is inert. Pin a working QA branch for a run with `molecule converge -- --extra-vars 'audit_git_version=2026_AUG_QA_V2R8'`. |
| `audit_output_destination` | `/opt/audit_summaries/` | Where fetched JSONs land on the controller. The scenario sets this to a path under the working tree so they don't pollute system paths. |
| `rhel8stig_disruption_high` | `false` | Enable to exercise the high-disruption code paths (account locks, password lifetime resets). Safe in throwaway containers; risky on real hosts. |

## Why this can't use a newer Ansible

The fundamental constraint is unfixable without rebuilding dnf bindings from source:

| Python on managed node | dnf bindings? | Runs Ansible 2.19+ modules? |
|---|---|---|
| 3.6 (platform-python) | yes | **no** (`from __future__ import annotations` SyntaxError) |
| 3.9 (`dnf module install python39`) | **no** | yes |
| 3.11 (`dnf install python3.11`) | **no** | yes |

There is no Python on RHEL 8 / Rocky 8 that satisfies both constraints from the distro repos. The Ansible 2.16 venv is the pragmatic answer.
