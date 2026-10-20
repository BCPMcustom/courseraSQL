WITH orderInfo AS (

	SELECT
    productCode,
	quantityOrdered,
	priceEach,
	(quantityOrdered * priceEach) AS lineRevenue

	FROM mintclassics.orderdetails
    ),
    
    productInfo AS (
    
	SELECT 
	productCode,
	warehouseCode,
	productName,
	productLine,
	productVendor,
	buyPrice,
	quantityInStock
	FROM mintclassics.products
    )
    
SELECT 
	pi.productCode,
    pi.warehouseCode,
    pi.productName,
    pi.productLine,
    pi.productVendor,
    pi.quantityInStock,
    (pi.buyPrice * pi.quantityInStock) AS investmentValue,
    SUM(oi.lineRevenue) AS grossRevenue
FROM productInfo pi
LEFT JOIN orderInfo oi ON pi.productCode = oi.productCode
GROUP BY
	pi.productCode,
	pi.warehouseCode,
    pi.productName,
    pi.productLine,
    pi.productVendor,
    pi.buyPrice,
    pi.quantityInStock
;