# TransRoute Logisztika Kft. – Szerverek (Oracle VirtualBox) Beállítási Útmutató
**Felelős:** Richter Márk  
**Követelmény:** Minimum 1 Windows Server + 1 Linux Server, összesen 7 kötelező szolgáltatással (KKK 8.4.2 A).

---

## 1. Oracle VirtualBox Hálózati Beállítások
Mindkét virtuális gépnél (`WinSrv-DC` és `LinuxSrv`):
- **Adapter 1:** `Bridged Adapter` (a fizikai hálózati kártyához kötve, amire a Packet Tracer Cloud csatlakozik)
- **Promiscuous Mode:** `Allow All`
- **Windows Server statikus IP:** `10.10.20.10 /26` | Átjáró: `10.10.20.1` | DNS: `127.0.0.1` | IPv6: `2001:db8:100:20::10/64`
- **Linux Server statikus IP:** `10.10.20.20 /26` | Átjáró: `10.10.20.1` | DNS: `10.10.20.10` | IPv6: `2001:db8:100:20::20/64`

---

## 2. A 7 kötelező szolgáltatás megvalósítása

### 1. Címtárszolgáltatás (Windows Server – Active Directory Domain Services)
1. Server Manager → **Add Roles and Features** → **Active Directory Domain Services (AD DS)** telepítése.
2. Előléptetés tartományvezérlővé (**Promote this server to a domain controller**):
   - Új erdő létrehozása (**Add a new forest**), Root domain name: `transroute.local`
3. Szervezeti egységek (OU-k) és felhasználók létrehozása (`Active Directory Users and Computers`):
   - `OU=Vezetoseg`, `OU=Diszpecser`, `OU=Raktar_Gyor`, `OU=Iroda_Szeged`, `OU=IT`

### 2. DNS szolgáltatás (Windows DNS + Linux Forward)
- Az AD telepítésével automatikusan létrejön a `transroute.local` zóna.
- **Forward Lookup Zone** rekordok felvétele:
  - `portal.transroute.local` -> `A` rekord: `10.10.20.20` (Linux HTTPS webszerver)
  - `fajl.transroute.local` -> `A` rekord: `10.10.20.10` (Fájlszerver)
- **Reverse Lookup Zone** (`10.10.20.in-addr.arpa`) beállítása a visszafelé irányuló névfeloldáshoz.

### 3. DHCP szolgáltatás (Windows Server DHCP)
1. **DHCP Server** szerepkör telepítése és autorizálása az AD-ban.
2. Hatókörök (**Scopes**) létrehozása:
   - Budapest Iroda (`10.10.30.20 - 10.10.30.150`, maszk `255.255.255.0`, Router `10.10.30.1`, DNS `10.10.20.10`)
   - Budapest WiFi (`10.10.40.20 - 10.10.40.200`, maszk `255.255.255.0`, Router `10.10.40.1`, DNS `10.10.20.10`)

### 4. HTTP / HTTPS Webszerver (Linux – Ubuntu/Debian + Nginx + SSL)
```bash
sudo apt update && sudo apt install -y nginx openssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/transroute.key \
  -out /etc/ssl/certs/transroute.crt \
  -subj "/C=HU/ST=Budapest/L=Budapest/O=TransRoute Logisztika Kft./CN=portal.transroute.local"
```
- Az Nginx konfigurációban állítsd be a `443 ssl` portot a tanúsítvánnyal, és helyezz el egy egyszerű vállalati intranetes főoldalt (`/var/www/html/index.html`) a fuvarnyilvántartó portálhoz.

### 5. Fájl- és nyomtatómegosztás (Windows File & Print Services + Linux Samba)
- **Windows:** Hozz létre egy `C:\Kozos_Dokumentumok` mappát (`Fuvarlevelek`, `Penzugy`, `Sablonok` almappákkal), oszd meg jogosultságokkal (AD csoportokra szabva), és telepítsd a **Print and Document Services** szerepkört egy hálózati fuvarlevél-nyomtatóval.
- **Linux (Samba):** `sudo apt install -y samba` -> `/srv/raktar_megosztas` megosztása a raktári terminálok számára.

### 6. Automatizált mentés (Windows Server Backup + Linux Cron/Rsync)
- **Windows:** **Windows Server Backup** telepítése → **Backup Schedule** varázslóval napi ütemezett mentés beállítása az AD System State-ről és a megosztott mappákról külön meghajtóra/hálózati helyre.
- **Linux:** Napi ütemezett mentés `crontab -e` segítségével:
  `0 2 * * * tar -czf /backup/webportal_$(date +\%F).tar.gz /var/www/html`

### 7. Kliensekre automatizált szoftvertelepítés (Active Directory GPO)
1. Helyezz el egy `.msi` telepítőcsomagot (pl. `7z2408-x64.msi` vagy `LibreOffice.msi`) egy hálózati megosztásban (`\\WinSrv-DC\Telepitok`).
2. **Group Policy Management** → Új GPO létrehozása (`Kliens_Alapszoftverek`) és csatolása a kliens gépek OU-jához.
3. **Computer Configuration → Policies → Software Settings → Software installation → New → Package** → válaszd ki az `.msi` fájlt (`Assigned` módban).
4. Kliens gépen tesztelés: `gpupdate /force` majd újraindítás.
