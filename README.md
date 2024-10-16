# Battery Management System (BMS) - Battery Parameter Checker  

## Overview

Electric Vehicles (EVs) rely heavily on **Battery Management Systems (BMS)** to monitor and safeguard the battery during charging and usage. This project focuses on ensuring the **health of the battery** during the charging phase of **Li-ion batteries** by validating key parameters:

1. **Temperature**  
2. **State of Charge (SOC)**  
3. **Charge Rate**

The goal is to ensure the battery operates within safe limits while also providing **early warnings** to alert users when a parameter approaches critical values.

---

## Purpose

A BMS performs various essential tasks for managing the health and performance of batteries, such as:  
- **Protecting batteries** during charging: at home, in public places, or through regenerative braking in vehicles.  
- **Estimating life, inventory, and supply chains** for battery production and usage.

The **charging phase** is critical, as improper conditions can reduce battery life or cause safety hazards. This project focuses on **charging-phase monitoring** to prevent such issues.

---

## Issues Addressed by this Project  

1. **High complexity** of a single function:  
   - Refactored logic into smaller, reusable methods.  
   - Cyclomatic complexity reduced by isolating parameter checks.

2. **Incomplete tests**:  
   - All conditions are now covered, including boundary and edge cases.  
   - Abnormal vitals are reported along with the **specific type of breach** (high/low).  

3. **Avoid duplication**:  
   - Similar logic is merged into shared functions for simplicity and maintainability.  

4. **Pluggable reporters**:  
   - Reporters (like **FileReporter** and **ListReporter**) are now modular and can be plugged in dynamically.

---

## Programming Paradigms Used

This project employs multiple **programming paradigms** to address different design needs effectively:

1. **Procedural Programming**:  
   - For sequences where operations are performed step by step (e.g., parameter evaluation).

2. **Functional Programming**:  
   - Shared logic, such as warning thresholds, is abstracted into pure functions that map inputs to outputs.

3. **Object-Oriented Programming**:  
   - Encapsulates state (parameters, limits) and actions (evaluation, reporting) inside classes like `BatteryChecker`.

4. **Aspect-Oriented Programming**:  
   - Repeating aspects like **reporting breaches** and **early warnings** are captured and modularized into reporters.

---

## Key Features

1. **Early Warning System**:
   - A **5% tolerance** is applied to the upper threshold of parameters to provide early warnings.
   - Example for SOC (range: 20 to 80):
     - **20 to 24**: *"Approaching discharge"*
     - **76 to 80**: *"Approaching charge-peak"*

2. **Dynamic Reporters**:
   - **FileReporter**: Logs messages to a file.
   - **ListReporter**: Collects reports in memory for testing.
   - Additional reporters can be implemented and plugged in without changing core logic.

3. **Abnormal Vital Reporting**:
   - The system reports **which parameter breached** and whether it was **too high** or **too low**.  

4. **Configurable Warning System**:
   - Warnings are **optional** per parameter, and new parameters can be added easily in the future.

---
