#!/usr/bin/env python3
"""
SISTEMA DE RECUPERACIÓN - INTERFAZ PROFESIONAL
Flujo correcto: RSA-2048 (clave AES) → AES-256 (datos)
"""

import os
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes

TARGET_DIR = "./test_files/"
RSA_PRIVATE_KEY = "./private_key.pem"
BOX_WIDTH = 60

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class BoxChars:
    HORIZONTAL = '═'
    VERTICAL = '║'
    TOP_LEFT = '╔'
    TOP_RIGHT = '╗'
    BOTTOM_LEFT = '╚'
    BOTTOM_RIGHT = '╝'
    VERTICAL_LEFT = '╠'
    VERTICAL_RIGHT = '╣'
    HORIZONTAL_DOWN = '╦'
    HORIZONTAL_UP = '╩'
    CROSS = '╬'

class ProfessionalFileDecryptor:
    def __init__(self):
        self.stats = {'recovered_files': 0, 'error_files': 0, 'total_files': 0}
        self.private_key = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_boxed(self, text, width, color, is_title=False):
        """Imprimir texto en una caja con estilo"""
        lines = text.split('\n')
        
        # Línea superior
        print(f"{color}{BoxChars.TOP_LEFT}{BoxChars.HORIZONTAL * (width-2)}{BoxChars.TOP_RIGHT}{Colors.RESET}")
        
        for line in lines:
            if is_title:
                # Centrar texto para títulos
                padded_line = line.center(width-2)
            else:
                # Alinear a la izquierda para contenido
                padded_line = f" {line.ljust(width-3)}"
            
            print(f"{color}{BoxChars.VERTICAL}{Colors.RESET}{padded_line}{color}{BoxChars.VERTICAL}{Colors.RESET}")
        
        # Línea inferior
        print(f"{color}{BoxChars.BOTTOM_LEFT}{BoxChars.HORIZONTAL * (width-2)}{BoxChars.BOTTOM_RIGHT}{Colors.RESET}")

    def print_header(self):
        """Imprimir encabezado del sistema de recuperación"""
        self.clear_screen()
        
        # Título principal
        title = f"{Colors.BOLD}{Colors.GREEN}        🔓 SISTEMA DE RECUPERACIÓN DE ARCHIVOS 🔓         {Colors.RESET}"
        self.print_boxed(title, BOX_WIDTH, Colors.GREEN, True)
        
        # Descripción
        description = f"{Colors.BLUE}         📁 Descifrado seguro de archivos cifrados        {Colors.RESET}"
        self.print_boxed(description, BOX_WIDTH, Colors.BLUE, True)

    def decrypt_aes_key_with_rsa(self, encrypted_aes_key):
        """Descifrar clave AES con RSA privada (Paso 1 del flujo inverso)"""
        try:
            return self.private_key.decrypt(
                encrypted_aes_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            print(f"{Colors.RED}❌ Error descifrando clave AES con RSA: {str(e)}{Colors.RESET}")
            return None

    def decrypt_file_hybrid(self, file_path):
        """
        Descifrado híbrido con flujo inverso correcto:
        1. 🔓 RSA-2048 (Descifrar clave AES) - Recupera la clave
        2. 🔓 AES-256 (Descifrar datos) - Recupera el archivo
        3. 📁 ARCHIVO ORIGINAL RECUPERADO
        """
        try:
            with open(file_path, 'rb') as f:
                # Leer estructura: IV + clave_AES_cifrada + archivo_cifrado
                iv = f.read(16)  # Primeros 16 bytes: IV
                key_len_bytes = f.read(4)  # Siguientes 4 bytes: longitud clave
                key_len = int.from_bytes(key_len_bytes, 'big')
                encrypted_aes_key = f.read(key_len)  # Clave AES cifrada
                ciphertext = f.read()  # Resto: datos cifrados

            # ==================== FASE 1: RECUPERACIÓN CLAVE ====================
            # Paso 1: Descifrar la clave AES con RSA privada
            aes_key = self.decrypt_aes_key_with_rsa(encrypted_aes_key)
            if not aes_key:
                return False

            # ==================== FASE 2: DESCIFRADO DATOS ====================
            # Paso 2: Descifrar los datos con AES
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Remover padding
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(decrypted_padded) + unpadder.finalize()

            # ==================== FASE 3: GUARDADO ====================
            # Paso 3: Guardar archivo original
            original_path = file_path[:-10]  # Remover ".encrypted"
            with open(original_path, 'wb') as f:
                f.write(plaintext)
            
            # Eliminar archivo cifrado
            os.remove(file_path)
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error en descifrado híbrido {file_path}: {str(e)}{Colors.RESET}")
            return False

    def perform_professional_recovery(self):
        self.print_header()
        
        # Buscar archivos cifrados
        encrypted_files = [
            os.path.join(root, f) for root, _, files in os.walk(TARGET_DIR)
            for f in files if f.endswith('.encrypted')
        ]
        
        self.stats['total_files'] = len(encrypted_files)
        
        if not encrypted_files:
            no_files_title = f"{Colors.BOLD}{Colors.BLUE} 📊 Estado del sistema:                                {Colors.RESET}"
            no_files_list = [
                f"{Colors.GREEN} •{Colors.RESET} No hay archivos cifrados para recuperar{' ':>10}{Colors.RESET}"
            ]
            no_files_text = no_files_title + "\n" + "\n".join(no_files_list)
            self.print_boxed(no_files_text, BOX_WIDTH, Colors.BLUE, False)
            
            input(f"\n{Colors.YELLOW}Presione Enter para continuar...{Colors.RESET}")
            return
        
        # Mostrar información
        files_title = f"{Colors.BOLD}{Colors.CYAN} 📋 Información de recuperación:                         {Colors.RESET}"
        files_list = [
            f"{Colors.GREEN} •{Colors.RESET} Archivos cifrados encontrados: {Colors.CYAN}{len(encrypted_files)}{' ':>18}   {Colors.RESET}",
            f"{Colors.GREEN} •{Colors.RESET} Flujo de descifrado: {Colors.CYAN}RSA(clave) → AES(datos){' ':>10}{Colors.RESET}"
        ]
        files_text = files_title + "\n" + "\n".join(files_list)
        self.print_boxed(files_text, BOX_WIDTH, Colors.CYAN, False)
        
        confirm = input(f"{Colors.BOLD}{Colors.CYAN}¿Iniciar recuperación? (s/n): {Colors.RESET}").strip().lower()
        if confirm != 's':
            print(f"{Colors.RED}❌ Recuperación cancelada{Colors.RESET}")
            return
        
        # Cargar clave RSA privada
        if not os.path.exists(RSA_PRIVATE_KEY):
            error_title = f"{Colors.BOLD}{Colors.RED} ❌ Error del sistema:                                  {Colors.RESET}"
            error_list = [
                f"{Colors.RED} •{Colors.RESET} No se encontró la clave privada{' ':>18}{Colors.RESET}",
                f"{Colors.YELLOW} •{Colors.RESET} Buscar archivo: {RSA_PRIVATE_KEY}{' ':>20}{Colors.RESET}",
                f"{Colors.YELLOW} •{Colors.RESET} Sin la clave RSA, no se puede descifrar{' ':>7}{Colors.RESET}"
            ]
            error_text = error_title + "\n" + "\n".join(error_list)
            self.print_boxed(error_text, BOX_WIDTH, Colors.RED, False)
            
            input(f"\n{Colors.YELLOW}Presione Enter para continuar...{Colors.RESET}")
            return
        
        print(f"\n{Colors.BLUE}🔄 Cargando clave privada RSA...{Colors.RESET}")
        with open(RSA_PRIVATE_KEY, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(), password=None, backend=default_backend()
            )
        
        # Recuperación
        print(f"{Colors.GREEN}🔄 Recuperando archivos...{Colors.RESET}")
        print(f"{Colors.CYAN}Flujo: RSA-2048(clave AES) → AES-256(datos){Colors.RESET}")
        
        for i, file_path in enumerate(encrypted_files):
            if self.decrypt_file_hybrid(file_path):
                self.stats['recovered_files'] += 1
            else:
                self.stats['error_files'] += 1
            
            progress = (i + 1) / len(encrypted_files) * 100
            bars = "█" * int(progress / 5) + " " * (20 - int(progress / 5))
            print(f"{Colors.CYAN}[{bars}] {progress:.1f}%{Colors.RESET}", end='\r')
            time.sleep(0.1)
        
        print()  # Nueva línea después de la barra de progreso
        
        self.show_professional_summary()

    def show_professional_summary(self):
        """Mostrar resumen de recuperación - Sin cuadro de resultado final adicional"""
        self.print_header()

        summary_title = f"{Colors.BOLD}{Colors.GREEN} 📊 Resumen de recuperación:                             {Colors.RESET}"
        summary_list = [
            f"{Colors.GREEN} •{Colors.RESET} Total de archivos: {Colors.CYAN}{self.stats['total_files']:<25}          {Colors.RESET}",
            f"{Colors.GREEN} •{Colors.RESET} Archivos recuperados: {Colors.CYAN}{self.stats['recovered_files']:<23}         {Colors.RESET}",
            f"{Colors.GREEN} •{Colors.RESET} Archivos con error: {Colors.CYAN}{self.stats['error_files']:<25}         {Colors.RESET}"
        ]

        if self.stats['total_files'] > 0:
            success_rate = (self.stats['recovered_files'] / self.stats['total_files']) * 100
            summary_list.append(f"{Colors.GREEN} •{Colors.RESET} Tasa de éxito: {Colors.CYAN}{success_rate:.1f}%{' ':>30}   {Colors.RESET}")

        # 👉 Aquí ya no se añaden frases extra (status_icon, status_msg, details_msg)
        summary_text = summary_title + "\n" + "\n".join(summary_list)
        self.print_boxed(summary_text, BOX_WIDTH, Colors.GREEN, False)

        # Limpieza de archivos de simulación
        files_to_remove = ["./private_key.pem", "./public_key.pem", "./README_RECOVER.txt", "./INSTRUCCIONES_RESCATE.pdf"]
        removed = 0

        for file_path in files_to_remove:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    removed += 1
                except:
                    pass

        if removed > 0:
            cleanup_title = f"{Colors.BOLD}{Colors.BLUE} 🧹 Limpieza del sistema:                                {Colors.RESET}"
            cleanup_list = [
                f"{Colors.BLUE} •{Colors.RESET} Archivos de simulación limpiados: {Colors.CYAN}{removed}{' ':>10}         {Colors.RESET}"
            ]
            cleanup_text = cleanup_title + "\n" + "\n".join(cleanup_list)
            self.print_boxed(cleanup_text, BOX_WIDTH, Colors.BLUE, False)

        input(f"\n{Colors.YELLOW}Presione Enter para continuar...{Colors.RESET}")

def main():
    decryptor = ProfessionalFileDecryptor()
    decryptor.perform_professional_recovery()

if __name__ == "__main__":
    main()