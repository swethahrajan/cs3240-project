from django.contrib.auth.decorators import user_passes_test

def executive_only(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_executive,
        login_url='/',
        redirect_field_name=None
    )(view_func)

def member_only(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_member,
        login_url='/',
        redirect_field_name=None
    )(view_func)

def user_admin_only(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_user_admin,
        login_url='/',
        redirect_field_name=None
    )(view_func)