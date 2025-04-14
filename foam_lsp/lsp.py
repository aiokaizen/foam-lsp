import logging

from pygls.cli import start_server

from foam_lsp.server import server


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    start_server(server)
