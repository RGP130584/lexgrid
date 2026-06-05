import re

def validate_cnpj(cnpj: str) -> bool:
    # Clean CNPJ from non-digits
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    if len(cnpj) != 14:
        return False
        
    # Exclude known invalid patterns
    if cnpj in [c * 14 for c in "0123456789"]:
        return False
        
    # Validate first verification digit
    soma = 0
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(12):
        soma += int(cnpj[i]) * pesos[i]
    digito1 = 11 - (soma % 11)
    digito1 = 0 if digito1 >= 10 else digito1
    
    if int(cnpj[12]) != digito1:
        return False
        
    # Validate second verification digit
    soma = 0
    pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(13):
        soma += int(cnpj[i]) * pesos[i]
    digito2 = 11 - (soma % 11)
    digito2 = 0 if digito2 >= 10 else digito2
    
    return int(cnpj[13]) == digito2
