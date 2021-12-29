#!/bin/bash

shopt -s nullglob

action="$1"
name="$2"

case "$action" in
    add)
        vagrant ssh-config "$name" > ".vagrant-ssh-config-${name}"
        ;;
    remove)
        rm -f ".vagrant-ssh-config-${name}"
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
