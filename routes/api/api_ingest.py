import os
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from services.document_processor import rag_chat, extract_text_from_file
import jwt
import hashlib
from db.db_table_schema import Document_Hash, MessageHistory
from db.db_engine import get_db, AsyncSession
from sqlalchemy import select, func
from langchain_core.messages import HumanMessage, AIMessage
from typing import Annotated
load_dotenv()

secret_key = os.environ.get("secret_key")
router = APIRouter(prefix="/api", tags=["Ingest"])

security = HTTPBearer()

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/ingest")
async def ingest_data(
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    token = validate_token(credentials)
    role = token.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission")

    extension = file.filename.split(".")[-1]
    accepted_extensions = ["html", "doc", "docx", "pdf", "txt"]
    if extension not in accepted_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Read and check file size
    file_content_bytes = await file.read()
    if len(file_content_bytes) > 8 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 8MB")
    
    # Check if already exists
    file_hash = hashlib.md5(file_content_bytes).hexdigest()
    query = select(Document_Hash).where(Document_Hash.doc_hash == file_hash)
    result = await db.execute(query)
    existing_doc = result.scalar_one_or_none()
    if existing_doc:
        raise HTTPException(status_code=400, detail="File already uploaded")
    
    # Process file
    try:
        file_content_str = extract_text_from_file(
            file_content_bytes, 
            file.filename, 
            extension
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
    
    # Store in database
    doc_record = Document_Hash(doc_hash=file_hash, filename=file.filename)
    db.add(doc_record)
    await db.commit()
    
    return {
        "status": "success",
        "message": f"File {file.filename} uploaded successfully",
        "file_hash": file_hash
    }

@router.get("/files")
async def get_file_list(
    db: Annotated[AsyncSession, Depends(get_db)],
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = validate_token(credentials)
    role = token.get("role")
    query = select(Document_Hash).add_columns(Document_Hash.filename, Document_Hash.doc_hash).order_by(Document_Hash.docid.desc()).limit(10)
    result = await db.execute(query)
    files = result.scalars().all()
    
    return {
        "status": "success",
        "files": [{"filename": file.filename, "hash": file.doc_hash} for file in files]
    }

@router.post("/chat")
async def chat_with_user(user_input: str, db: Annotated[AsyncSession, Depends(get_db)], credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = validate_token(credentials)
    email_str = token.get("sub")
    query = select(func.count(MessageHistory.human)).where(MessageHistory.email==email_str)
    response = await db.execute(query)
    val = response.scalar()
    if val>5:
        raise HTTPException(status_code=400, detail="Chat limit exceeded")
    query = select(MessageHistory).where(MessageHistory.email==email_str).order_by(MessageHistory.generatedon.desc())
    response = await db.execute(query)
    message_history = response.scalars().all()
    messages = []
    for msg in reversed(message_history):  # reverse to maintain chronological order
        messages.append(HumanMessage(content=msg.human))
        messages.append(AIMessage(content=msg.ai))
    async def generate():
        response=""
        for chunk in rag_chat(user_input, messages):
            response+=chunk
            yield chunk
        entry = MessageHistory(email = email_str,human=user_input, ai=response)
        db.add(entry)
        await db.commit()
    return StreamingResponse(generate(), media_type="text/plain")
