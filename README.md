# OT-IOT-Industrial-Secure-Network-Security-project
Purdue Model industrial network simulation with pfSense, OpenPLC, SCADA, Wazuh and full VLAN segmentation


# OT/IoT Industrial Secure Network Security

> A fully functional simulation of a secure industrial network for a textile dyeing factory, built on the **Purdue Model** with complete IT/OT segmentation, SCADA, PLC automation, IoT data pipeline, and enterprise security monitoring.

---

## 🏭 Project Overview

This project simulates the complete network infrastructure of **Team3 Textile Industrial** — a fictional textile dyeing factory. It was built as part of a university course on industrial and enterprise network security.

The infrastructure spans **5 security levels** following the Purdue Model, deployed on a shared Proxmox virtualisation host with over 14 virtual machines, all segmented via pfSense VLANs and firewall rules.

---

## 🏗️ Architecture

```
Internet
    │
   WAN
    │
┌───────────────────────────────────┐
│          pfSense Firewall         │
│     (VLAN segmentation + VPN)     │
└───┬───────┬───────┬───────┬───────┘
    │       │       │       │
 VLAN10  VLAN20  VLAN30  VLAN35  VLAN40
 Level1  Level2  Level3  DMZ     Level4
  PLC     IoT     OT    Web      IT
```

### Network Segments (Purdue Model)

| VLAN | Level | Subnet | Description |
|------|-------|--------|-------------|
| VLAN10 | Level 1 | 10.10.10.0/24 | PLC / Field Devices |
| VLAN20 | Level 2 | 10.10.20.0/24 | IoT Gateway / SCADA |
| VLAN30 | Level 3 | 10.10.30.0/24 | OT Operations / Historian |
| VLAN35 | Level 3.5 | 10.10.35.0/24 | DMZ / Web |
| VLAN40 | Level 4 | 10.10.40.0/24 | Enterprise IT |

---

## 🖥️ Virtual Machines

| VM | IP | Role |
|----|-----|------|
| PLC-SIM01 | 10.10.10.10 | OpenPLC Runtime — temperature/motor simulation |
| HMI-DESKTOP | 10.10.10.12 | Node-RED HMI dashboard |
| IOT-GW01 | 10.10.20.10 | Mosquitto MQTT broker + pymodbus bridge |
| WIN-ENG01 | 10.10.30.10 | Windows engineering workstation |
| HISTORIAN01 | 10.10.30.20 | InfluxDB 2.0 + Grafana |
| SCADA01 | 10.10.30.30 | ScadaBR SCADA system |
| WEB-DMZ01 | 10.10.35.10 | Apache web server |
| REVERSE-PROXY | 10.10.35.20 | Nginx reverse proxy |
| DC01 | 10.10.40.10 | Windows Server — Active Directory / DNS |
| WAZUH01 | 10.10.40.20 | Wazuh SIEM / security monitoring |
| WIN-USER01/02 | 10.10.40.30/40 | Domain user workstations |
| WIN-ADMIN01 | 10.10.40.50 | Domain admin workstation |

---

## ⚙️ Technology Stack

### OT / Industrial
- **OpenPLC Runtime** — Structured Text PLC program simulating temperature cycling (20–85°C), alarm at 80°C triggering motor/pump shutoff
- **Modbus TCP** — PLC communication protocol on port 502
- **ScadaBR** — SCADA system with graphical factory dashboard
- **Node-RED** — HMI dashboard reading live PLC registers and coils

### IoT / Data Pipeline
- **Mosquitto MQTT** — Message broker on IOT-GW01
- **pymodbus** — Python library reading PLC holding registers and coils
- **InfluxDB 2.0** — Time-series database storing factory sensor data
- **Grafana** — Real-time operational dashboard for IT/management

### Network / Security
- **pfSense 2.7.2** — Firewall, VLAN routing, DHCP, OpenVPN
- **OpenVPN** — Remote access SSL/TLS VPN for secure management
- **Wazuh** — SIEM with agents on all machines for security monitoring
- **Nginx** — Reverse proxy in DMZ
- **Active Directory** — Windows domain with DNS, user/group policies

### Virtualisation
- **Proxmox VE 8.4** — Hypervisor hosting all VMs

---

## 🔒 Firewall Policy (Purdue Model Segmentation)

All inter-VLAN traffic is controlled by pfSense rules per interface. Key policies:

### Level 1 — PLC Network
- ✅ Modbus TCP (port 502) within VLAN10
- ✅ Modbus TCP to IoT Gateway only
- ❌ No internet access
- ❌ No access from/to IT network

### Level 2 — IoT Gateway
- ✅ Modbus TCP to PLC only
- ❌ No internet access
- ❌ No access to IT or OT networks

### Level 3 — OT Operations
- ✅ MQTT subscribe to IoT Gateway (port 1883)
- ✅ Wazuh agent reporting (port 1514)
- ✅ Management internet for engineering workstation only
- ❌ Historian blocked from reaching PLC directly

### Level 3.5 — DMZ
- ✅ Internet accessible (web server)
- ✅ Wazuh agent reporting
- ❌ Cannot reach any internal VLAN (OT, IT, IoT, PLC)

### Level 4 — Enterprise IT
- ✅ Read Grafana dashboard (port 3000)
- ✅ Access company website in DMZ
- ✅ Internet access
- ❌ Cannot reach PLC network (VLAN10)
- ❌ Cannot reach IoT network (VLAN20)

---

## 📊 Data Flow

```
PLC (OpenPLC)
    │  Modbus TCP port 502
    ▼
IOT-GW01 (pymodbus → Mosquitto MQTT)
    │  MQTT publish factory/# topics
    ▼
HISTORIAN01 (mqtt_to_influx.py → InfluxDB)
    │  Grafana reads InfluxDB
    ▼
Grafana Dashboard (accessible from IT - VLAN40)
```

---

## 🌐 Public Access

The company website is publicly accessible via Serveo tunnel:
**https://t3textile.serveousercontent.com**

---

## 🛡️ Security Monitoring

Wazuh agents are deployed on all machines and report to the Wazuh manager on `10.10.40.20`. Custom user `t3admin` manages the dashboard. All inter-VLAN policy violations are logged.

---

## 📁 Repository Structure

```
├── README.md
├── configs/
│   └── pfsense-firewall-rules.md     # Documented firewall rules per VLAN
├── scripts/
│   ├── SensorSim.st                  # OpenPLC Structured Text program
│   ├── plc_to_mqtt.py                # Modbus → MQTT bridge
│   └── mqtt_to_influx.py             # MQTT → InfluxDB writer
├── docs/
│   └── Firewall_Policy_Demo.docx     # Full policy + demo script
└── screenshots/
    └── (Grafana, ScadaBR, Node-RED, pfSense)
```

---

## 🎓 What I Learned

- Designing and implementing a **Purdue Model** industrial network from scratch
- Configuring **pfSense** VLANs, firewall rules, DHCP static mappings, and OpenVPN
- Programming **PLCs** in Structured Text and integrating with Modbus TCP
- Building an **IoT data pipeline**: PLC → Modbus → MQTT → InfluxDB → Grafana
- Deploying **SCADA** and **HMI** systems for industrial monitoring
- Setting up **Active Directory**, DNS, and domain policies
- Implementing **Wazuh SIEM** across all network segments
- Hardening network segmentation and testing firewall policies live

---

## 👤 Author

**Ilias** — Network & Security Engineer  
University project — Industrial & Enterprise Network Security

---

> *Built on Proxmox VE | pfSense | OpenPLC | ScadaBR | Node-RED | InfluxDB | Grafana | Wazuh | Mosquitto MQTT*
