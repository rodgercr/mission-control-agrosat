"""Motor de análise da Mission Control AI — Trilha AgroSat."""
import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path
from src import telemetria, alertas as mod_alertas

load_dotenv()

TRILHA = "agrosat"

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")}
)


# ---------------------------------------------------------------------------
# Função de integração com o LLM — ponto único de contato com a IA
# ---------------------------------------------------------------------------

def llm(prompt: str, system: str = None, max_tokens: int = 900, temperature: float = 0.3) -> str:
    """Envia prompt ao gpt-oss:120b via Ollama Cloud e retorna texto."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        return client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False,
        )["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"


def load_system_prompt() -> str:
    """Lê o system prompt de prompts/system_prompt.md."""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente de operações do satélite AgroSat-1."


# ---------------------------------------------------------------------------
# Motor principal
# ---------------------------------------------------------------------------

class MissionEngine:
    """Motor de análise integrado — telemetria + alertas + IA generativa."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self._historico: list[str] = []

    def is_ready(self) -> bool:
        return True

    # ------------------------------------------------------------------
    # status_snapshot — resumo visual da telemetria atual
    # ------------------------------------------------------------------

    def status_snapshot(self) -> str:
        """Coleta telemetria e retorna resumo formatado para exibição na CLI."""
        dados = telemetria.coletar()
        lista_alertas = mod_alertas.avaliar(dados)
        nivel = mod_alertas.nivel_geral(lista_alertas)

        linhas = [
            f"[bold]AGROSAT-1[/bold] · Status: {self._cor_nivel(nivel)}",
            f"Ciclo [cyan]#{dados['ciclo']}[/cyan] · {dados['timestamp'][:19]}Z",
            "",
            f"  [cyan]Sensor NDVI     :[/cyan] {dados['ndvi_saude_pct']:.1f}%",
            f"  [cyan]Temp. Payload   :[/cyan] {dados['temperatura_payload_c']:.1f}°C",
            f"  [cyan]Armazenamento   :[/cyan] {dados['armazenamento_usado_pct']:.1f}%",
            f"  [cyan]Janela Downlink :[/cyan] {dados['janela_downlink_min']:.1f} min",
            f"  [cyan]Estab. Atitude  :[/cyan] {dados['estabilidade_atitude_mrad']:.3f} mrad",
            f"  [cyan]Energia         :[/cyan] {dados['energia_pct']:.1f}%",
            f"  [cyan]Sinal Comms     :[/cyan] {dados['qualidade_sinal_dbm']:.1f} dBm",
        ]

        if lista_alertas:
            linhas.append("")
            linhas.append(f"[bold]Alertas ativos ({len(lista_alertas)}):[/bold]")
            for a in lista_alertas:
                icon = "🔴" if a.nivel == "critico" else "🟡"
                linhas.append(f"  {icon} {a.mensagem}")

            acoes = mod_alertas.acoes_automaticas(lista_alertas)
            if acoes:
                linhas.append("")
                linhas.append("[bold]Ações automáticas executadas:[/bold]")
                for acao in acoes:
                    linhas.append(f"  ⚡ {acao}")
        else:
            linhas.append("")
            linhas.append("[green]✓ Todos os parâmetros nominais. Missão operando normalmente.[/green]")

        return "\n".join(linhas)

    # ------------------------------------------------------------------
    # analyze — interface pública chamada pela UI
    # ------------------------------------------------------------------

    def analyze(self, pergunta_usuario: str) -> str:
        """Analisa a pergunta com base em telemetria em tempo real + alertas + IA."""
        dados = telemetria.coletar()
        return self._analyze_with_dados(dados, pergunta_usuario)

    def analyze_critico(self, pergunta_usuario: str) -> str:
        """Analisa usando cenário crítico simulado."""
        dados = telemetria.cenario_critico()
        return self._analyze_with_dados(dados, pergunta_usuario)

    def analyze_normal(self, pergunta_usuario: str) -> str:
        """Analisa usando cenário normal simulado."""
        dados = telemetria.cenario_normal()
        return self._analyze_with_dados(dados, pergunta_usuario)

    # ------------------------------------------------------------------
    # Lógica interna de análise
    # ------------------------------------------------------------------

    def _analyze_with_dados(self, dados: dict, pergunta_usuario: str) -> str:
        """Núcleo da análise: monta contexto, chama LLM, atualiza histórico."""
        # 1. Avaliar alertas via lógica Python
        lista_alertas = mod_alertas.avaliar(dados)
        nivel = mod_alertas.nivel_geral(lista_alertas)
        acoes = mod_alertas.acoes_automaticas(lista_alertas)

        # 2. Montar contexto de telemetria
        ctx = (
            f"TELEMETRIA AGROSAT-1 — Ciclo #{dados['ciclo']} ({dados['timestamp'][:19]}Z)\n"
            f"{'━' * 50}\n"
            f"Sensor NDVI (saúde)     : {dados['ndvi_saude_pct']:.1f}%\n"
            f"Temperatura Payload     : {dados['temperatura_payload_c']:.1f}°C\n"
            f"Armazenamento Usado     : {dados['armazenamento_usado_pct']:.1f}%\n"
            f"Janela Downlink         : {dados['janela_downlink_min']:.1f} min\n"
            f"Estabilidade Atitude    : {dados['estabilidade_atitude_mrad']:.3f} mrad\n"
            f"Energia Disponível      : {dados['energia_pct']:.1f}%\n"
            f"Qualidade Sinal Comms   : {dados['qualidade_sinal_dbm']:.1f} dBm\n"
            f"{'━' * 50}\n"
            f"NÍVEL GERAL DA MISSÃO: {nivel}\n"
        )

        if lista_alertas:
            ctx += "\nALERTAS ATIVOS:\n"
            for a in lista_alertas:
                ctx += f"  [{a.nivel.upper()}] {a.mensagem}\n"

        if acoes:
            ctx += "\nAÇÕES AUTOMÁTICAS JÁ EXECUTADAS PELO SISTEMA:\n"
            for acao in acoes:
                ctx += f"  • {acao}\n"

        # 3. Incluir histórico dos últimos ciclos (memória de contexto)
        if self._historico:
            ctx += "\nHISTÓRICO RECENTE DA MISSÃO (últimos ciclos):\n"
            for h in self._historico[-4:]:
                ctx += f"  - {h}\n"

        # 4. Prompt final para o LLM
        prompt = (
            f"{ctx}\n"
            f"PERGUNTA DO OPERADOR: {pergunta_usuario}\n\n"
            "Responda em português brasileiro de forma clara, técnica e orientada a ação. "
            "Sempre conecte a situação orbital ao impacto concreto no agronegócio brasileiro."
        )

        # 5. Consultar IA
        resposta = llm(prompt, system=self.system_prompt)

        # 6. Atualizar memória de contexto
        resumo = f"Ciclo {dados['ciclo']}: {nivel}, {len(lista_alertas)} alerta(s)"
        self._historico.append(resumo)
        if len(self._historico) > 8:
            self._historico.pop(0)

        return resposta

    # ------------------------------------------------------------------
    # Utilitário
    # ------------------------------------------------------------------

    @staticmethod
    def _cor_nivel(nivel: str) -> str:
        cores = {
            "NOMINAL": "[bold green]NOMINAL[/bold green]",
            "AVISO":   "[bold yellow]AVISO[/bold yellow]",
            "CRITICO": "[bold red]CRITICO[/bold red]",
        }
        return cores.get(nivel, nivel)
