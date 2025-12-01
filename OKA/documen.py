from abc import ABC, abstractmethod


class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class Report(Document):
    def render(self) -> str:
        return "=== REPORT ===\nThis is a generated report."


class Invoice(Document):
    def render(self) -> str:
        return "*** INVOICE ***\nAmount due: $1000"


class Contract(Document):
    def render(self) -> str:
        return "--- CONTRACT ---\nAgreement between parties."

class NullDocument(Document):
    def render(self) -> str:
        return "[Error] Unknown document type."


class DocumentFactory:
    @staticmethod
    def create(doc_type: str) -> Document:
        doc_type = doc_type.lower()

        mapping = {
            "report": Report,
            "invoice": Invoice,
            "contract": Contract
        }

        if doc_type in mapping:
            return mapping[doc_type]()
        else:
            return NullDocument()


def client_code(doc_type: str):
    document = DocumentFactory.create(doc_type)
    print(document.render())


client_code("report")
client_code("invoice")
client_code("contract")
client_code("unknown")
