from domain.todo import ToDo


def main():
    to_do = ToDo.create("Buy Milk")
    print(vars(to_do))

    to_do.mark_as_done()
    print(vars(to_do))

    print(vars(ToDo.load_from_history(to_do.flush_events())))


if __name__ == "__main__":
    main()
