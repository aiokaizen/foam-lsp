import re

from lsprotocol import types

from foam_lsp.server import server, FOAMLanguageServer
from foam_lsp.patterns import (
    ARGUMENT,
)


@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: FOAMLanguageServer, params: types.DidOpenTextDocumentParams):
    """Parse each document when it is opened"""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    ls.parse(doc)


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: FOAMLanguageServer, params: types.DidOpenTextDocumentParams):
    """Parse each document when it is changed"""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    ls.parse(doc)


@server.feature(types.TEXT_DOCUMENT_TYPE_DEFINITION)
def goto_type_definition(ls: FOAMLanguageServer, params: types.TypeDefinitionParams):
    """Jump to an object's type definition."""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    index = ls.index.get(doc.uri)
    if index is None:
        return

    try:
        line = doc.lines[params.position.line]
    except IndexError:
        line = ""

    word = doc.word_at_position(params.position)

    for match in ARGUMENT.finditer(line):
        if match.group("name") == word:
            if (range_ := index["types"].get(match.group("type"), None)) is not None:
                return types.Location(uri=doc.uri, range=range_)


@server.feature(types.TEXT_DOCUMENT_DEFINITION)
def goto_definition(ls: FOAMLanguageServer, params: types.DefinitionParams):
    """Jump to an object's definition."""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    index = ls.index.get(doc.uri)
    if index is None:
        return

    word = doc.word_at_position(params.position)

    # Is word a type?
    if (range_ := index["types"].get(word, None)) is not None:
        return types.Location(uri=doc.uri, range=range_)


@server.feature(types.TEXT_DOCUMENT_DECLARATION)
def goto_declaration(ls: FOAMLanguageServer, params: types.DeclarationParams):
    """Jump to an object's declaration."""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    index = ls.index.get(doc.uri)
    if index is None:
        return

    try:
        line = doc.lines[params.position.line]
    except IndexError:
        line = ""

    word = doc.word_at_position(params.position)

    for match in ARGUMENT.finditer(line):
        if match.group("name") == word:
            linum = params.position.line
            return types.Location(
                uri=doc.uri,
                range=types.Range(
                    start=types.Position(line=linum, character=match.start()),
                    end=types.Position(line=linum, character=match.end()),
                ),
            )


@server.feature(types.TEXT_DOCUMENT_IMPLEMENTATION)
def goto_implementation(ls: FOAMLanguageServer, params: types.ImplementationParams):
    """Jump to an object's implementation."""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    index = ls.index.get(doc.uri)
    if index is None:
        return

    word = doc.word_at_position(params.position)

    # Is word a function?
    if (range_ := index["functions"].get(word, None)) is not None:
        return types.Location(uri=doc.uri, range=range_)


@server.feature(types.TEXT_DOCUMENT_REFERENCES)
def find_references(ls: FOAMLanguageServer, params: types.ReferenceParams):
    """Find references of an object."""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    index = ls.index.get(doc.uri)
    if index is None:
        return

    word = doc.word_at_position(params.position)
    is_object = any([word in index[name] for name in index])
    if not is_object:
        return

    references = []
    for linum, line in enumerate(doc.lines):
        for match in re.finditer(f"\\b{word}\\b", line):
            references.append(
                types.Location(
                    uri=doc.uri,
                    range=types.Range(
                        start=types.Position(line=linum, character=match.start()),
                        end=types.Position(line=linum, character=match.end()),
                    ),
                )
            )

    return references
