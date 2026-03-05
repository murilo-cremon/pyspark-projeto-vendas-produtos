from pathlib import Path

# Variáveis raíz do projeto
current_path = Path(__file__).resolve()
BASE_DIR = current_path.parent.parent.parent.parent

# Variáveis dos diretórios da arquitetura medalhão
MEDALLION_ARCHITECTURE_PATH = f'{BASE_DIR}/medallion_architecture/'

# Diretório da landing zone e arquivo para ingestão
LANDING_ZONE = f'{MEDALLION_ARCHITECTURE_PATH}/landing_zone/'
LANDING_ZONE_FILE = f'{LANDING_ZONE}/product-sales.csv'

RAW_ZONE = f'{MEDALLION_ARCHITECTURE_PATH}/raw_zone/'
TRUSTED_ZONE = f'{MEDALLION_ARCHITECTURE_PATH}/trusted_zone/'
REFINED_ZONE = f'{MEDALLION_ARCHITECTURE_PATH}/refined_zone/'

# Variáveis de aplicação para o Spark
APP_NAME = 'product_sales'