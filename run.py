from flask import Flask
from app import view



if __name__ == "__main__":
    view.app.run(debug=True)