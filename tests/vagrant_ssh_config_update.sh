#!/bin/bash

shopt -s nullglob

action="$1"
name="$2"

case "$action" in
    add)
        vagrant ssh-config "$name" > ".vagrant-ssh-config-${name}"
        ssh -F ".vagrant-ssh-config-${name}" "$name" cat .ssh/authorized_keys > ".vagrant-authorized_keys-${name}"
        ;;
    remove)
        rm -f ".vagrant-ssh-config-${name}" ".vagrant-authorized_keys-${name}"
        ;;
    *)
        echo "unknown action" >&2
        exit 1
esac

configs=(.vagrant-ssh-config-*)
if (( "${#configs[@]}" > 0 )); then
     cat "${configs[@]}" > .vagrant-ssh-config
else
     rm -f .vagrant-ssh-config
fi

authorized_keys=(.vagrant-authorized_keys-*)
if (( "${#authorized_keys[@]}" > 0 )); then
    cat "${authorized_keys[@]}" > authorized_keys
else
    rm -f authorized_keys
fi
