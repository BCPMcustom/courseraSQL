WITH shiptime AS (

SELECT 
orderNumber,
orderDate,
shippedDate,
DATEDIFF(shippedDate, orderDate) AS daysToShipping
FROM mintclassics.orders
WHERE shippedDate IS NOT NULL
ORDER BY daysToShipping
),

	productinfo AS (
SELECT
orderNumber,
productCode,
quantityOrdered * priceEach AS lineTotal
FROM mintclassics.orderdetails
    )

SELECT
	st.orderNumber,
    p.warehouseCode,
    pro.productcode,
    st.daysToShipping,
    pro.lineTotal
FROM shiptime st 
JOIN productinfo pro ON st.orderNumber = pro.orderNumber
JOIN mintclassics.products p ON p.productCode = pro.productCode
-- The order shipped at 65 days (#10165) was due to a consumer credit problem and will not be conidered
WHERE st.orderNumber != 10165
ORDER BY daysToShipping DESC;