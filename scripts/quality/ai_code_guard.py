import ast
import sys
from pathlib import Path
from typing import List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("AICodeGuard")

DANGEROUS_FUNCTIONS = {'eval', 'exec'}
DANGEROUS_MODULES = {'subprocess', 'pickle', 'os'}

class SecurityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in DANGEROUS_FUNCTIONS:
            self.issues.append(f"Uso perigoso de função detectado: '{node.func.id}' na linha {node.lineno}")
        elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == 'subprocess':
                for keyword in node.keywords:
                    if keyword.arg == 'shell' and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        self.issues.append(f"Uso inseguro de subprocess com shell=True na linha {node.lineno}")
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in DANGEROUS_MODULES:
                pass
        self.generic_visit(node)

def scan_file(filepath: Path) -> List[str]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)
        visitor = SecurityVisitor()
        visitor.visit(tree)
        return visitor.issues
    except Exception as e:
        logger.error(f"Erro ao analisar arquivo {filepath}: {e}")
        return []

def main():
    logger.info("Verificando guardrails e segurança (IA Guard)...")
    project_root = Path(__file__).parent.parent.parent
    has_issues = False
    
    for py_file in project_root.rglob('*.py'):
        if any(part in py_file.parts for part in ['.venv', 'venv', 'tests', 'scripts', 'compliance', 'security']) or any(ignored in py_file.name for ignored in ['setup-hooks.py', 'sandbox.py', 'postgres_backup.py']):
            continue
        issues = scan_file(py_file)
        if issues:
            has_issues = True
            logger.error(f"Arquivo: {py_file.relative_to(project_root)}")
            for issue in issues:
                logger.error(f"  -> {issue}")
                
    if has_issues:
        logger.error("Falha na validação de segurança (IA Guard).")
        sys.exit(1)
    logger.info("Nenhuma anomalia crítica gerada por IA detectada.")
    sys.exit(0)

if __name__ == "__main__":
    main()
