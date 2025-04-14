from lsprotocol import types

from foam_lsp.server import FOAMLanguageServer, server


@server.feature(types.TEXT_DOCUMENT_HOVER)
def hover(ls: FOAMLanguageServer, params: types.HoverParams):
    pos = params.position
    document_uri = params.text_document.uri
    document = ls.workspace.get_text_document(document_uri)

    try:
        line = document.lines[pos.line]
    except IndexError:
        return None

    # for fmt in DATE_FORMATS:
    #     try:
    #         value = datetime.strptime(line.strip(), fmt)
    #         break
    #     except ValueError:
    #         pass

    if 1:
        pass
    else:
        # No valid datetime found.
        return None

    documentation = ""

    return types.Hover(
        contents=types.MarkupContent(
            kind=types.MarkupKind.Markdown,
            value=documentation,
        ),
        range=types.Range(
            start=types.Position(line=pos.line, character=0),
            end=types.Position(line=pos.line + 1, character=0),
        ),
    )
