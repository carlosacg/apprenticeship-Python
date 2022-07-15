from datetime import datetime


def test_func(date: datetime = datetime.now()) -> None:
    print("NOW", date)


test_func()
test_func()
test_func()
test_func(datetime.now())
test_func()
test_func()
