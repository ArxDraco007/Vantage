# Vantage: The Autonomous Navigation Co-Pilot

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-v2.0-red.svg)](https://pytorch.org/)
[![YOLOv8](https://img.shields.io/badge/YOLO-v8-green)](https://github.com/ultralytics/ultralytics)
[![Status](https://img.shields.io/badge/Status-Prototype-orange)]()

> **"Bridging the gap between spatial GPS and situational awareness to grant the visually impaired true autonomy."**

---

## 📖 Overview

**Vantage** is a wearable "Cyber-Physical System" designed to solve the *Autonomy Gap* for the visually impaired. While traditional GPS tells a user *where* they are (Spatial Awareness), it fails to tell them *what* is immediately in front of them (Situational Awareness).

Vantage fuses these two worlds. It is a dual-layer system that combines **Macro-Navigation** (GPS routing) with **Micro-Safety** (Real-time Computer Vision) to guide users through chaotic urban environments like Indian streets safely and independently.

---

## ⚙️ System Architecture

Vantage utilizes a **Split-Compute Architecture** to balance wearability with processing power:

### 1. The Headset (The Interface)
* **Form Factor:** Lightweight, 3D-printed frames.
* **Sensors:** High-speed Micro-Camera (IMX219) for vision input.
* **Audio:** **Bone Conduction Transducers** that transmit audio via the temple bone, leaving the user's ears open to ambient traffic noise.

### 2. The Pocket Unit (The Brain)
* **Hardware:** Raspberry Pi 5 (8GB) + Battery Pack.
* **Function:** Runs the heavy AI inference (YOLOv8) and GPS logic offline to ensure zero latency.
* **Connectivity:** Tethered via a discrete USB-C cable for power and data.

---

## 🧠 The Dual-Layer AI

Vantage runs two distinct intelligence layers simultaneously:

1.  **Micro-Safety Layer (Completed):**
    * **Tech:** YOLOv8n (Nano) running on PyTorch/OpenCV.
    * **Task:** Scans the immediate path (0-5 meters) for "High-Stakes" hazards:
        * **Verticality:** Stairs, curbs, open manholes.
        * **Dynamic Threats:** Moving vehicles, pedestrians.
    * **Output:** Instant bone-conduction warnings (e.g., *"Stop. Drop-off ahead."*).

2.  **Macro-Navigation Layer (In Progress):**
    * **Tech:** GPS API + LLM Voice Chatbot (Whisper).
    * **Task:** Handles turn-by-turn routing (e.g., *"Take me to the pharmacy"*).

3.  **The Arbitrator:**
    * A logic engine that prioritizes **Safety** over **Routing**. If GPS says "Walk Forward" but Vision sees an obstacle, the Arbitrator blocks the instruction and issues a warning.

---

## 🚀 Getting Started (Software Prototype)

Currently, the repository contains the **Micro-Safety Layer** prototype, which uses your laptop's webcam to simulate the headset.

### Prerequisites
* Python 3.10+
* A Webcam

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/vantage-core.git](https://github.com/YOUR_USERNAME/vantage-core.git)
    cd vantage-core
    ```

2.  **Install Dependencies**
    ```bash
    pip install ultralytics opencv-python
    ```

3.  **Run the Pilot Script**
    ```bash
    python vantage_pilot.py
    ```

---

## 🛠️ Hardware Bill of Materials (BOM)

To build the physical "Pocket-Compute" unit:

| Component | Specification | Function |
| :--- | :--- | :--- |
| **Compute Board** | Raspberry Pi 5 (8GB) | Main AI Processor |
| **Camera** | Raspberry Pi Camera Module 3 / IMX219 | Vision Input |
| **Audio Amp** | Adafruit PAM8302 Mono Amplifier | Drives the transducers |
| **Transducers** | Bone Conduction Transducer (8 Ohm 1W) | "Silent" Audio Output |
| **Power** | 10,000mAh Power Bank (USB-C PD) | Portable Power |
| **Chassis** | SLS Nylon 3D Print | Custom Headset Frame |

---

## 🗺️ Roadmap (Learning Planet Grant)

This project is currently participating in the **Learning Planet Youth Design Challenge**.

* **Phase 1 (Current):** Developed the Micro-Safety software layer (YOLOv8 logic) and validated the "Verticality Detection" model.
* **Phase 2 (Months 1-3):** Porting code to Raspberry Pi 5 and integrating the GPS/Voice API.
* **Phase 3 (Months 4-6):** Fabricating the physical headset and soldering the Bone Conduction circuit.
* **Phase 4 (Months 7-12):** Field testing in Tamil Nadu (Unstructured Urban Environments).

---

## 👤 Author

**Aryan India Gavaskar**
* *Student Developer & Social Innovator*
* *Tamil Nadu, India*
* **Focus:** AI, Computer Vision, & Inclusive Design.

---
