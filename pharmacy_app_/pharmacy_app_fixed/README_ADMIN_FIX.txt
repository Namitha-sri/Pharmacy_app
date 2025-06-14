
# Pharmacy Management System - Admin Access Fix

## ✅ Fixed Issue:
This project previously showed:
> "You are authenticated as Namitha, but are not authorized to access this page."

### 🔍 Reason:
You were logged in, but **not as an admin (superuser)**. Admin-only actions like add/update/delete medicine are protected in code using `request.user.is_superuser`.

---

## 🛠 How to Fix:
Create a superuser account so you can access all admin-only features.

### 💻 Step-by-step:

1. Open terminal in the project directory.
2. Run the command:

```
python manage.py createsuperuser
```

3. Enter a username, email, and password for the admin.
4. Login at `/login/` with those credentials.
5. You will now be able to access:

   - `/add/` (Add medicine)
   - `/update/<id>/`
   - `/delete/<id>/`
   - `/admin-page/`

---

## 💡 Tip:
- Regular users can only **view** medicines and access `/dashboard/`.
- Admin (superuser) can do **everything**.

