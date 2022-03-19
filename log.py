def log_write(str):
    f = open("log.txt", "a",encoding="utf-8")
    f.write(str)
    f.close
