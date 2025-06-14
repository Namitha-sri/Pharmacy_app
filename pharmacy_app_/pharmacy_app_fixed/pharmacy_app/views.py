from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine
from .forms import MedicineForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm

# 👉 Combined login page
def combined_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')  # Redirect admin to Django admin
            else:
                return redirect('user_dashboard')  # Normal user dashboard
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'combined_login.html')

# 👉 User dashboard
@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

# 👉 View medicines - accessible to all logged-in users
@login_required
def view_medicines(request):
    medicines = Medicine.objects.all()
    return render(request, 'view.html', {'medicines': medicines})

# 👉 Add medicine - admin only
@login_required
def add_medicine(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admin can add medicines.")
    
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view')
    else:
        form = MedicineForm()
    return render(request, 'add.html', {'form': form})

# 👉 Update medicine - admin only
@login_required
def update_medicine(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admin can update medicines.")
    
    medicine = get_object_or_404(Medicine, id=id)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('view')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'update.html', {'form': form, 'medicine': medicine})

# 👉 Delete medicine - admin only
@login_required
def delete_medicine(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admin can delete medicines.")
    
    medicine = get_object_or_404(Medicine, id=id)
    medicine.delete()
    return redirect('view')

# 👉 Logout
def logout_user(request):
    logout(request)
    return redirect('combined_login')

# 👉 Register new user
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful. Please login.")
        return redirect('combined_login')

    return render(request, 'register.html')


# 👉 Admin-only custom page (optional)
@login_required
def admin_only_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to view this page.")
    return render(request, 'admin_page.html')

# 👉 Optional: login choice landing
def login_choice(request):
    return render(request, 'login_choice.html')


def add_to_cart(request, medicine_id):
    cart = request.session.get('cart', {})
    cart[str(medicine_id)] = cart.get(str(medicine_id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for id, qty in cart.items():
        med = get_object_or_404(Medicine, id=id)
        cart_items.append({'medicine': med, 'quantity': qty, 'subtotal': qty * med.price})
        total += qty * med.price
    return render(request, 'pharmacy_app/cart.html', {'cart_items': cart_items, 'total': total})



@login_required
def buy_medicines(request):
    if request.method == 'POST':
        total = 0
        items = []
        for med in Medicine.objects.all():
            qty = int(request.POST.get(f'quantity_{med.id}', 0))
            if qty > 0:
                if qty > med.stock:
                    messages.error(request, f"Not enough stock for {med.name}")
                    return redirect('buy_medicines')
                subtotal = qty * med.price
                total += subtotal
                items.append((med, qty, subtotal))

        if items:
            order = Order.objects.create(user=request.user, total_amount=total)
            for med, qty, subtotal in items:
                OrderItem.objects.create(order=order, medicine=med, quantity=qty, subtotal=subtotal)
                med.stock -= qty
                med.save()
            messages.success(request, "Order placed successfully.")
            return redirect('order_success')
        else:
            messages.error(request, "Please select at least one medicine.")
    medicines = Medicine.objects.all()
    return render(request, 'pharmacy_app/buy_medicines.html', {'medicines': medicines})

def order_success(request):
    return render(request, 'pharmacy_app/order_success.html')