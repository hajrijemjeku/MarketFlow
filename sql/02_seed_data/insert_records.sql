-- Categories table - insert data
SET IDENTITY_INSERT dbo.Categories ON;

INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (1, 'Laptops & Computers', 'Agent every development say.', 'Active');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (2, 'Monitors & Displays', 'Beautiful instead ahead despite measure ago current.', 'Inactive');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (3, 'PC Components', 'Information last everything thank serve civil institution.', 'Active');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (4, 'Storage & Networking', 'Choice whatever from behavior benefit.', 'Active');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (5, 'Audio & Headphones', 'Page southern role movie win her.', 'Active');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (6, 'Smart Home Devices', 'Fall pick those gun court attorney product.', 'Active');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (7, 'Wearables & Fitness', 'World talk term herself law.', 'Active');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (8, 'Gaming & Consoles', 'Class great prove reduce raise author.', 'Inactive');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (9, 'Keyboards & Mice', 'Move each left establish.', 'Active');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (10, 'Mobile & Tablets', 'Detail food shoulder argue start source husband.', 'Inactive');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (11, 'Cameras & Video', 'Decision wall then fire.', 'Active');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (12, 'Cables & Adapters', 'How trip learn enter east no enjoy.', 'Active');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (13, 'Printers & Supplies', 'Investment on gun young catch management sense technology.', 'Inactive');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (14, 'Power & Batteries', 'Physical society instead as.', 'Active');
INSERT INTO dbo.Categories (CategoryID, CategoryName, Description, CategoryStatus) VALUES (15, 'Office Tech Accessories', 'Other life edge network wall quite.', 'Active');

SET IDENTITY_INSERT dbo.Categories OFF;
GO

SELECT * FROM dbo.Categories;

-- Suppliers table - insert data
BULK INSERT dbo.Suppliers
FROM 'C:\Users\NewAdmin123\Desktop\creativehubkos\sql\projects\marketflow\data\suppliers.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    FORMAT = 'CSV',
    KEEPIDENTITY
);
GO

SELECT * FROM dbo.Suppliers;


-- Employees table - insert data
BULK INSERT dbo.Employees
FROM 'C:\Users\NewAdmin123\Desktop\creativehubkos\sql\projects\marketflow\data\employees.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    FORMAT = 'CSV',
    KEEPIDENTITY
);
GO

SELECT * FROM dbo.Employees;


-- Customers table - insert data
BULK INSERT dbo.Customers
FROM 'C:\Users\NewAdmin123\Desktop\creativehubkos\sql\projects\marketflow\data\customers.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    FORMAT = 'CSV',
    KEEPIDENTITY
);
GO

SELECT * FROM dbo.Customers;


-- Products table - insert data
BULK INSERT dbo.Products
FROM 'C:\Users\NewAdmin123\Desktop\creativehubkos\sql\projects\marketflow\data\products.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    FORMAT = 'CSV',
    KEEPIDENTITY
);
GO

SELECT * FROM dbo.products;


-- Orders table - insert data
BULK INSERT dbo.Orders
FROM 'C:\Users\NewAdmin123\Desktop\creativehubkos\sql\projects\marketflow\data\orders.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    FORMAT = 'CSV',
    KEEPIDENTITY
);
GO

SELECT * FROM dbo.orders;


-- OrderDetails table - insert data
BULK INSERT dbo.OrderDetails
FROM 'C:\Users\NewAdmin123\Desktop\creativehubkos\sql\projects\marketflow\data\order_details.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    FORMAT = 'CSV',
    KEEPIDENTITY
);
GO

SELECT * FROM dbo.orderdetails;


-- Payments table - insert data
BULK INSERT dbo.Payments
FROM 'C:\Users\NewAdmin123\Desktop\creativehubkos\sql\projects\marketflow\data\payments.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    FORMAT = 'CSV',
    KEEPIDENTITY
);
GO

SELECT * FROM dbo.payments;



-- Shipments table - insert data
-- 1. Drop the strict UNIQUE constraint causing the error
ALTER TABLE dbo.Shipments 
DROP CONSTRAINT UQ_ShipmentTracking;
GO

-- 2. Run BULK INSERT
BULK INSERT dbo.Shipments
FROM 'C:\Users\NewAdmin123\Desktop\creativehubkos\sql\projects\marketflow\data\shipments.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    FORMAT = 'CSV',
    KEEPIDENTITY
);
GO

-- 3. Re-apply a unique rule that IGNORES NULL/blank values
CREATE UNIQUE NONCLUSTERED INDEX UQ_ShipmentTracking_Filtered
ON dbo.Shipments(TrackingNumber)
WHERE TrackingNumber IS NOT NULL;
GO

SELECT * FROM dbo.shipments;



-- Returns table - insert data
BULK INSERT dbo.Returns
FROM 'C:\Users\NewAdmin123\Desktop\creativehubkos\sql\projects\marketflow\data\returns.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    FORMAT = 'CSV',
    KEEPIDENTITY
);
GO

SELECT * FROM dbo.returns;