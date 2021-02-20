from domain.customer import Customer, CustomerCreatedEvent


def main():
    customer = Customer.create("Marcelo Santos")
    print(vars(customer))

    customer.change_name("John Doe")
    print(vars(customer))

    new_customer = Customer.load_from_history(customer.flush_events())
    print(vars(new_customer))

    try:
        customer.change_name(1234)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
