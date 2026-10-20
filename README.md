# ultra-fan

<p align="center">
  <img src="https://img.shields.io/badge/Linux-Dell%20Fan%20Control-0A84FF?logo=linux&logoColor=white" alt="Linux Dell Fan Control" />
  <img src="https://img.shields.io/badge/Python-3-%233776AB?logo=python&logoColor=white" alt="Python 3" />
  <img src="https://img.shields.io/badge/Hardware-Dell%20OptiPlex-007DB8?logo=dell&logoColor=white" alt="Dell OptiPlex" />
  <img src="https://img.shields.io/badge/Status-DIY%20Project-orange" alt="DIY project" />
</p>

<p align="center">
  <strong>A tiny Linux fan-tuning project for Dell mini PCs and compact desktops.</strong>
</p>

`ultra-fan` is a small Python script that keeps an eye on the CPU temperature and adjusts the Dell fan speed automatically. It is the kind of project you build when you want a quieter PC, a cooler CPU, and a little bit of hardware hacking without buying a fancy external controller.

If your Dell machine exposes its fan controls through `/sys/class/hwmon`, this script can use that interface to make the fan react to heat instead of running at a fixed, noisy speed.

This is based on the idea by TyTiTaM's <A href="https://www.reddit.com/r/SleepingOptiplex/comments/1rudwdu/ultimate_fan_control_guide_for_dell_optiplex_linux/">Reddit article</a>.

## What this project does

This script:

- reads the CPU temperature from `coretemp`
- reads the current fan RPM from the Dell `hwmon` interface
- checks the current PWM setting
- changes the fan output based on temperature thresholds
- prints the live status so you can see what the machine is doing

The result is a simple closed-loop fan controller that reacts to heat in real time.

## Why I built it

Dell machines are usually fine out of the box, but sometimes the fan policy is either too aggressive or too lazy. On a quiet home setup, a little custom tuning can make a big difference.

This project is for people who like to:

- tinker with Linux hardware
- make their PC quieter without sacrificing cooling
- experiment with `/sys` and `hwmon`
- build a small, practical project instead of installing a giant desktop utility

## DIY maker vibe

This is not a polished enterprise controller. It is a practical script for a hobbyist workflow:

- plug it in
- test it
- watch the temps
- tweak the thresholds
- keep the machine cool without the fan screaming

It is the sort of tool you might use on a bench setup, a home lab box, or a small Dell machine that deserves a bit more control.

## How it works

The script loops continuously and does this every second:

1. Reads CPU temperature
2. Reads fan RPM from the Dell sensor path
3. Chooses a mode based on the current temperature
4. Adjusts the PWM value for the fan
5. Logs the current state to the terminal

The logic is intentionally simple and easy to understand. That is the point: keep it readable, tweakable, and useful.

## Supported hardware

This project is aimed at Dell systems that expose:

- `coretemp`
- `dell_smm` or `dell_smm_hwmon`
- fan control via `/sys/class/hwmon/.../pwm1`

Typical examples:

- Dell OptiPlex 7000 Micro
- Other Dell desktops and workstations with exposed Linux fan interfaces

## Requirements

You will need:

- Linux with `coretemp` available
- a Dell fan interface exposed in `/sys/class/hwmon/`
- Python 3
- permission to write to the relevant sysfs files

Typical paths the script checks:

```bash
/sys/class/hwmon/
/sys/class/hwmon/.../name
/sys/class/hwmon/.../temp1_input
/sys/class/hwmon/.../fan1_input
/sys/class/hwmon/.../pwm1
```

## Quick start

## Installing as a systemd service

You can install the controller as a background service so it starts automatically on boot.

1. Clone the repo and enter the project directory:

```bash
git clone https://github.com/topivi/ultra-fan.git
cd ultra-fan
```

Make it executable:

```bash
chmod +x ultra_fan.py
```

Run it:

```bash
sudo python3 ultra_fan.py
```

Stop it with:

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

## Fan curve

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

This is intentionally basic and easy to tune. If your machine runs hotter or cooler, you can edit the thresholds and PWM values.

## Tuning it yourself

This is a good DIY project because the logic is straightforward. If you want to tune the behavior:

- change the temperature thresholds
- adjust the PWM values
- swap in different RPM targets
- add logging for longer-term analysis

For example, if your machine runs warm but stays stable, you could move the thresholds a few degrees upward to keep it quieter.

## Troubleshooting

### Missing `hwmon` paths

Check whether the platform is exposing the sensors:

```bash
ls /sys/class/hwmon
```

If `coretemp` or `dell_smm` is missing, the script will not have what it needs.

### No fan response

Verify that the PWM file is writable:

```bash
ls -l /sys/class/hwmon/*/pwm1
```

If access is restricted, run the script with `sudo`.

### Temperature looks wrong

Check the raw sensor files:

```bash
cat /sys/class/hwmon/*/temp1_input
```

If the values look invalid, your hardware may expose different sensor names or paths.

### Another service is already controlling the fan

This is common on some systems. If a different fan-management tool is active, it may fight with this script. Disable the competing service before testing.

## Safety notes

This script writes directly to Linux hardware interfaces, so use it with care:

- it can change thermal behavior
- it may conflict with OEM utilities
- it depends on your hardware and kernel exposing the right files
- it is not a universal fix for every Dell model

If you are experimenting on a machine you care about, keep an eye on temperatures and test slowly.

## Project status

This is a small, experimental, DIY-minded fan control tool for Linux-based Dell systems. It works best when you are comfortable with low-level `/sys` access and are happy to tweak the behavior for your specific hardware.

## Contributing

If you have:

- better temperature thresholds
- support for more Dell models
- a cleaner fan curve
- better logging or safety checks

feel free to open an issue or send a pull request.

## License

This project is provided as-is for personal and experimental use.

---

Built for quiet tinkering, practical cooling, and a little bit of Linux hardware hacking.
