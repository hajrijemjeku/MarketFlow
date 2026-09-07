    CREATE TABLE dbo.Customers (
        CustomerID INT IDENTITY(1,1) CONSTRAINT PK_Customers PRIMARY KEY,
        FirstName NVARCHAR(50) NOT NULL,
        LastName NVARCHAR(50) NOT NULL,
        Email NVARCHAR(100) NOT NULL CONSTRAINT UQ_CustomerEmail UNIQUE,
        Phone NVARCHAR(25) NULL,
        DateOfBirth DATE NULL,
        Gender NVARCHAR(20) NULL,
        City NVARCHAR(50) NULL,
        Country NVARCHAR(50) NULL,
        RegistrationDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        CustomerStatus NVARCHAR(20) NOT NULL DEFAULT 'Active',
        Notes NVARCHAR(255) NULL,
        CONSTRAINT CK_Customers_Status CHECK (CustomerStatus IN ('Active', 'Inactive'))
    );



    CREATE TABLE dbo.Categories (
        CategoryID INT IDENTITY(1,1) CONSTRAINT PK_Categories PRIMARY KEY,
        CategoryName NVARCHAR(50) NOT NULL CONSTRAINT UQ_CategoryName UNIQUE,
        Description NVARCHAR(255) NULL,
        CategoryStatus NVARCHAR(20) NOT NULL DEFAULT 'Active',
        CONSTRAINT CK_Categories_Status CHECK (CategoryStatus IN ('Active', 'Inactive'))
    );


    CREATE TABLE dbo.Suppliers (
        SupplierID INT IDENTITY(1,1) CONSTRAINT PK_Suppliers PRIMARY KEY,
        SupplierName NVARCHAR(100) NOT NULL,
        ContactEmail NVARCHAR(50) NOT NULL CONSTRAINT UQ_SupplierEmail UNIQUE,
        Country NVARCHAR(50) NOT NULL DEFAULT 'Germany'
    );


    CREATE TABLE dbo.Products (
        ProductID INT IDENTITY(1,1) CONSTRAINT PK_Products PRIMARY KEY,
        ProductName NVARCHAR(100) NOT NULL,
        CategoryID INT NOT NULL,
        SupplierID INT NOT NULL,
        Price DECIMAL(10,2) NOT NULL,
        Cost DECIMAL(10,2) NOT NULL,
        StockQuantity INT NOT NULL DEFAULT 0,
        ProductStatus NVARCHAR(20) NOT NULL DEFAULT 'Active',
    
        -- Foreign Key Relationships
        CONSTRAINT FK_Products_Categories FOREIGN KEY (CategoryID) REFERENCES dbo.Categories(CategoryID),
    
        -- Business Rules
        CONSTRAINT CK_Products_Price CHECK (Price > 0),
        CONSTRAINT CK_Products_Cost CHECK (Cost >= 0),
        CONSTRAINT CK_Products_Stock CHECK (StockQuantity >= 0),
        CONSTRAINT CK_Products_Status CHECK (ProductStatus IN ('Active', 'Out of Stock', 'Discontinued'))
    );


    CREATE TABLE dbo.Employees (
        EmployeeID INT IDENTITY(1,1) CONSTRAINT PK_Employees PRIMARY KEY,
        FirstName NVARCHAR(50) NOT NULL,
        LastName NVARCHAR(50) NOT NULL,
        Email NVARCHAR(100) NOT NULL CONSTRAINT UQ_EmployeeEmail UNIQUE,
        Phone NVARCHAR(25) NULL,
        Department NVARCHAR(50) NOT NULL,
        HireDate DATE NOT NULL,
        EmployeeStatus NVARCHAR(20) NOT NULL DEFAULT 'Active',

        -- Business Rules
        CONSTRAINT CK_Employees_Status 
            CHECK (EmployeeStatus IN ('Active', 'Inactive'))
    );


    CREATE TABLE dbo.Orders (
        OrderID INT IDENTITY(1,1) CONSTRAINT PK_Orders PRIMARY KEY,
        CustomerID INT NOT NULL,
        EmployeeID INT NULL,
        OrderDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        OrderStatus NVARCHAR(20) NOT NULL DEFAULT 'Pending',
        ShippingAddress NVARCHAR(255) NOT NULL,
        ShippingCity NVARCHAR(50) NOT NULL,
        ShippingCountry NVARCHAR(50) NOT NULL,
    
        -- Foreign Key Relationships
        CONSTRAINT FK_Orders_Customers
            FOREIGN KEY (CustomerID) REFERENCES dbo.Customers(CustomerID),

        CONSTRAINT FK_Orders_Employees
            FOREIGN KEY (EmployeeID) REFERENCES dbo.Employees(EmployeeID),

        -- Business Rules
        CONSTRAINT CK_Orders_Status
            CHECK (OrderStatus IN ('Pending', 'Processing', 'Shipped', 'Delivered'))
    );


    CREATE TABLE dbo.OrderDetails (
        OrderDetailID INT IDENTITY(1,1) CONSTRAINT PK_OrderDetails PRIMARY KEY,
        OrderID INT NOT NULL,
        ProductID INT NOT NULL,
        Quantity INT NOT NULL,
        UnitPrice DECIMAL(10,2) NOT NULL,
        Discount DECIMAL(5,2) NOT NULL DEFAULT 0,

        -- Foreign Key Relationships
        CONSTRAINT FK_OrderDetails_Orders
            FOREIGN KEY (OrderID) REFERENCES dbo.Orders(OrderID),

        CONSTRAINT FK_OrderDetails_Products
            FOREIGN KEY (ProductID) REFERENCES dbo.Products(ProductID),

        -- Business Rules
        CONSTRAINT CK_OrderDetails_Quantity
            CHECK (Quantity > 0),

        CONSTRAINT CK_OrderDetails_UnitPrice
            CHECK (UnitPrice > 0),

        CONSTRAINT CK_OrderDetails_Discount
            CHECK (Discount >= 0 AND Discount <= 100)
    );


    CREATE TABLE dbo.Returns (
        ReturnID INT IDENTITY(1,1) CONSTRAINT PK_Returns PRIMARY KEY,
        OrderDetailID INT NOT NULL,
        ReturnDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        ReturnQuantity INT NOT NULL,
        ReturnReason NVARCHAR(255) NULL,
        ReturnStatus NVARCHAR(20) NOT NULL DEFAULT 'Requested',

        -- Foreign Key Relationship
        CONSTRAINT FK_Returns_OrderDetails
            FOREIGN KEY (OrderDetailID) REFERENCES dbo.OrderDetails(OrderDetailID),

        -- Business Rules
        CONSTRAINT CK_Returns_Quantity
            CHECK (ReturnQuantity > 0),

        CONSTRAINT CK_Returns_Status
            CHECK (ReturnStatus IN ('Requested', 'Approved', 'Rejected', 'Completed'))
    );


    CREATE TABLE dbo.Payments (
        PaymentID INT IDENTITY(1,1) CONSTRAINT PK_Payments PRIMARY KEY,
        OrderID INT NOT NULL,
        PaymentDate DATETIME2 NOT NULL DEFAULT GETDATE(),
        PaymentMethod NVARCHAR(30) NOT NULL,
        PaymentAmount DECIMAL(10,2) NOT NULL,
        PaymentStatus NVARCHAR(20) NOT NULL DEFAULT 'Pending',
        TransactionReference NVARCHAR(100) NULL,

        -- Foreign Key Relationship
        CONSTRAINT FK_Payments_Orders
            FOREIGN KEY (OrderID) REFERENCES dbo.Orders(OrderID),

        -- Business Rules
        CONSTRAINT CK_Payments_Amount
            CHECK (PaymentAmount > 0),

        CONSTRAINT CK_Payments_Method
            CHECK (PaymentMethod IN ('Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery')),

        CONSTRAINT CK_Payments_Status
            CHECK (PaymentStatus IN ('Pending', 'Completed', 'Failed', 'Refunded'))
    );


    CREATE TABLE dbo.Shipments (
        ShipmentID INT IDENTITY(1,1) CONSTRAINT PK_Shipments PRIMARY KEY,
        OrderID INT NOT NULL,
        ShipmentDate DATETIME2 NULL,
        EstimatedDeliveryDate DATE NULL,
        ActualDeliveryDate DATE NULL,
        ShippingMethod NVARCHAR(30) NOT NULL,
        TrackingNumber NVARCHAR(100) NULL CONSTRAINT UQ_ShipmentTracking UNIQUE,
        ShipmentStatus NVARCHAR(20) NOT NULL DEFAULT 'Pending',

        -- Foreign Key Relationship
        CONSTRAINT FK_Shipments_Orders
            FOREIGN KEY (OrderID) REFERENCES dbo.Orders(OrderID),

        -- Business Rules
        CONSTRAINT CK_Shipments_Status
            CHECK (ShipmentStatus IN ('Pending', 'Shipped', 'In Transit', 'Delivered', 'Cancelled')),

        CONSTRAINT CK_Shipments_DeliveryDates 
            CHECK (
                (EstimatedDeliveryDate IS NULL OR ShipmentDate IS NULL OR EstimatedDeliveryDate >= CAST(ShipmentDate AS DATE)) AND
                (ActualDeliveryDate IS NULL OR ShipmentDate IS NULL OR ActualDeliveryDate >= CAST(ShipmentDate AS DATE))
            )
    );






drop table if exists [dbo].[Shipments]
drop table if exists [dbo].[Returns]
drop table if exists [dbo].[Payments]
drop table if exists [dbo].[OrderDetails]
drop table if exists [dbo].[Orders]
drop table if exists [dbo].[Products]
drop table if exists [dbo].[Employees]
drop table if exists [dbo].[Customers]
drop table if exists [dbo].[Categories]
drop table if exists [dbo].[Suppliers]
