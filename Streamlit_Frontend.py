import streamlit as st
import requests
import pandas as pd
from typing import Dict, List

# הגדרת URL של ה-API
API_BASE_URL = "http://localhost:8000"


def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Main"


def login_page():
    st.title("Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            try:
                response = requests.post(f"{API_BASE_URL}/users/login",
                                         json={"username": username, "password": password})
                if response.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.user_data = response.json()
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            except:
                st.error("Connection error")

    with tab2:
        st.subheader("Register")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        country = st.text_input("Country")
        city = st.text_input("City")
        new_username = st.text_input("Username", key="reg_username")
        new_password = st.text_input("Password", type="password", key="reg_password")

        if st.button("Register"):
            user_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "country": country,
                "city": city,
                "username": new_username,
                "password": new_password
            }

            try:
                response = requests.post(f"{API_BASE_URL}/users/register", json=user_data)
                if response.status_code == 200:
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Registration failed")
            except:
                st.error("Connection error")


def main_page():
    st.title("🛍️ Shopping Website")

    # חיפוש
    st.subheader("Search Products")
    col1, col2 = st.columns([3, 1])

    with col1:
        search_term = st.text_input("Search by product name", placeholder="Enter product name...")
    with col2:
        search_button = st.button("🔍 Search")

    # חיפוש מתקדן
    with st.expander("Advanced Search"):
        col1, col2 = st.columns(2)
        with col1:
            min_price = st.number_input("Min Price", min_value=0.0, value=0.0)
            min_stock = st.number_input("Min Stock", min_value=0, value=0)
        with col2:
            max_price = st.number_input("Max Price", min_value=0.0, value=10000.0)
            max_stock = st.number_input("Max Stock", min_value=0, value=1000)

        advanced_search_button = st.button("🔍 Advanced Search")

    # הצגת מוצרים
    try:
        products = []
        # חיפוש רגיל לפי שם
        if search_button and search_term:
            response = requests.post(f"{API_BASE_URL}/products/search",
                                     json={"names": search_term})
            if response.status_code == 200:
                products_data = response.json()
                products = products_data.get("products", [])
            else:
                products = []
                st.warning("No products found")

        # חיפוש מתקדם לפי מחיר ומלאי
        elif advanced_search_button:
            search_data = {}

            # הוספת פרמטרים רק אם הם שונים מהברירת מחדל
            if min_price > 0:
                search_data["min_price"] = min_price
            if max_price < 10000:
                search_data["max_price"] = max_price
            if min_stock > 0:
                search_data["min_stock"] = min_stock
            if max_stock < 1000:
                search_data["max_stock"] = max_stock

            # קריאה ל-API
            response = requests.post(f"{API_BASE_URL}/products/search", json=search_data)
            if response.status_code == 200:
                products_data = response.json()
                products = products_data.get("products", [])
                st.info(f"Found {len(products)} products matching your criteria")
            else:
                products = []
                st.warning("No products found matching your criteria")

        # הצגת כל המוצרים (ברירת מחדל)
        else:
            response = requests.get(f"{API_BASE_URL}/products/")
            products = response.json() if response.status_code == 200 else []

        # הצגת המוצרים
        if products:
            st.subheader(f"Products ({len(products)} found)")

            # הוספת כפתורים לכל מוצר
            for index, product in enumerate(products):
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

                with col1:
                    st.write(f"**{product['Name']}**")
                with col2:
                    st.write(f"${product['Price']}")
                with col3:
                    stock_color = "🟢" if product['Stock'] > 0 else "🔴"
                    st.write(f"{stock_color} {product['Stock']}")
                with col4:
                    if st.session_state.logged_in and product['Stock'] > 0:
                        if st.button("🛒 Add to Cart", key=f"cart_{product['ProductID']}"):
                            add_to_cart(product['ProductID'])
                with col5:
                    if st.session_state.logged_in:
                        if st.button("❤️ Favorite", key=f"fav_{product['ProductID']}"):
                            add_to_favorites(product['ProductID'])
        else:
            st.info("No products available")

    except Exception as e:
        st.error(f"Error loading products: {e}")


def add_to_cart(product_id: int):
    try:
        order_data = {
            "user_id": st.session_state.user_data["user_id"],
            "product_id": product_id,
            "quantity": 1,
            "shipping_address": "Default Address"  # יש לשפר
        }
        response = requests.post(f"{API_BASE_URL}/orders/add-item", json=order_data)
        if response.status_code == 200:
            st.success("Item added to cart!")
        else:
            st.error("Failed to add item to cart")
    except Exception as e:
        st.error(f"Error: {e}")


def add_to_favorites(product_id: int):
    try:
        favorite_data = {
            "user_id": st.session_state.user_data["user_id"],
            "product_id": product_id
        }
        response = requests.post(f"{API_BASE_URL}/favorites/add", json=favorite_data)
        if response.status_code == 200:
            st.success("Item added to favorites!")
        else:
            st.error("Failed to add to favorites")
    except Exception as e:
        st.error(f"Error: {e}")


def orders_page():
    st.title("📦 My Orders")

    if not st.session_state.logged_in:
        st.warning("Please login to view orders")
        return

    try:
        user_id = st.session_state.user_data["user_id"]
        response = requests.get(f"{API_BASE_URL}/orders/user/{user_id}")

        if response.status_code == 200:
            orders = response.json()

            if orders:
                for order in orders:
                    status_color = "🟡" if order["OrderStatus"] == "TEMP" else "🟢"

                    with st.expander(
                            f"{status_color} Order #{order['OrderID']} - {order['OrderStatus']} - ${order['TotalPrice']}"):
                        st.write(f"**Date:** {order['OrderDate']}")
                        st.write(f"**Shipping Address:** {order['ShippingAddress']}")
                        st.write(f"**Total Price:** ${order['TotalPrice']}")

                        if order["OrderStatus"] == "TEMP":
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button(f"💳 Purchase Order", key=f"purchase_{order['OrderID']}"):
                                    purchase_order(user_id)
                            with col2:
                                if st.button(f"🗑️ Delete Order", key=f"delete_{order['OrderID']}"):
                                    # הוסף פונקציונליות מחיקה
                                    st.info("Delete functionality")
            else:
                st.info("No orders found")
        else:
            st.error("Failed to load orders")
    except Exception as e:
        st.error(f"Error: {e}")


def purchase_order(user_id: int):
    try:
        response = requests.post(f"{API_BASE_URL}/orders/purchase/{user_id}")
        if response.status_code == 200:
            st.success("Order purchased successfully!")
            st.rerun()
        else:
            st.error("Failed to purchase order")
    except Exception as e:
        st.error(f"Error: {e}")


def favorites_page():
    st.title("❤️ My Favorites")

    if not st.session_state.logged_in:
        st.warning("Please login to view favorites")
        return

    try:
        user_id = st.session_state.user_data["user_id"]
        response = requests.get(f"{API_BASE_URL}/favorites/user/{user_id}")

        if response.status_code == 200:
            favorites = response.json()

            if favorites:
                for fav in favorites:
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                    with col1:
                        st.write(f"**{fav['Name']}**")
                    with col2:
                        st.write(f"${fav['Price']}")
                    with col3:
                        stock_color = "🟢" if fav['Stock'] > 0 else "🔴"
                        st.write(f"{stock_color} {fav['Stock']}")
                    with col4:
                        if st.button("🗑️ Remove", key=f"remove_fav_{fav['ProductID']}"):
                            remove_from_favorites(fav['ProductID'])
            else:
                st.info("No favorite items")
        else:
            st.error("Failed to load favorites")
    except Exception as e:
        st.error(f"Error: {e}")


def remove_from_favorites(product_id: int):
    try:
        favorite_data = {
            "user_id": st.session_state.user_data["user_id"],
            "product_id": product_id
        }
        response = requests.delete(f"{API_BASE_URL}/favorites/remove", json=favorite_data)
        if response.status_code == 200:
            st.success("Item removed from favorites!")
            st.rerun()
        else:
            st.error("Failed to remove from favorites")
    except Exception as e:
        st.error(f"Error: {e}")


def chat_page():
    st.title("🤖 Chat Assistant")

    if not st.session_state.logged_in:
        st.warning("Please login to use chat assistant")
        return

    # Chat interface
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for i, (question, response) in enumerate(st.session_state.chat_history):
        st.write(f"**You:** {question}")
        st.write(f"**Assistant:** {response}")
        st.write("---")

    # Input for new question
    question = st.text_input("Ask a question about our products:")

    if st.button("Send") and question:
        try:
            chat_data = {
                "user_id": st.session_state.user_data["user_id"],
                "question": question
            }
            response = requests.post(f"{API_BASE_URL}/chat/ask", json=chat_data)

            if response.status_code == 200:
                result = response.json()
                st.session_state.chat_history.append((question, result["response"]))
                st.write(f"**Remaining questions:** {result['remaining_prompts']}")
                st.rerun()
            elif response.status_code == 429:
                st.error("You have reached the maximum limit of 5 questions per session")
            else:
                st.error("Chat service error")
        except Exception as e:
            st.error(f"Error: {e}")


def main():
    st.set_page_config(page_title="Shopping Website", page_icon="🛍️", layout="wide")

    init_session_state()

    # Sidebar navigation
    if st.session_state.logged_in:
        st.sidebar.title(f"Welcome, {st.session_state.user_data['first_name']}!")

        pages = ["Main", "Orders", "Favorites", "Chat Assistant"]
        st.session_state.current_page = st.sidebar.radio("Navigation", pages)

        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.session_state.current_page = "Main"
            st.rerun()
    else:
        st.sidebar.title("Shopping Website")
        st.session_state.current_page = st.sidebar.radio("Navigation", ["Main", "Login"])

    # Page routing
    if not st.session_state.logged_in and st.session_state.current_page == "Login":
        login_page()
    elif st.session_state.current_page == "Main":
        main_page()
    elif st.session_state.current_page == "Orders":
        orders_page()
    elif st.session_state.current_page == "Favorites":
        favorites_page()
    elif st.session_state.current_page == "Chat Assistant":
        chat_page()


if __name__ == "__main__":
    main()
