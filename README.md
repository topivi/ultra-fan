# ultra-fan

<p align="center">
  <img src="https://img.shields.io/badge/Linux-CPU%20Fan%20Control-0A84FF?logo=linux&logoColor=white" alt="Linux CPU Fan Control" />
  <img src="https://img.shields.io/badge/Python-3-%233776AB?logo=python&logoColor=white" alt="Python 3" />
  <img src="https://img.shields.io/badge/Hardware-Dell%20OptiPlex-007DB8?logo=dell&logoColor=white" alt="Dell OptiPlex" />
</p>

A small Python utility that watches the CPU temperature and adjusts the Dell system fan duty cycle in real time by writing to the Linux hardware monitoring interfaces exposed by `coretemp` and `dell_smm`.

This project is designed for Dell OptiPlex systems that expose Dell fan control through `/sys/class/hwmon/*`, allowing a lightweight fan curve to reduce noise while keeping the CPU within safe operating temperatures.

## Why this exists

Dell systems often expose EC or SMM-backed fan control through Linux `hwmon` entries. This script reads:

- CPU temperature from `coretemp`
- Current fan speed from the Dell hwmon interface
- Fan PWM target from `/sys/class/hwmon/.../pwm1`

It then applies a simple thermal profile with stages such as:

- SILENT
- QUIET
- LOW
- MEDIUM
- HIGH
- PERFORMANCE
- ULTRA

The goal is to keep the system responsive without running the fan at maximum speed all the time.

## Features

- Monitors CPU temperature in a loop
- Detects `coretemp` and `dell_smm` automatically
- Adjusts Dell fan PWM dynamically
- Uses a stepped temperature-based profile
- Keeps running until interrupted with `Ctrl+C`
- Minimal dependencies: only Python standard library

## Requirements

This script is intended for Linux systems with:

- `coretemp` kernel module loaded
- `dell_smm_hwmon` or similar Dell hwmon interface available
- root or write access to the relevant `/sys` entries
- Python 3 installed

Typical paths that the script looks for include:

- `/sys/class/hwmon/`
- `/sys/class/hwmon/.../name`
- `/sys/class/hwmon/.../temp1_input`
- `/sys/class/hwmon/.../fan1_input`
- `/sys/class/hwmon/.../pwm1`

## Supported hardware

This project is primarily aimed at:

- Dell OptiPlex 7000 Micro
- Dell systems exposing `dell_smm` and `coretemp` under `/sys/class/hwmon`

If your system does not expose these devices, the script exits with a helpful error.

## Quick start

1. Clone the repo:

```bash
git clone https://github.com/topivi/ultra-fan.git
cd ultra-fan
```

2. Make the script executable:

```bash
chmod +x ultra_fan.py
```

3. Run it:

```bash
sudo python3 ultra_fan.py
```

4. Stop it with:

```bash
Ctrl+C
```

## How it works

The script performs a continuous loop:

- Reads the CPU temperature from `temp1_input`
- Reads the current RPM from `fan1_input`
- Chooses a target fan response based on temperature thresholds
- Writes a PWM value to `pwm1`
- Prints a status line such as:

```text
[12:34:56] Lämpötila: 61.2°C | RPM: 1200 | Tavoite: 1200 | PWM: 128 (MED_PLUS)
```

The thermal thresholds are tuned for a conservative but responsive fan curve:

| Temperature | Mode | Typical behavior |
| --- | --- | --- |
| < 45°C | SILENT | Very low fan speed |
| 45–49°C | QUIET | Gentle ramp-up |
| 50–54°C | LOW | Increased airflow |
| 55–59°C | MEDIUM | Balanced cooling |
| 60–64°C | MED_PLUS | Active cooling |
| 65–69°C | HIGH | Strong cooling |
| 70–74°C | PERFORMANCE | Aggressive response |
| 75°C+ | ULTRA | Full cooling effort |

## Important notes

- This script writes directly to Linux hardware control files.
- It modifies fan behavior at the system level; use with care.
- On some systems, the `dell_smm` interface may require a specific kernel module or BIOS settings.
- If your fan is already controlled by another service, this script may conflict with it.
- Always test carefully before relying on it for long-running thermal control.

## Troubleshooting

### Script reports missing hwmon paths

Check that the relevant modules are loaded:

```bash
ls /sys/class/hwmon
```

Look for entries such as:

- `coretemp`
- `dell_smm` / `dell_smm_hwmon`

If they are missing, verify the kernel modules and system configuration.

### No fan response

Confirm that the Dell fan interface is writable:

```bash
ls -l /sys/class/hwmon/*/pwm1
```

If permissions are restricted, run the script with `sudo` or adjust your system access.

### CPU temperature reads as zero or invalid

This can happen if the sensor is not exposed or the file path differs on your platform. Check:

```bash
cat /sys/class/hwmon/*/temp1_input
```

and verify the correct sensor path for your hardware.

## Security and safety

This project is a fan-control tool, not a general-purpose system service. It is intentionally small and direct. Use it responsibly and understand that changing fan PWM can affect thermal behavior and hardware wear.

## License

This project is provided as-is for personal and experimental use.

## Project status

This repository is a lightweight, focused utility for Linux-based Dell fan control. It is best suited for users comfortable working with low-level hardware interfaces and `/sys` entries.

## Contributing

Issues, improvements, and pull requests are welcome. If you have a new temperature profile, hardware compatibility notes, or a cleaner fan curve, feel free to contribute.

---

Built for quiet, temperature-aware fan control on compatible Dell Linux systems.
