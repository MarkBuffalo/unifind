# Hopelessly broken.
This is currently borked in the current state. You will have to edit `options.json` to make sure what you're looking for is actually on the page. 

# unifind
Scans the Ubiquiti site to see if a product is in stock or not. Currently in beta. Requires geckodriver.

# Install

```
    pip3 install -r requirements.txt
    pip3 install PyObjC
    brew install geckodriver
```

# Usage

- NOTE: You must edit `product_list.txt` and place line-separated unifi product page urls. Not pages that list multiple products, but the actual product page for the product you want. There are examples already inside.

```
python3 unifind.py
```

or

```
./unifind.py
```
