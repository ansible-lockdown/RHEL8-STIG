RHEL 8 DISA STIG
================

[![pipeline status](https://gitlab.com/mindpointgroup/lockdown-enterprise/rhel-8-stig/badges/master/pipeline.svg)](https://gitlab.com/mindpointgroup/lockdown-enterprise/rhel-8-stig/commits/master)

Configure a RHEL 8 system to be DISA STIG compliant. All findings will be audited by default. Non-disruptive CAT I, CAT II, and CAT III findings will be corrected by default. Disruptive finding remediation can be enabled by setting `rhel8stig_disruption_high` to `yes`.

This role is based on RHEL 8 DISA STIG: [Version 1, Rel .01 released on May 11, 2020](https://dl.dod.cyber.mil/wp-content/uploads/stigs/zip/U_RHEL_8_V1R0-1_IDraftSTIG.zip).

Requirements
------------

RHEL 8 or CentOS 8 - Other versions are not supported.


Dependencies
------------

The following packages must be installed on the controlling host/host where ansible is executed:

- python2-passlib (or just passlib, if using python3)
- python-lxml
- python-xmltodict
- python-jmespath

Package 'python-xmltodict' is required if you enable the OpenSCAP tool installation and run a report. Packages python(2)-passlib and python-jmespath are required for tasks with custom filters or modules. These are all required on the controller host that executes Ansible.


Role Variables
--------------

| Name              | Default Value       | Description          |
|-------------------|---------------------|----------------------|
| `rhel8stig_oscap_scan` | `no` | Install and run an OpenSCAP report before and after the application of this role        |
| `rhel8stig_cat1_patch` | `yes` | Correct CAT I findings        |
| `rhel8stig_cat2_patch` | `yes`  | Correct CAT II findings       |
| `rhel8stig_cat3_patch` | `yes`  | Correct CAT III findings      |
| `rhel_07_######` | [see defaults/main.yml](./defaults/main.yml)  | Individual variables to enable/disable each STIG ID. |
| `rhel8stig_gui` | `no` | Whether or not to run tasks related to auditing/patching the desktop environment |
| `rhel8stig_system_is_router` | `no` | Run tasks that disable router functions. |
| `rhel8stig_time_service` | `chronyd` | Set to `ntpd` or `chronyd`. |
| `rhel8stig_firewall_service` | `firewalld` | Set to `firewalld` or `iptables`. |
| `rhel8stig_tftp_required` | `no` | If set to `no`, remove `tftp` client and server packages. |
| `rhel8stig_bootloader_password` | `Boot1tUp!` | GRUB2 bootloader password. This should be stored in an Ansible Vault. |
| `rhel8stig_boot_superuser` | `root` | Used to set the boot superuser in the GRUB2 config. |
| `rhel8stig_aide_cron` | [see defaults/main.yml](./defaults/main.yml) | AIDE Cron settings |
| `rhel8stig_maxlogins` | `10` | Set maximum number of simultaneous system logins (RHEL-07-040000) |
| `rhel8stig_logon_banner` | [see defaults/main.yml](./defaults/main.yml) | Logon banner displayed when logging in to the system. Defaults to nicely formatted standard logon banner. |
| `rhel8stig_password_complexity` | see below for specific settings | Dictionary of password complexity settings |
| `rhel8stig_password_complexity.ucredit` | `-1` | Minimum number of upper-case characters to be set in a new password - expressed as a negative number.  |
| `rhel8stig_password_complexity.lcredit` | `-1` | Minimum number of lower-case characters to be set in a new password - expressed as a negative number.  |
| `rhel8stig_password_complexity.dcredit` | `-1` | Minimum number of numeric characters to be set in a new password - expressed as a negative number.  |
| `rhel8stig_password_complexity.ocredit` | `-1` | Minimum number of special characters to be set in a new password - expressed as a negative number.  |
| `rhel8stig_password_complexity.difok` | `8` | Minimum number of characters in new password that must not be present in the old password.  |
| `rhel8stig_password_complexity.minclass` | `4` | Minimum number of required classes of characters for the new password. (digits, upper, lower, other)  |
| `rhel8stig_password_complexity.maxrepeat` | `3` | Maximum number of allowed same consecutive characters in a new password. |
| `rhel8stig_password_complexity.maxclassrepeat` | `4` | Maximum number of allowed same consecutive characters in the same **class** in the new password. |
| `rhel8stig_password_complexity.minlen` | `15` | Minimum number of characters in a new password. |
| `rhel8stig_shell_session_timeout` | `file: /etc/profile` `timeout: 600` | Dictionary of session timeout setting and file (TMOUT setting can be set in multiple files) |
| `rhel8stig_interactive_uid_start` | `1000` | Interactive user start point (UID_MIN) from /etc/login.defs |
| `rhel8stig_ntp_server_name: server.name` | `server.name` | The NTP Server Name |
| `rhel8stig_custom_firewall_zone` | `new_fw_zone` | The name of the new firewalld zone created to meet STIG requirements |
| `rhel8stig_fapolicy_white_list` | `LIST` | This is a list of the whitelist for the fapolicy controls, must end with deny all all |
| `rhel8stig_sshd_compression` | `no` | The Compression parameter in /etc/ssh/sshd_config needs to be set to no or delayed |
| `rhel8stig_path_to_sshkey` | `/root/.ssh/` | Custom path to the ssh key |
| `rhel8stig_hashing_rounds` | `5000` | The rounds parameter goes into pamd configs and needs to be set to now lower than 5000 |
| `rhel8stig_dns_servers` | `9.9.9.9 and 149.112.112.112` | To conform to STIG standards you need two DNS servers, parameter is in list form |
| `rhel8stig_nfs_mounts` | `vars` | NFS file system mounts pull automatcially with prelim task |
| `rhel8stig_nfs_mounts_query` | `[?starts_with(fstype, 'nfs')].mount` | The query for mounts |


Example Playbook
----------------

    - hosts: servers
      roles:
          - role: rhel-8-stig
            when:
                - ansible_os_family == 'RedHat'
                - ansible_distribution_major_version | version_compare('8', '=')

