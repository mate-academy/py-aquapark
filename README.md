# Aqua-park

**Read** [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before starting.

You are a visitor of aqua-park. There are several slides with different limitations of height, weight and age. 
Let's create a system that determines whether a visitor can use the slide depending on the own parameters.

To implement it, create the following classes:

#### 1. `IntegerRange` class - descriptor for parameters limitations
Its constructor takes 2 values and stores them:
   - `min_amount` - min integer accessible value of the visitor's parameter
   - `max_amount` - max integer accessible value of the visitor's parameter

Create `__get__()`, `__set__()` and `__set_name__()` methods.


#### 2. `Visitor` class that is responsible for the user's personal data
Its constructor takes `name`, `age`, `weight`, and `height`.


#### 3. `SlideLimitationValidator` class, inherited from `ABC` class
Its constructor takes `age`, `weight`, and `height`.


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


#### 5. `Slide` class
Its constructor takes 2 arguments:
   - `name` - string value, slide's name
   - `limitation_class` - instance of `SlideLimitationValidator` class which sets restrictions on the use of the slide

Create `can_access` method that takes instance of `Visitor` class and returns if the visitor can use the slide.
