from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Person:
    name: str
    age: int

@dataclass(frozen=True)
class Company:
    name: str
    ceo: Person

# Example usage
sw = Company(name="SimilarWeb", ceo=Person("Or Ofer", age=40))

print(sw.ceo.age)

# sw.ceo.age = 41  ### error

sw1 = replace(sw, ceo=replace(sw.ceo, age=sw.ceo.age+1))

from CT import *

comp2ceo_lens = gs2lens(
    lambda company: company.ceo,
    lambda company, newceo: replace(company, ceo=newceo)
)

person2age_lens = gs2lens(
    lambda person: person.age,
    lambda person, newage: replace(person, age=newage)
)

comp2age_lens = lambda x: comp2ceo_lens(person2age_lens(x))

compCeoInc = fmapLens(comp2age_lens, lambda a: a+1)

print(compCeoInc(sw))