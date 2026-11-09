import argparse
import random
import time

import requests


def main():
    p = argparse.ArgumentParser(description="Simula um sensor enviando temperatura por HTTP")
    p.add_argument("--url", required=True, help="Ex.: http://127.0.0.1:8000")
    p.add_argument("--id", type=int, required=True, help="ID do dispositivo")
    p.add_argument("--token", required=True, help="Token do dispositivo (veja no /admin/)")
    p.add_argument("--intervalo", type=int, default=30, help="Segundos entre envios")
    a = p.parse_args()

    endpoint = f"{a.url.rstrip('/')}/forum/dispositivos/{a.id}/leituras/"
    temperatura = 24.0
    while True:
        temperatura += random.uniform(-0.6, 0.6)
        try:
            r = requests.post(
                endpoint,
                json={"temperatura": round(temperatura, 1)},
                headers={"X-API-Key": a.token},
                timeout=90,  # o Render gratuito pode demorar para "acordar"
            )
            print(time.strftime("%H:%M:%S"), r.status_code, round(temperatura, 1))
        except requests.RequestException as erro:
            print("erro:", erro)
        time.sleep(a.intervalo)


if __name__ == "__main__":
    main()