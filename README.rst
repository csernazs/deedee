deedee
~~~~~~
Dependency inversion for python, the easy way


Nutshell
--------

Deedee provides an API which enables the developer to use late binding for
default values in function definition.

Example:


.. code-block:: python

    import deedee

    class Database:
        def select(self, query):
            print("select", query)


    @deedee.resolve
    def handler(param_a, param_b, database=deedee.context.database):
        print(param_a, param_b)  # param_a and param_b are unchanged
        print(database) # this will print a database instance
        database.select("select * from table order by id")  # this call will be successful


    def main():
        # register the default value (which will be used when calling handler)
        deedee.context.register("database", Database())

        # call the handler, the 3rd parameter will be the previously registered value
        handler("param_1", "param_2")


    if __name__ == '__main__':
        main()


In python the binding of the default value happens at the function
defintion, so it is not possible to set the default parameter later on, the
expression after the '=' sign gets evaluated at the function definition.

With `deedee` this changes, so you can specify a reference instead, and later on, specify the value for that reference.

When the function is called later on, the decorator `deedee.resolve` will
resolve the reference of the default value.

This can be used to implement dependency injection and dependency inversion
patterns without using any boilerplate classes or functions.


Features
--------
* Lazy evaluation of the default parameters
* Default value can be overriden by specifying it during the call (same behaviour as 'normal' default values)
* It can be traced which function references to a given default parameter (soon)
* It can be checked that all references can be resolved in the future, so it
  can be ensured that there will be no error with resolving during function
  calls
* Context objects can be implemented by the user (it is not required to use deedee.context)
* Annotations can be use freely, the library doesn't use or change them
* Nearly straightforward implementation, good test coverage


Name
----
According to urban dictionary, deedee is:

    A person who is always there when you need them. A strong survivor who can make it through anything.

In deedee the values you are registering to a context behave like this – they are always there when you need them.
