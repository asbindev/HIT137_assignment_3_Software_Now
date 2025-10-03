from gui import AppGUI
from models import ModelManager
from oop_demo import OOPDemo

def main():
    # Initialize model manager (lazy loads models on demand)
    model_manager = ModelManager()
    # Create OOP demo instance
    oop_demo = OOPDemo()
    # Start GUI
    app = AppGUI(model_manager=model_manager, oop_demo=oop_demo)
    app.run()

if __name__ == '__main__':
    main()
