# Tina's Gift Shop Website
#### Video Demo:  https://youtu.be/C-pPYVtTrUQ
#### Description:
This project is a website for a real business, with real products.
The website includes:
- Main page: Welcome page that has 3 banners inviting the customer to shop. It includes a section to explore the product categories and a section for trendy products.
- Shop: The shop is divided in sections for each type of product. Each section displays the available products which you can zoom in and see the details, you can add the products to your shopping cart and add personalization to the product.
- User: It has a dashboard that includes the profile details, this is only available when the user is signed in.
- About Us: This page shows a description of the business.
- Contact Us: This page has a form that submits a message to the admin user. The message will be saved in the database and can be deleted after you read it.
- Log in: It lets the customer log into their existing account. It verifies the account exists and validates the password is correct.
- Sign Up: It lets the customer sign up for a new account. It validates that the email has not been previously use to create an account. 
- My Messages (Admin Only): This page is only available when the admin user is logged in. It shows the messages received and has the option to delete the messages from the database.
- My Orders (Admin Only): This page is only available when the admin user is logged in. It shows a table with the users, another table for the orders and the order items. 
- Create Product (Admin Only): This page is only available when the admin user is logged in. The admin can create a new product by submitting the form, and it shows a table with the existing products in stock.


The project includes an app folder. 
The app folder includes the static folder, the templates folder and the main .py files.
The static folder includes all the static files: css, images, js and plugins.
The templates folder includes all the HTML files used.
The __init__.py file contains the basic configuration for the app.
The views.py file contains the main views available to the customer.
The admin_views.py file contains the admin views only available to the admin user.
The db.py file contains the database tables set up.
The authorization.py file contains the routes for log in and sign up, it also loads the user and handles the "page not found" error.

The project includes a requirements.txt file.
The project includes a run.py file to run the app.