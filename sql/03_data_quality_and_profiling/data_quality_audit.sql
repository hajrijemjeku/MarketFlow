SELECT 'Categories' AS TableName, COUNT(*) as 'RowCount' FROM dbo.Categories
UNION ALL
SELECT 'Suppliers', COUNT(*) FROM dbo.Suppliers
UNION ALL
SELECT 'Employees', COUNT(*) FROM dbo.Employees
UNION ALL
SELECT 'Customers', COUNT(*) FROM dbo.Customers
UNION ALL
SELECT 'Products', COUNT(*) FROM dbo.Products
UNION ALL
SELECT 'Orders', COUNT(*) FROM dbo.Orders
UNION ALL
SELECT 'OrderDetails', COUNT(*) FROM dbo.OrderDetails
UNION ALL
SELECT 'Returns', COUNT(*) FROM dbo.Returns
UNION ALL
SELECT 'Payments', COUNT(*) FROM dbo.Payments
UNION ALL
SELECT 'Shipments', COUNT(*) FROM dbo.Shipments;


-- 1.1 NULL analysis

-- 1.Orders with a CustomerID that doesn't exist
SELECT o.OrderID, o.CustomerID
FROM dbo.Orders o
LEFT JOIN dbo.Customers c
    ON o.CustomerID = c.CustomerID
WHERE c.CustomerID IS NULL;



-- 2.OrderDetails with an OrderID that doesn't exist
SELECT od.OrderDetailID, od.OrderID
FROM dbo.OrderDetails od
LEFT JOIN dbo.Orders o
    ON od.OrderID = o.OrderID
WHERE o.OrderID IS NULL;


-- 3.OrderDetails with a ProductID that doesn't exist
SELECT od.OrderDetailID, od.ProductID
FROM dbo.OrderDetails od
LEFT JOIN dbo.Products p
    ON od.ProductID = p.ProductID
WHERE p.ProductID IS NULL;


-- 4.Returns with an OrderDetailID that doesn't exist
SELECT r.ReturnID, r.OrderDetailID
FROM dbo.Returns r
LEFT JOIN dbo.OrderDetails od
    ON r.OrderDetailID = od.OrderDetailID
WHERE od.OrderDetailID IS NULL;


-- 5.Products with a CategoryID that doesn't exist
SELECT p.ProductID, p.CategoryID
FROM dbo.Products p
LEFT JOIN dbo.Categories c
    ON p.CategoryID = c.CategoryID
WHERE c.CategoryID IS NULL;


-- 6.Products with a SupplierID that doesn't exist
SELECT p.ProductID, p.SupplierID
FROM dbo.Products p
LEFT JOIN dbo.Suppliers s
    ON p.SupplierID = s.SupplierID
WHERE s.SupplierID IS NULL;




-- 1. NULL Values on Customers table
SELECT
    COUNT(*) AS TotalCustomers,
    SUM(CASE WHEN Phone IS NULL THEN 1 ELSE 0 END) AS MissingPhone,
    SUM(CASE WHEN DateOfBirth IS NULL THEN 1 ELSE 0 END) AS MissingDateOfBirth,
    SUM(CASE WHEN Gender IS NULL THEN 1 ELSE 0 END) AS MissingGender,
    SUM(CASE WHEN City IS NULL THEN 1 ELSE 0 END) AS MissingCity,
    SUM(CASE WHEN Country IS NULL THEN 1 ELSE 0 END) AS MissingCountry
FROM dbo.Customers;

-- 2. NULL Values on Categories table
SELECT 
    COUNT(*) AS TotalCategories,
    SUM(CASE WHEN CategoryID IS NULL THEN 1 ELSE 0 END) AS MissingCategoryID,
    SUM(CASE WHEN CategoryName IS NULL THEN 1 ELSE 0 END) AS MissingCategoryName,
    SUM(CASE WHEN Description IS NULL THEN 1 ELSE 0 END) AS MissingDescription,
    SUM(CASE WHEN CategoryStatus IS NULL THEN 1 ELSE 0 END) AS MissingCategoryStatus
FROM dbo.Categories;

-- 3. NULL Values on Suppliers table
SELECT 
    COUNT(*) AS TotalSuppliers,
    SUM(CASE WHEN SupplierID IS NULL THEN 1 ELSE 0 END) AS MissingSupplierID,
    SUM(CASE WHEN SupplierName IS NULL THEN 1 ELSE 0 END) AS MissingSupplierName,
    SUM(CASE WHEN ContactEmail IS NULL THEN 1 ELSE 0 END) AS MissingContactEmail,
    SUM(CASE WHEN Country IS NULL THEN 1 ELSE 0 END) AS MissingCountry
FROM dbo.Suppliers;

-- 4. NULL Values on Products table
SELECT 
    COUNT(*) AS TotalProducts,
    SUM(CASE WHEN ProductID IS NULL THEN 1 ELSE 0 END) AS MissingProductID,
    SUM(CASE WHEN ProductName IS NULL THEN 1 ELSE 0 END) AS MissingProductName,
    SUM(CASE WHEN CategoryID IS NULL THEN 1 ELSE 0 END) AS MissingCategoryID,
    SUM(CASE WHEN SupplierID IS NULL THEN 1 ELSE 0 END) AS MissingSupplierID,
    SUM(CASE WHEN Price IS NULL THEN 1 ELSE 0 END) AS MissingPrice,
    SUM(CASE WHEN Cost IS NULL THEN 1 ELSE 0 END) AS MissingCost,
    SUM(CASE WHEN StockQuantity IS NULL THEN 1 ELSE 0 END) AS MissingStockQuantity,
    SUM(CASE WHEN ProductStatus IS NULL THEN 1 ELSE 0 END) AS MissingProductStatus
FROM dbo.Products;

-- 5. NULL Values on Employees table
SELECT 
    COUNT(*) AS TotalEmployees,
    SUM(CASE WHEN EmployeeID IS NULL THEN 1 ELSE 0 END) AS MissingEmployeeID,
    SUM(CASE WHEN FirstName IS NULL THEN 1 ELSE 0 END) AS MissingFirstName,
    SUM(CASE WHEN LastName IS NULL THEN 1 ELSE 0 END) AS MissingLastName,
    SUM(CASE WHEN Email IS NULL THEN 1 ELSE 0 END) AS MissingEmail,
    SUM(CASE WHEN Phone IS NULL THEN 1 ELSE 0 END) AS MissingPhone,
    SUM(CASE WHEN Department IS NULL THEN 1 ELSE 0 END) AS MissingDepartment,
    SUM(CASE WHEN HireDate IS NULL THEN 1 ELSE 0 END) AS MissingHireDate,
    SUM(CASE WHEN EmployeeStatus IS NULL THEN 1 ELSE 0 END) AS MissingEmployeeStatus
FROM dbo.Employees;

-- 6. NULL Values on Orders table
SELECT 
    COUNT(*) AS TotalOrders,
    SUM(CASE WHEN OrderID IS NULL THEN 1 ELSE 0 END) AS MissingOrderID,
    SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END) AS MissingCustomerID,
    SUM(CASE WHEN EmployeeID IS NULL THEN 1 ELSE 0 END) AS MissingEmployeeID,
    SUM(CASE WHEN OrderDate IS NULL THEN 1 ELSE 0 END) AS MissingOrderDate,
    SUM(CASE WHEN OrderStatus IS NULL THEN 1 ELSE 0 END) AS MissingOrderStatus,
    SUM(CASE WHEN ShippingAddress IS NULL THEN 1 ELSE 0 END) AS MissingShippingAddress,
    SUM(CASE WHEN ShippingCity IS NULL THEN 1 ELSE 0 END) AS MissingShippingCity,
    SUM(CASE WHEN ShippingCountry IS NULL THEN 1 ELSE 0 END) AS MissingShippingCountry
FROM dbo.Orders;

-- 7. NULL Values on OrderDetails table
SELECT 
    COUNT(*) AS TotalOrderDetails,
    SUM(CASE WHEN OrderDetailID IS NULL THEN 1 ELSE 0 END) AS MissingOrderDetailID,
    SUM(CASE WHEN OrderID IS NULL THEN 1 ELSE 0 END) AS MissingOrderID,
    SUM(CASE WHEN ProductID IS NULL THEN 1 ELSE 0 END) AS MissingProductID,
    SUM(CASE WHEN Quantity IS NULL THEN 1 ELSE 0 END) AS MissingQuantity,
    SUM(CASE WHEN UnitPrice IS NULL THEN 1 ELSE 0 END) AS MissingUnitPrice,
    SUM(CASE WHEN Discount IS NULL THEN 1 ELSE 0 END) AS MissingDiscount
FROM dbo.OrderDetails;

-- 8. NULL Values on Payments table
SELECT 
    COUNT(*) AS TotalPayments,
    SUM(CASE WHEN PaymentID IS NULL THEN 1 ELSE 0 END) AS MissingPaymentID,
    SUM(CASE WHEN OrderID IS NULL THEN 1 ELSE 0 END) AS MissingOrderID,
    SUM(CASE WHEN PaymentDate IS NULL THEN 1 ELSE 0 END) AS MissingPaymentDate,
    SUM(CASE WHEN PaymentMethod IS NULL THEN 1 ELSE 0 END) AS MissingPaymentMethod,
    SUM(CASE WHEN PaymentAmount IS NULL THEN 1 ELSE 0 END) AS MissingPaymentAmount,
    SUM(CASE WHEN PaymentStatus IS NULL THEN 1 ELSE 0 END) AS MissingPaymentStatus,
    SUM(CASE WHEN TransactionReference IS NULL THEN 1 ELSE 0 END) AS MissingTransactionReference
FROM dbo.Payments;

-- 9. NULL Values on Shipments table
SELECT 
    COUNT(*) AS TotalShipments,
    SUM(CASE WHEN ShipmentID IS NULL THEN 1 ELSE 0 END) AS MissingShipmentID,
    SUM(CASE WHEN OrderID IS NULL THEN 1 ELSE 0 END) AS MissingOrderID,
    SUM(CASE WHEN ShipmentDate IS NULL THEN 1 ELSE 0 END) AS MissingShipmentDate,
    SUM(CASE WHEN EstimatedDeliveryDate IS NULL THEN 1 ELSE 0 END) AS MissingEstimatedDeliveryDate,
    SUM(CASE WHEN ActualDeliveryDate IS NULL THEN 1 ELSE 0 END) AS MissingActualDeliveryDate,
    SUM(CASE WHEN ShippingMethod IS NULL THEN 1 ELSE 0 END) AS MissingShippingMethod,
    SUM(CASE WHEN TrackingNumber IS NULL THEN 1 ELSE 0 END) AS MissingTrackingNumber,
    SUM(CASE WHEN ShipmentStatus IS NULL THEN 1 ELSE 0 END) AS MissingShipmentStatus
FROM dbo.Shipments;

-- 10. NULL Values on Returns table
SELECT 
    COUNT(*) AS TotalReturns,
    SUM(CASE WHEN ReturnID IS NULL THEN 1 ELSE 0 END) AS MissingReturnID,
    SUM(CASE WHEN OrderDetailID IS NULL THEN 1 ELSE 0 END) AS MissingOrderDetailID,
    SUM(CASE WHEN ReturnDate IS NULL THEN 1 ELSE 0 END) AS MissingReturnDate,
    SUM(CASE WHEN ReturnQuantity IS NULL THEN 1 ELSE 0 END) AS MissingReturnQuantity,
    SUM(CASE WHEN ReturnReason IS NULL THEN 1 ELSE 0 END) AS MissingReturnReason,
    SUM(CASE WHEN ReturnStatus IS NULL THEN 1 ELSE 0 END) AS MissingReturnStatus
FROM dbo.Returns;



-- 1.2 Duplicate checks

-- Check if customer email is unique
select email, count(*) as emailcount
from customers 
group by email 
order by emailcount desc


-- Check if employee email is unique
select email, count(*) as emailcount
from Employees
group by email
having count(email) > 1  
order by emailcount desc

-- Check if supplier email is unique
select contactemail, count(*) as emailcount
from Suppliers
group by contactemail
order by emailcount desc

-- Check if category names are unique
select CategoryName, count(*) namecount
from Categories
group by CategoryName
having count(*) > 1 
order by namecount asc

-- Check if tracking numbers is unique
select trackingnumber,count(*) as numbercount
from Shipments
where trackingnumber is not null
group by trackingnumber
having count(*) > 1
order by numbercount desc;




-- 1.3 Range/value validation

-- check price > 0, cost < 0, cost <= price, stockuantity < 0 or valid productStatus at products

select * from products
where price <= 0 
or cost < 0
or StockQuantity < 0
or cost >= price
or ProductStatus not in ('active', 'out of stock', 'discontinued')



-- check quantity >= 0 , unitprice >= 0 , discount between 0 and 100 at orderdetails
select *
from OrderDetails
where quantity <= 0
    or unitprice <= 0
    or discount < 0 
    or discount > 100


-- check paymentamount >= 0, valid payment methods, valid payment statuses
select * 
from Payments
where PaymentAmount <= 0
or PaymentMethod not IN ('Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery')
or PaymentStatus not in ('Pending', 'Completed', 'Failed', 'Refunded')


-- check returnquantity >= 0, returnquantity <= purchased quantity at returns
select r.returnid, r.OrderDetailID, r.ReturnQuantity, od.Quantity
from returns r
inner join OrderDetails od
on r.OrderDetailID = od.OrderDetailID
where r.ReturnQuantity <= 0
or r.ReturnQuantity > od.Quantity


-- 1.4 Referential integrity

-- verify that relationships are valid
select 'Orders -> Customers' as relationship, count(*) as orphanedrows 
from dbo.Orders 
where customerid not in (select customerid from dbo.Customers)

union all
select 'Orders -> Employees', count(*) 
from dbo.Orders 
where employeeid is not null 
  and employeeid not in (select employeeid from dbo.Employees)

union all
select 'OrderDetails -> Orders', count(*) 
from dbo.OrderDetails 
where orderid not in (select orderid from dbo.Orders)

union all
select 'OrderDetails -> Products', count(*) 
from dbo.OrderDetails 
where productid not in (select productid from dbo.Products)

union all
select 'Products -> Categories', count(*) 
from dbo.Products 
where categoryid not in (select categoryid from dbo.Categories)

union all
select 'Products -> Suppliers', count(*) 
from dbo.Products 
where supplierid not in (select supplierid from dbo.Suppliers)

union all
select 'Returns -> OrderDetails', count(*) 
from dbo.Returns 
where orderdetailid not in (select orderdetailid from dbo.OrderDetails)

union all
select 'Payments -> Orders', count(*) 
from dbo.Payments 
where orderid not in (select orderid from dbo.Orders)

union all
select 'Shipments -> Orders', count(*) 
from dbo.Shipments 
where orderid not in (select orderid from dbo.Orders);



-- 1.5 Check Date Logic

-- A customer shouldn't place an order before registering.
select 'Order before Registration' as ViolationType, count(*) as 'ViolationCount'
from dbo.customers c
inner join orders o
on c.CustomerID = o.CustomerID
where o.orderdate < c.RegistrationDate

union all
-- Shipment dispatched before order date
select 'Shipment before Order', count(*)
from dbo.orders o
inner join dbo.shipments sh on o.orderid = sh.orderid
where sh.shipmentdate < o.orderdate

union all
  -- Actual Delivery occurred before shipment date
select 'Actual Delivery before Shipment', count(*)
from dbo.shipments
where actualdeliverydate is not null 
  and actualdeliverydate < shipmentdate

union all
  -- Estumated Delivery occurred before shipment date
select 'Estimated Delivery before Shipment', count(*)
from dbo.shipments
where estimateddeliverydate < shipmentdate

union all
-- A return shouldn't happen before delivery.
select 'Return before Delivery', count(*)
from dbo.returns r
inner join dbo.orderdetails od on r.orderdetailid = od.orderdetailid
inner join dbo.shipments sh on od.orderid = sh.orderid
where sh.actualdeliverydate is not null 
  and r.returndate < sh.actualdeliverydate;



-- 1.6 Business-rule validation

-- number of customers who didnt order and products never sold
select 'Customers who didnt order' as 'check', count(*) as 'count'
from customers c
left join orders o
on c.CustomerID = o.CustomerID
where o.customerid is null or o.CustomerID = ''
union all
select 'Products never sold' , count(*) 
from Products p
left join orderdetails od
on p.ProductID = od.ProductID
where od.ProductID is null or od.ProductID = ''

--Orders with different statuses
select orderstatus, count(*) as orderCount
from orders 
group by OrderStatus

--Employees are only assigned to active employees
select e.EmployeeStatus, count(*) as StatusCount
from orders o
join Employees e 
on o.EmployeeID = e.EmployeeID
group by e.EmployeeStatus

--Delivered shipments have delivery dates
select count(*) as deliveredMissingDateCount
from Shipments
where ShipmentStatus = 'Delivered' 
and ActualDeliveryDate is null

--Undelivered shipments don't have actual delivery dates
select count(*) as undeliveredWithDateCount
from Shipments
where ShipmentStatus <> 'Delivered'
and ActualDeliveryDate is not null

--Automated orders have EmployeeID = NULL
select
    sum( case when employeeid is null then 1 else 0 end) as 'online/automated orders',
    sum( case when employeeid is not null then 1 else 0 end) as 'staff assisted orders',
    count(*) as 'total orders'
from Orders










