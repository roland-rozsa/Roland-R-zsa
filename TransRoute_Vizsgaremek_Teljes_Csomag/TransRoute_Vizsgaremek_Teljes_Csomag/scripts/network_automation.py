#!/usr/bin/env python3
"""
TransRoute Logisztika Kft. - Programozott hálózatkonfiguráló és ellenőrző szkript
Felelős: Háda Patrik (KKK 8.4.2 A - Programozott hálózatkonfiguráció)
"""

import socket
import time

DEVICES = [
    {"name": "R1-BP1", "ip": "10.10.10.2", "site": "Budapest HQ"},
    {"name": "R1-BP2", "ip": "10.10.10.3", "site": "Budapest HQ"},
    {"name": "Core-SW1", "ip": "10.10.10.11", "site": "Budapest HQ"},
    {"name": "Core-SW2", "ip": "10.10.10.12", "site": "Budapest HQ"},
    {"name": "R2-GYOR", "ip": "10.20.10.1", "site": "Győr Raktár"},
    {"name": "R3-SZEGED", "ip": "10.30.10.1", "site": "Szeged Iroda"},
]

CONFIG_TEMPLATE = """! Automatikusan generált biztonsági és banner konfiguráció
banner motd # FIGYELEM! TransRoute Logisztika Kft. - Csak jogosult IT szemelyzetnek! #
service password-encryption
logging buffered 16384
ntp server 10.10.20.10
end
write memory
"""

def check_ssh_port(ip: str, port: int = 22, timeout: float = 1.5) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except OSError:
        return False

def generate_device_configs():
    print("=== TransRoute Hálózat Automatizáció Indítása ===")
    for dev in DEVICES:
        filename = f"auto_cfg_{dev['name']}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"hostname {dev['name']}\n")
            f.write(CONFIG_TEMPLATE)
        ssh_ok = check_ssh_port(dev["ip"])
        status = "ELÉRHETŐ (SSH/22)" if ssh_ok else "OFFLINE / SZIMULÁLT"
        print(f"[OK] {dev['name']} ({dev['site']} - {dev['ip']}) -> Konfig generálva: {filename} | Állapot: {status}")

if __name__ == "__main__":
    generate_device_configs()
