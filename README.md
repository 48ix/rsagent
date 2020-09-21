<div align="center">
  
  <img href="https://48ix.net" src="https://res.cloudinary.com/ix-48/image/upload/v1594108320/logo-wide-light.svg" />

  <br/>
  <div style="color: #808080; font-style:italic;">
    <h3>
      ROUTE SERVER AGENT
    </h3>
  </div>

</div>

<hr/>

This repository contains code used for automated internal management of [48 IX](https://48ix.net) route servers.

## How it Works

Upon receiving a signal from [48ix/routingpolicy](https://github.com/48ix/routingpolicy) (RPS), the RS Agent (RSA) ingests a delta [FRRouting](https://frrouting.org) configuration. Prior to sending the actual payload, RPS creates a SHA-256 hash of the config file, encrypts the file, and creates a second hash of the now-encrypted config file. RPS then sends both hashes to RSA, followed by the encrypted config file payload. RSA validates that both the encrypted & decrypted data match the hashes sent by RPS and decrypts the config file. Then, RSA uses the [FRR Reload](http://docs.frrouting.org/en/latest/frr-reload.html) script to test that the config is valid, and if it is, RSA applies the new config and reloads FRRouting.

## Configuration

There are only 4 configuration variables, and only one is required. All are picked up via environment variables.

| Environment Variable        | Function                                               | Default                      |
| :-------------------------- | ------------------------------------------------------ | ---------------------------- |
| `ix_rsagent_listen_address` | IPv4/IPv6 Address for the RS Agent Server to listen on | `::`                         |
| `ix_rsagent_listen_port`    | TCP Port used for RSA to RPS communication             | `4848`                       |
| `ix_rsagent_frr_reload`     | Path to frr-reload script                              | `/usr/lib/frr/frr-reload.py` |
| `ix_rsagent_key`            | Encryption key used for RSA to RPS communication       |                              |
