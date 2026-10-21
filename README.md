# ultra-fan

<p align="center">
  <img src="https://img.shields.io/badge/Linux-Dell%20Fan%20Control-0A84FF?logo=linux&logoColor=white" alt="Linux Dell Fan Control" />
  <img src="https://img.shields.io/badge/Python-3-%233776AB?logo=python&logoColor=white" alt="Python 3" />
  <img src="https://img.shields.io/badge/Hardware-Dell%20OptiPlex-007DB8?logo=dell&logoColor=white" alt="Dell OptiPlex" />
  <img src="https://img.shields.io/badge/Status-DIY%20Project-orange" alt="DIY project" />
</p>

<p align="center">
  <strong>Linux fan control for Dell OptiPlex machines.</strong>
</p>

`ultra-fan` is a lightweight Python utility for Dell systems that exposes fan control through `/sys/class/hwmon`. It reads the CPU temperature, watches the current RPM, and adjusts the PWM value to keep the machine cooler without running the fan aggressively all the time.

This project is intended for Dell desktops and mini PCs where the stock fan policy is too noisy or too slow. It is especially useful on OptiPlex systems with `coretemp` and `dell_smm`/`dell_smm_hwmon` exposed in Linux.

Important: on many Dell systems the `dell_smm_hwmon` kernel module must be loaded with these parameters before the fan-control files become writable:

```bash
sudo modprobe dell_smm_hwmon restricted=0 ignore_dmi=1
```

Without these parameters, Linux may expose the hwmon directory but still block writes to the PWM files, so the script cannot adjust the fan speed.

This is based on the idea described in TyTiTaM's Reddit guide for Dell fan control on Linux.

## Features

- reads CPU temperature from `coretemp`
- reads current fan RPM from the Dell `hwmon` interface
- checks the active PWM value
- adjusts the fan speed dynamically based on temperature thresholds
- prints live status information every second
- can be installed as a `systemd` service

## Supported hardware

This project is designed for Dell systems that expose:

- `coretemp`
- `dell_smm` or `dell_smm_hwmon`
- fan control under `/sys/class/hwmon/.../pwm1`

Examples include:

- Dell OptiPlex 7000 Micro
- other Dell systems with a comparable Linux `hwmon` layout

## Requirements

You will need:

- Linux with `coretemp` available
- a Dell fan interface exposed in `/sys/class/hwmon/`
- the `dell_smm_hwmon` kernel module loaded with `restricted=0` and `ignore_dmi=1`
- Python 3
- root permissions to write to the relevant sysfs files

Typical paths checked by the script:

```bash
/sys/class/hwmon/
/sys/class/hwmon/.../name
/sys/class/hwmon/.../temp1_input
/sys/class/hwmon/.../fan1_input
/sys/class/hwmon/.../pwm1
```

## Repository contents

- `ultra_fan.py` — main fan control loop
- `install_service.sh` — installs the application and creates a `systemd` service
- `systemd/` — service configuration related files
- `README.md` — project documentation

## Quick start

### 1. Load the Dell hwmon module with the required parameters

Before running the script, load the Dell module correctly:

```bash
sudo modprobe dell_smm_hwmon restricted=0 ignore_dmi=1
```

If the module is not loaded or the parameters are missing, the interface may exist but writes to `/sys/class/hwmon/.../pwm1` will fail.

### 2. Clone the repository

```bash
git clone https://github.com/topivi/ultra-fan.git
cd ultra-fan
```

### 3. Install as a systemd service

Run the installer as root or with `sudo`:

```bash
sudo bash install_service.sh
```

This script:

- copies the project to `/opt/ultra-fan`
- creates a `systemd` unit named `dell-fan.service`
- reloads systemd
- enables and starts the service

### 4. Verify the service

```bash
sudo systemctl status dell-fan.service --no-pager --lines 20
```

### 5. View logs

```bash
sudo journalctl -u dell-fan.service -f
```

The installed service runs:

```bash
/usr/bin/python3 -u /opt/ultra-fan/ultra_fan.py
```

## Manual run for testing

If you want to test it without installing the service:

```bash
cd ultra-fan
chmod +x ultra_fan.py
sudo modprobe dell_smm_hwmon restricted=0 ignore_dmi=1
sudo python3 ultra_fan.py
```

Stop it with:

```bash
Ctrl+C
```

## How it works

The script loops once per second and performs the following:

1. reads CPU temperature
2. reads current RPM from the Dell sensor path
3. selects a thermal mode based on the current temperature
4. updates the PWM value for the fan
5. logs the current state to the terminal

The logic is intentionally simple and easy to adjust.

## Example output

```text
--- Dell Smart Fan Control: Active (Ubuntu 26.04) ---
[12:34:56] Lämpötila: 61.2°C | RPM: 1200 | Tavoite: 1200 | PWM: 128 (MED_PLUS)
[12:34:57] Lämpötila: 62.4°C | RPM: 1400 | Tavoite: 1600 | PWM: 128 (MED_PLUS)
[12:34:58] Lämpötila: 58.7°C | RPM: 1000 | Tavoite: 900 | PWM: 128 (MEDIUM)
```

## Fan behavior

The script uses a simple thermal ladder:

| Temperature | Mode | Typical behavior |
| --- | --- | --- |
| < 45°C | SILENT | Fan stays quiet |
| 45–49°C | QUIET | Gentle ramp up |
| 50–54°C | LOW | Steady airflow |
| 55–59°C | MEDIUM | Balanced cooling |
| 60–64°C | MED_PLUS | More active cooling |
| 65–69°C | HIGH | Strong cooling |
| 70–74°C | PERFORMANCE | Aggressive response |
| 75°C+ | ULTRA | Full cooling effort |

This is intentionally basic and designed to be easy to tune.

## Tuning it yourself

If your hardware runs hotter or cooler than expected, edit the thresholds and PWM values in `ultra_fan.py`.

Common customizations:

- change temperature thresholds
- adjust PWM values
- tune RPM goals
- add extra logging or safety checks

## Troubleshooting

### Missing hwmon paths

Check whether the platform exposes the sensors:

```bash
ls /sys/class/hwmon
```

If `coretemp` or `dell_smm` is missing, the script will not have what it needs.

### `dell_smm_hwmon` is present but writes fail

This is the most common issue on Dell systems. The module must be loaded with the following options:

```bash
sudo modprobe dell_smm_hwmon restricted=0 ignore_dmi=1
```

If you still cannot write to `/sys/class/hwmon/.../pwm1`, check that the module is actually active:

```bash
ls /sys/class/hwmon
cat /sys/module/dell_smm_hwmon/parameters/* 2>/dev/null || true
```

### No fan response

Verify that the PWM file is writable:

```bash
ls -l /sys/class/hwmon/*/pwm1
```

If access is restricted, run the script with `sudo`.

### Temperature looks wrong

Check the raw sensor values:

```bash
cat /sys/class/hwmon/*/temp1_input
```

If the values look invalid, your hardware may expose different sensor names or paths.

### Another service is already controlling the fan

Some systems run another fan-management utility that conflicts with this script. Disable the competing service before testing.

## Safety notes

This project writes directly to Linux hardware interfaces, so use it carefully:

- it changes thermal behavior
- it may conflict with OEM utilities
- it depends on your hardware and kernel exposing the correct files
- it is not a universal fix for every Dell model

If you are experimenting on a machine you care about, keep an eye on temperatures and test carefully.

## Project status

This is a small, experimental, DIY-oriented fan control utility for Linux-based Dell systems. It works best when you are comfortable with low-level `/sys` access and willing to tune behavior to match your hardware.

## License

This project is provided as-is for personal and experimental use.

---

Built for quiet tinkering, practical cooling, and a little bit of Linux hardware hacking.
