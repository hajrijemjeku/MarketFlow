import os
import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Fixed seed for reproducible output
fake = Faker()
Faker.seed(42)
random.seed(42)

OUTPUT_DIR = "data"

NUM_CATEGORIES = 15
NUM_SUPPLIERS = 25
NUM_EMPLOYEES = 40
NUM_CUSTOMERS = 1800
NUM_PRODUCTS = 280
NUM_ORDERS = 13500

print("Initializing MarketFlow Data Generation Engine...")

# =============================================================================
# 1. CATEGORIES (15 Rows - Category 12 set to 'Inactive')
# =============================================================================
categories_data = [
    (1, "Laptops & Computers", "Laptops, desktop PCs, and workstations", "Active"),
    (2, "Monitors & Displays", "4K monitors, gaming displays, and stands", "Active"),
    (3, "PC Components", "CPUs, GPUs, motherboards, and power supplies", "Active"),
    (4, "Storage & Networking", "SSDs, external drives, and Wi-Fi routers", "Active"),
    (5, "Audio & Headphones", "Noise-canceling headphones and speakers", "Active"),
    (6, "Smart Home Devices", "Smart speakers, cameras, and hubs", "Active"),
    (7, "Wearables & Fitness", "Smartwatches and fitness trackers", "Active"),
    (8, "Gaming & Consoles", "Consoles, controllers, and VR headsets", "Active"),
    (9, "Keyboards & Mice", "Mechanical keyboards and ergonomic mice", "Active"),
    (10, "Mobile & Tablets", "Tablets, smartphones, and accessories", "Active"),
    (11, "Cameras & Video", "Mirrorless cameras, webcams, and tripods", "Active"),
    (12, "Cables & Adapters", "HDMI cables, USB-C hubs, and adapters", "Inactive"), # Retired category (tests CK_Categories_Status)
    (13, "Printers & Supplies", "Laser printers, ink cartridges, and paper", "Active"),
    (14, "Power & Batteries", "UPS backups, power banks, and chargers", "Active"),
    (15, "Office Tech Accessories", "Laptop bags, monitor arms, and desk mounts", "Active")
]

categories = [
    {"CategoryID": cid, "CategoryName": name, "Description": desc, "CategoryStatus": status}
    for cid, name, desc, status in categories_data
]

# =============================================================================
# 2. SUPPLIERS (25 Rows - Strict Schema Compliance)
# =============================================================================
suppliers = []
for sid in range(1, NUM_SUPPLIERS + 1):
    company = fake.company().replace(",", "").replace("'", "")
    clean_name = f"{company}_{sid}" # Ensures uniqueness
    email = f"contact@{clean_name.lower().replace(' ', '')[:15]}.com"
    suppliers.append({
        "SupplierID": sid,
        "SupplierName": clean_name,
        "ContactEmail": email,
        "Country": random.choice(["United States", "Taiwan", "China", "South Korea", "Germany", "Japan"])
    })

# =============================================================================
# 3. EMPLOYEES (40 Rows - Strict Schema Compliance)
# =============================================================================
employees = []
departments = ["Customer Support", "Logistics & Order Processing", "Account Management", "Sales & B2B"]

for eid in range(1, NUM_EMPLOYEES + 1):
    first = fake.first_name()
    last = fake.last_name()
    email = f"{first.lower()}.{last.lower()}{eid}@marketflow.com"
    dept = random.choice(departments)
    hire_date = fake.date_between(start_date="-5y", end_date="-1y").strftime("%Y-%m-%d")
    status = "Active" if random.random() > 0.10 else "Inactive" # Matches CK_Employees_Status
    
    employees.append({
        "EmployeeID": eid,
        "FirstName": first,
        "LastName": last,
        "Email": email,
        "Phone": fake.phone_number()[:25],
        "Department": dept,
        "HireDate": hire_date,
        "EmployeeStatus": status
    })

# Active employees pool for realistic order assignment
active_employee_ids = [e["EmployeeID"] for e in employees if e["EmployeeStatus"] == "Active"]

# =============================================================================
# 4. CUSTOMERS (1,800 Rows)
# =============================================================================
customers = []
for cid in range(1, NUM_CUSTOMERS + 1):
    first = fake.first_name()
    last = fake.last_name()
    email = f"{first.lower()}.{last.lower()}{cid}@{fake.free_email_domain()}"
    phone = "" if random.random() < 0.15 else fake.phone_number()[:25]
    dob = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%Y-%m-%d")
    reg_date = fake.date_time_between(start_date="-3y", end_date="-6m").strftime("%Y-%m-%d %H:%M:%S")
    
    customers.append({
        "CustomerID": cid,
        "FirstName": first,
        "LastName": last,
        "Email": email,
        "Phone": phone,
        "DateOfBirth": dob,
        "Gender": random.choice(["Male", "Female", "Non-Binary"]),
        "City": fake.city(),
        "Country": random.choice(["United States", "Canada", "United Kingdom", "Germany"]),
        "RegistrationDate": reg_date,
        "CustomerStatus": "Active" if random.random() > 0.05 else "Inactive"
    })

# =============================================================================
# 5. PRODUCTS (280 Rows)
# =============================================================================
products = []
for pid in range(1, NUM_PRODUCTS + 1):
    cat_id = random.randint(1, NUM_CATEGORIES)
    sup_id = random.randint(1, NUM_SUPPLIERS)
    cost = round(random.uniform(10.0, 800.0), 2)
    price = round(cost * random.uniform(1.20, 1.60), 2)
    
    rand_st = random.random()
    if rand_st < 0.08:
        status, stock = "Discontinued", 0
    elif rand_st < 0.16:
        status, stock = "Out of Stock", 0
    else:
        status, stock = "Active", random.randint(10, 500)
        
    products.append({
        "ProductID": pid,
        "ProductName": f"{fake.color_name().capitalize()} {fake.word().capitalize()} {pid}",
        "CategoryID": cat_id,
        "SupplierID": sup_id,
        "Price": price,
        "Cost": cost,
        "StockQuantity": stock,
        "ProductStatus": status
    })

# =============================================================================
# 6. TRANSACTIONAL POOLS & WEIGHTING SETUP
# =============================================================================

# Customers Who Never Order (15% = 270 customers)
purchasing_customers = list(range(1, 1531))

# Customer Order Frequency Skew
# Customers are assigned different purchase propensities rather than fixed order counts.
low_frequency = purchasing_customers[:765]
medium_frequency = purchasing_customers[765:1346]
high_frequency = purchasing_customers[1346:]
customer_pool = (low_frequency * 1) + (medium_frequency * 3) + (high_frequency * 10)

# Product Sales Skew
# Top 20% of selling products receive substantially higher selection probability.
selling_products = products[:258] # Products 259-280 never sell
top_prods = selling_products[:52]
other_prods = selling_products[52:]
product_pool = (top_prods * 16) + (other_prods * 1)

orders, order_details, payments, shipments, returns = [], [], [], [], []

od_counter = 1
shipment_counter = 1
payment_counter = 1
return_counter = 1

month_weights = {1: 0.7, 2: 0.7, 3: 0.9, 4: 0.9, 5: 1.0, 6: 1.0, 7: 1.4, 8: 1.0, 9: 1.0, 10: 1.1, 11: 2.2, 12: 2.2}

print("Generating Orders, Details, Payments, Shipments, and Returns (2023-2026 timeframe)...")

CUTOFF_DATE = datetime(2026, 9, 1, 23, 59, 59)

for oid in range(1, NUM_ORDERS + 1):
    cust_id = random.choice(customer_pool)
    cust_reg = datetime.strptime(customers[cust_id - 1]["RegistrationDate"], "%Y-%m-%d %H:%M:%S")
    
    # Generate OrderDate between 2023 and Sept 2026 after Customer Registration
    # Generate OrderDate between customer registration and cutoff date directly
    start_dt = max(cust_reg, datetime(2023, 1, 1))
    if start_dt >= CUTOFF_DATE:
        start_dt = CUTOFF_DATE - timedelta(days=30)
    
    delta_seconds = int((CUTOFF_DATE - start_dt).total_seconds())
    random_seconds = random.randint(0, max(0, delta_seconds))
    order_date_dt = start_dt + timedelta(seconds=random_seconds)

    order_date_str = order_date_dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # 80% automated (NULL EmployeeID), 20% manually processed by Active employees
    emp_id = "" if random.random() < 0.80 else str(random.choice(active_employee_ids))
    
    order_status = random.choices(
        ["Delivered", "Shipped", "Processing", "Pending", "Cancelled"],
        weights=[0.65, 0.12, 0.08, 0.08, 0.07]
    )[0]

    cust_ref = customers[cust_id - 1]
    orders.append({
        "OrderID": oid,
        "CustomerID": cust_id,
        "EmployeeID": emp_id,
        "OrderDate": order_date_str,
        "OrderStatus": order_status,
        "ShippingAddress": fake.street_address(),
        "ShippingCity": cust_ref["City"],
        "ShippingCountry": cust_ref["Country"]
    })

    # Shipments Setup
    act_del_dt = None
    if order_status in ["Shipped", "Delivered"]:
        ship_date_dt = order_date_dt + timedelta(days=random.randint(1, 2))
        ship_date_str = ship_date_dt.strftime("%Y-%m-%d %H:%M:%S")
        est_del_str = (ship_date_dt + timedelta(days=4)).strftime("%Y-%m-%d")
        
        if order_status == "Delivered":
            act_del_dt = ship_date_dt + timedelta(days=random.randint(2, 5))
            act_del_str = act_del_dt.strftime("%Y-%m-%d")
            shipment_status = "Delivered"
        else:
            act_del_str = ""
            shipment_status = "In Transit"
            
        shipments.append({
            "ShipmentID": shipment_counter,
            "OrderID": oid,
            "ShipmentDate": ship_date_str,
            "EstimatedDeliveryDate": est_del_str,
            "ActualDeliveryDate": act_del_str,
            "ShippingMethod": random.choice(["Standard Ground", "Express Courier", "Next-Day Air"]),
            "TrackingNumber": f"TRK-{oid}-{shipment_counter}",
            "ShipmentStatus": shipment_status
        })
        shipment_counter += 1

    # OrderDetails Target Scale (~2.25 line items per order -> ~30,375 details)
    num_items = random.choices([1, 2, 3, 4, 5], weights=[0.30, 0.35, 0.20, 0.10, 0.05])[0]
    
    # Sample distinct products per order
    chosen_prods = []
    while len(chosen_prods) < num_items:
        candidate = random.choice(product_pool)
        if candidate["ProductID"] not in [p["ProductID"] for p in chosen_prods]:
            chosen_prods.append(candidate)
    
    order_total = 0.0

    for prod in chosen_prods:
        qty = random.choices([1, 2, 3, 4, 5], weights=[0.60, 0.25, 0.10, 0.03, 0.02])[0]
        unit_price = prod["Price"]
        discount = random.choices([0.00, 5.00, 10.00, 15.00, 20.00], weights=[0.70, 0.10, 0.10, 0.05, 0.05])[0]
        
        line_total = (unit_price * qty) * (1.0 - (discount / 100.0))
        order_total += line_total
        
        od_id = od_counter
        order_details.append({
            "OrderDetailID": od_id,
            "OrderID": oid,
            "ProductID": prod["ProductID"],
            "Quantity": qty,
            "UnitPrice": unit_price,
            "Discount": discount
        })
        od_counter += 1

        # Returns (Delivered orders only; ~5.0% probability per delivered line item -> approximately 1,000 returns)
        if order_status == "Delivered" and act_del_dt is not None and random.random() < 0.05:
            return_qty = random.randint(1, qty)
            return_date = (act_del_dt + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d %H:%M:%S")
            returns.append({
                "ReturnID": return_counter,
                "OrderDetailID": od_id,
                "ReturnDate": return_date,
                "ReturnQuantity": return_qty,
                "ReturnReason": random.choice(["Defective", "Changed Mind", "Incorrect Item", "Late Arrival"]),
                "ReturnStatus": random.choice(["Requested", "Approved", "Rejected", "Completed"])
            })
            return_counter += 1

    # Payments
    pay_method = random.choice(["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash on Delivery"])
    if order_status == "Cancelled":
        pay_status = random.choice(["Failed", "Refunded"])
    elif order_status in ["Pending", "Processing"]:
        pay_status = random.choice(["Completed", "Pending"])
    else:
        pay_status = "Completed"

    pay_date = (order_date_dt + timedelta(minutes=random.randint(1, 10))).strftime("%Y-%m-%d %H:%M:%S")
    tx_ref = "" if pay_status in ["Failed", "Pending"] else f"TXN-{oid}-{payment_counter}"

    payments.append({
        "PaymentID": payment_counter,
        "OrderID": oid,
        "PaymentDate": pay_date,
        "PaymentMethod": pay_method,
        "PaymentAmount": round(order_total, 2),
        "PaymentStatus": pay_status,
        "TransactionReference": tx_ref
    })
    payment_counter += 1

# =============================================================================
# 7. COMPREHENSIVE VALIDATION ENGINE
# =============================================================================

print("\nRunning Exhaustive Data & DDL Constraint Validation Checks...")

def validate_all():
    errors = []
    
    # 1. Primary Key Uniqueness
    for name, dataset, pk in [
        ("Categories", categories, "CategoryID"), ("Suppliers", suppliers, "SupplierID"),
        ("Employees", employees, "EmployeeID"), ("Customers", customers, "CustomerID"),
        ("Products", products, "ProductID"), ("Orders", orders, "OrderID"),
        ("OrderDetails", order_details, "OrderDetailID"), ("Payments", payments, "PaymentID"),
        ("Shipments", shipments, "ShipmentID"), ("Returns", returns, "ReturnID")
    ]:
        pks = [r[pk] for r in dataset]
        if len(pks) != len(set(pks)):
            errors.append(f"PK Error: Duplicate Primary Key in {name}")

    # 2. UNIQUE Constraints
    cust_emails = [c["Email"] for c in customers]
    if len(cust_emails) != len(set(cust_emails)): errors.append("UQ Error: Duplicate Customer Email")
    
    emp_emails = [e["Email"] for e in employees]
    if len(emp_emails) != len(set(emp_emails)): errors.append("UQ Error: Duplicate Employee Email")
    
    sup_emails = [s["ContactEmail"] for s in suppliers]
    if len(sup_emails) != len(set(sup_emails)): errors.append("UQ Error: Duplicate Supplier Email")
    
    tracking_nums = [s["TrackingNumber"] for s in shipments if s["TrackingNumber"] != ""]
    if len(tracking_nums) != len(set(tracking_nums)): errors.append("UQ Error: Duplicate Tracking Number")

    # 3. Foreign Key Integrity
    cust_ids = set(c["CustomerID"] for c in customers)
    emp_ids = set(e["EmployeeID"] for e in employees)
    prod_ids = set(p["ProductID"] for p in products)
    order_ids = set(o["OrderID"] for o in orders)
    od_ids = set(od["OrderDetailID"] for od in order_details)
    order_detail_quantities = {od["OrderDetailID"]: od["Quantity"] for od in order_details}

    for o in orders:
        if o["CustomerID"] not in cust_ids: errors.append(f"FK Error: Order {o['OrderID']} invalid CustomerID")
        if o["EmployeeID"] != "" and int(o["EmployeeID"]) not in emp_ids: errors.append(f"FK Error: Order {o['OrderID']} invalid EmployeeID")

    for p in payments:
        if p["OrderID"] not in order_ids: errors.append(f"FK Error: Payment {p['PaymentID']} invalid OrderID")

    for s in shipments:
        if s["OrderID"] not in order_ids: errors.append(f"FK Error: Shipment {s['ShipmentID']} invalid OrderID")

    for r in returns:
        if r["OrderDetailID"] not in od_ids:
            errors.append(f"FK Error: Return {r['ReturnID']} invalid OrderDetailID")
        elif r["ReturnQuantity"] > order_detail_quantities[r["OrderDetailID"]]:
            errors.append(f"Business Error: Return {r['ReturnID']} exceeds purchased quantity")

    # 4. CHECK Constraints & Data Bounds Validation
    for c in categories:
        if c["CategoryStatus"] not in ['Active', 'Inactive']: errors.append("CHECK Error: CategoryStatus invalid")

    for p in products:
        if p["Price"] <= 0: errors.append(f"CHECK Error: Product {p['ProductID']} Price <= 0")
        if p["Cost"] < 0 or p["Cost"] >= p["Price"]: errors.append(f"CHECK Error: Product {p['ProductID']} invalid Cost/Price")
        if p["StockQuantity"] < 0: errors.append(f"CHECK Error: Product {p['ProductID']} Stock < 0")
        if p["ProductStatus"] not in ['Active', 'Out of Stock', 'Discontinued']: errors.append("CHECK Error: ProductStatus invalid")

    for e in employees:
        if e["EmployeeStatus"] not in ['Active', 'Inactive']: errors.append("CHECK Error: EmployeeStatus invalid")

    for o in orders:
        if o["OrderStatus"] not in ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']: errors.append("CHECK Error: OrderStatus invalid")

    for od in order_details:
        if od["Quantity"] <= 0: errors.append("CHECK Error: Quantity <= 0")
        if od["UnitPrice"] <= 0: errors.append("CHECK Error: UnitPrice <= 0")
        if not (0 <= od["Discount"] <= 100): errors.append("CHECK Error: Discount out of bounds")

    for r in returns:
        if r["ReturnQuantity"] <= 0: errors.append("CHECK Error: ReturnQuantity <= 0")
        if r["ReturnStatus"] not in ['Requested', 'Approved', 'Rejected', 'Completed']: errors.append("CHECK Error: ReturnStatus invalid")

    for pay in payments:
        if pay["PaymentAmount"] <= 0: errors.append("CHECK Error: PaymentAmount <= 0")
        if pay["PaymentMethod"] not in ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery']: errors.append("CHECK Error: PaymentMethod invalid")
        if pay["PaymentStatus"] not in ['Pending', 'Completed', 'Failed', 'Refunded']: errors.append("CHECK Error: PaymentStatus invalid")

    for sh in shipments:
        if sh["ShipmentStatus"] not in ['Pending', 'Shipped', 'In Transit', 'Delivered', 'Cancelled']: errors.append("CHECK Error: ShipmentStatus invalid")

    # Output Summary Counts
    print(f"  Categories Rows:   {len(categories)}")
    print(f"  Suppliers Rows:    {len(suppliers)}")
    print(f"  Employees Rows:    {len(employees)}")
    print(f"  Customers Rows:    {len(customers)}")
    print(f"  Products Rows:     {len(products)}")
    print(f"  Orders Rows:       {len(orders)}")
    print(f"  OrderDetails Rows: {len(order_details)}")
    print(f"  Payments Rows:     {len(payments)}")
    print(f"  Shipments Rows:    {len(shipments)}")
    print(f"  Returns Rows:      {len(returns)}")

    if errors:
        print("\nValidation Failed:")
        for err in set(errors): print(f"  - {err}")
        return False
    else:
        print("\nALL DDL CONSTRAINTS & BUSINESS VALIDATION CHECKS PASSED PERFECTLY!")
        return True

if not validate_all():
    exit(1)

# =============================================================================
# 8. CSV EXPORT
# =============================================================================
os.makedirs(OUTPUT_DIR, exist_ok=True)

dataset_mapping = {
    "categories.csv": categories,
    "suppliers.csv": suppliers,
    "employees.csv": employees,
    "customers.csv": customers,
    "products.csv": products,
    "orders.csv": orders,
    "order_details.csv": order_details,
    "payments.csv": payments,
    "shipments.csv": shipments,
    "returns.csv": returns,
}

print(f"\nWriting clean CSV files to '/{OUTPUT_DIR}'...")
for filename, rows in dataset_mapping.items():
    filepath = os.path.join(OUTPUT_DIR, filename)
    headers = list(rows[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

print("MarketFlow data generation complete.")