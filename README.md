# FreePBX-Breaker
PoC y código automatizado para explotar CVE-2025-57819 en FreePBX. Demuestra la vulnerabilidad de Ejecución Remota de Código (RCE) mediante inyección de comandos en el sistema Asterisk. Ideal para entornos HackTheBox.
# FreePBX Exploitation: CVE-2025-57819 Attack Guide

##  Resumen General
Este repositorio contiene la Prueba de Concepto (PoC) y la metodología detallada para explotar la vulnerabilidad **CVE-2025-57819** en instalaciones de FreePBX, específicamente diseñada para el entorno de la máquina **Connected** en HackTheBox.

Esta vulnerabilidad permite a un atacante obtener accesos elevados o ejecutar comandos arbitrarios en el sistema operativo subyacente (Asterisk/FreePBX) mediante la manipulación de parámetros de entrada, lo que deriva en una **Ejecución Remota de Código (RCE)**.

*   **Sistema Afectado:** FreePBX
*   **ID de Vulnerabilidad:** CVE-2025-57819
*   **Impacto:** Crítico (Ejecución Remota de Código $\rightarrow$ Compromiso total del sistema).

---

## ¿En Qué Consiste el Exploit? (Concepto de la Vulnerabilidad)

### ¿Qué es CVE-2025-57819?
La vulnerabilidad reside en el [Especificar Módulo/Componente, ej: Gestor de Dialplan, Oyente AMI, o API Gateway] dentro del marco de FreePBX. La falla se encuentra en cómo el sistema **sanitiza la entrada de usuario** al procesar funciones específicas (como la adición de extensiones, configuración de troncales o ejecución de scripts personalizados).

**Mecanismo de Falla (El "Cómo"):**
1.  **Punto de Ataque:** El atacante dirige su ataque a un parámetro específico (ej: `extension_name`, `ivr_command`, o un parámetro API).
2.  **Construcción del Payload:** En lugar de proporcionar un valor válido, el atacante introduce caracteres especiales del *shell* (como `;`, `|`, `&&`, `$()`).
3.  **Flujo de Ejecución:** El código vulnerable ejecuta la cadena de entrada directamente a través de un *shell* del sistema (usando funciones como `system()` en C/C++ o `subprocess.run()` en Python). El *parser* del shell interpreta los caracteres inyectados, permitiendo al atacante encadenar comandos maliciosos después o en lugar del comando original.
4.  **Objetivo:** El atacante utiliza esta cadena para ejecutar comandos como `whoami`, `cat /etc/shadow`, o descargar *backdoors*.

---

## ¿Cómo Usar el Exploit? (Guía Paso a Paso)

Este repositorio provee un script de Python para automatizar el ataque.

### Prerrequisitos
*   **Python 3:** Instalado en tu máquina atacante.
*   **Librería `requests`:** Debe estar instalada (`pip install requests`).
*   **Detalles del Target:** Necesitas la dirección IP y el puerto específico del servicio de FreePBX que estás atacando en la máquina Connected.

### Pasos de Ejecución

**Paso 1: Identificación del Target**
Para la máquina Connected de HackTheBox, confirma el punto de entrada vulnerable (¿Es la UI web? ¿Es el puerto AMI? ¿Es una API REST?).

*   **IP Target:** `[IP_DE_LA_MAQUINA_CONNECTED]`
*   **Endpoint Vulnerable:** `[URL_DEL_ENDPOINT_VULNERABLE]`

**Paso 2: Configuración del Payload**
Debes ajustar las variables dentro del archivo `exploit.py`:

*   `TARGET_URL`: Establece la URL completa del punto de ataque.
*   `MALICIOUS_PAYLOAD`: **Este es el componente clave.**
    *   Si el ataque es RCE: Define el campo `"command"` con el comando shell que deseas ejecutar (ej: `"id"`, `"cat /etc/passwd"`).
    *   Si es otra inyección: Modifica la estructura de este diccionario para que coincida con el modelo de datos del endpoint afectado.

**Paso 3: Ejecución**
Ejecuta el script desde tu terminal:
```bash
python3 exploit.py
