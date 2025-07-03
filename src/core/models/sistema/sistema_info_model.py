"""
Modelo de informações do sistema operacional.

Classes:
    SistemaInfo: Representa o estado atual do sistema com metadados essenciais.
"""

from datetime import datetime
from pydantic import BaseModel


class SistemaInfo(BaseModel):
    """
    Informações abrangentes sobre o sistema operacional e ambiente.

    Atributos:
        sistema_operacional: Nome do SO (e.g. 'Linux', 'Windows')
        versao: Versão detalhada do SO
        arquitetura: Arquitetura da CPU (e.g. 'x86_64')
        nome_maquina: Hostname do sistema
        tempo_atividade: Uptime em segundos
        diretorio_atual: Caminho do working directory
        usuario: Nome do usuário atual
        permissoes: Nível de privilégios (root/admin/padrão)
        data_hora: Timestamp da coleta
    """

    sistema_operacional: str
    versao: str
    arquitetura: str
    nome_maquina: str
    tempo_atividade: float
    diretorio_atual: str
    usuario: str
    permissoes: str  # 'root', 'admin', 'padrão'
    data_hora: datetime = datetime.now()

    @property
    def resumo(self) -> str:
        """Versão resumida para logging."""
        return (
            f"{self.sistema_operacional} {self.versao} ({self.arquitetura}) | "
            f"User: {self.usuario} | Uptime: {self.tempo_atividade:.2f}s"
        )
