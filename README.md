# 🔒 SafeRansomwareLab

> [!WARNING]  
>**AVISO IMPORTANTE:** Este software es **ÚNICAMENTE** para fines educativos en entornos controlados. El mal uso de este código puede violar leyes locales e internacionales. **No me hago responsables del uso indebido.**

![Banner](./images/banner-Shutterstock.png)

> [!NOTE]  
> Photo © Shutterstock

## 🎯 Descripción del Proyecto
**SafeRansomwareLab** es un **simulador educativo de ransomware** que implementa un **sistema de cifrado híbrido** combinando RSA para el intercambio seguro de claves y AES-256 para el cifrado de archivos. Desarrollado en Python, el software simula el comportamiento de ransomware real generando un par de claves pública/privada RSA, donde la clave AES simétrica utilizada para cifrar archivos (documentos, imágenes, PDFs, comprimidos, etc.) en la carpeta `test_files` es a su vez cifrada con la clave pública RSA. El sistema incluye mecanismos de recuperación educativos que permiten descifrar los archivos utilizando la clave privada RSA correspondiente, demostrando así técnicas criptográficas avanzadas en un entorno controlado y seguro para fines de formación en ciberseguridad.

## 💻 Requisitos del Sistema

### 📦 Requisitos del Sistema `requirements.txt`
```
cryptography>=3.4.8
rich>=10.0.0
questionary>=1.10.0
reportlab>=3.6.8
qrcode[pil]>=7.3.1
Pillow>=8.3.0
```

### 🗃️ Archivos generados tras el cifrado/captura de los archivos
- `private_key.pem`: Clave privada RSA (recuperación)  
- `public_key.pem`: Clave pública RSA (cifrado)  
- `INSTRUCCIONES_RESCATE.pdf`: PDF de “rescate” simulado con los pasos a seguir

## 🔐 Especificaciones Criptográficas Usadas

| Componente | Algoritmo | Parámetros | Propósito | Nivel de Seguridad |
|------------|-----------|------------|-----------|-------------------|
| **Cifrado de Datos** | AES-256 | CBC Mode, PKCS7 Padding | Cifrado eficiente de archivos | 256 bits |
| **Intercambio de Claves** | RSA-2048 | OAEP with SHA-256 | Protección segura de claves AES | ~112 bits |
| **Generación de IV** | CSPRNG | 16 bytes | Unicidad por archivo | 128 bits |
| **Padding Asimétrico** | RSA-OAEP | MGF1 SHA-256 | Prevención de ataques | Estándar PKCS#1 |

## 🖼️ Galería de la Demo **SafeRansomwareLab**

1. **Archivos Desencriptados**  
   ![0-archivos-desencriptados](./images/0-archivos-desencriptados.png)

2. **Menú Principal**  
   ![1-menu-principal](./images/1-menu-principal.png)

3. **Menú Principal – Opción 1**  
   ![2-menu-principal-opcion-1](./images/2-menu-principal-opcion-1.png)

4. **Menú Principal – Opción 1 (Fin)**  
   ![3-menu-principal-opcion-1-fin](./images/3-menu-principal-opcion-1-fin.png)

5. **Archivos Encriptados**  
   ![4-archivos-encriptados](./images/4-archivos-encriptados.png)

6. **Archivos – Recuperación**  
   ![5-archivos-recuperacion](./images/5-archivos-recuperacion.png)

7. **Menú Principal – Opción 2**  
   ![6-menu-principal-opcion-2](./images/6-menu-principal-opcion-2.png)

8. **Menú Secundario**  
   ![7-menu-secundario](./images/7-menu-secundario.png)

9. **Menú Secundario – S**  
   ![8-menu-secundario-S](./images/8-menu-secundario-S.png)


## 📫 Contact

Si tienes dudas o deseas aportar sugerencias puedes escribirme a: [marichu.private@proton.me](mailto:marichu.private@proton.me)

## 📄 License

Este proyecto está licenciado bajo la **Licencia MIT**. Consulte el archivo [LICENCIA](LICENCIA) para más detalles.
