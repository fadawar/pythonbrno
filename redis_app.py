ADMIN_ROLE = 'admin'
USERS = {
    'karel': ADMIN_ROLE,
    'pepa': 'regular_user'
}


def authorize(needed_role):
    def wrapper(func):
        def authorize_and_call(*args, **kwargs):
            user = kwargs.get('user', '')
            user_role = USERS.get(user)
            if user_role == needed_role or user_role == ADMIN_ROLE:
                return func(*args, **kwargs)
            return 'Unauthorized Access! user={}, needed_role={}, user_role={}'.format(user, needed_role, user_role)
        return authorize_and_call
    return wrapper


@authorize('admin')
def show_admin(user, page='index.html'):
    return 'admin.html'


@authorize('regular_user')
def show_index(user, page='index.html'):
    return 'index.html'


if __name__ == '__main__':

    print show_index(user='pepa')

    print show_admin(user='pepa')

    print show_admin(user='karel')

    print show_index(user='karel')

