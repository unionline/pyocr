from views.gui import Application
from tkinter import Tk


def main():

    root = Tk()
    app = Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
