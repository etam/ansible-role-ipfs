# IPFS

Features:
  - Automatic `Peering.Peers` generation.
  - Configuration is applied via `ipfs config` using custom module. Supports idempotence and generating diffs.
  - Allows to specify custom IP public address, if running behind router.
  - Downloads binaries for updates via local IPFS gateway, if already installed.
  - Runs `ipfs repo gc` as a separate service.
  - Supports x86_64 and aarch64.


## Requirements

- Target system uses systemd


## Role Variables

- `ipfs_ansible_group`: Ansible group, that contains managed ipfs nodes. Default: `all`.
- `ipfs_home_dir`: default `/var/lib/ipfs`
- `ipfs_version`: (it's obvious)
- `ipfs_init_profile`: Profile to apply when initializing ipfs (see [Configure profile](https://docs.ipfs.tech/how-to/default-profile/))
- `ipfs_gc_when`: When to run `ipfs repo gc`. Systemd time (see `man systemd.time`).
- `ipfs_swarm_port`: 4001
- `ipfs_public_addresses`: Public swarm addresses. Default:
  - `/ip4/{{ ansible_default_ipv4['address'] }}/tcp/{{ ipfs_swarm_port }}`
  - `/ip4/{{ ansible_default_ipv4['address'] }}/udp/{{ ipfs_swarm_port }}/quic`
  - `/ip4/{{ ansible_default_ipv4['address'] }}/udp/{{ ipfs_swarm_port }}/quic-v1`
  - `/ip4/{{ ansible_default_ipv4['address'] }}/udp/{{ ipfs_swarm_port }}/quic-v1/webtransport`
- `ipfs_private_addresses`: Formatted like `ipfs_public_addresses`. Used for direct connection between IPFS nodes. May be useful when connecting over LAN on VPN.
- `ipfs_config_extra`: Additional IPFS node config. The yaml structure is converted to json and sent to `ipfs config`. Default value is
    ```yaml
    ipfs_config_extra:
      Gateway.PublicGateways:
        localhost: null
    ```
    This results in running
    ```sh
    ipfs config --json Gateway.PublicGateways '{"localhost": null}'
    ```
    which comes from https://github.com/ipfs/kubo/blob/master/docs/config.md#implicit-defaults-of-gatewaypublicgateways


## Dependencies

None


## Example Playbook

Just:
```yml
- hosts: ipfs
  roles: [ipfs]
```


## License

[GPL-3.0-or-later](COPYING.txt)


## Author Information

Adam "etam" Mizerski <adam@mizerski.pl> https://etam-software.eu
