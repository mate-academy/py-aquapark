# Aqua-park

**Read** [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before starting.

You are a visitor of aqua-park. There are several slides with different limitations of height, weight and age. 
Let's create a system that determines whether a visitor can use the slide depending on the own parameters.

To implement it, create the following classes:

#### 1. `IntegerRange` class - descriptor for parameters limitations
Its `__init__` method takes 2 values and stores them:
   - `min_amount` - min integer accessible value of the visitor's parameter
   - `max_amount` - max integer accessible value of the visitor's parameter

Create `__get__()`, `__set__()` and `__set_name__()` methods.
The `__set__()` method needs to have a logic to validate that the value is between `min_amount` and `max_amount` and will be used in Validator classes.
Do not forget to check the type of value before setting it. You can raise TypeError or ValueError
during validation. Error messages can be skipped.


#### 2. `Visitor` class that is responsible for the user's personal data
Its `__init__` method takes `name`, `age`, `weight`, and `height`. `Visitor` does not have any limitations.


#### 3. `SlideLimitationValidator` class
Its `__init__` method takes `age`, `weight`, and `height`. No additional methods are needed here.
This is a base class for Validators, so no validation is needed.


#### 4. `ChildrenSlideLimitationValidator` and `AdultSlideLimitationValidator` classes, it's a limitation validators for slides 
Aqua-park has two types of slides: for adult and for children.

`ChildrenSlideLimitationValidator` class and set values:
   - `age` in range of `4` and `14`
   - `height` in range of `80` and `120`
   - `weight` in range of `20` and `50`

`AdultSlideLimitationValidator` class and set values:
   - `age` in range of `14` and `60`
   - `height` in range of `120` and `220`
   - `weight` in range of `50` and `120`

These classes should be inherited from `SlideLimitationValidator`. No additional methods are needed here.

#### 5. `Slide` class
Its `__init__` method takes 2 arguments:
   - `name` - string value, slide's name
   - `limitation_class` - one of the `SlideLimitationValidator` child class which sets restrictions on the use of the Slide.
   Please note that the constructor should only store the class itself and not instantiate an instance of it.   

Create a method called `can_access` that checks whether a Visitor can use the slide, returning True or False.
To validate the Visitor's attributes, create an instance of `limitation_class`. You don't need to store this instance anywhere.
The `can_access` method should handle all possible errors that may be raised by the `limitation_class`.

### Note: Check your code using this [checklist](checklist.md) before pushing your solution.

