# TransRoute Logisztika Kft. – Vizsgaremek

**Szakma:** Informatikai rendszer- és alkalmazás-üzemeltető technikus (5 0612 12 02)  
**Csapattagok:**
- **Rózsa Kálmán Roland** – Core hálózat, Routing/WAN, Dual-Stack IPv4/IPv6 címterv, Hálózati dokumentáció
- **Háda Patrik** – Kapcsolás (VLAN, STP, EtherChannel), WiFi, Site-to-Site VPN, Cisco ASA tűzfal, Python automatizáció, Tesztelés
- **Richter Márk** – Windows & Linux szerverek (7 kötelező szolgáltatás), GitHub/Projects menedzsment, Bemutató videó

## Projekt áttekintése (Project Overview)
A projekt a **TransRoute Logisztika Kft.** 3 telephelyes (Budapest Központ, Győr Logisztikai Raktár, Szeged Fiókiroda) konvergált vállalati hálózatának tervezését, prototípusának kivitelezését és tesztelését valósítja meg Cisco Packet Tracer és Oracle VirtualBox környezetben.

### Mappastruktúra (Repository Structure)
- `/docs` – Cégprofil, IPv4/IPv6 címterv, topológiai tervrajz és dokumentációs sablonok
- `/packet-tracer-configs` – Az összes hálózati eszköz (`R1-BP1`, `R1-BP2`, `R2-GYOR`, `R3-SZEGED`, `ISP-RTR`, `Core-SW1`, `Core-SW2`, `Access-SW-BP`, `SW-GYOR`, `SW-SZEGED`, `ASA-BP`) teljes CLI konfigurációja
- `/scripts` – Programozott hálózatkonfigurációt végző Python szkript (`network_automation.py`)
- `/servers` – Windows Server (`transroute.local`) és Linux szerver beállítási útmutató (AD, DNS, DHCP, HTTPS, Fájl/Nyomtató, Mentés, GPO)
