# import argparse
# from app.core.controllers.conversao_controller import ConversaoController


# def main() -> None:
#     parser = argparse.ArgumentParser(description="CLI para o HTMLReader")
#     parser.add_argument("/home/", help="Caminho para o arquivo HTML")
#     args = parser.parse_args()

#     controller = ConversaoController()
#     try:
#         with open(args.arquivo, "r", encoding="utf-8") as f:
#             conteudo = f.read()
#         resultado = controller.converter_html_para_json(conteudo)
#         print("Resultado da conversão:")
#         print(resultado)
#     except (OSError, UnicodeDecodeError) as e:
#         print(f"Erro: {e}")


# if __name__ == "__main__":
#     main()
