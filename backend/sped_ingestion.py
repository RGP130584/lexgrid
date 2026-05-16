from domain.entities.sped import SpedFile, SpedRecord
from sped.declaracoes.icmsipi import EFD_ICMS_IPI


class SpedIngestionUseCase:
    def __init__(self, repository=None):
        self.repository = repository

    def execute(self, filename: str, content: str) -> SpedFile:
        """
        Processa o conteúdo cru de um arquivo SPED e o converte em entidades de domínio.
        """
        records = []
        
        # Instancia o objeto da biblioteca para validação profunda
        sped_lib = EFD_ICMS_IPI()
        file_type = "SPED Fiscal (ICMS/IPI)"

        for line in content.splitlines():
            line = line.strip()
            if line.startswith("|"):
                parts = line.split("|")
                if len(parts) > 1:
                    register_type = parts[1]
                    
                    # Registro 0000 contém os metadados do período/empresa
                    if register_type == "0000" and len(parts) > 10:
                        file_type = f"SPED de {parts[10]} - CNPJ: {parts[7]}"

                    records.append(
                        SpedRecord(register_type=register_type, data={"raw": line})
                    )

        sped_file = SpedFile(
            filename=filename,
            file_type=file_type,
            records=records
        )
        
        if self.repository:
            self.repository.save(sped_file)
            
        return sped_file