# & "C:/Users/My Computer/AppData/Local/Microsoft/WindowsApps/python3.11.exe" -m streamlit run "c:\Users\My Computer\Documents\Important Stuff\School\College\Coding\Capstone - Streamlit\Capstone.py" --server.headless true --server.runOnSave true --server.allowRunOnSave true

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# Configure page to use wide layout
st.set_page_config(
    page_title="T-Shirt Printing Shop",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'orders' not in st.session_state:
    st.session_state.orders = [
        {
            "order_id": "ORD001", 
            "customer": "John Doe", 
            "email": "john@email.com",
            "phone": "123-456-7890",
            "items": [{"design_name": "Custom Design", "quantity": 5, "size": "L", "price": 1250}],
            "total": 1250,
            "status": "Designing", 
            "date": "2024-01-15"
        },
        {
            "order_id": "ORD002", 
            "customer": "Jane Smith", 
            "email": "jane@email.com",
            "phone": "123-456-7891",
            "items": [{"design_name": "White Shirt", "quantity": 3, "size": "M", "price": 750}],
            "total": 750,
            "status": "Printing", 
            "date": "2024-01-16"
        }
    ]

if 'completed_orders' not in st.session_state:
    st.session_state.completed_orders = [
        {
            "order_id": "ORD099", 
            "customer": "Alice Brown", 
            "items": [{"design_name": "Blue Shirt", "quantity": 2, "size": "S", "price": 500}],
            "total": 500,
            "date": "2024-01-10"
        }
    ]

# Prices for customers
pShirt = 250

# Materials cost
mShirt = 80
mInk = 20
mPackaging = 10
mTotal = mShirt + mInk + mPackaging

# Direct labor cost
lDesigner = 18000
lPrinter = 15000
lPacker = 12000
lTotal = lDesigner + lPrinter + lPacker

# Misc costs
electricity = 12
misc = 20

# Create tabs for different pages
tab1, tab2 = st.tabs(["Customer Dashboard", "Vendor Dashboard"])

with tab1:
    st.title("Place Your Order")
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    # Create main columns for better space utilization
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.subheader("Add Items to Cart")

        design_type = st.radio("Design Type", ["Choose from Templates", "Upload Custom Design"])

        if design_type == "Choose from Templates":
            st.write("Choose a template:")
            template_choice = st.radio("Select Template", ["White Shirt", "Black Shirt", "Blue Shirt"], horizontal=True)

            # Make images larger and use full width
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image("https://i5.walmartimages.com/seo/Men-Heavy-Cotton-Multi-Colors-T-Shirt-Color-White-Small-Size_3cc03e24-2c97-4eaf-b99a-99eea6bb9221.1604d1a89fc6a8669bdb1896f8dd8da3.jpeg", caption="White Shirt", use_container_width=True)
            with col2:
                st.image("https://i5.walmartimages.com/seo/Men-Heavy-Cotton-Multi-Colors-T-Shirt-Color-Tweed-Small-Size_c5a4f611-2789-4081-8901-e15983d6ac9d.129328f6e3d2ab4c61120daccd4599ed.jpeg", caption="Black Shirt", use_container_width=True)
            with col3:
                st.image("https://i5.walmartimages.com/seo/Men-Heavy-Cotton-Multi-Colors-T-Shirt-Color-Neon-Blue-Small-Size_114ac5d7-632b-4975-9006-f341620eedb7.fdff6c7b97b5c4fcea877b9ce35c1598.jpeg", caption="Blue Shirt", use_container_width=True)

            # Use columns for form inputs
            qty_col, size_col = st.columns(2)
            with qty_col:
                quantity = st.number_input("Number of Shirts", min_value=1, value=1, key="template_qty")
            with size_col:
                shirt_size = st.selectbox("Shirt Size", ["XS", "S", "M", "L", "XL", "XXL"], key="template_size")
            design_name = template_choice
        else:
            uploaded_file = st.file_uploader("Upload your design", type=['png', 'jpg', 'jpeg'])
            qty_col, size_col = st.columns(2)
            with qty_col:
                quantity = st.number_input("Number of Shirts", min_value=1, value=1, key="custom_qty")
            with size_col:
                shirt_size = st.selectbox("Shirt Size", ["XS", "S", "M", "L", "XL", "XXL"], key="custom_size")
            design_name = st.text_input("Design Name (optional)", key="custom_name")
            
        if st.button("Add to Cart", use_container_width=True):
            item = {
                "design_type": design_type,
                "design_name": design_name if design_name else ("Custom Design" if design_type == "Upload Custom Design" else template_choice),
                "quantity": quantity,
                "size": shirt_size,
                "price_per_item": pShirt,
                "total_price": quantity * pShirt
            }
            st.session_state.cart.append(item)
            st.success("Item added to cart!")
            st.rerun()
    
    with right_col:
        if st.session_state.cart:
            st.subheader("Shopping Cart")
            
            for i, item in enumerate(st.session_state.cart):
                with st.container():
                    st.write(f"**{item['design_name']}**")
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"Qty: {item['quantity']} | Size: {item['size']}")
                        st.write(f"₱{item['price_per_item']}/each = **₱{item['total_price']}**")
                    with col2:
                        if st.button("Remove", key=f"remove_{i}", use_container_width=True):
                            st.session_state.cart.pop(i)
                            st.rerun()
                    st.divider()
            
            total_items = sum(item['quantity'] for item in st.session_state.cart)
            total_cost = sum(item['total_price'] for item in st.session_state.cart)
            
            st.subheader("Cart Summary")
            st.write(f"Total Items: {total_items} shirts")
            st.write(f"**Total Cost: ₱{total_cost}**")
        else:
            st.info("Your cart is empty. Add some items!")

        # Customer information section - moved to right column
        if st.session_state.cart:
            st.subheader("Customer Information")
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            address = st.text_area("Shipping Address")
            
            checkout_col1, checkout_col2 = st.columns(2)
            with checkout_col1:
                if st.button("Clear Cart", use_container_width=True):
                    st.session_state.cart = []
                    st.rerun()
            
            with checkout_col2:
                if st.button("Checkout", type="primary", use_container_width=True):
                    if name and email and phone:
                        order_id = f"ORD{str(uuid.uuid4())[:3].upper()}{len(st.session_state.orders) + 1:03d}"
                        
                        new_order = {
                            "order_id": order_id,
                            "customer": name,
                            "email": email,
                            "phone": phone,
                            "items": [
                                {
                                    "design_name": item['design_name'],
                                    "quantity": item['quantity'],
                                    "size": item['size'],
                                    "price": item['total_price']
                                }
                                for item in st.session_state.cart
                            ],
                            "total": sum(item['total_price'] for item in st.session_state.cart),
                            "status": "Pending",
                            "date": datetime.now().strftime("%Y-%m-%d")
                        }
                        
                        st.session_state.orders.append(new_order)
                        
                        st.success(f"Order {order_id} placed successfully for {name}!")
                        st.info("You will receive a confirmation email shortly. Your order will appear in the vendor dashboard.")
                        st.write("**Order Details:**")
                        for item in st.session_state.cart:
                            st.write(f"- {item['design_name']}: {item['quantity']} × {item['size']} = ₱{item['total_price']}")
                        st.write(f"**Total: ₱{sum(item['total_price'] for item in st.session_state.cart)}**")
                        st.write(f"**Order ID: {order_id}**")
                        
                        st.session_state.cart = []
                    else:
                        st.error("Please fill in all customer information fields.")

with tab2:
    st.title("Vendor Dashboard")
    st.write("Printing shop vendor management system")
    
    vendor_tab1, vendor_tab2, vendor_tab3, vendor_tab4, vendor_tab5 = st.tabs(["Overview", "Pending Orders", "Shipping Orders", "Past Orders", "Revenue"])
    
    with vendor_tab1:
        # Use columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Current Material Pricing")
            st.write("**As of September 2025:**")
            st.write(f"Shirt: ₱{mShirt}")
            st.write(f"Ink: ₱{mInk}")
            st.write(f"Packaging: ₱{mPackaging}")
            st.write(f"**Total Materials: ₱{mTotal}**")
        
        with col2:
            st.subheader("Labor Costs")
            st.write("**Monthly Salaries:**")
            st.write(f"Designer: ₱{lDesigner}")
            st.write(f"Printer: ₱{lPrinter}")
            st.write(f"Packer: ₱{lPacker}")
            st.write(f"**Total Labor: ₱{lTotal}**")
            st.write("Per shirt labor cost: ₱30 (Assuming 1500 shirts per month)")
    
    with vendor_tab2:
        st.subheader("Pending Orders")
        
        if st.session_state.orders:
            # Use columns to display more orders side by side
            orders_to_display = [order for order in st.session_state.orders if order['status'] not in ["Shipped", "Shipping"]]
            
            if orders_to_display:
                for i in range(0, len(orders_to_display), 2):
                    col1, col2 = st.columns(2)
                    
                    # First order in the row
                    with col1:
                        if i < len(orders_to_display):
                            order = orders_to_display[i]
                            order_index = st.session_state.orders.index(order)
                            
                            with st.expander(f"Order {order['order_id']} - {order['customer']} - ₱{order['total']}"):
                                st.write(f"**Customer:** {order['customer']}")
                                st.write(f"**Email:** {order['email']}")
                                st.write(f"**Phone:** {order['phone']}")
                                st.write(f"**Order Date:** {order['date']}")
                                st.write("**Items:**")
                                for item in order['items']:
                                    st.write(f"- {item['design_name']}: {item['quantity']} × {item['size']} = ₱{item['price']}")
                                st.write(f"**Total: ₱{order['total']}**")
                                
                                new_status = st.selectbox(
                                    "Status", 
                                    ["Pending", "Designing", "Printing", "Packing", "Shipping", "Shipped", "Completed"], 
                                    index=["Pending", "Designing", "Printing", "Packing", "Shipping", "Shipped", "Completed"].index(order['status']),
                                    key=f"status_{order_index}"
                                )
                                
                                if st.button("Update Status", key=f"update_{order_index}", use_container_width=True):
                                    if new_status == "Completed":
                                        completed_order = {
                                            "order_id": order['order_id'],
                                            "customer": order['customer'],
                                            "items": order['items'],
                                            "total": order['total'],
                                            "date": datetime.now().strftime("%Y-%m-%d")
                                        }
                                        st.session_state.completed_orders.append(completed_order)
                                        st.session_state.orders.pop(order_index)
                                        st.success("Order marked as completed and moved to past orders!")
                                        st.rerun()
                                    else:
                                        st.session_state.orders[order_index]['status'] = new_status
                                        st.success(f"Status updated to {new_status}")
                                        st.rerun()
                    
                    # Second order in the row
                    with col2:
                        if i + 1 < len(orders_to_display):
                            order = orders_to_display[i + 1]
                            order_index = st.session_state.orders.index(order)
                            
                            with st.expander(f"Order {order['order_id']} - {order['customer']} - ₱{order['total']}"):
                                st.write(f"**Customer:** {order['customer']}")
                                st.write(f"**Email:** {order['email']}")
                                st.write(f"**Phone:** {order['phone']}")
                                st.write(f"**Order Date:** {order['date']}")
                                st.write("**Items:**")
                                for item in order['items']:
                                    st.write(f"- {item['design_name']}: {item['quantity']} × {item['size']} = ₱{item['price']}")
                                st.write(f"**Total: ₱{order['total']}**")
                                
                                new_status = st.selectbox(
                                    "Status", 
                                    ["Pending", "Designing", "Printing", "Packing", "Shipping", "Shipped", "Completed"], 
                                    index=["Pending", "Designing", "Printing", "Packing", "Shipping", "Shipped", "Completed"].index(order['status']),
                                    key=f"status_{order_index}"
                                )
                                
                                if st.button("Update Status", key=f"update_{order_index}", use_container_width=True):
                                    if new_status == "Completed":
                                        completed_order = {
                                            "order_id": order['order_id'],
                                            "customer": order['customer'],
                                            "items": order['items'],
                                            "total": order['total'],
                                            "date": datetime.now().strftime("%Y-%m-%d")
                                        }
                                        st.session_state.completed_orders.append(completed_order)
                                        st.session_state.orders.pop(order_index)
                                        st.success("Order marked as completed and moved to past orders!")
                                        st.rerun()
                                    else:
                                        st.session_state.orders[order_index]['status'] = new_status
                                        st.success(f"Status updated to {new_status}")
                                        st.rerun()
            else:
                st.info("No pending orders at the moment.")
        else:
            st.info("No pending orders at the moment.")
    
    with vendor_tab3:
        st.subheader("Orders Being Shipped")
        
        if st.session_state.orders:
            shipping_orders = [order for order in st.session_state.orders if order['status'] in ["Shipped", "Shipping"]]
            
            if shipping_orders:
                # Similar layout for shipping orders
                for i in range(0, len(shipping_orders), 2):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if i < len(shipping_orders):
                            order = shipping_orders[i]
                            order_index = st.session_state.orders.index(order)
                            
                            with st.expander(f"Order {order['order_id']} - {order['customer']} - ₱{order['total']} - Status: {order['status']}"):
                                st.write(f"**Customer:** {order['customer']}")
                                st.write(f"**Email:** {order['email']}")
                                st.write(f"**Phone:** {order['phone']}")
                                st.write(f"**Order Date:** {order['date']}")
                                st.write("**Items:**")
                                for item in order['items']:
                                    st.write(f"- {item['design_name']}: {item['quantity']} × {item['size']} = ₱{item['price']}")
                                st.write(f"**Total: ₱{order['total']}**")
                                
                                new_status = st.selectbox(
                                    "Status", 
                                    ["Shipping", "Shipped", "Completed"], 
                                    index=["Shipping", "Shipped", "Completed"].index(order['status']) if order['status'] in ["Shipping", "Shipped"] else 0,
                                    key=f"shipping_status_{order_index}"
                                )
                                
                                if st.button("Update Status", key=f"shipping_update_{order_index}", use_container_width=True):
                                    if new_status == "Completed":
                                        completed_order = {
                                            "order_id": order['order_id'],
                                            "customer": order['customer'],
                                            "items": order['items'],
                                            "total": order['total'],
                                            "date": datetime.now().strftime("%Y-%m-%d")
                                        }
                                        st.session_state.completed_orders.append(completed_order)
                                        st.session_state.orders.pop(order_index)
                                        st.success("Order marked as completed and moved to past orders!")
                                        st.rerun()
                                    else:
                                        st.session_state.orders[order_index]['status'] = new_status
                                        st.success(f"Status updated to {new_status}")
                                        st.rerun()
                    
                    with col2:
                        if i + 1 < len(shipping_orders):
                            order = shipping_orders[i + 1]
                            order_index = st.session_state.orders.index(order)
                            
                            with st.expander(f"Order {order['order_id']} - {order['customer']} - ₱{order['total']} - Status: {order['status']}"):
                                st.write(f"**Customer:** {order['customer']}")
                                st.write(f"**Email:** {order['email']}")
                                st.write(f"**Phone:** {order['phone']}")
                                st.write(f"**Order Date:** {order['date']}")
                                st.write("**Items:**")
                                for item in order['items']:
                                    st.write(f"- {item['design_name']}: {item['quantity']} × {item['size']} = ₱{item['price']}")
                                st.write(f"**Total: ₱{order['total']}**")
                                
                                new_status = st.selectbox(
                                    "Status", 
                                    ["Shipping", "Shipped", "Completed"], 
                                    index=["Shipping", "Shipped", "Completed"].index(order['status']) if order['status'] in ["Shipping", "Shipped"] else 0,
                                    key=f"shipping_status_{order_index}"
                                )
                                
                                if st.button("Update Status", key=f"shipping_update_{order_index}", use_container_width=True):
                                    if new_status == "Completed":
                                        completed_order = {
                                            "order_id": order['order_id'],
                                            "customer": order['customer'],
                                            "items": order['items'],
                                            "total": order['total'],
                                            "date": datetime.now().strftime("%Y-%m-%d")
                                        }
                                        st.session_state.completed_orders.append(completed_order)
                                        st.session_state.orders.pop(order_index)
                                        st.success("Order marked as completed and moved to past orders!")
                                        st.rerun()
                                    else:
                                        st.session_state.orders[order_index]['status'] = new_status
                                        st.success(f"Status updated to {new_status}")
                                        st.rerun()
            else:
                st.info("No orders currently being shipped.")
        else:
            st.info("No orders currently being shipped.")
    
    with vendor_tab4:
        st.subheader("Past Orders")
        
        if st.session_state.completed_orders:
            past_orders_display = []
            for order in st.session_state.completed_orders:
                items_summary = ", ".join([f"{item['design_name']} ({item['quantity']}x{item['size']})" for item in order['items']])
                past_orders_display.append({
                    "Order ID": order['order_id'],
                    "Customer": order['customer'],
                    "Items": items_summary,
                    "Date": order['date'],
                    "Total": f"₱{order['total']}"
                })
            
            st.dataframe(past_orders_display, use_container_width=True)
        else:
            st.info("No completed orders yet.")
    
    with vendor_tab5:
        st.subheader("Revenue Summary")
        
        material_cost_per_shirt = mTotal
        labor_cost_per_shirt = 30 
        total_cost_per_shirt = material_cost_per_shirt + labor_cost_per_shirt
        profit_per_shirt = pShirt - total_cost_per_shirt
        profit_margin_percent = (profit_per_shirt / pShirt) * 100
        
        today_revenue = sum(order['total'] for order in st.session_state.completed_orders if order['date'] == datetime.now().strftime("%Y-%m-%d"))
        total_orders = len(st.session_state.orders) + len(st.session_state.completed_orders)
        total_revenue = sum(order['total'] for order in st.session_state.completed_orders)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Today's Revenue", f"₱{today_revenue}", "₱0")
        
        with col2:
            st.metric("Total Revenue", f"₱{total_revenue}", f"₱{total_revenue}")
        
        with col3:
            st.metric("Total Orders", str(total_orders), str(len(st.session_state.orders)))
        
        with col4:
            st.metric("Profit Margin", f"{profit_margin_percent:.1f}%", f"₱{profit_per_shirt}/shirt")

        revenue_data = pd.DataFrame({
            'Date': ['Jan 10', 'Jan 11', 'Jan 12', 'Jan 13', 'Jan 14', 'Jan 15', 'Jan 16'],
            'Revenue': [1500, 2200, 1800, 2500, 3000, 1750, 2250]
        })
        st.line_chart(revenue_data.set_index('Date'), use_container_width=True)