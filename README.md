<p align="center">
  <img src="https://img.shields.io/badge/Pentest%20Tool-Automated-red?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/github/license/USERNAME/REPO?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python"/>
</p>

<h1 align="center">🕵‍♂ OSINT Ghost Root</h1>
<p align="center">
  All-in-one OSINT username enumeration toolkit (Recon → Scan → Report).<br/>
  <em>Educational & Ethical Use Only — gunakan hanya pada target yang Anda miliki izin eksplisit.</em>
</p>

---
## Tampilan Awal

<p align="center">
  <img src="/img/awal.png" alt="Contoh output web_scanner_ghost" width="800"/><br>
  <em>Demo Script Dijalankan: <code><br>Masukan Nama target<pentest_output/</code>.</em>
</p>

## Tampilan Akhir

<p align="center">
  <img src="/img/akhir.png" alt="Contoh output web_scanner_ghost" width="800"/><br>
  <em>Demo akhir: <code><br>Informasi Akun sosmed ditemukan<pentest_output/</code>.</em></p>






## 🔎 Ringkasan

_OSINT Ghost Root_ adalah toolkit Python untuk melakukan enumerasi username di berbagai platform sosial media (Twitter, Instagram, TikTok, Facebook, YouTube, Reddit, GitHub, Telegram, LinkedIn).  
Output disimpan dalam JSON, disertai animasi CLI, progress bar, dan generator variasi username (prefix/suffix, angka, leet).

Fokus: kemudahan pemakaian, laporan terstruktur, kompatibilitas Linux & Termux (Android).

---

## ✨ Fitur Utama

- Multi-platform username checking: Twitter, Instagram, TikTok, Facebook, YouTube, Reddit, GitHub, Telegram, LinkedIn.
- Status deteksi akun: _active, **private, **inactive, **not_found, **error_.
- Generator variasi username: kombinasi, angka, prefix/suffix, leet.
- UX CLI: typing effect, glitch effect, progress bar.
- Hasil tersimpan otomatis ke results/hasil*<target>*<timestamp>.json.
- Tanpa proxy (No-proxy version).
- Ringkas, mudah di-extend, siap dipasang di Kali Linux & Termux.

---

### Cara Clone

```bash
git clone https://github.com/Sneijderlino/Osint_Ghost.git
cd Osint_Ghost
```

<h1 align="center">Instalasi & Setup</h1>

### Cara Clone

#### (Rekomdasi: Gunakan Virtualenv)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### install(Kali Linux / Debian-based)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git
git clone https://github.com/Sneijderlino/Osint_Ghost.git
cd Osint_Ghost
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txtt

```

#### Catatan SSL / aiohttp: jika menemukan error SSL, pastikan OpenSSL & certifi terpasang

```bash
sudo apt install -y openssl ca-certificates
pip install certifi
```

### instalasi (Termux-Android)

```bash
pkg update && pkg upgrade -y
pkg install -y python git clang openssl libffi
git clone https://github.com/Sneijderlino/Osint_Ghost.git
cd Osint_Ghost
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```

### Jika aiohttp mengeluhkan SSL, pastikan variabel lingkungan menunjuk ke cert bundle Termux:

```bash
export LD_LIBRARY_PATH=$PREFIX/lib
export SSL_CERT_FILE=$PREFIX/etc/tls/cert.pem
```

### Cara Menjalankan

```bash
# Linux / Termux
python3 osint_ghost

# Jika environment menggunakan 'python' sebagai alias
python osint_ghost
```


