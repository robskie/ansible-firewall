# Ansible Role: Firewall

This role manages iptables rules and enables them at boot time. This installs a
`firewall` init service after a successul run that you can use to control the
firewall. For example, to stop the firewall, type `service firewall stop` in the
command line. Other service commands are `start` and `restart`.

## Requirements

None.

## Role Variables

Here are the available variables for this role with their default values.

    firewall_default_file: default.yml

This is the path where the file containing the default firewall rules can be
found. Note that this is relative to the playbook directory. For the default
rules, see `vars/default.yml`

    firewall_blacklist: ''
    firewall_whitelist: ''

The files that have the blacklisted and whitelisted ip addresses.

    firewall_prehook: ''
    firewall_posthook: ''

These are the commands to execute before and after the firewall rules are
loaded.

    firewall_clear_rules: no

This role creates a directory `/etc/firewall/rule.d` where each firewall rule
is saved. These rules are then combined before being loaded to the system. By
default, this directory is not cleared every time this role is run. If you don't
want this behavior and to prevent previous rules from being loaded, set
`firewall_clear_rules` to `yes`.

    firewall_rules:
      - name: Example rules
        position: 100
        forward_tcp_ports:
          - { src: 25, dest: 2525 }
        forward_udp_ports:
          - { src: 3478, dest: 3479 }
        allow_udp_ports:
          - 3074
        allow_tcp_ports:
          - 22
          - 80
          - 123
          - 443
        custom_rules:
          - -A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

This is an example that uses all the available options for the `firewall_rules`
variable. The `position` parameter dictates where the given rules are inserted.
A lower value means that the rules are inserted near the top (ie. has higher
priority) and vice versa. It is recommended that this value vary between `100`
and `900`.

## Configuration Files Format

The following shows the correct format for each configuration file.

**Default Rules File**

    ---
    firewall_default_rules:
      000 - Default policies:
        - -P INPUT ACCEPT
        - -P OUTPUT ACCEPT
        - -P FORWARD ACCEPT
      001 - Allow loopback:
        - -A INPUT -i lo -j ACCEPT
      990 - Allow established:
        - -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
      999 - Drop other:
        - -A INPUT -j DROP

**Blacklist/Whitelist File**

    1.2.3.4
    5.6.7.8
    1.0.0.0/8
    2.2.0.0/16

## Tags

  - firewall
  - install
  - configure
  - firewall:install
  - firewall:configure

## Dependencies

None.

## Example Playbook

    ---
    hosts: servers
    become: yes
    roles:
      - role: robskie.firewall
        firewall_default_file: files/firewall-default.yml
        firewall_prehook: service fail2ban stop
        firewall_posthook: service fail2ban start
        firewall_rules:
          - name: Allow ports
            position: 100
            allow_tcp_ports: [22, 25 80, 123, 443]
          - name: Allow ping requests
            position: 110
            custom_rules:
              - -A INPUT -p icmp -m icmp --icmp-type echo-request -j ACCEPT

## License

MIT
