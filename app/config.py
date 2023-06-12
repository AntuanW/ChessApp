my_username = None


# my_username = "tomek"

def set_username(username):
    global my_username
    my_username = username


def get_username():
    return my_username
