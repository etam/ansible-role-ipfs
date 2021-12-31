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
module: ipfs_config

short_description: configure IPFS node

description:
  - Configure IPFS node.

options:
  key:
    description:
      - Key of the config entry
    required: true
  value:
    description:
      - Value of the config entry
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
- name: Disable AutoNAT
  ipfs_config:
    key: AutoNAT.ServiceMode
    value: disabled
'''


import json
import yaml

from ansible.module_utils.basic import AnsibleModule


def try_json_loads(s):
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return s.rstrip()


def get_config(module):
    _, stdout, _ = module.run_command(
        ["ipfs", "config", module.params['key']],
        check_rc=True,
    )

    return try_json_loads(stdout)


def set_config(module, conf):
    module.run_command(
        ["ipfs", "config", "--json",
         module.params['key'], json.dumps(conf)],
        check_rc=True,
    )


def run_module():
    module_args = {
        'key': {
            'type': 'str',
            'required': True,
        },
        'value': {
            'type': 'json',
            'required': True,
        },
    }

    result = {
        'diff': {
            'before': None,
            'after': None,
        },
        'changed': False,
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    conf_pre = get_config(module)
    conf_post = try_json_loads(module.params['value'])
    result['diff']['before'] = yaml.dump(conf_pre)
    result['diff']['after'] = yaml.dump(conf_post)

    if conf_pre == conf_post:
        module.exit_json(**result)

    result['changed'] = True

    if module.check_mode:
        module.exit_json(**result)

    set_config(module, conf_post)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
