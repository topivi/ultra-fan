#!/usr/bin/env python3
import os
import time

# --- PATH CONFIGURATION ---
def find_hwmon_by_name(name):
    hwmon_dir = "/sys/class/hwmon/"
    if not os.path.exists(hwmon_dir):
        return None
    for path in os.listdir(hwmon_dir):
        try:
            with open(os.path.join(hwmon_dir, path, "name"), "r") as f:
                if name in f.read():
                    return os.path.join(hwmon_dir, path)
        except (FileNotFoundError, PermissionError):
            continue
    return None

DELL_PATH = find_hwmon_by_name("dell_smm")
CORE_PATH = find_hwmon_by_name("coretemp")

if not DELL_PATH or not CORE_PATH:
    print("Virhe: Tarvittavia hwmon-polkuja ei löytynyt. Tarkista, että dell_smm_hwmon ja coretemp ovat ladattuina.")
    exit(1)

TEMP_PATH = os.path.join(CORE_PATH, "temp1_input")
RPM_PATH = os.path.join(DELL_PATH, "fan1_input")
PWM_PATH = os.path.join(DELL_PATH, "pwm1")

def get_val(path):
    try:
        with open(path, "r") as f:
            return int(f.read().strip())
    except Exception:
        return 0

def set_pwm(val):
    try:
        with open(PWM_PATH, "w") as f:
            f.write(str(int(val)))
    except Exception:
        pass

# Dell Hardware Commands
CMD_LOW = 30
CMD_MED = 128
CMD_MAX = 255

current_pwm = CMD_LOW
print("--- Dell Smart Fan Control: Active (Ubuntu 26.04) ---")

try:
    while True:
        t = get_val(TEMP_PATH) / 1000.0
        rpm = get_val(RPM_PATH)

        if t < 45:
            target, up, down, high, low, mode = 300, CMD_LOW, CMD_LOW, 350, 0, "SILENT"
        elif 45 <= t < 50:
            target, up, down, high, low, mode = 500, CMD_MED, CMD_LOW, 550, 450, "QUIET"
        elif 50 <= t < 55:
            target, up, down, high, low, mode = 700, CMD_MED, CMD_LOW, 750, 650, "LOW"
        elif 55 <= t < 60:
            target, up, down, high, low, mode = 900, CMD_MED, CMD_LOW, 950, 850, "MEDIUM"
        elif 60 <= t < 65:
            target, up, down, high, low, mode = 1200, CMD_MED, CMD_LOW, 1250, 1150, "MED_PLUS"
        elif 65 <= t < 70:
            target, up, down, high, low, mode = 1600, CMD_MED, CMD_MED, 1700, 1500, "HIGH"
        elif 70 <= t < 75:
            target, up, down, high, low, mode = 1900, CMD_MAX, CMD_MED, 1950, 1900, "PERFORMANCE"
        else:
            target, up, down, high, low, mode = 2500, CMD_MAX, CMD_MAX, 2600, 2400, "ULTRA"

        if rpm > high:
            current_pwm = down
        elif rpm < low:
            current_pwm = up

        if mode in ["SILENT", "HIGH", "ULTRA"]:
            current_pwm = up

        set_pwm(current_pwm)
        print(f"[{time.strftime('%H:%M:%S')}] Lämpötila: {t:.1f}°C | RPM: {rpm} | Tavoite: {target} | PWM: {current_pwm} ({mode})")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\nOhjelma keskeytetty. Palautetaan tuulettimen hallinta takaisin järjestelmälle.")

