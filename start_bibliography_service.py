#!/usr/bin/env python3
"""
JurisRank Bibliography Service Starter
Script para inicializar y gestionar el servicio completo de bibliografía
"""

import os
import sys
import subprocess
import time
import json
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BibliographyServiceManager:
    """Gestor del servicio de bibliografía JurisRank"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config_file = self.project_root / "bibliography_config.json"
        self.supervisor_conf = self.project_root / "supervisord_bibliography.conf"
        self.logs_dir = self.project_root / "logs"
        
        # Cargar configuración
        self.config = self.load_config()
        
    def load_config(self):
        """Cargar configuración desde archivo JSON"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_file}")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Configuración por defecto"""
        return {
            "web_interface": {
                "host": "0.0.0.0",
                "port": 5001,
                "debug": False
            },
            "logging": {
                "level": "INFO"
            }
        }
    
    def setup_environment(self):
        """Configurar el entorno necesario"""
        logger.info("🔧 Setting up environment...")
        
        # Crear directorio de logs
        self.logs_dir.mkdir(exist_ok=True)
        logger.info(f"✅ Logs directory created: {self.logs_dir}")
        
        # Verificar dependencias
        self.check_dependencies()
        
        # Verificar archivos necesarios
        self.verify_files()
        
    def check_dependencies(self):
        """Verificar que las dependencias estén instaladas"""
        logger.info("📦 Checking dependencies...")
        
        try:
            import flask
            import requests
            logger.info("✅ Flask and requests available")
        except ImportError as e:
            logger.error(f"❌ Missing dependencies: {e}")
            logger.info("Installing requirements...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                          check=True)
        
        try:
            import supervisor
            logger.info("✅ Supervisor available")
        except ImportError:
            logger.info("Installing supervisor...")
            subprocess.run([sys.executable, "-m", "pip", "install", "supervisor"], check=True)
    
    def verify_files(self):
        """Verificar que todos los archivos necesarios existen"""
        required_files = [
            "src/bibliography_manager.py",
            "bibliography_api.py",
            "jurisrank_bibliography_integration.py",
            "bibliography_config.json"
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                logger.error(f"❌ Required file not found: {file_path}")
                raise FileNotFoundError(f"Required file not found: {file_path}")
        
        logger.info("✅ All required files verified")
    
    def start_with_supervisor(self):
        """Iniciar el servicio usando Supervisor"""
        logger.info("🚀 Starting Bibliography Service with Supervisor...")
        
        try:
            # Verificar si supervisor ya está corriendo
            result = subprocess.run(['supervisorctl', '-c', str(self.supervisor_conf), 'status'], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                # Iniciar supervisord
                logger.info("Starting supervisord...")
                subprocess.run(['supervisord', '-c', str(self.supervisor_conf)], check=True)
                time.sleep(2)
            
            # Verificar el estado del servicio
            result = subprocess.run(['supervisorctl', '-c', str(self.supervisor_conf), 'status'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Bibliography Service started successfully with Supervisor")
                logger.info(f"📊 Service status:\n{result.stdout}")
                return True
            else:
                logger.error(f"❌ Failed to start service: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Supervisor startup failed: {e}")
            return False
    
    def start_direct(self):
        """Iniciar el servicio directamente (desarrollo)"""
        logger.info("🚀 Starting Bibliography Service directly...")
        
        try:
            # Establecer variables de entorno
            env = os.environ.copy()
            env['PYTHONPATH'] = f"{self.project_root}:{self.project_root}/src"
            
            # Ejecutar el API server
            process = subprocess.Popen([
                sys.executable, 
                str(self.project_root / "bibliography_api.py")
            ], env=env, cwd=str(self.project_root))
            
            # Esperar un momento para que inicie
            time.sleep(3)
            
            # Verificar que el proceso esté corriendo
            if process.poll() is None:
                logger.info("✅ Bibliography Service started successfully")
                return process
            else:
                logger.error("❌ Service failed to start")
                return None
                
        except Exception as e:
            logger.error(f"❌ Direct startup failed: {e}")
            return None
    
    def test_service(self):
        """Probar que el servicio esté funcionando"""
        logger.info("🧪 Testing service connectivity...")
        
        import requests
        import time
        
        # Esperar un poco más para que el servicio inicie completamente
        time.sleep(5)
        
        port = self.config.get('web_interface', {}).get('port', 5001)
        test_url = f"http://localhost:{port}/health"
        
        max_retries = 10
        for attempt in range(max_retries):
            try:
                response = requests.get(test_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"✅ Service is responding: {data.get('status', 'unknown')}")
                    return True
            except requests.exceptions.RequestException:
                if attempt < max_retries - 1:
                    logger.info(f"⏳ Attempt {attempt + 1}/{max_retries} - Service not ready, waiting...")
                    time.sleep(2)
                else:
                    logger.error("❌ Service is not responding after multiple attempts")
        
        return False
    
    def get_service_info(self):
        """Obtener información del servicio"""
        port = self.config.get('web_interface', {}).get('port', 5001)
        
        info = {
            'web_interface': f"http://localhost:{port}",
            'health_check': f"http://localhost:{port}/health",
            'api_base': f"http://localhost:{port}/api/v1/bibliography",
            'config_file': str(self.config_file),
            'logs_directory': str(self.logs_dir)
        }
        
        return info
    
    def run(self, use_supervisor=True):
        """Ejecutar el servicio completo"""
        logger.info("=" * 60)
        logger.info("🚀 JurisRank Bibliography Service Manager")
        logger.info("=" * 60)
        
        try:
            # Configurar entorno
            self.setup_environment()
            
            # Iniciar servicio
            if use_supervisor:
                success = self.start_with_supervisor()
            else:
                process = self.start_direct()
                success = process is not None
            
            if not success:
                logger.error("❌ Failed to start service")
                return False
            
            # Probar servicio
            if self.test_service():
                # Mostrar información del servicio
                info = self.get_service_info()
                
                logger.info("=" * 60)
                logger.info("✅ JurisRank Bibliography Service is running!")
                logger.info("=" * 60)
                logger.info(f"🌐 Web Interface: {info['web_interface']}")
                logger.info(f"📋 Health Check: {info['health_check']}")
                logger.info(f"🔌 API Base URL: {info['api_base']}")
                logger.info(f"📝 Configuration: {info['config_file']}")
                logger.info(f"📊 Logs Directory: {info['logs_directory']}")
                logger.info("=" * 60)
                logger.info("📚 Features Available:")
                logger.info("   • Academic reference parsing and management")
                logger.info("   • JurisRank integration for legal analysis")
                logger.info("   • Multi-format bibliography export")
                logger.info("   • Advanced relevance scoring")
                logger.info("   • Web-based management interface")
                logger.info("=" * 60)
                
                if not use_supervisor:
                    logger.info("🔄 Service running in foreground mode")
                    logger.info("Press Ctrl+C to stop the service")
                    try:
                        process.wait()
                    except KeyboardInterrupt:
                        logger.info("\n🛑 Stopping service...")
                        process.terminate()
                        process.wait()
                        logger.info("✅ Service stopped")
                
                return True
            else:
                logger.error("❌ Service health check failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="JurisRank Bibliography Service Manager")
    parser.add_argument("--direct", action="store_true", 
                       help="Run service directly (development mode)")
    parser.add_argument("--supervisor", action="store_true", default=True,
                       help="Run service with Supervisor (production mode)")
    
    args = parser.parse_args()
    
    # Determinar modo de ejecución
    use_supervisor = not args.direct
    
    # Inicializar y ejecutar el gestor
    manager = BibliographyServiceManager()
    success = manager.run(use_supervisor=use_supervisor)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)