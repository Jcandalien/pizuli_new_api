from fastapi_admin.app import app
from fastapi_admin.resources import Field, Link, Model, Action
from fastapi_admin.widgets import displays, filters, inputs
from db.models.franchise import Franchise, FranchiseType
from db.models.order import Order, OrderStatus
from db.models.animal import Animal
from db.models.meat import Meat
from db.models.recipe import Recipe
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.resources import  Resource
from db.models.user import User
from core.security import verify_password
from fastapi import Request

@app.register
class Home(Resource):
    label = "Home"
    icon = "fas fa-home"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dashboard = None

    async def get_widgets(self, request: Request):
        order_count = await Order.all().count()
        franchise_count = await Franchise.all().count()
        animal_count = await Animal.all().count()
        meat_count = await Meat.all().count()
        recipe_count = await Recipe.all().count()

        order_status_data = {status.value: await Order.filter(status=status).count() for status in OrderStatus}
        franchise_type_data = {franchise_type.value: await Franchise.filter(type=franchise_type).count() for franchise_type in FranchiseType}

        return [
            {"type": "card", "value": order_count, "label": "Total Orders", "icon": "fas fa-shopping-cart", "color": "primary"},
            {"type": "card", "value": franchise_count, "label": "Total Franchises", "icon": "fas fa-store", "color": "info"},
            {"type": "card", "value": animal_count, "label": "Total Animals", "icon": "fas fa-paw", "color": "success"},
            {"type": "card", "value": meat_count, "label": "Total Meats", "icon": "fas fa-drumstick-bite", "color": "warning"},
            {"type": "card", "value": recipe_count, "label": "Total Recipes", "icon": "fas fa-utensils", "color": "danger"},
            {"type": "chart", "label": "Orders by Status", "chart": "pie", "data": order_status_data},
            {"type": "chart", "label": "Franchises by Type", "chart": "bar", "data": franchise_type_data},
        ]

@app.register
class FranchiseResource(Model):
    label = "Franchises"
    model = Franchise
    icon = "fas fa-store"
    page_pre_title = "franchise list"
    page_title = "Franchises"
    filters = [
        filters.Search(
            name="name",
            label="Name",
            search_mode="contains",
            placeholder="Search franchise name",
        ),
        filters.Enum(enum=FranchiseType, name="type", label="Type"),
    ]
    fields = [
        "id",
        "name",
        "type",
        "owner.username",
        "location",
        Field(
            name="is_approved",
            label="Approved",
            input_=inputs.Switch(),
        ),
    ]
    actions = [
        Action(
            label="Approve",
            icon="fas fa-check",
            name="approve",
            method="POST",
            ajax=True,
            confirm="Are you sure you want to approve this franchise?",
        ),
    ]

@app.register
class OrderResource(Model):
    label = "Orders"
    model = Order
    icon = "fas fa-shopping-cart"
    page_pre_title = "order list"
    page_title = "Orders"
    filters = [
        filters.Search(
            name="user__username",
            label="User",
            search_mode="contains",
            placeholder="Search by username",
        ),
        filters.Enum(enum=OrderStatus, name="status", label="Status"),
    ]
    fields = [
        "id",
        "user.username",
        "franchise.name",
        "total_amount",
        "status",
        "created_at",
    ]
    actions = [
        Action(
            label="Process",
            icon="fas fa-cogs",
            name="process",
            method="POST",
            ajax=True,
            confirm="Are you sure you want to process this order?",
        ),
    ]

@app.register
class AnimalResource(Model):
    label = "Animals"
    model = Animal
    icon = "fas fa-paw"
    page_pre_title = "animal list"
    page_title = "Animals"
    filters = [
        filters.Search(
            name="breed",
            label="Breed",
            search_mode="contains",
            placeholder="Search animal breed",
        ),
        filters.Search(
            name="age",
            label="Age",
            search_mode="exact",
            placeholder="Enter age",
        ),
    ]
    fields = [
        "id",
        "type.name",
        "breed",
        "age",
        "weight",
        "health_status",
        "price",
        "quantity",
        "owner.name",
    ]

@app.register
class MeatResource(Model):
    label = "Meats"
    model = Meat
    icon = "fas fa-drumstick-bite"
    page_pre_title = "meat list"
    page_title = "Meats"
    filters = [
        filters.Search(
            name="cut",
            label="Cut",
            search_mode="contains",
            placeholder="Search meat cut",
        ),
        filters.Search(
            name="price",
            label="Price",
            search_mode="exact",
            placeholder="Enter price",
        ),
        filters.Boolean(name="is_frozen", label="Frozen"),
        filters.Boolean(name="is_fresh", label="Fresh"),
    ]
    fields = [
        "id",
        "type.name",
        "cut",
        "grade",
        "weight",
        "price",
        "is_frozen",
        "is_fresh",
        "franchise.name",
        "stock_quantity",
    ]

@app.register
class RecipeResource(Model):
    label = "Recipes"
    model = Recipe
    icon = "fas fa-utensils"
    page_pre_title = "recipe list"
    page_title = "Recipes"
    filters = [
        filters.Search(
            name="name",
            label="Name",
            search_mode="contains",
            placeholder="Search recipe name",
        ),
        filters.Search(
            name="cooking_time",
            label="Cooking Time",
            search_mode="exact",
            placeholder="Enter cooking time",
        ),
    ]
    fields = [
        "id",
        "name",
        "description",
        "ingredients",
        "instructions",
        "cooking_time",
        "difficulty",
        "franchise.name",
    ]

def setup_admin():
    login_provider = UsernamePasswordProvider(
        login_logo_url="https://preview.tabler.io/static/logo.svg",
        admin_model=User,
    )

    async def login(request: Request):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        user = await User.get_or_none(username=username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    app.add_middleware(login_provider, login=login)

    return app


