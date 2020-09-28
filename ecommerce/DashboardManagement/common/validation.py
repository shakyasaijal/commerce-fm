def reset_password(request):
    err = None

    if  not request.POST['new_password'] == request.POST['confirm_password']:
        err = "Passwords do not match."
        return err
    
    if len(request.POST['new_password']) < 8:
        err = "Password must be atleast 8 characters long."
        return err

    return err

def change_password(request):
    err = None

    if  not request.POST['new_password'] == request.POST['confirm_password']:
        err = "Passwords do not match."
        return err
    
    if len(request.POST['new_password']) < 8:
        err = "Password must be atleast 8 characters long."
        return err

    if request.POST['new_password'] == request.POST['old_password']:
        err = "New password should be different than old password."
        return err
        
    return err
