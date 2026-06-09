"""Thresholds e regras de decisão para o AgroSat-1.

Lógica em Python puro — a IA contextualiza, o código decide.
"""
from dataclasses import dataclass
from typing import List

# ---------------------------------------------------------------------------
# Estrutura de alerta
# ---------------------------------------------------------------------------

@dataclass
class Alerta:
    parametro: str
    nivel: str          # "critico" | "aviso"
    valor: float
    limite: float
    mensagem: str
    acao_automatica: str = ""


# ---------------------------------------------------------------------------
# Thresholds dos parâmetros do AgroSat-1
# ---------------------------------------------------------------------------

THRESHOLDS = {
    "ndvi_saude_pct": {
        "critico_abaixo": 50.0,
        "aviso_abaixo":   70.0,
    },
    "temperatura_payload_c": {
        "critico_acima": 65.0,
        "aviso_acima":   55.0,
    },
    "armazenamento_usado_pct": {
        "critico_acima": 95.0,
        "aviso_acima":   85.0,
    },
    "janela_downlink_min": {
        "critico_abaixo": 5.0,
        "aviso_abaixo":  10.0,
    },
    "estabilidade_atitude_mrad": {
        "critico_acima": 2.0,
        "aviso_acima":   1.0,
    },
    "energia_pct": {
        "critico_abaixo": 20.0,
        "aviso_abaixo":   35.0,
    },
    "qualidade_sinal_dbm": {
        "critico_abaixo": -90.0,
        "aviso_abaixo":   -80.0,
    },
}


# ---------------------------------------------------------------------------
# Função principal de avaliação
# ---------------------------------------------------------------------------

def avaliar(dados: dict) -> List[Alerta]:
    """Avalia a telemetria e retorna lista de alertas ordenada por severidade."""
    alertas: List[Alerta] = []

    # --- Sensor NDVI ---
    ndvi = dados.get("ndvi_saude_pct", 100.0)
    if ndvi < THRESHOLDS["ndvi_saude_pct"]["critico_abaixo"]:
        alertas.append(Alerta(
            parametro="ndvi_saude_pct", nivel="critico",
            valor=ndvi, limite=THRESHOLDS["ndvi_saude_pct"]["critico_abaixo"],
            mensagem=f"Sensor NDVI com saúde crítica ({ndvi:.1f}%). Imagens multiespectrais comprometidas.",
            acao_automatica="Diagnóstico automático do sensor óptico iniciado. Captura de imagens pausada."
        ))
    elif ndvi < THRESHOLDS["ndvi_saude_pct"]["aviso_abaixo"]:
        alertas.append(Alerta(
            parametro="ndvi_saude_pct", nivel="aviso",
            valor=ndvi, limite=THRESHOLDS["ndvi_saude_pct"]["aviso_abaixo"],
            mensagem=f"Saúde do sensor NDVI reduzida ({ndvi:.1f}%). Monitorar degradação.",
        ))

    # --- Temperatura do payload ---
    temp = dados.get("temperatura_payload_c", 40.0)
    if temp > THRESHOLDS["temperatura_payload_c"]["critico_acima"]:
        alertas.append(Alerta(
            parametro="temperatura_payload_c", nivel="critico",
            valor=temp, limite=THRESHOLDS["temperatura_payload_c"]["critico_acima"],
            mensagem=f"Temperatura do payload em {temp:.1f}°C. Risco de dano térmico permanente.",
            acao_automatica="Modo de resfriamento ativado. Taxa de captura reduzida em 60%."
        ))
    elif temp > THRESHOLDS["temperatura_payload_c"]["aviso_acima"]:
        alertas.append(Alerta(
            parametro="temperatura_payload_c", nivel="aviso",
            valor=temp, limite=THRESHOLDS["temperatura_payload_c"]["aviso_acima"],
            mensagem=f"Temperatura do payload elevada ({temp:.1f}°C). Dentro do limite operacional.",
        ))

    # --- Armazenamento ---
    armazenamento = dados.get("armazenamento_usado_pct", 50.0)
    if armazenamento > THRESHOLDS["armazenamento_usado_pct"]["critico_acima"]:
        alertas.append(Alerta(
            parametro="armazenamento_usado_pct", nivel="critico",
            valor=armazenamento, limite=THRESHOLDS["armazenamento_usado_pct"]["critico_acima"],
            mensagem=f"Armazenamento crítico ({armazenamento:.1f}%). Risco de perda de imagens.",
            acao_automatica="Capturas não prioritárias suspensas. Downlink da próxima janela priorizado."
        ))
    elif armazenamento > THRESHOLDS["armazenamento_usado_pct"]["aviso_acima"]:
        alertas.append(Alerta(
            parametro="armazenamento_usado_pct", nivel="aviso",
            valor=armazenamento, limite=THRESHOLDS["armazenamento_usado_pct"]["aviso_acima"],
            mensagem=f"Armazenamento em {armazenamento:.1f}%. Planejar downlink nas próximas horas.",
        ))

    # --- Janela de downlink ---
    downlink = dados.get("janela_downlink_min", 20.0)
    if downlink < THRESHOLDS["janela_downlink_min"]["critico_abaixo"]:
        alertas.append(Alerta(
            parametro="janela_downlink_min", nivel="critico",
            valor=downlink, limite=THRESHOLDS["janela_downlink_min"]["critico_abaixo"],
            mensagem=f"Janela de downlink crítica ({downlink:.1f} min). Transmissão comprometida.",
            acao_automatica="Priorizando transmissão dos dados NDVI mais recentes para estação terrena."
        ))
    elif downlink < THRESHOLDS["janela_downlink_min"]["aviso_abaixo"]:
        alertas.append(Alerta(
            parametro="janela_downlink_min", nivel="aviso",
            valor=downlink, limite=THRESHOLDS["janela_downlink_min"]["aviso_abaixo"],
            mensagem=f"Janela de downlink reduzida ({downlink:.1f} min). Otimizar schedule de transmissão.",
        ))

    # --- Estabilidade de atitude ---
    atitude = dados.get("estabilidade_atitude_mrad", 0.5)
    if atitude > THRESHOLDS["estabilidade_atitude_mrad"]["critico_acima"]:
        alertas.append(Alerta(
            parametro="estabilidade_atitude_mrad", nivel="critico",
            valor=atitude, limite=THRESHOLDS["estabilidade_atitude_mrad"]["critico_acima"],
            mensagem=f"Instabilidade de atitude crítica ({atitude:.3f} mrad). Imagens com distorção severa.",
            acao_automatica="Controle de atitude de emergência ativado. Thrusters auxiliares ligados."
        ))
    elif atitude > THRESHOLDS["estabilidade_atitude_mrad"]["aviso_acima"]:
        alertas.append(Alerta(
            parametro="estabilidade_atitude_mrad", nivel="aviso",
            valor=atitude, limite=THRESHOLDS["estabilidade_atitude_mrad"]["aviso_acima"],
            mensagem=f"Atitude levemente instável ({atitude:.3f} mrad). Qualidade de imagem reduzida.",
        ))

    # --- Energia ---
    energia = dados.get("energia_pct", 70.0)
    if energia < THRESHOLDS["energia_pct"]["critico_abaixo"]:
        alertas.append(Alerta(
            parametro="energia_pct", nivel="critico",
            valor=energia, limite=THRESHOLDS["energia_pct"]["critico_abaixo"],
            mensagem=f"Energia crítica ({energia:.1f}%). Risco de desligamento de subsistemas.",
            acao_automatica="Modo de economia de energia ativado. Sistemas não essenciais desligados."
        ))
    elif energia < THRESHOLDS["energia_pct"]["aviso_abaixo"]:
        alertas.append(Alerta(
            parametro="energia_pct", nivel="aviso",
            valor=energia, limite=THRESHOLDS["energia_pct"]["aviso_abaixo"],
            mensagem=f"Energia em {energia:.1f}%. Verificar eficiência dos painéis solares.",
        ))

    # --- Qualidade do sinal ---
    sinal = dados.get("qualidade_sinal_dbm", -65.0)
    if sinal < THRESHOLDS["qualidade_sinal_dbm"]["critico_abaixo"]:
        alertas.append(Alerta(
            parametro="qualidade_sinal_dbm", nivel="critico",
            valor=sinal, limite=THRESHOLDS["qualidade_sinal_dbm"]["critico_abaixo"],
            mensagem=f"Sinal de comunicação crítico ({sinal:.1f} dBm). Risco de perda de link.",
            acao_automatica="Potência do transmissor aumentada ao máximo para compensar degradação."
        ))
    elif sinal < THRESHOLDS["qualidade_sinal_dbm"]["aviso_abaixo"]:
        alertas.append(Alerta(
            parametro="qualidade_sinal_dbm", nivel="aviso",
            valor=sinal, limite=THRESHOLDS["qualidade_sinal_dbm"]["aviso_abaixo"],
            mensagem=f"Qualidade de sinal reduzida ({sinal:.1f} dBm). Verificar antena.",
        ))

    # Ordena: críticos primeiro
    alertas.sort(key=lambda a: (0 if a.nivel == "critico" else 1))
    return alertas


def nivel_geral(alertas: List[Alerta]) -> str:
    """Retorna o nível de severidade geral da missão."""
    if any(a.nivel == "critico" for a in alertas):
        return "CRITICO"
    if any(a.nivel == "aviso" for a in alertas):
        return "AVISO"
    return "NOMINAL"


def acoes_automaticas(alertas: List[Alerta]) -> List[str]:
    """Retorna lista de ações automáticas disparadas pelos alertas."""
    return [a.acao_automatica for a in alertas if a.acao_automatica]
