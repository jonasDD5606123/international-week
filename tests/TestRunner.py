import os
from behave.__main__ import main as behave_main

if __name__ == "__main__":
    args = [
        "Feature/",
    ]
    behave_main(args)