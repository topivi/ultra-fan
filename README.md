# ultra-fan

<p align="center">
  <img src="https://img.shields.io/badge/Linux-Dell%20Fan%20Control-0A84FF?logo=linux&logoColor=white" alt="Linux Dell Fan Control" />
  <img src="https://img.shields.io/badge/Python-3-%233776AB?logo=python&logoColor=white" alt="Python 3" />
  <img src="https://img.shields.io/badge/Hardware-Dell%20OptiPlex-007DB8?logo=dell&logoColor=white" alt="Dell OptiPlex" />
  <img src="https://img.shields.io/badge/Status-Experimental-orange" alt="Experimental status" />
</p>

<p align="center">
  <strong>Smart CPU fan control for Dell OptiPlex systems running Linux.</strong>
</p>

<p align="center">
  <img alt="Fan control dashboard" width="900" src="https://raw.githubusercontent.com/topivi/ultra-fan/main/assets/fan-curve-preview.png" />
</p>

> Note: The banner image above is intentionally optional and can be replaced with a local asset in the repository if you want a fully self-hosted look.

`ultra-fan` is a lightweight Python utility that reads CPU temperature from Linux `hwmon` sensors and adjusts the Dell fan PWM in real time. It is designed for systems where the Dell fan control is exposed via `/sys/class/hwmon/*`, making it useful for laptops and desktops with `coretemp` and `dell_smm` interfaces.

## Overview

This project is focused on one goal: keep the CPU cool without letting the fan scream at full speed all the time.

The script watches:

- CPU temperature from `coretemp`
- Current fan RPM from the Dell hardware monitor
- Fan PWM level from the Dell `hwmon` interface

It then applies a step-based thermal curve to softly ramp the fan up or down based on the current temperature.

## Why this project exists

Many Dell systems expose hardware fan control through Linux sysfs, but they do not automatically provide a quiet or adaptive thermal curve under Ubuntu or other Linux distributions. This utility helps bridge that gap by giving the system a simple, temperature-driven fan policy.

## Highlights

- Automatic detection of `coretemp` and `dell_smm` entries
- Real-time CPU temperature monitoring
- Fan speed adjustment using PWM values
- Simple thermal profile with several operating modes
- Minimal dependencies: only Python standard library
- Built for Linux kernel `hwmon` interfaces

## Features

- Reads CPU sensor values from `/sys/class/hwmon`
- Detects the correct sensor paths dynamically
- Monitors and reacts to fan RPM changes
- Applies a stepped thermal response curve
- Logs current temperature, RPM, target, and mode
- Stops cleanly on `Ctrl+C`

## Supported hardware

This script is primarily intended for:

- Dell OptiPlex systems exposing `dell_smm` / `dell_smm_hwmon`
- Systems with `coretemp` loaded in Linux
- Fan controllers exposed through `/sys/class/hwmon/*/pwm1`

Examples of compatible scenarios include:

- Dell OptiPlex 7000 Micro
- Other Dell workstation and desktop models with accessible fan control interfaces

## Requirements

You need:

- Linux with `coretemp` enabled
- A Dell hardware interface exposed under `/sys/class/hwmon/`
- Python 3 installed
- Permission to write to the relevant `/sys` files

Typical paths include:

```bash
/sys/class/hwmon/
/sys/class/hwmon/.../name
/sys/class/hwmon/.../temp1_input
/sys/class/hwmon/.../fan1_input
/sys/class/hwmon/.../pwm1
```

## Quick start

1. Clone the repository:

```bash
git clone https://github.com/topivi/ultra-fan.git
cd ultra-fan
```

2. Make the script executable:

```bash
chmod +x ultra_fan.py
```

3. Run the script:

```bash
sudo python3 ultra_fan.py
```

4. Stop it with:

```bash
Ctrl+C
```

## Example output

```text
--- Dell Smart Fan Control: Active (Ubuntu 26.04) ---
[12:34:56] Lämpötila: 61.2°C | RPM: 1200 | Tavoite: 1200 | PWM: 128 (MED_PLUS)
[12:34:57] Lämpötila: 62.4°C | RPM: 1400 | Tavoite: 1600 | PWM: 128 (MED_PLUS)
[12:34:58] Lämpötila: 58.7°C | RPM: 1000 | Tavoite: 900 | PWM: 128 (MEDIUM)
```

## Fan control profile

The script uses temperature ranges to select different operational modes:

| Temperature | Mode | Behavior |
| --- | --- | --- |
| < 45°C | SILENT | Very low fan speed |
| 45–49°C | QUIET | Gentle ramp up |
| 50–54°C | LOW | Steady cooling |
| 55–59°C | MEDIUM | Balanced airflow |
| 60–64°C | MED_PLUS | Active thermal response |
| 65–69°C | HIGH | More aggressive cooling |
| 70–74°C | PERFORMANCE | Strong airflow |
| 75°C+ | ULTRA | Full cooling effort |

## How it works

The loop is intentionally simple:

1. Read the CPU temperature.
2. Read the current fan RPM.
3. Compare the values against the configured thresholds.
4. Increase or decrease PWM depending on whether the fan is too slow or too fast.
5. Write the new setting to `pwm1`.
6. Repeat every second.

This creates a simple closed-loop control scheme that responds to thermal load in near real time.

## Troubleshooting

### Missing `hwmon` paths

If the script exits with a missing hardware error:

```bash
ls /sys/class/hwmon
```

Check whether `coretemp` and `dell_smm` are present. If they are missing, the kernel modules may not be loaded or the hardware may not expose them.

### Fan does not react

Verify that the PWM interface is available and writable:

```bash
ls -l /sys/class/hwmon/*/pwm1
```

If access is restricted, run the script with `sudo`.

### Temperature reads zero or invalid values

Check the actual sensor output:

```bash
cat /sys/class/hwmon/*/temp1_input
```

If the file is missing or reports invalid data, your sensor layout may differ from what this script expects.

### Another fan service is active

If a different daemon is controlling the fan, this script may fight with it. In those cases, disable the competing service before running this tool.

## Safety and limitations

This project writes directly to hardware-level Linux files. That means:

- It can affect system cooling behavior
- It may conflict with OEM or system services
- It is hardware- and kernel-dependent
- It is not a universal solution for every Dell platform

Use it carefully and test it on a system you can monitor.

## Project status

This repository is a focused, experimental utility for Linux-based fan tuning on compatible Dell hardware. It is best suited for users comfortable working with low-level `/sys` interfaces and hardware monitoring.

## Contributing

Contributions are welcome. If you have:

- better temperature thresholds
- support for additional Dell models
- improvements to the fan curve
- better logging or safety checks

please open an issue or submit a pull request.

## License

This project is provided as-is for personal and experimental use.

---

Built for quiet, temperature-aware fan control on compatible Dell Linux systems.
