import csv
import os
import random
import sys
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker with seed for full reproducibility
fake = Faker()
Faker.seed(42)
random.seed(42)

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

print("==================================================================")
print("  MARKETFLOW ENTERPRISE DATA GENERATOR & VALIDATION PIPELINE")
print("==================================================================\n")

# =============================================================================
# CONFIGURATION & PARAMETERS
# =============================================================================
NUM_CUSTOMERS = 2500
NUM_BUYING_CUSTOMERS = 2200  # Exactly 300 customers never order

NUM_CATEGORIES = 15
NUM_SUPPLIERS = 20

NUM_PRODUCTS = 400
NUM_SOLD_PRODUCTS = 350      # Exactly 50 products never sell

NUM_EMPLOYEES = 50
NUM_ORDERS = 20000

# Order Date Horizon
START_DATE = datetime(2023, 1, 1, 0, 0, 0)
END_DATE = datetime(2026, 8, 31, 23, 59, 59)

# Monthly Seasonality Weights (Jan - Dec)
MONTH_WEIGHTS = [7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 14, 16]

# Allowed Vocabularies
ALLOWED_ORDER_STATUS = {"Delivered", "Shipped", "Processing", "Pending", "Cancelled"}
ALLOWED_PAYMENT_STATUS = {"Completed", "Pending", "Failed", "Refunded"}
ALLOWED_PAYMENT_METHODS = {'Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery'}
ALLOWED_SHIPMENT_STATUS = {"Delivered", "In Transit", "Pending", "Cancelled"}
ALLOWED_SHIPPING_METHODS = {'Standard Ground', 'Express Courier', 'Next-Day Air'}
ALLOWED_RETURN_STATUS = {"Requested", "Approved", "Rejected", "Completed"}

ALLOWED_CUSTOMER_STATUS = {"Active", "Inactive"}
ALLOWED_EMPLOYEE_STATUS = {"Active", "Inactive"}
ALLOWED_PRODUCT_STATUS = {"Active", "Out of Stock", "Discontinued"}
ALLOWED_CATEGORY_STATUS = {"Active", "Inactive"}

def make_dirty_text(text, probability=0.15):
    """Helper to inject whitespace or casing variations for text normalization exercises."""
    if random.random() < probability:
        choices = [
            f" {text.lower()}",       # " germany"
            text.upper(),             # "GERMANY"
            f"{text.capitalize()} ",  # "Germany "
            text.lower()              # "germany"
        ]
        return random.choice(choices)
    return text

def generate_seasonal_date(c_reg_date):
    """Generates an order date honoring registration date and monthly seasonality."""
    while True:
        year = random.randint(c_reg_date.year, END_DATE.year)
        month = random.choices(range(1, 13), weights=MONTH_WEIGHTS, k=1)[0]
        
        # Days in month logic
        if month in [1, 3, 5, 7, 8, 10, 12]:
            max_days = 31
        elif month in [4, 6, 9, 11]:
            max_days = 30
        else:
            max_days = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
            
        day = random.randint(1, max_days)
        hour = random.randint(7, 22)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        candidate_date = datetime(year, month, day, hour, minute, second)
        
        if c_reg_date <= candidate_date <= END_DATE:
            return candidate_date

# =============================================================================
# 1. CATEGORIES & SUPPLIERS
# =============================================================================
category_names = [
    "Laptops & Computers", "Monitors & Displays", "PC Components", "Storage & Networking",
    "Audio & Headphones", "Smart Home Devices", "Wearables & Fitness", "Gaming & Consoles",
    "Keyboards & Mice", "Mobile & Tablets", "Cameras & Video", "Cables & Adapters",
    "Printers & Supplies", "Power & Batteries", "Office Tech Accessories"
]

categories = []
for cid, name in enumerate(category_names, 1):
    categories.append({
        "CategoryID": cid,
        "CategoryName": name,
        "Description": fake.sentence(),
        "CategoryStatus": "Active" if random.random() > 0.10 else "Inactive"
    })

suppliers = []
for sid in range(1, NUM_SUPPLIERS + 1):
    email = f"contact_{sid}@{fake.domain_name()}"
    suppliers.append({
        "SupplierID": sid,
        "SupplierName": fake.company(),
        "ContactEmail": email,
        "Country": make_dirty_text(random.choice(["Germany", "USA", "Albania", "UK", "Japan"]), probability=0.25)
    })

# =============================================================================
# 2. CUSTOMERS
# =============================================================================
customers = []
customer_reg_dates = {}

for cid in range(1, NUM_CUSTOMERS + 1):
    gender = random.choice(["Male", "Female", None]) if random.random() > 0.15 else None
    phone = fake.phone_number()[:25] if random.random() > 0.20 else None
    city = fake.city() if random.random() > 0.10 else None
    country = make_dirty_text(random.choice(["Germany", "Kosovo", "Albania", "USA", "Switzerland"]), probability=0.20) if random.random() > 0.05 else None

    reg_date = fake.date_time_between(start_date=START_DATE, end_date=END_DATE - timedelta(days=30))
    customer_reg_dates[cid] = reg_date

    customers.append({
        "CustomerID": cid,
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
        "Email": f"cust_{cid}_{fake.unique.email()}",
        "Phone": phone,
        "DateOfBirth": fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
        "Gender": gender,
        "City": city,
        "Country": country,
        "RegistrationDate": reg_date.isoformat(),
        "CustomerStatus": "Active" if random.random() > 0.12 else "Inactive"
    })

# =============================================================================
# 3. EMPLOYEES & ACTIVE FILTERING
# =============================================================================
employees = []
active_employee_ids = []
departments = ["Sales", "Logistics", "Customer Support", "IT"]

for eid in range(1, NUM_EMPLOYEES + 1):
    emp_status = "Active" if random.random() > 0.08 else "Inactive"
    if emp_status == "Active":
        active_employee_ids.append(eid)

    employees.append({
        "EmployeeID": eid,
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
        "Email": f"emp_{eid}@{fake.domain_name()}",
        "Phone": fake.phone_number()[:25] if random.random() > 0.25 else None,
        "Department": random.choice(departments),
        "HireDate": fake.date_between(start_date=datetime(2020, 1, 1), end_date=datetime(2025, 1, 1)).isoformat(),
        "EmployeeStatus": emp_status
    })

# =============================================================================
# 4. PRODUCTS & BEHAVIORAL WEIGHTING
# =============================================================================
PRODUCT_TEMPLATES = {
    1: ("VoltBook Pro 14", "Apex Workstation 16", "Titan Desktop PC", "FlexBook Air"),
    2: ("VisionMax 27\"", "UltraView 4K 32\"", "ProDisplay HD 24\"", "GamingView 144Hz"),
    3: ("CoreStrike i7 CPU", "Vortex RTX GPU", "Prime Z690 Motherboard", "PowerCore 750W"),
    4: ("FastStore NVMe SSD", "CloudLink Wi-Fi 6 Router", "DataVault External HD", "SpeedPro NAS"),
    5: ("SoundWave Pro Headphones", "SoundWave Mini Speaker", "AudioPulse Wireless Earbuds", "StudioBass Soundbar"),
    6: ("SmartHub Central", "SecureCam Outdoor 4K", "EcoGlow Smart Bulb", "SmartThermo V2"),
    7: ("PulseBand Fitness Tracker", "Chronos Smartwatch Pro", "FitActive GPS Watch", "PulseRing Sport"),
    8: ("GameBox X Console", "ProGrip Controller", "VRVerse Headset", "ArcadeFight Stick"),
    9: ("MechType RGB Keyboard", "PrecisionClick Mouse", "ErgoPad Wrist Rest", "MacroDeck 12-Key"),
    10: ("TechNova X1 Smartphone", "TabPro 10.5 Tablet", "TechNova Lite 5G", "FoldTech Duo"),
    11: ("ProLens Mirrorless Camera", "ClearStream 4K Webcam", "FlexiPod Tripod", "CineLight Ring LED"),
    12: ("UltraLink HDMI Cable", "MultiHub USB-C Adapter", "PowerSync Braided Cable", "DisplayPort Adapter"),
    13: ("LaserJet Pro Printer", "ColorInk XL Cartridge", "EcoPaper 500-Sheet Ream", "ScanMaster Scanner"),
    14: ("PowerMax 20K Power Bank", "VoltGuard UPS Battery", "FastCharge 65W Plug", "SolarPower Pad"),
    15: ("ErgoArm Dual Mount", "ProCarry Laptop Bag", "DeskFlex Leather Mat", "CableClean Tray")
}

products = []
for pid in range(1, NUM_PRODUCTS + 1):
    cat_id = random.randint(1, NUM_CATEGORIES)
    sup_id = random.randint(1, NUM_SUPPLIERS)
    
    base_name = random.choice(PRODUCT_TEMPLATES[cat_id])
    product_name = f"{base_name} (v{pid})"
    
    cost = round(random.uniform(5.0, 700.0), 2)
    price = round(cost * random.uniform(1.25, 1.75), 2)
    
    stock = 0 if random.random() < 0.15 else random.randint(10, 500)
    status = "Discontinued" if stock == 0 and random.random() < 0.5 else ("Out of Stock" if stock == 0 else "Active")
    
    products.append({
        "ProductID": pid,
        "ProductName": product_name,
        "CategoryID": cat_id,
        "SupplierID": sup_id,
        "Price": price,
        "Cost": cost,
        "StockQuantity": stock,
        "ProductStatus": status
    })

sold_product_ids = list(range(1, NUM_SOLD_PRODUCTS + 1))
product_weights = [100 if pid <= 30 else (20 if pid <= 150 else 3) for pid in sold_product_ids]

buying_customer_ids = list(range(1, NUM_BUYING_CUSTOMERS + 1))
customer_weights = [50 if cid <= 100 else (10 if cid <= 600 else 2) for cid in buying_customer_ids]

# =============================================================================
# 5. ORDERS, PAYMENTS, & SHIPMENTS
# =============================================================================
orders = []
payments = []
shipments = []

order_status_choices = ["Delivered", "Shipped", "Processing", "Pending", "Cancelled"]
order_status_weights = [0.70, 0.08, 0.07, 0.07, 0.08]

payment_methods = list(ALLOWED_PAYMENT_METHODS)
shipping_methods = list(ALLOWED_SHIPPING_METHODS)

# Step A: Guarantee exactly 1 order for every buying customer (1 to 2,200)
order_customer_assignments = list(buying_customer_ids)

# Step B: Distribute remaining orders via weighted sampling
remaining_orders_count = NUM_ORDERS - NUM_BUYING_CUSTOMERS
sampled_customers = random.choices(buying_customer_ids, weights=customer_weights, k=remaining_orders_count)
order_customer_assignments.extend(sampled_customers)

# Step C: Shuffle to interleave order sequence
random.shuffle(order_customer_assignments)

tracking_numbers_used = set()

for oid, cid in enumerate(order_customer_assignments, 1):
    eid = random.choice(active_employee_ids) if random.random() > 0.30 else None
    
    c_reg_date = customer_reg_dates[cid]
    order_date = generate_seasonal_date(c_reg_date)

    o_status = random.choices(order_status_choices, weights=order_status_weights, k=1)[0]
    
    orders.append({
        "OrderID": oid,
        "CustomerID": cid,
        "EmployeeID": eid,
        "OrderDate": order_date.isoformat(),
        "OrderStatus": o_status,
        "ShippingAddress": fake.street_address(),
        "ShippingCity": fake.city(),
        "ShippingCountry": make_dirty_text(random.choice(["Germany", "Kosovo", "Albania", "USA", "Switzerland"]), probability=0.15)
    })

    # Payment Status Logic
    if o_status in ["Delivered", "Shipped"]:
        p_status = "Completed"
    elif o_status == "Cancelled":
        p_status = "Failed" if random.random() < 0.85 else "Refunded"
    else:
        p_status = "Pending" if random.random() < 0.90 else "Completed"

    payments.append({
        "PaymentID": oid,
        "OrderID": oid,
        "PaymentDate": (order_date + timedelta(minutes=random.randint(1, 30))).isoformat(),
        "PaymentMethod": random.choice(payment_methods),
        "PaymentAmount": 0.0,  # Calculated after OrderDetails
        "PaymentStatus": p_status,
        "TransactionReference": f"TXN-{fake.uuid4()[:8].upper()}" if p_status in ["Completed", "Refunded"] else None
    })
    
    # Shipment Timeline Logic
    if o_status in ["Delivered", "Shipped"]:
        ship_date = order_date + timedelta(days=random.randint(1, 2))
        est_delivery = ship_date + timedelta(days=random.randint(3, 7))
        act_delivery = est_delivery - timedelta(days=random.randint(0, 2)) if o_status == "Delivered" else None
        s_status = "Delivered" if o_status == "Delivered" else "In Transit"
        
        while True:
            trk = f"TRK-{fake.uuid4()[:10].upper()}"
            if trk not in tracking_numbers_used:
                tracking_numbers_used.add(trk)
                break
    else:
        ship_date, est_delivery, act_delivery = None, None, None
        s_status = "Pending" if o_status != "Cancelled" else "Cancelled"
        trk = None
        
    shipments.append({
        "ShipmentID": oid,
        "OrderID": oid,
        "ShipmentDate": ship_date.isoformat() if ship_date else None,
        "EstimatedDeliveryDate": est_delivery.date().isoformat() if est_delivery else None,
        "ActualDeliveryDate": act_delivery.date().isoformat() if act_delivery else None,
        "ShippingMethod": random.choice(shipping_methods),
        "TrackingNumber": trk,
        "ShipmentStatus": s_status
    })

shipment_objects = {s["OrderID"]: s for s in shipments}

# =============================================================================
# 6. ORDER DETAILS & RETURNS
# =============================================================================
order_details = []
returns = []

od_id_counter = 1
return_id_counter = 1

return_reasons = ["Defective Item", "Wrong Size/Color", "Late Delivery", "Buyer Remorse", "Not as Described"]
return_statuses = list(ALLOWED_RETURN_STATUS)

sold_product_assignments = list(sold_product_ids)

for o in orders:
    oid = o["OrderID"]
    o_status = o["OrderStatus"]
    
    num_items = random.randint(1, 5)
    
    selected_products = []
    while sold_product_assignments and len(selected_products) < num_items:
        p_needed = sold_product_assignments.pop()
        selected_products.append(p_needed)
        
    if len(selected_products) < num_items:
        pool = [p for p in sold_product_ids if p not in selected_products]
        weights = [product_weights[p - 1] for p in pool]
        needed = num_items - len(selected_products)
        for _ in range(needed):
            chosen = random.choices(pool, weights=weights, k=1)[0]
            idx = pool.index(chosen)
            pool.pop(idx)
            weights.pop(idx)
            selected_products.append(chosen)

    order_total = 0.0
    
    for pid in selected_products:
        p = products[pid - 1]
        qty = random.randint(1, 4)
        unit_price = p["Price"]
        discount = random.choice([0.0, 0.0, 0.0, 5.0, 10.0, 15.0])
        
        line_total = (unit_price * (1 - discount / 100.0)) * qty
        order_total += line_total
        
        order_details.append({
            "OrderDetailID": od_id_counter,
            "OrderID": oid,
            "ProductID": pid,
            "Quantity": qty,
            "UnitPrice": unit_price,
            "Discount": discount
        })
        
        # Return Date logically chained: ReturnDate >= ActualDeliveryDate
        if o_status == "Delivered" and random.random() < 0.05:
            act_del_str = shipment_objects[oid]["ActualDeliveryDate"]
            act_del_dt = datetime.fromisoformat(act_del_str)
            return_dt = act_del_dt + timedelta(days=random.randint(1, 14))
            
            ret_qty = random.randint(1, qty)
            returns.append({
                "ReturnID": return_id_counter,
                "OrderDetailID": od_id_counter,
                "ReturnDate": return_dt.isoformat(),
                "ReturnQuantity": ret_qty,
                "ReturnReason": random.choice(return_reasons) if random.random() > 0.15 else None,
                "ReturnStatus": random.choice(return_statuses)
            })
            return_id_counter += 1
            
        od_id_counter += 1
        
    payments[oid - 1]["PaymentAmount"] = round(order_total, 2)

# =============================================================================
# 7. AUTOMATED PRE-EXPORT VALIDATION ENGINE
# =============================================================================
print("[Running Comprehensive Validation Engine]...")

def run_validation():
    errors = []

    # 1. Foreign Key Checks
    valid_category_ids = set(c["CategoryID"] for c in categories)
    valid_supplier_ids = set(s["SupplierID"] for s in suppliers)
    valid_customer_ids = set(c["CustomerID"] for c in customers)
    valid_employee_ids = set(e["EmployeeID"] for e in employees)
    valid_product_ids = set(p["ProductID"] for p in products)
    valid_order_ids = set(o["OrderID"] for o in orders)
    valid_order_detail_ids = set(od["OrderDetailID"] for od in order_details)

    for p in products:
        if p["CategoryID"] not in valid_category_ids:
            errors.append(f"FK Error: Product {p['ProductID']} references invalid CategoryID {p['CategoryID']}")
        if p["SupplierID"] not in valid_supplier_ids:
            errors.append(f"FK Error: Product {p['ProductID']} references invalid SupplierID {p['SupplierID']}")

    for o in orders:
        if o["CustomerID"] not in valid_customer_ids:
            errors.append(f"FK Error: Order {o['OrderID']} references invalid CustomerID {o['CustomerID']}")
        if o["EmployeeID"] is not None and o["EmployeeID"] not in valid_employee_ids:
            errors.append(f"FK Error: Order {o['OrderID']} references invalid EmployeeID {o['EmployeeID']}")

    for od in order_details:
        if od["OrderID"] not in valid_order_ids:
            errors.append(f"FK Error: OrderDetail {od['OrderDetailID']} references invalid OrderID {od['OrderID']}")
        if od["ProductID"] not in valid_product_ids:
            errors.append(f"FK Error: OrderDetail {od['OrderDetailID']} references invalid ProductID {od['ProductID']}")

    for p in payments:
        if p["OrderID"] not in valid_order_ids:
            errors.append(f"FK Error: Payment {p['PaymentID']} references invalid OrderID {p['OrderID']}")

    for s in shipments:
        if s["OrderID"] not in valid_order_ids:
            errors.append(f"FK Error: Shipment {s['ShipmentID']} references invalid OrderID {s['OrderID']}")

    for r in returns:
        if r["OrderDetailID"] not in valid_order_detail_ids:
            errors.append(f"FK Error: Return {r['ReturnID']} references invalid OrderDetailID {r['OrderDetailID']}")

    # 2. Vocabulary Checks across all Status fields
    for c in categories:
        if c["CategoryStatus"] not in ALLOWED_CATEGORY_STATUS:
            errors.append(f"Vocab Error: Category {c['CategoryID']} invalid status '{c['CategoryStatus']}'")

    for c in customers:
        if c["CustomerStatus"] not in ALLOWED_CUSTOMER_STATUS:
            errors.append(f"Vocab Error: Customer {c['CustomerID']} invalid status '{c['CustomerStatus']}'")

    for e in employees:
        if e["EmployeeStatus"] not in ALLOWED_EMPLOYEE_STATUS:
            errors.append(f"Vocab Error: Employee {e['EmployeeID']} invalid status '{e['EmployeeStatus']}'")

    for p in products:
        if p["ProductStatus"] not in ALLOWED_PRODUCT_STATUS:
            errors.append(f"Vocab Error: Product {p['ProductID']} invalid status '{p['ProductStatus']}'")

    for o in orders:
        if o["OrderStatus"] not in ALLOWED_ORDER_STATUS:
            errors.append(f"Vocab Error: Order {o['OrderID']} invalid status '{o['OrderStatus']}'")
            
    for p in payments:
        if p["PaymentStatus"] not in ALLOWED_PAYMENT_STATUS:
            errors.append(f"Vocab Error: Payment {p['PaymentID']} invalid status '{p['PaymentStatus']}'")
        if p["PaymentMethod"] not in ALLOWED_PAYMENT_METHODS:
            errors.append(f"Vocab Error: Payment {p['PaymentID']} invalid method '{p['PaymentMethod']}'")

    for s in shipments:
        if s["ShipmentStatus"] not in ALLOWED_SHIPMENT_STATUS:
            errors.append(f"Vocab Error: Shipment {s['ShipmentID']} invalid status '{s['ShipmentStatus']}'")
        if s["ShippingMethod"] not in ALLOWED_SHIPPING_METHODS:
            errors.append(f"Vocab Error: Shipment {s['ShipmentID']} invalid method '{s['ShippingMethod']}'")

    for r in returns:
        if r["ReturnStatus"] not in ALLOWED_RETURN_STATUS:
            errors.append(f"Vocab Error: Return {r['ReturnID']} invalid status '{r['ReturnStatus']}'")

    # 3. Numeric Business Rules Validation
    for p in products:
        if p["Price"] <= 0:
            errors.append(f"Numeric Error: Product {p['ProductID']} Price <= 0")
        if p["Cost"] <= 0:
            errors.append(f"Numeric Error: Product {p['ProductID']} Cost <= 0")
        if p["Cost"] > p["Price"]:
            errors.append(f"Numeric Error: Product {p['ProductID']} Cost > Price")
        if p["StockQuantity"] < 0:
            errors.append(f"Numeric Error: Product {p['ProductID']} StockQuantity < 0")

    for od in order_details:
        if od["Quantity"] <= 0:
            errors.append(f"Numeric Error: OrderDetail {od['OrderDetailID']} Quantity <= 0")
        if not (0.0 <= od["Discount"] <= 100.0):
            errors.append(f"Numeric Error: OrderDetail {od['OrderDetailID']} Discount out of range [0, 100]")

    for r in returns:
        if r["ReturnQuantity"] <= 0:
            errors.append(f"Numeric Error: Return {r['ReturnID']} ReturnQuantity <= 0")

    # 4. Uniqueness Checks
    cust_emails = [c["Email"] for c in customers]
    if len(cust_emails) != len(set(cust_emails)):
        errors.append("Uniqueness Error: Duplicate emails found in Customers!")

    emp_emails = [e["Email"] for e in employees]
    if len(emp_emails) != len(set(emp_emails)):
        errors.append("Uniqueness Error: Duplicate emails found in Employees!")

    sup_emails = [s["ContactEmail"] for s in suppliers]
    if len(sup_emails) != len(set(sup_emails)):
        errors.append("Uniqueness Error: Duplicate contact emails found in Suppliers!")

    trackings = [s["TrackingNumber"] for s in shipments if s["TrackingNumber"] is not None]
    if len(trackings) != len(set(trackings)):
        errors.append("Uniqueness Error: Duplicate TrackingNumbers found in Shipments!")

    # 5. Entity Population & Behavior Checks
    if len(customers) != NUM_CUSTOMERS:
        errors.append(f"Customer count expected {NUM_CUSTOMERS}, got {len(customers)}")
    ordering_custs = set(o["CustomerID"] for o in orders)
    if len(ordering_custs) != NUM_BUYING_CUSTOMERS:
        errors.append(f"Buying customers count expected exactly {NUM_BUYING_CUSTOMERS}, got {len(ordering_custs)}")

    if len(products) != NUM_PRODUCTS:
        errors.append(f"Product count expected {NUM_PRODUCTS}, got {len(products)}")
    sold_prods = set(od["ProductID"] for od in order_details)
    if len(sold_prods) != NUM_SOLD_PRODUCTS:
        errors.append(f"Sold products count expected exactly {NUM_SOLD_PRODUCTS}, got {len(sold_prods)}")

    # 6. Payment Amount & Calculation Reconciliation
    calculated_order_totals = {}
    for od in order_details:
        oid = od["OrderID"]
        line_total = (od["UnitPrice"] * (1.0 - od["Discount"] / 100.0)) * od["Quantity"]
        calculated_order_totals[oid] = calculated_order_totals.get(oid, 0.0) + line_total

    for p in payments:
        calc_tot = round(calculated_order_totals[p["OrderID"]], 2)
        if round(p["PaymentAmount"], 2) != calc_tot:
            errors.append(f"Calculation Error: Payment {p['PaymentID']} amount ({p['PaymentAmount']}) != Order total ({calc_tot})")

    # 7. Date Sequences & Chronology Validation
    cust_map = {c["CustomerID"]: datetime.fromisoformat(c["RegistrationDate"]) for c in customers}
    order_map = {o["OrderID"]: datetime.fromisoformat(o["OrderDate"]) for o in orders}

    for o in orders:
        c_reg = cust_map[o["CustomerID"]]
        o_date = datetime.fromisoformat(o["OrderDate"])
        if o_date < c_reg:
            errors.append(f"Date Error: Order {o['OrderID']} date ({o_date}) precedes Registration ({c_reg})")

    # Shipment Timeline Verification
    for s in shipments:
        oid = s["OrderID"]
        order_dt = order_map[oid]

        if s["ShipmentDate"]:
            ship_dt = datetime.fromisoformat(s["ShipmentDate"])
            if ship_dt < order_dt:
                errors.append(f"Date Error: Shipment {s['ShipmentID']} date ({ship_dt}) precedes Order date ({order_dt})")

            if s["EstimatedDeliveryDate"]:
                est_dt = datetime.fromisoformat(f"{s['EstimatedDeliveryDate']}T23:59:59")
                if est_dt < ship_dt:
                    errors.append(f"Date Error: Shipment {s['ShipmentID']} estimated delivery ({est_dt}) precedes Shipment date ({ship_dt})")

                if s["ActualDeliveryDate"]:
                    act_dt = datetime.fromisoformat(f"{s['ActualDeliveryDate']}T23:59:59")
                    if act_dt < ship_dt:
                        errors.append(f"Date Error: Shipment {s['ShipmentID']} actual delivery ({act_dt}) precedes Shipment date ({ship_dt})")

    # Return Timeline Verification
    od_map = {od["OrderDetailID"]: od for od in order_details}
    for r in returns:
        od = od_map[r["OrderDetailID"]]
        if r["ReturnQuantity"] > od["Quantity"]:
            errors.append(f"Return Error: Return {r['ReturnID']} quantity exceeds line item quantity")
        
        ship = shipment_objects[od["OrderID"]]
        if ship["ActualDeliveryDate"]:
            del_dt = datetime.fromisoformat(f"{ship['ActualDeliveryDate']}T00:00:00")
            ret_dt = datetime.fromisoformat(r["ReturnDate"])
            if ret_dt < del_dt:
                errors.append(f"Date Error: Return {r['ReturnID']} date ({ret_dt}) precedes Delivery Date ({del_dt})")

    # 8. Active Employee Constraint Check
    inactive_emp_ids = set(e["EmployeeID"] for e in employees if e["EmployeeStatus"] == "Inactive")
    for o in orders:
        if o["EmployeeID"] in inactive_emp_ids:
            errors.append(f"Constraint Error: Order {o['OrderID']} assigned to Inactive Employee {o['EmployeeID']}")

    # 9. Order Details Product Uniqueness Check
    od_pairs = set()
    for od in order_details:
        pair = (od["OrderID"], od["ProductID"])
        if pair in od_pairs:
            errors.append(f"Constraint Error: Duplicate Product {od['ProductID']} in Order {od['OrderID']}")
        od_pairs.add(pair)

    # 10. Shipment NULL Constraints Check
    for s in shipments:
        if s["ShipmentStatus"] == "Delivered" and not s["ActualDeliveryDate"]:
            errors.append(f"Constraint Error: Shipment {s['ShipmentID']} status Delivered but ActualDeliveryDate is NULL")
        if s["ShipmentStatus"] in ["Pending", "Cancelled"] and s["ShipmentDate"]:
            errors.append(f"Constraint Error: Shipment {s['ShipmentID']} status {s['ShipmentStatus']} has non-null ShipmentDate")

    if errors:
        print("\n❌ VALIDATION ENGINE FAILED WITH THE FOLLOWING ERRORS:")
        for err in errors[:15]:
            print(f"  - {err}")
        print("\nAborting CSV export.")
        sys.exit(1)
    
    print("✓ PASS: All foreign keys, vocabularies, numeric rules, date timelines, and behavioral constraints verified successfully!\n")

run_validation()

# =============================================================================
# 8. CSV EXPORT
# =============================================================================
def export_csv(filename, data, fieldnames):
    filepath = os.path.join("data", filename)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Exported {len(data):>6} rows -> {filepath}")

export_csv("categories.csv", categories, ["CategoryID", "CategoryName", "Description", "CategoryStatus"])
export_csv("suppliers.csv", suppliers, ["SupplierID", "SupplierName", "ContactEmail", "Country"])
export_csv("customers.csv", customers, ["CustomerID", "FirstName", "LastName", "Email", "Phone", "DateOfBirth", "Gender", "City", "Country", "RegistrationDate", "CustomerStatus"])
export_csv("employees.csv", employees, ["EmployeeID", "FirstName", "LastName", "Email", "Phone", "Department", "HireDate", "EmployeeStatus"])
export_csv("products.csv", products, ["ProductID", "ProductName", "CategoryID", "SupplierID", "Price", "Cost", "StockQuantity", "ProductStatus"])
export_csv("orders.csv", orders, ["OrderID", "CustomerID", "EmployeeID", "OrderDate", "OrderStatus", "ShippingAddress", "ShippingCity", "ShippingCountry"])
export_csv("order_details.csv", order_details, ["OrderDetailID", "OrderID", "ProductID", "Quantity", "UnitPrice", "Discount"])
export_csv("payments.csv", payments, ["PaymentID", "OrderID", "PaymentDate", "PaymentMethod", "PaymentAmount", "PaymentStatus", "TransactionReference"])
export_csv("shipments.csv", shipments, ["ShipmentID", "OrderID", "ShipmentDate", "EstimatedDeliveryDate", "ActualDeliveryDate", "ShippingMethod", "TrackingNumber", "ShipmentStatus"])
export_csv("returns.csv", returns, ["ReturnID", "OrderDetailID", "ReturnDate", "ReturnQuantity", "ReturnReason", "ReturnStatus"])

# =============================================================================
# 9. FINAL EXECUTION REPORT
# =============================================================================
print("\n==================================================================")
print("  MARKETFLOW GENERATION COMPLETE REPORT")
print("==================================================================")
print(f"• Total Customers Generated:    {len(customers)} (Exactly 300 never placed an order)")
print(f"• Total Products Generated:     {len(products)} (Exactly 50 never sold)")
print(f"• Total Active Employees:       {len(active_employee_ids)} of {NUM_EMPLOYEES}")
print(f"• Total Orders Generated:       {len(orders)}")
print(f"• Total Order Detail Lines:     {len(order_details)}")
print(f"• Total Returns Tracked:        {len(returns)}")
print("==================================================================\n")