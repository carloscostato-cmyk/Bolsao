-- Seed data for pontos_bolsao (sample from production)
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

DELETE FROM pontos_bolsao WHERE point_pack_number = 'ELAVM4715259066';

INSERT INTO pontos_bolsao
    (point_pack_number, responsavel, projetos, pontos, used_amount, registration_date, expiration_date, previsao_inicio, tempo_projeto_meses)
VALUES
    ('ELAVM4715259066', 'Projetos Especiais', 'Proderj', 50000, 50000.00, '2024-11-04', '2029-11-03', NULL, NULL);

COMMIT;
PRAGMA foreign_keys=ON;
