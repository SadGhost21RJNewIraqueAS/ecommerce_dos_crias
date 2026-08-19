from fastapi import APIRouter, File, UploadFile, status, HTTPException
from pathlib import Path
import shutil

router = APIRouter(prefix="/arquivos", tags=["Arquivos"])

PASTA_UPLOAD = Path("uploads")

PASTA_UPLOAD.mkdir(exist_ok=True)

TIPOS_DE_ARQUIVO_PERMITIDOS = ["image/jpeg", "image/png"]  
TAMANHO_MAXIMO_ARQUIVO = 5 * 1024 * 1024  # 5MB  


@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload(arquivo: UploadFile = File(...)):
    if arquivo.content_type not in TIPOS_DE_ARQUIVO_PERMITIDOS:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                           detail="Tipo de arquivo não permitido, envie somente arquivos JPEG ou PNG.")
    conteudo = arquivo.file.read()
    if len(conteudo) > TAMANHO_MAXIMO_ARQUIVO:
       raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, 
                           detail="Arquivo muito grande (MAX 5MB).")

    nome_seguro = Path(arquivo.filename or "arquivo").name
    destino = PASTA_UPLOAD / nome_seguro

    with destino.open("wb") as buffer:
       buffer.write(conteudo)
    return {"arquivo": nome_seguro}

@router.post("/upload-multiplos", status_code=status.HTTP_201_CREATED)
def upload_multiplos(arquivos: list[UploadFile] = File(...)):
    arquivos_salvos = []
    for arquivo in arquivos:
        if arquivo.content_type not in TIPOS_DE_ARQUIVO_PERMITIDOS:
            raise HTTPException(status_code=400, detail="Envie somente arquivos JPEG ou PNG.")
        nome = Path(arquivo.filename or "arquivo").name
        with (PASTA_UPLOAD / nome).open("wb") as buffer:
            shutil.copyfileobj(arquivo.file, buffer)
        arquivos_salvos.append(nome)

    return {"arquivos": arquivos_salvos}
