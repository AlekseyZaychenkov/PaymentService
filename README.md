Simple payment service with using Django 4 and Stripe API 5


To run project on Ubuntu:

1) Create and prepare virtual environment:

    python3.10 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    python3.10 -m pip install --upgrade pip

2) Install Node.js and npm:

    sudo apt update
    sudo apt install nodejs
    sudo apt install npm
    npm init
    npm install stripe --save

3) Prepare environmental variables:
    
    Create in directory PaymentService file .env
    With variables:
        SECRET_KEY=any-random-key-for
        STRIPE_PUBLISHABLE_KEY=my-secret-stripe-publishable-key
        STRIPE_SECRET_KEY=my-stripe-secret-key
    , where 'my-secret-stripe-publishable-key' and 'my-stripe-secret-key' you need get from your personal account from https://dashboard.stripe.com/test/apikeys

4) Prepare database:

    python3.10 manage.py makemigrations
    python3.10 manage.py migrate

5) Run app:
    
    python manage.py runserver

