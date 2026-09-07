-- 1. DROP the unneeded Notes column on Customers
ALTER TABLE dbo.Customers
DROP COLUMN Notes;

-- 2. ALTER Suppliers ContactEmail column length from 50 to 100
ALTER TABLE dbo.Suppliers
ALTER COLUMN ContactEmail NVARCHAR(100) NOT NULL;

-- 3. ADD the missing Foreign Key constraint on Products
ALTER TABLE dbo.Products
ADD CONSTRAINT FK_Products_Suppliers 
    FOREIGN KEY (SupplierID) REFERENCES dbo.Suppliers(SupplierID);

-- 4. MODIFY Orders CHECK constraint to include 'Cancelled'
ALTER TABLE dbo.Orders
DROP CONSTRAINT CK_Orders_Status;

ALTER TABLE dbo.Orders
ADD CONSTRAINT CK_Orders_Status 
    CHECK (OrderStatus IN ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'));

