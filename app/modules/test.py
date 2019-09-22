
class MyError(Exception):
    pass

def foo():
    try:
        f,g = 10,20
        if f < g:
            raise TypeError("GGGGGG")
    except:
        raise MyError("My Error")
    finally:
        print("Finally close")

try:
    foo()
except MyError:
    print("Erroo")