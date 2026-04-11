import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "sql_expert"


def sql_expert(descripcion: str, tipo: str = "query", dialecto: str = "mysql") -> str:
    """
    Crea consultas SQL, esquemas, seeders y optimiza queries.
    Tipos: query, schema, seeder, optimizar
    Dialectos: mysql, postgresql, sqlite
    """
    instrucciones = f"""
Eres un experto en SQL y diseño de bases de datos para {dialecto}.

ESPECIALIDADES:
- Consultas: SELECT con joins, subqueries, CTEs, window functions
- Esquemas: CREATE TABLE, ALTER, índices, foreign keys, constraints
- Seeds: Datos de ejemplo realistas para populate
- Optimización: Análisis de queries, sugerencias de índices

REGLAS ESTRICTAS PARA {dialecto.upper()}:
1. SQL语法 correcta para {dialecto}
2. Nombres en snake_case (tablas y columnas)
3. Índices en columnas usadas en WHERE y JOIN
4. Foreign keys con nombres descriptivos
5. Comments explaining el "por qué" de decisiones de diseño

EJEMPLOS DE FORMATO PARA {dialecto.upper()}:

Query simple:
```sql
SELECT u.name, COUNT(o.id) as orders
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.active = 1
GROUP BY u.id
ORDER BY orders DESC
LIMIT 10;
```

Schema:
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB;
```

Seeder:
```sql
INSERT INTO users (name, email) VALUES
('Admin', 'admin@example.com'),
('User Test', 'test@example.com');
```
"""

    if LECCIONES_CONSOLIDADAS.strip():
        instrucciones += (
            f"\n--- LECCIONES PERMANENTES ---\n{LECCIONES_CONSOLIDADAS.strip()}\n"
        )

    memorias = engram.recuperar_engramas(SKILL_NAME)
    if "Sin memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\n--- LECCIONES TEMPORALES ---\n{memorias}\n"

    prompt = f"""
Tipo de operación: {tipo}
Dialecto: {dialecto}

Necesidad: {descripcion}
"""

    try:
        response = config_lm.complete(
            messages=[
                {"role": "system", "content": instrucciones.strip()},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1200,
        )
        return response.choices[0].message.content
    except Exception as e:
        return (
            f"Error en sql_expert: {str(e)}\n\nConsejos: Especifica más detalles sobre la estructura de tablas o el tipo de consulta que necesitas."
            ""
        )
