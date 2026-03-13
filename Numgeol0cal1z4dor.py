#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import requests
import json

def print_banner():
    print("\033[1;36m")
    print("╔══════════════════════════════════════╗")
    print("║       GeoLocalizador Telefónico      ║")
    print("║         (Para uso ético y legal)     ║")
    print("╚══════════════════════════════════════╝")
    print("\033[0m")

def info_basica(numero):
    try:
        num_parseado = phonenumbers.parse(numero, None)
        if not phonenumbers.is_valid_number(num_parseado):
            return None, "Número inválido"

        pais = geocoder.description_for_number(num_parseado, "es")
        operador = carrier.name_for_number(num_parseado, "es")
        zona = timezone.time_zones_for_number(num_parseado)
        tipo = "Móvil" if phonenumbers.number_type(num_parseado) == 1 else "Fijo/VOIP"

        return {
            "pais": pais,
            "operador": operador,
            "zona_horaria": zona,
            "tipo": tipo,
            "valido": True
        }, None
    except Exception as e:
        return None, f"Error al parsear: {str(e)}"

def info_geolocalizacion(numero):
    try:
        url = f"https://api.veriphone.io/v2/verify?phone={numero}"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get("phone_valid"):
            return {
                "pais_iso": data.get("country_code"),
                "pais": data.get("country"),
                "operador_api": data.get("carrier")
            }, None
        else:
            return None, "API no devuelve datos válidos"
    except:
        return None, "No se pudo conectar a la API externa"

def main():
    print_banner()
    if len(sys.argv) != 2:
        print("\033[1;33mUso: python3 migeolocalizador.py +521234567890\033[0m")
        sys.exit(1)

    numero = sys.argv[1]
    print(f"\n[*] Analizando número: {numero}")

    info, error = info_basica(numero)
    if error:
        print(f"\033[1;31m[!] Error: {error}\033[0m")
        sys.exit(1)

    print("\n[+] Información básica:")
    print(f"   País: {info['pais']}")
    print(f"   Operador: {info['operador']}")
    print(f"   Zona horaria: {info['zona_horaria']}")
    print(f"   Tipo de línea: {info['tipo']}")

    print("\n[*] Consultando APIs externas...")
    geo_info, geo_error = info_geolocalizacion(numero)
    if geo_info:
        print(f"   API: {geo_info.get('pais')} (Operador: {geo_info.get('operador_api')})")
    else:
        print(f"   {geo_error}")

    print("\n\033[1;32m[✓] Análisis completado.\033[0m")

if __name__ == "__main__":
    main()
