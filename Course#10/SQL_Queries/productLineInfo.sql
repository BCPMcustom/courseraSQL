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
        od.priceEach AS salePrice,
        od.orderNumber,
        od.quantityOrdered AS quantitySold,
		(od.quantityOrdered * od.priceEach) AS lineRevenue

FROM mintclassics.orderdetails od
GROUP BY od.productCode, od.orderNumber, od.priceEach
)

SELECT
	pli.productCode,
    pli.productLine,
    pli.productVendor,
    pli.buyPrice,
    pli.warehouseCode,
    pli.quantityInStock,
    pli.investmentValue,
    SUM(ri.quantitySold * ri.lineRevenue) AS grossRevenue

FROM productLinesInfo pli
JOIN revenueInfo ri ON pli.productCode = ri.productCode

GROUP BY
	pli.productCode,
    pli.productLine,
    pli.productVendor,
    pli.buyPrice,
    pli.warehouseCode,
    pli.quantityInStock,
    pli.investmentValue

;