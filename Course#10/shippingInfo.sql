SELECT  
		od.orderNumber,
        od.productCode,
        p.warehouseCode,
        od.quantityOrdered,
        od.priceEach,
        o.orderDate,
        o.requiredDate,
        o.shippedDate,
        o.shippedDate - o.orderDate AS daysToShipping
FROM mintclassics.orderdetails od
JOIN mintclassics.orders o ON od.orderNumber = o.orderNumber
JOIN mintclassics.products p ON p.productCode = od.productCode;