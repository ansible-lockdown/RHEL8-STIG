# RHEL 8 DISA STIG

## Configure a RHEL8 based system to be complaint with Disa STIG

This role is based on RHEL 8 DISA STIG: [Version 1, Rel 10 released on April 24, 2023](https://dl.dod.cyber.mil/wp-content/uploads/stigs/zip/U_RHEL_8_V1R10_STIG.zip).

---

![Org Stars](https://img.shields.io/github/stars/ansible-lockdown?label=Org%20Stars&style=social)
![Stars](https://img.shields.io/github/stars/ansible-lockdown/rhel8-stig?label=Repo%20Stars&style=social)
![Forks](https://img.shields.io/github/forks/ansible-lockdown/rhel8-stig?style=social)
![followers](https://img.shields.io/github/followers/ansible-lockdown?style=social)
[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/AnsibleLockdown.svg?style=social&label=Follow%20%40AnsibleLockdown)](https://twitter.com/AnsibleLockdown)

![Ansible Galaxy Quality](https://img.shields.io/ansible/quality/56380?label=Quality&&logo=ansible)
![Discord Badge](https://img.shields.io/discord/925818806838919229?logo=discord)

![Devel Build Status](https://img.shields.io/github/actions/workflow/status/ansible-lockdown/rhel8-stig/linux_benchmark_testing.yml?label=Devel%20Build%20Status)
![Devel Commits](https://img.shields.io/github/commit-activity/m/ansible-lockdown/rhel8-stig/devel?color=dark%20green&label=Devel%20Branch%20commits)

![Release Branch](https://img.shields.io/badge/Release%20Branch-Main-brightgreen) 
![Main Build Status](https://img.shields.io/github/actions/workflow/status/ansible-lockdown/rhel8-stig/linux_benchmark_testing.yml?label=Build%20Status)
![Main Release Date](https://img.shields.io/github/release-date/ansible-lockdown/rhel8-stig?label=Release%20Date)
![Release Tag](https://img.shields.io/github/v/tag/ansible-lockdown/rhel8-stig?label=Release%20Tag&&color=success)

![Issues Open](https://img.shields.io/github/issues-raw/ansible-lockdown/rhel8-stig?label=Open%20Issues)
![Issues Closed](https://img.shields.io/github/issues-closed-raw/ansible-lockdown/rhel8-stig?label=Closed%20Issues&&color=success)
![Pull Requests](https://img.shields.io/github/issues-pr/ansible-lockdown/rhel8-stig?label=Pull%20Requests)

![License](https://img.shields.io/github/license/ansible-lockdown/rhel8-stig?label=License)

---

## Looking for support?

[Lockdown Enterprise](https://www.lockdownenterprise.com#GH_AL_RH8_stig)

[Ansible support](https://www.mindpointgroup.com/cybersecurity-products/ansible-counselor#GH_AL_RH8_stig)

### Community

On our [Discord Server](https://discord.io/ansible-lockdown) to ask questions, discuss features, or just chat with other Ansible-Lockdown users

---

Configure a RHEL/Rocky 8 system to be DISA STIG compliant.
Non-disruptive CAT I, CAT II, and CAT III findings will be corrected by default.
Disruptive finding remediation can be enabled by setting `rhel8stig_disruption_high` to `true`.

## Updating

Coming from a previous release.

As with all releases and updates, It is suggested to test and align controls.
This contains rewrites and ID reference changes as per STIG documentation.

## Auditing

This can be turned on or off within the defaults/main.yml file with the variable rhel7cis_run_audit. The value is false by default, please refer to the wiki for more details. The defaults file also populates the goss checks to check only the controls that have been enabled in the ansible role.

This is a much quicker, very lightweight, checking (where possible) config compliance and live/running settings.

A new form of auditing has been developed, by using a small (12MB) go binary called [goss](https://github.com/goss-org/goss) along with the relevant configurations to check. Without the need for infrastructure or other tooling.
This audit will not only check the config has the correct setting but aims to capture if it is running with that configuration also trying to remove [false positives](https://www.mindpointgroup.com/blog/is-compliance-scanning-still-relevant/) in the process.

## Documentation

- [Read The Docs](https://ansible-lockdown.readthedocs.io/en/latest/)
- [Getting Started](https://www.lockdownenterprise.com/docs/getting-started-with-lockdown#GH_AL_RH8_stig)
- [Customizing Roles](https://www.lockdownenterprise.com/docs/customizing-lockdown-enterprise#GH_AL_RH8_stig)
- [Per-Host Configuration](https://www.lockdownenterprise.com/docs/per-host-lockdown-enterprise-configuration#GH_AL_RH8_stig)
- [Getting the Most Out of the Role](https://www.lockdownenterprise.com/docs/get-the-most-out-of-lockdown-enterprise#GH_AL_RH8_stig)

## Requirements

- RHEL/Rocky/AlmaLinux/OL 8 - Other versions are not supported.
- Other OSs can be checked by changing the skip_os_check to true for testing purposes.
- Access to download or add the goss binary and content to the system if using auditing. options are available on how to get the content to the system.

## Dependencies

The following packages must be installed on the controlling host/host where ansible is executed:

- python2-passlib (or just passlib, if using python3)
- python-lxml
- python-xmltodict
- python-jmespath

Package 'python-xmltodict' is required if you enable the OpenSCAP tool installation and run a report. Packages python(2)-passlib and python-jmespath are required for tasks with custom filters or modules. These are all required on the controller host that executes Ansible.

## Role Variables

This role is designed that the end user should not have to edit the tasks themselves. All customizing should be done via the defaults/main.yml file or with extra vars within the project, job, workflow, etc.

### Tags

There are many tags available for added control precision. Each control has it's own set of tags noting the control number as well as what parts of the system that control addresses.

Below is an example of the tag section from a control within this role. Using this example if you set your run to skip all controls with the tag ssh, this task will be skipped. The
opposite can also happen where you run only controls tagged with ssh.

```sh
tags:
    - RHEL-08-010050
    - ssh
    - dod_logon_banner
```

### Example Audit Summary

This is based on a vagrant image with selections enabled. e.g. No Gui or firewall.
Note: More tests are run during audit as we check config and running state.

```sh
ok: [rocky8_efi] => 
  msg:
  - 'The pre remediation results are: Count: 804, Failed: 416, Duration: 6.488s.'
  - 'The post remediation results are: Count: 804, Failed: 28, Duration: 68.687s.'
  - Full breakdown can be found in /opt

PLAY RECAP ****************************************************************************************************************
rocky8_efi                 : ok=482  changed=269  unreachable=0    failed=0    skipped=207  rescued=0    ignored=0   
```

## Branches

- **devel** - This is the default branch and the working development branch. Community pull requests will pull into this branch
- **main** - This is the release branch
- **reports** - This is a protected branch for our scoring reports, no code should ever go here
- **gh_pages** - github pages
- **all other branches** - Individual community member branches

## Containers - testing

- system_is_container

This is set to false by defaults/main.yml
If discovered it is a container type or ansible_connection == docker it will convert to run to with with true.
Some controls will skip is this is true as they are not applicable at all. Others runs a subset of controls found in vars/is_container.yml based on a vendor supplied un altered image.

**NON altered vendor image.**

- container_vars_file: is_container.yml

This vars file runs controls are grouped into tags so if the container does later have ssh it could be re-enabled by loading an alternative vars file.

## Community Contribution

We encourage you (the community) to contribute to this role. Please read the rules below.

- Your work is done in your own individual branch. Make sure to Signed-off and GPG sign all commits you intend to merge.
- All community Pull Requests are pulled into the devel branch
- Pull Requests into devel will confirm your commits have a GPG signature, Signed-off, and a functional test before being approved
- Once your changes are merged and a more detailed review is complete, an authorized member will merge your changes into the main branch for a new release.

## Pipeline Testing

uses:

- ansible-core 2.12
- ansible collections - pulls in the latest version based on requirements file
- runs the audit using the devel branch
- This is an automated test that occurs on pull requests into devel

## Known Issues

If adopting stig rule RHEL-08-040134

This will affect cloud init as per [bug 1839899](https://bugs.launchpad.net/cloud-init/+bug/1839899)

## Support

This is a community project at its core and will be managed as such.

If you would are interested in dedicated support to assist or provide bespoke setups

- [Ansible Counselor](https://www.mindpointgroup.com/products/ansible-counselor-on-demand-ansible-services-and-consulting/)
- [Try us out](https://engage.mindpointgroup.com/try-ansible-counselor)

## Credits

This repo originated from work done by [Sam Doran](https://github.com/samdoran/ansible-role-stig)
