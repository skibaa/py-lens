from typing import *
from abc import ABC, abstractmethod

A = TypeVar('A')
B = TypeVar('B')
S = TypeVar('S')
T = TypeVar('T')
F = TypeVar('F', bound='Functor')  # Bound F to ensure it's a Functor

class Functor(ABC, Generic[A]):
    @abstractmethod
    def fmap(self, func: Callable[[A], B]) -> 'Functor[B]':
        pass

Lens=Callable[[Callable[[A], F]], Callable[[S], F]]

Getter=Callable[[S], A]
Setter=Callable[[S,B], T]

def gs2lens(g: Getter, st: Setter) -> Lens:
  def f(afb: Callable[[A], F]) -> Callable[[S], F]:
     def sft(s: S) -> F:
        a = g(s)        # Getter S -> A
        fb = afb(a)     # A -> F[B]
        # TODO: assert fb is indeed Functor[B]
        ft = fb.fmap(lambda b: st(s, b))
        # TODO: assert ft is indeed Functor[T]
        return ft
     return sft	
  return f

class ConstFunctor(Functor[A], Generic[T, A]):
    def __init__(self, value: T):
        self.value = value

    def getValue(self) -> T:
        return self.value

    def fmap(self, f: Callable[[A], B]) -> 'Functor[B]':
        return ConstFunctor(self.value)

class IdFunctor(Functor[A], Generic[A]):
    def __init__(self, value: A):
        self.value = value

    def getValue(self) -> A:
        return self.value

    def fmap(self, f: Callable[[A], B]) -> 'Functor[B]':
        return IdFunctor(f(self.value))

def lens2getter(l: Lens) -> Getter:
    def get(s: S) -> A:
        sft = l(lambda a: ConstFunctor(a))
        ft = sft(s)   # F[T] is Const(a)
        return ft.getValue()

def lens2setter(l: Lens) -> Setter:
    def set(s: S, b: B) -> T:
        sft = l(lambda a: IdFunctor(b))
        ft = sft(s)   # F[T] is Id[T]
        return ft.getValue()

listIntGetter: Getter[List[int], int] = lambda s: s[0]
listIntSetter: Setter[List[int], int, List[int]] = lambda s, b: (s.__setitem__(0, b), s)[1]
listIntLens: Lens[int, F, List[int]] = gs2lens(listIntGetter, listIntSetter)

dictListGetter: Getter[Dict[str, List[int]], List[int]] = lambda s: s['lst']
dictListSetter: Setter[Dict[str, List[int]], List[int], Dict[str, List[int]]] = lambda s, b: (s.update({'lst': b}), s)[1]
dictListLens: Lens[List[int], F, Dict[str, List[int]]] = gs2lens(dictListGetter, dictListSetter)

dictIntLens = lambda afb: dictListLens(listIntLens(afb))

def fmapLens(l: Lens, f:Callable[[A], B]) -> Callable[[S], T]:
    def st(s: S) -> T:
        afb = lambda a: IdFunctor(f(a))
        sft = l(afb)
        ft = sft(s)
        t = ft.getValue()
        return t
    return st

myList = [10,20,30]
myDict = {'aaa': [11,12], 'lst': myList}

#print(fmapLens(listIntLens, lambda a: a+1)(myList))
#print(intLensInc(dictIntLens, lambda a: a+1)(myDict))
