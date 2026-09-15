WITH volumeinfo AS (

SELECT 
		p.productCode,
        p.productLine,
        p.warehouseCode,
        w.warehousePctCap,
        p.quantityInStock,
        md.`estimatedFootprint(sq.ft)`,
        md.`estimatedVolume(cu.ft)`,
        md.`estimatedVolume(cu.ft)` * p.quantityInStock AS `totalVolume(cu.ft)`
FROM mintclassics.products p
JOIN mintclassics.modelsDescription md ON p.productCode = md. productCode
JOIN mintclassics.warehouses w ON w.warehouseCode = p.warehouseCode
)

SELECT
        warehouseCode,
        warehousePctCap,
        SUM(`totalVolume(cu.ft)`) AS stockVolume,
        SUM(`totalVolume(cu.ft)`) / (warehousePctCap / 100) AS warehouseCapacity,
        (SUM(`totalVolume(cu.ft)`) / (warehousePctCap / 100)) - SUM(`totalVolume(cu.ft)`) AS spaceRemaining
FROM volumeinfo
GROUP BY warehouseCode;