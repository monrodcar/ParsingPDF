// Technologies Graph:

LOAD CSV WITH HEADERS FROM "file:///technologies.csv" AS row

WITH [key in keys(row)] AS roles, row
UNWIND roles AS role
WITH role, row[role] as skill
WHERE skill IS NOT NULL
MERGE (r:Role {name:role})
MERGE (s:Skill {name:skill})
MERGE (r)-[:REQUIRES_SKILL]->(s);

MATCH (r:Role),(s:Skill),(s)<-[:REQUIRES_SKILL]-(r)
WHERE r.name IN ["backend", "frontend", "database engineer"]
MERGE (r1:Role {name:"fullstack"})
MERGE (r1)-[:REQUIRES_SKILL]->(s)
MATCH (r1:Role),(r2:Role),(s:Skill),(s)<-[:REQUIRES_SKILL]-(r1)
WHERE r1.name = "database engineer" AND r2.name = "backend"
MERGE (r2)-[:REQUIRES_SKILL]-(s);