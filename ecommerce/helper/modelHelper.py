availability_choice = (
    (True, 'In stock'),
    (False, 'Out of stock'),
)

email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
password_reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

size = (
    (1, 'XS'),
    (2, 'SM'),
    (3, 'M'),
    (4, 'L'),
    (5, 'XL'),
    (6, 'XXL'),
    (7, 'XXXL'),
)

is_featured = (
    (False, "Not a featured."),
    (True, "Is featured."),
)

order_status_choice = (
    (1, 'Pending'),
    (2, 'In Progress'),
    (3, 'Delivered'),
    (4, 'Cancelled'),
)   

soft_delete = (
    (True, "Soft Deleted"),
    (False, "Not Deleted")
)

genesis_block = (
    (True, "Is a Genesis Block."),
    (False, "Is not a Genesis Block."),
)

notice_status = (
    (True, "Send Notice Now"),
    (False, "Don't Send Notice Now"),
)

importance_status = (
    (1, "Critical"),
    (2, "Very Important"),
    (3, "Important")
)
