"""
Agent de formatage SQL (logique reutilisable, sans dependance a Streamlit).

Applique les regles definies dans .sqlfluff a une chaine de code SQL
et renvoie la version corrigee ainsi que la liste des violations restantes.
"""

from pathlib import Path

import sqlfluff
from sqlfluff.core import FluffConfig, Linter

CONFIG_DIR = Path(__file__).resolve().parent
CONFIG_PATH = CONFIG_DIR / ".sqlfluff"


def format_sql(sql: str) -> str:
    """Retourne la version corrigee du code SQL selon les regles de l'equipe."""
    return sqlfluff.fix(sql, config_path=str(CONFIG_PATH), fix_even_unparsable=True)


def lint_sql(sql: str) -> list[dict]:
    """Retourne la liste des violations restantes (apres correction eventuelle)."""
    config = FluffConfig.from_path(str(CONFIG_DIR))
    linter = Linter(config=config)
    result = linter.lint_string(sql)
    return [
        {
            "line": v.line_no,
            "position": v.line_pos,
            "code": v.rule_code(),
            "description": v.desc(),
        }
        for v in result.violations
    ]
