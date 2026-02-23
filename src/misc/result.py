from dataclasses import dataclass


@dataclass
class Ok[T]:
    val: T


@dataclass
class Err[E]:
    err: E


type Result[T, E] = Ok[T] | Err[E]
type ResultE[T] = Ok[T] | Err[Exception]
