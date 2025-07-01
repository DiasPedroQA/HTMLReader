# """
# Controlador de operações de criação e leitura de arquivos.

# Utiliza a classe `Arquivo` para realizar operações como:
# - Criação condicional de arquivos
# - Escrita com controle de sobrescrita
# - Leitura de conteúdo e metadados
# """

# from pathlib import Path

# from app.core.models.model_arquivo import Arquivo


# def demonstrar_uso_arquivo() -> None:
#     """Exemplo completo de criação, leitura e exibição de dados do arquivo."""

#     # Caminho do arquivo a ser criado/testado
#     caminho_arquivo = Path("/home/pedro-pm-dias/Downloads/Firefox/exemplo4.txt")
#     conteudo = "Este é um exemplo completo de uso da classe Arquivo."

#     # Instanciação e escrita
#     objeto_arquivo = Arquivo(caminho=caminho_arquivo)
#     sucesso: bool = objeto_arquivo.escrever_texto_objeto_arquivo(
# conteudo=conteudo, existente=False)

#     if not sucesso:
#         print("[ERRO] Não foi possível criar o arquivo.")
#         return

#     # Impressão das propriedades básicas e avançadas
#     print("\n🔍 Informações do Arquivo")
#     print(f"🧾 Nome completo .............: {objeto_arquivo.objeto_arquivo_nome}")
#     print(f"📄 Nome (sem extensão) .......: {objeto_arquivo.objeto_arquivo_nome_base}")
#     print(f"🧩 Extensão ..................: {objeto_arquivo.objeto_arquivo_existe}")
#     print(
#         f"📁 Diretório pai .............: {objeto_arquivo.objeto_arquivo_diretorio_pai}"
#     )
#     print(f"📦 Existe ....................: {objeto_arquivo.objeto_arquivo_existe}")
#     print(
#         f"📏 Tamanho (bytes) ...........: {objeto_arquivo.objeto_arquivo_tamanho_bytes}"
#     )
#     print(
#         f"📐 Tamanho formatado .........: {objeto_arquivo.objeto_arquivo_tamanho_humano}"
#     )
#     print(f"📅 Criado em .................: {objeto_arquivo.objeto_arquivo_criado_em}")
#     print(
#         f"🕓 Modificado em .............: {objeto_arquivo.objeto_arquivo_modificado_em}"
#     )
#     print(f"🙈 É oculto ..................: {objeto_arquivo.objeto_arquivo_eh_oculto}")

#     # Leitura via método ler_objeto_arquivo()
#     print("\n📖 Leitura do conteúdo (ler_objeto_arquivo):")
#     texto: str | None = objeto_arquivo.ler_objeto_arquivo()
#     if texto:
#         print(f"▶️ Conteúdo: {texto}")
#     else:
#         print("[ERRO] Falha ao ler o conteúdo do arquivo.")

#     # Demonstração do uso do operador /
#     print("\n🧪 Usando operador `/` para gerar sub arquivo:")
#     sub_arquivo: Arquivo = objeto_arquivo / "log.txt"
#     print(f"📂 Sub arquivo: {sub_arquivo}")


# def demonstrar_leitura_arquivo_existente() -> None:
#     """Exemplo de leitura de um arquivo existente no disco."""

#     caminho_existente = Path("/home/pedro-pm-dias/Downloads/Firefox/exemplo.txt")

#     objeto_arquivo = Arquivo(caminho=caminho_existente)

#     print("\n📂 [Leitura de Arquivo Existente]")
#     if not objeto_arquivo.objeto_arquivo_existe:
#         print(f"[ERRO] Arquivo não encontrado: {objeto_arquivo.caminho}")
#         return

#     # Impressão dos dados disponíveis
#     print(f"🧾 Nome completo .............: {objeto_arquivo.objeto_arquivo_nome}")
#     print(f"📄 Nome (sem extensão) .......: {objeto_arquivo.objeto_arquivo_nome_base}")
#     print(f"🧩 Extensão ..................: {objeto_arquivo.objeto_arquivo_extensao}")
#     print(
#         f"📁 Diretório pai .............: {objeto_arquivo.objeto_arquivo_diretorio_pai}"
#     )
#     # print(f"📦 Existe ....................: {objeto_arquivo.objeto_arquivo_existe}")
#     print(
#         f"📏 Tamanho (bytes) ...........: {objeto_arquivo.objeto_arquivo_tamanho_bytes}"
#     )
#     print(
#         f"📐 Tamanho formatado .........: {objeto_arquivo.objeto_arquivo_tamanho_humano}"
#     )
#     print(f"📅 Criado em .................: {objeto_arquivo.objeto_arquivo_criado_em}")
#     print(
#         f"🕓 Modificado em .............: {objeto_arquivo.objeto_arquivo_modificado_em}"
#     )
#     print(f"🙈 É oculto ..................: {objeto_arquivo.objeto_arquivo_eh_oculto}")

#     # Leitura direta do conteúdo
#     print("\n📖 Leitura com método ler_objeto_arquivo():")
#     conteudo: str | None = objeto_arquivo.ler_objeto_arquivo()
#     if conteudo:
#         print(f"▶️ Conteúdo lido:\n{conteudo[:500]}")  # limitar a 500 caracteres
#     else:
#         print("[ERRO] Falha ao ler conteúdo do arquivo.")


# # ✅ Atualize seu `main` para testar os dois cenários:

# if __name__ == "__main__":
#     demonstrar_uso_arquivo()
#     demonstrar_leitura_arquivo_existente()


# class ArquivosController:
#     """Controlador de operações de criação e leitura de arquivos."""

#     def criar_arquivo(self, caminho_arquivo: str | Path, conteudo: str = "") -> Arquivo:
#         """
#         Cria um arquivo e escreve conteúdo, se fornecido.

#         Args:
#             caminho_arquivo (str | Path): Caminho do arquivo a ser criado.
#             conteudo (str): Conteúdo opcional a ser escrito.

#         Returns:
#             Arquivo: Instância do arquivo criado ou existente.
#         """
#         objeto_arquivo = Arquivo(caminho=caminho_arquivo)
#         if conteudo:
#             objeto_arquivo.escrever_conteudo(
#                 conteudo_arquivo=conteudo, sobrescrever=False
#             )
#         else:
#             objeto_arquivo.criar_arquivo_se_nao_existir()
#         return objeto_arquivo

#     def ler_conteudo_arquivo(self, caminho_arquivo: str | Path):
#         """
#         Lê o conteúdo de um arquivo.

#         Args:
#             caminho_arquivo (str | Path): Caminho do arquivo a ser lido.

#         Returns:
#             str | None: Conteúdo do arquivo.
#         """
#         objeto_arquivo = Arquivo(caminho=caminho_arquivo)
#         return objeto_arquivo.ler_conteudo()

#     def ler_metadados_arquivo(
#         self, caminho_arquivo: str | Path
#     ) -> dict[str, Any | str]:
#         """
#         Lê informações de metadados de um arquivo, sem o conteúdo.

#         Args:
#             caminho_arquivo (str | Path): Caminho do arquivo a ser lido.

#         Returns:
#             dict[str, str | None]: Dicionário com metadados sem o conteúdo do arquivo.
#         """
#         objeto_arquivo = Arquivo(caminho=caminho_arquivo)
#         return {
#             "nome": objeto_arquivo.nome_caminho,
#             "nome_sem_extensao": objeto_arquivo.nome_sem_extensao,
#             "extensao_arquivo": objeto_arquivo.extensao_arquivo,
#             "extensao_legivel": objeto_arquivo.extensao_legivel,
#             "tamanho_legivel": objeto_arquivo.tamanho_legivel,
#             "eh_oculto": "Sim" if objeto_arquivo.eh_arquivo_oculto else "Não",
#             "data_criacao": objeto_arquivo.data_criacao_legivel,
#             "data_modificacao": objeto_arquivo.data_modificacao_legivel,
#         }
