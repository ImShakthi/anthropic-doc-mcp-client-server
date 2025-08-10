from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
def read_document_contents(
        doc_id: str = Field(description="ID of the document to read"),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id '{doc_id}' not found.")
    return docs[doc_id]


@mcp.tool(
    name="edit_document_content",
    description="Edit a document by replacing string in the documents content with the provided new string.",
)
def write_document_contents(
        doc_id: str = Field(description="ID of the document to edit"),
        old_string: str = Field(
            description="The text to replace. Must match exactly, including whitespace."),
        new_string: str = Field(description="The new text to replace the old string with.")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id '{doc_id}' not found.")

    docs[doc_id] = docs[doc_id].replace(old_string, new_string)
    return docs[doc_id]


@mcp.resource("docs://documents",  # URI
              mime_type="application/json")
def list_documents() -> list[str]:
    return list(docs.keys())


@mcp.resource("docs://documents/{doc_id}",  # URI
              mime_type="plain/text")
def fetch_documents(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")

    return docs[doc_id]


@mcp.prompt(
    name="format",
    description="Rewrite the content of document in markdown format.",
)
def format_document(
        doc_id: str = Field(description="ID of the document to format")
) -> list[base.Message]:
    prompt = f"""
        Your goal is to reformat a document to be written with markdown syntax.

        The id of the document you need to reformat is:
        <document_id>
        {doc_id}
        </document_id>
        
        Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
        Use the 'edit_document' tool to edit the document. After the document has been reformatted...
        """

    return [base.UserMessage(prompt)]


# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
