## snips-app-relay-switch
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/snipsco/snips-app-relay-switch/blob/master/LICENSE)

Action code for the ***Turn on/off [Relay]*** bundle. It can control the relay connected on Raspberry Pi.

## Usage
***```"Hey snips, please turn on my light"```***

***```"Sure, it's done"```***

## Installation

### Install with assistant
1. Create a Snips account ***[here](https://console.snips.ai/?ref=Qr4Gq17mkPk)***
2. Create an English assistant in ***[Snips console](https://console.snips.ai/)***
3. Add APP ***Turn on/off [Relay]*** (Available soon)
4. Deploy assistant by ***[Sam](https://snips.gitbook.io/documentation/console/deploy-your-assistant)***
5. (On Pi) Add permission to `_snips-skill` user to access gpio: `sudo usermod -a -G i2c,spi,gpio,audio _snips-skills`
6. (On Pi) Restart snips-skill-server: `sudo systemctl restart snips-skill-server`
7. Have fun ***;-)***

### Install only action
```
sam install actions -g https://github.com/snipsco/snips-app-relay-switch.git
```
## Configuration

### MQTT

| Config | Description | Value | Default |
| --- | --- | --- | --- |
| `mqtt_host` | MQTT host name | `<ip address>`/`<hostname>` | `localhost` |
| `mqtt_port` | MQTT port number | `<mqtt port>` | `1883` |

> ***To make satellite work correctly, please change here***

### Device Info

| Config | Description | Value | Default |
| --- | --- | --- | --- |
| `site_id` | Snips device ID | Refering to the actual `snips.toml` | `default` |

> ***To make satellite work correctly, please change here***

### Relay GPIO pin

| Config | Description | Value | Default |
| --- | --- | --- | --- |
| `gpio_bcm_relay` | The BCM GPIO number | [Available BCM pin number](https://www.raspberrypi.org/documentation/usage/gpio/README.md) | `12` |

## Contributing

Please see the [Contribution Guidelines](https://github.com/snipsco/snips-app-relay-switch/blob/master/CONTRIBUTING.md).

## Copyright

This library is provided by [Snips](https://www.snips.ai) as Open Source software. See [LICENSE](https://github.com/snipsco/snips-app-relay-switch/blob/master/LICENSE) for more information.
