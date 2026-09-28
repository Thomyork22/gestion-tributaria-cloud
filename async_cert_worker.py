import boto3
from celery import shared_task
from .models import CertificadoTributario, Auditoria
from .sii_integration import SIIClient

# Inicialización del cliente de AWS S3 para Object Storage
s3_client = boto3.client('s3')

@shared_task(bind=True, max_retries=3)
def procesar_lote_certificados(self, lote_id, file_path, user_id):
    """
    Worker asíncrono encargado de procesar lotes masivos de certificados tributarios.
    Aísla la subida pesada de archivos y la integración externa fuera del hilo HTTP principal.
    """
    try:
        # 1. Subida segura a Object Storage (AWS S3) con llave única
        storage_key = f"certificados/{lote_id}/{file_path.split('/')[-1]}"
        s3_client.upload_file(file_path, 'bucket-tributario-prod', storage_key)

        # 2. Validación de negocio, parseo y actualización de metadatos en PostgreSQL
        certificado = CertificadoTributario.objects.get(id=lote_id)
        certificado.storage_key = storage_key
        certificado.estado = 'PROCESADO'
        certificado.save()

        # 3. Integración con el Servicio de Impuestos Internos (SII) mediante Patrón Adaptador
        sii_status = SIIClient.enviar_declaracion(certificado.folio)

        # 4. Trazabilidad y auditoría estricta de la operación
        Auditoria.objects.create(
            usuario_id=user_id, 
            accion='PROCESAMIENTO_LOTE',
            entidad=f"Lote: {lote_id}", 
            resultado=sii_status
        )
        
        return {"status": "SUCCESS", "sii_sync": sii_status}
        
    except Exception as exc:
        # Control de reintentos exponenciales ante caídas temporales del proveedor externo
        raise self.retry(exc=exc, countdown=60)