#!/bin/bash

exec ansible-playbook -i inventory.yml play.yml
