#!/usr/bin/python3


import deedee

# define a custom Database class
# which prints out the query to be executed


class Database:
    def select(self, query):
        print("select", query)


# define a function whose 'database' parameter's default
# value will be determined when it is called, not when it is defined
@deedee.resolve
def handler(param_a, param_b, database=deedee.context.database):
    print(param_a, param_b)  # param_a and param_b are unchanged
    # this will print a Database instance, something like <__main__.Database object at 0x7fb42217f400>
    # keep in mind that the Database instance at the point of the defintion of the function was not defined
    print(database)
    database.select("select * from table order by id")  # this call will be successful


def main():
    # register the default value for all references (eg. where
    # a function's default value is deedee.context.database) to a Database instance
    deedee.context.register("database", Database())

    # call the handler, the 3rd parameter will be the previously registered value
    # node: it is still possible to call the function with specifying the
    # 3rd parameter - this will override the default value
    handler("param_1", "param_2")


if __name__ == '__main__':
    main()
