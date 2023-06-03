from src.query import Query
import time

if __name__ == "__main__":
    q = Query()
    s = time.time()
    print(q.makeQuery("christina lopes and uc irvine"))
    e = time.time()
    print(f"time: {e-s}")