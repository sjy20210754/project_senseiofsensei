import service

def main():
    con=service.connect_database("data/sensei_of_sensei.db")

    service.initialize(con)


if __name__ == "__main__":
    main()
