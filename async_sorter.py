import asyncio
import aiofiles
import aiofiles.os
import aiofiles.ospath
import argparse
import logging
from pathlib import Path


# налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Тестовий запис, потім уберемо
logging.info("Логування ініціалізовано успішно.")


# --- Точка входу (тимчасова) ---
if __name__ == "__main__":
    print("Step 1: Імпорти та логування виконані успішно.")
