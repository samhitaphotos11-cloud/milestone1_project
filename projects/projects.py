"""E-commerce AI Recommendation Engine with login (FIXED)."""

import os
import sys
from typing import Any, Dict, List
import reflex as rx

APP_USERNAME = "admin"
APP_PASSWORD = "admin123"

data = None
tfidf_matrix = None
similarity = None


def load_recommendation_model():
    global data, tfidf_matrix, similarity
    try:
        import pandas as pd
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        try:
            data = pd.read_csv("projects/cleaned_output.csv")
        except:
            data = pd.read_csv("cleaned_output.csv")

        data["Tags"] = data["Tags"].fillna("")
        data["Rating"] = pd.to_numeric(data.get("Rating", 0), errors="coerce").fillna(0)
        data["Review Count"] = pd.to_numeric(data.get("Review Count", 0), errors="coerce").fillna(0)
        data["Description"] = data.get("Description", "").fillna("").astype(str)

        tfidf = TfidfVectorizer(stop_words="english", max_features=100)
        tfidf_matrix = tfidf.fit_transform(data["Tags"])
        similarity = cosine_similarity(tfidf_matrix)

    except Exception as e:
        print("Model load error:", e)


# ✅ SAFE IMAGE FIX
def safe_image(url: str) -> str:
    if not url or url == "nan":
        return "https://images.unsplash.com/photo-1523275335684-37898b6baf30"
    return url


class State(rx.State):
    search_query: str = ""
    selected_product: Dict[str, Any] = {}
    recommendations: List[Dict[str, Any]] = []

    cart: List[Dict[str, Any]] = []
    wishlist: List[Dict[str, Any]] = []

    username: str = ""
    password: str = ""
    is_authenticated: bool = False
    login_error: str = ""

    def login(self):
        if self.username == APP_USERNAME and self.password == APP_PASSWORD:
            self.is_authenticated = True
            return rx.redirect("/home")
        self.login_error = "Invalid credentials"

    def logout(self):
        self.is_authenticated = False
        return rx.redirect("/")

    # ✅ FIXED CART
    def add_to_cart(self, name: str):
        product = self._find_product(name)
        if product and not any(p["name"] == product["name"] for p in self.cart):
            self.cart = self.cart + [product]

    def remove_from_cart(self, name: str):
        self.cart = [p for p in self.cart if p["name"] != name]

    # ✅ FIXED WISHLIST
    def toggle_wishlist(self, name: str):
        product = self._find_product(name)
        if not product:
            return
        exists = any(p["name"] == product["name"] for p in self.wishlist)
        if exists:
            self.wishlist = [p for p in self.wishlist if p["name"] != name]
        else:
            self.wishlist = self.wishlist + [product]

    def _find_product(self, name: str):
        if data is None:
            return {}
        row = data[data["Name"] == name]
        if len(row) == 0:
            return {}
        r = row.iloc[0]
        return {
            "name": r["Name"],
            "brand": r["Brand"],
            "image": safe_image(r.get("ImageURL")),
            "rating": str(r.get("Rating", "N/A")),
        }

    def load_products(self):
        load_recommendation_model()
        if data is not None:
            self.recommendations = data.head(8).to_dict("records")


# ✅ PRODUCT CARD FIXED
def product_card(product: Dict[str, Any]):
    name = product.get("Name", "")
    return rx.box(
        rx.vstack(
            rx.image(
                src=safe_image(product.get("ImageURL")),
                height="150px",
                width="100%",
                object_fit="cover",
                border_radius="10px",
            ),
            rx.text(name, font_weight="bold"),
            rx.text(product.get("Brand", ""), size="2"),

            rx.hstack(
                rx.button(
                    "Add to Cart",
                    on_click=lambda: State.add_to_cart(name),
                    color="white",
                    background="red",
                ),
                rx.button(
                    "Wishlist",
                    on_click=lambda: State.toggle_wishlist(name),
                ),
            ),
        ),
        padding="10px",
        border="1px solid #333",
        border_radius="12px",
    )


# ✅ NAVBAR FIXED
def navbar():
    return rx.hstack(
        rx.button("Home", on_click=lambda: rx.redirect("/home")),
        rx.text(lambda: f"Cart ({len(State.cart)})"),
        rx.text(lambda: f"Wishlist ({len(State.wishlist)})"),
        rx.button("Logout", on_click=State.logout),
        spacing="4",
    )


# ✅ HOME PAGE
def home():
    return rx.box(
        rx.vstack(
            navbar(),
            rx.heading("Products"),
            rx.foreach(State.recommendations, product_card),
        ),
        padding="20px",
    )


# ✅ LOGIN PAGE
def login_page():
    return rx.center(
        rx.vstack(
            rx.heading("Login"),
            rx.input(placeholder="Username", on_change=State.set_username),
            rx.input(placeholder="Password", type_="password", on_change=State.set_password),
            rx.button("Login", on_click=State.login),
            rx.text(State.login_error, color="red"),
        )
    )


app = rx.App()
app.add_page(login_page, route="/")
app.add_page(home, route="/home", on_load=State.load_products)