
WITH 
	
    productLinesInfo AS (
SELECT 
        p.warehouseCode,
        p.productCode,
        p.productLine,
        p.productVendor,
        p.buyPrice,
        p.quantityInStock,
        p.buyPrice * p.quantityInStock AS investmentValue
FROM mintclassics.products p
),

	revenueInfo AS (
SELECT
        od.productCode,
        od.priceEach,
		SUM(od.quantityOrdered) AS quantitySold,
        SUM(od.priceEach) AS lineRevenue 
FROM mintclassics.orderdetails od
GROUP BY od.productCode, priceEach
)

SELECT
	pli.*,
    ri.priceEach,
    ri.quantitySold,
    ri.lineRevenue,
    ri.quantitySold * ri.lineRevenue AS grossRevenue
FROM productLinesInfo pli
JOIN revenueInfo ri ON pli.productCode = ri.productCode
;