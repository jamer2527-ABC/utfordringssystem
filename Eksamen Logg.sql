USE EksamenDB;

SELECT Handling, COUNT(*) AS AntallGanger, MIN(Tidspunkt) AS FørstGang, MAX(Tidspunkt) AS SistGang
FROM Logg
GROUP BY Handling
ORDER BY AntallGanger DESC;