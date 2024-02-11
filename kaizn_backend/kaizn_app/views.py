# kaizn_app/views.py

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ItemInventory
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .serializers import ItemInventorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def addseed(id):
    try:
        data = [{"user_id": id, "sku": "SKU003", "name": "Product 3", "tags": "Tag5, Tag8", "category": "Category9", "in_stock": 16, "available_stock": 11}, {"user_id": id, "sku": "SKU004", "name": "Product 4", "tags": "Tag5, Tag9", "category": "Category3", "in_stock": 13, "available_stock": 12}, {"user_id": id, "sku": "SKU005", "name": "Product 5", "tags": "Tag6, Tag6", "category": "Category8", "in_stock": 16, "available_stock": 10}, {"user_id": id, "sku": "SKU006", "name": "Product 6", "tags": "Tag10, Tag6", "category": "Category10", "in_stock": 10, "available_stock": 10}, {"user_id": id, "sku": "SKU007", "name": "Product 7", "tags": "Tag6, Tag7", "category": "Category10", "in_stock": 18, "available_stock": 5}, {"user_id": id, "sku": "SKU008", "name": "Product 8", "tags": "Tag9, Tag10", "category": "Category3", "in_stock": 17, "available_stock": 12}, {"user_id": id, "sku": "SKU009", "name": "Product 9", "tags": "Tag10, Tag6", "category": "Category6", "in_stock": 19, "available_stock": 12}, {"user_id": id, "sku": "SKU0010", "name": "Product 10", "tags": "Tag9, Tag5", "category": "Category9", "in_stock": 11, "available_stock": 15}, {"user_id": id, "sku": "SKU0011", "name": "Product 11", "tags": "Tag5, Tag9", "category": "Category9", "in_stock": 14, "available_stock": 10}, {"user_id": id, "sku": "SKU0012", "name": "Product 12", "tags": "Tag5, Tag5", "category": "Category9", "in_stock": 11, "available_stock": 11}]

        items = []
        for item_data in data:
            item = ItemInventory(**item_data)
            item.save()
            items.append(item)
    except User.DoesNotExist:
        print(f"User with id {id} does not exist.")

def redirect_if_logged_in(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('item_dashboard')  # Redirect to your desired page
        return view_func(request, *args, **kwargs)
    
    return wrapper

@swagger_auto_schema(
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password']
    ),
    responses={
        200: 'Successfully signed up and logged in and redirection to item_dashboard',
    },
    operation_summary='User Signup',
    operation_description='Sign up a user with a given username and password.'
)
@swagger_auto_schema(
    methods=['GET'],
    responses={
        200: 'Successfully retrieved signup form',
    },
    operation_summary='Get signup Form',
    operation_description='Retrieve the signup form for user login.'
)
@api_view(['GET', 'POST'])
@redirect_if_logged_in
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            try:        
                user = User.objects.create_user(username=username, password=password)
            except IntegrityError:
                # Handle the case where a duplicate entry is attempted
                error_message = "User already exists. Please choose a different username."
                return render(request, 'kaizn_app/signup.html', {'form': AuthenticationForm(), 'error_message': error_message})
            login(request, user)
            addseed(user.id)
            return redirect('item_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'kaizn_app/signup.html', {'form': form})


@swagger_auto_schema(
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password']
    ),
    responses={
        200: 'Successfully logged in and redirection to item_dashboard',
    },
    operation_summary='User Login',
    operation_description='Log in a user with a given username and password.'
)
@swagger_auto_schema(
    methods=['GET'],
    responses={
        200: 'Successfully retrieved login form',
    },
    operation_summary='Get Login Form',
    operation_description='Retrieve the login form for user login.'
)
@api_view(['GET', 'POST'])
@redirect_if_logged_in
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Handle case where user does not exist
            return render(request, 'kaizn_app/login.html', {'form': AuthenticationForm(), 'error_message': 'User does not exist'})

        # Now authenticate the user
        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            # User is authenticated, perform further actions
            login(request, authenticated_user)
            return redirect('item_dashboard')
        else:
            # Authentication failed, handle accordingly
            return render(request, 'kaizn_app/login.html', {'error_message': 'Invalid credentials'})

    # Render your login form for GET requests
    return render(request, 'kaizn_app/login.html', {'form': AuthenticationForm()})

@swagger_auto_schema(
    method='get',
    operation_summary='Get item inventory list',
    operation_description='Get a list of items in the inventory with optional category filter.',
    manual_parameters=[
        openapi.Parameter('category', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description='Filter items by category'),
    ],
    responses={
        200: ItemInventorySerializer(many=True),
        401: openapi.Response(description='Unauthorized'),
    }
)
@login_required(login_url='/login')
@api_view(['GET'])
def item_dashboard(request):
    current_user = request.user
    category_filter = request.GET.get('category')
    
    if category_filter:
        item_inventory_list = ItemInventory.objects.filter(user_id=current_user.id, category=category_filter)
    else:
        item_inventory_list = ItemInventory.objects.filter(user_id=current_user.id)
    
    print(item_inventory_list)
    context = {
        'item_inventory_list': item_inventory_list
    }
    return render(request, 'kaizn_app/item_dashboard.html', context)

@swagger_auto_schema(
    method='get',
    operation_summary='Get item inventory list',
    operation_description='Get a list of items in the inventory for the authenticated user.',
    responses={
        200: openapi.Response(description='Successful response with item inventory list'),
        401: openapi.Response(description='Unauthorized'),
    }
)
@login_required(login_url='/login')
@api_view(['GET'])
def get_item_inventory(request):
    current_user = request.user
    item_inventory_list = ItemInventory.objects.filter(user_id=current_user.id)
    serializer = ItemInventorySerializer(item_inventory_list, many=True)
    return Response(serializer.data)