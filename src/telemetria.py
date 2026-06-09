"""Geração de dados simulados de telemetria do AgroSat-1.

Satélite de sensoriamento multiespectral em órbita baixa (~620km),
similar ao CBERS-4A / Planet Labs, voltado ao agronegócio brasileiro.
"""
import random
from datetime import datetime, timezone

_CICLO = 0


def coletar() -> dict:
    """Gera uma leitura simulada dos sensores do AgroSat-1."""
    global _CICLO
    _CICLO += 1

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ciclo": _CICLO,
        # Saúde do sensor multiespectral NDVI (0-100%)
        "ndvi_saude_pct": round(max(0.0, min(100.0, random.gauss(84, 9))), 1),
        # Temperatura do payload óptico (°C) — aquece com exposição solar
        "temperatura_payload_c": round(random.gauss(43, 11), 1),
        # Capacidade de armazenamento usada (%)
        "armazenamento_usado_pct": round(max(0.0, min(100.0, random.uniform(32, 91))), 1),
        # Janela de downlink disponível (minutos)
        "janela_downlink_min": round(max(0.0, random.gauss(17, 7)), 1),
        # Estabilidade de atitude (desvio em mrad) — menor = melhor apontamento
        "estabilidade_atitude_mrad": round(abs(random.gauss(0.45, 0.38)), 3),
        # Energia dos painéis solares disponível (%)
        "energia_pct": round(max(0.0, min(100.0, random.gauss(73, 14))), 1),
        # Qualidade do sinal de comunicação (dBm)
        "qualidade_sinal_dbm": round(random.gauss(-63, 9), 1),
    }


def cenario_critico() -> dict:
    """Telemetria com múltiplos parâmetros fora do nominal — para testes."""
    dados = coletar()
    dados["temperatura_payload_c"] = round(random.uniform(66, 78), 1)
    dados["ndvi_saude_pct"] = round(random.uniform(12, 38), 1)
    dados["energia_pct"] = round(random.uniform(6, 17), 1)
    dados["armazenamento_usado_pct"] = round(random.uniform(93, 99), 1)
    dados["janela_downlink_min"] = round(random.uniform(1.0, 4.5), 1)
    dados["estabilidade_atitude_mrad"] = round(random.uniform(2.1, 3.8), 3)
    return dados


def cenario_normal() -> dict:
    """Telemetria com todos os parâmetros dentro do nominal — operação saudável."""
    dados = coletar()
    dados["temperatura_payload_c"] = round(random.uniform(31, 46), 1)
    dados["ndvi_saude_pct"] = round(random.uniform(88, 98), 1)
    dados["energia_pct"] = round(random.uniform(76, 91), 1)
    dados["armazenamento_usado_pct"] = round(random.uniform(33, 54), 1)
    dados["janela_downlink_min"] = round(random.uniform(14, 26), 1)
    dados["estabilidade_atitude_mrad"] = round(random.uniform(0.08, 0.35), 3)
    dados["qualidade_sinal_dbm"] = round(random.uniform(-72, -55), 1)
    return dados
