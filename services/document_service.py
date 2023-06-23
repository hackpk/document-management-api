from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from repositories.document_repository import DocumentRepository
from schemas.document import Document, DocumentCreate, DocumentUpdate


class DocumentService:
    """
    Service class for handling document-related operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the DocumentService.

        Args:
            db (Session): The SQLAlchemy database session.
        """
        self.db = db
        self.repository = DocumentRepository(db)

    def get_document(self, document_id: int) -> Optional[Document]:
        """
        Retrieve a document by its ID.

        Args:
            document_id (int): The ID of the document.

        Returns:
            Optional[Document]: The retrieved document, or None if not found.
        """
        return self.repository.get_document(document_id)

    def get_all_documents(self) -> List[Document]:
        """
        Retrieve all documents.

        Returns:
            List[Document]: A list of all documents.
        """
        return self.repository.get_all_documents()

    def create_document(self, document_data: DocumentCreate) -> Document:
        """
        Create a new document.

        Args:
            document_data (DocumentCreate): The data for creating the document.

        Returns:
            Document: The created document.
        """
        document = Document(
            title=document_data.title,
            file_type=document_data.file_type,
            file_url=document_data.file_url,
            description=document_data.description,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return self.repository.create_document(document)

    def update_document(self, document_id: int, document_data: DocumentUpdate) -> Optional[Document]:
        """
        Update an existing document.

        Args:
            document_id (int): The ID of the document to update.
            document_data (DocumentUpdate): The updated data for the document.

        Returns:
            Optional[Document]: The updated document, or None if not found.
        """
        document = self.repository.get_document(document_id)
        if document:
            document.title = document_data.title or document.title
            document.file_type = document_data.file_type or document.file_type
            document.file_url = document_data.file_url or document.file_url
            document.description = document_data.description or document.description
            document.updated_at = datetime.utcnow()
            return self.repository.update_document(document)
        return None

    def delete_document(self, document_id: int) -> bool:
        """
        Delete a document.

        Args:
            document_id (int): The ID of the document to delete.

        Returns:
            bool: True if the document was deleted successfully, False otherwise.
        """
        document = self.repository.get_document(document_id)
        if document:
            return self.repository.delete_document(document)
        return False
