#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Adam Mizerski <adam@mizerski.pl>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ipfs_config_get

short_description: configure IPFS node

description:
  - Configure IPFS node.

options:
  key:
    description:
      - Key of the config entry
    required: true

seealso:
  - name: IPFS config
    description: IPFS config reference
    link: https://github.com/ipfs/go-ipfs/blob/master/docs/config.md
  - name: IPFS cli config
    description: IPFS cli config reference
    link: https://docs.ipfs.io/reference/cli/#ipfs-config

author:
  - Adam Mizerski <adam@mizerski.pl>
'''

EXAMPLES = r'''
- name: Get AutoNAT current value
  ipfs_config_get:
    key: AutoNAT.ServiceMode
'''

RETURN = r'''
value:
    description: Config value
    type: json
    returned: always
'''


import json

from ansible.module_utils.basic import AnsibleModule


def get_config(module):
    _, stdout, _ = module.run_command(
        ["/usr/local/bin/ipfs", "config", module.params['key']],
        check_rc=True,
    )

    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return stdout.rstrip()


def run_module():
    module_args = dict(
        key=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    result['value'] = get_config(module)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
