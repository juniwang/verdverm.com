#!/bin/bash

TOKEN="e3e8b6cd7ed85db99459f5fddbcbe3111807ab42f69bc56d3a77dc7ace8db634"


function start-coreos() {

name=$1	

curl -X POST "https://api.digitalocean.com/v2/droplets" \
      -d'{
      	"name":"'${name}'",
      	"region":"nyc3",
      	"size":"512mb",
      	"private_networking":true,
      	"image":"coreos-beta",
      	"user_data":
"#cloud-config

coreos:
  etcd:
    # generate a new token for each unique cluster from https://discovery.etcd.io/new
    discovery: https://discovery.etcd.io/82b98a3a49a4ffd9c9c66a4735ca0758
    # multi-region deployments, multi-cloud deployments, and droplets without
    # private networking need to use $public_ipv4
    addr: $private_ipv4:4001
    peer-addr: $private_ipv4:7001
  fleet:
    public-ip: $private_ipv4   # used for fleetctl ssh command
  units:
    - name: etcd.service
      command: start
    - name: fleet.service
      command: start",
      "ssh_keys":[ {"name":"home"} ]
  }' \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json"

}


# start-coreos master
# start-coreos minion-1
# start-coreos minion-2

curl -X GET "https://api.digitalocean.com/v2/droplets" \
    -H "Authorization: Bearer $TOKEN" 

# curl -X GET "https://api.digitalocean.com/v2/account/keys" \
#     -H "Authorization: Bearer $TOKEN" 

# curl -X GET "https://api.digitalocean.com/v2/actions/32997163" \
#     -H "Authorization: Bearer $TOKEN" 
