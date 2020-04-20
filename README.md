# Two-Phase Commit

> Navn på biblioteket og eventuell lenke til continuous integration løsning

There is one major reason for many of the choices I made during this project:  
I am **one person** and had very little time.  
This necessitated limiting the scope of the project, and choosing simplicity wherever possible.

I started this project with creating a very simple demonstration. See
[testcoordinator.py](testcoordinator.py)
and
[testservice.py](testservice.py)
.

The current system blah blah ...

## Contents

## Introduction

rundown of 2pc

1. coordinator asks if parties can do the transaction
    - if all agree, proceed
    - if one disagrees, abort
2. coordinator asks parties to perform the action
    - if all succeed, the transaction is complete
    - if one fails, the state must be rolled back

## Implemented functionality

- [x] Simple 2PC demonstration
- [x] Simple data model
- [x] Events
- [x] Messages
- [x] Transaction coordinator
- [x] Warehouse service
- [ ] Ledger service
- [x] Abort of ready state
- [x] Rollback
- [ ] Retrying transaction if not _invalid_
- [ ] Transaction logging
- [ ] Undo and redo logs
- [ ] Dynamic coordination from anywhere (really?)

## Architecture choices ++

this is **very** important

> En beskrivelse og diskusjon/argumentasjon (denne delen en veldig viktig ved evaluering) av hvilke teknologi- og arkitektur-/designvalg dere har stått ovenfor (når dere skulle løse oppgaven), hva dere hadde å velge mellom og hvorfor dere har valgt det dere har valgt. Når det gjelder teknologivalg så kan denne delen begrenses til «pensum i faget».

Using simple TCP sockets blah blah


### Library choices

+ `pickle` to serialize message data
+ standard `socket` module
+ `logging` for creating readable logs

## Future improvements

> Fremtidig arbeid med oversikt over mangler og mulige forbedringer

## Installation

## Usage examples

> Eksempler som viser bruken av løsningen


## Testing

> Hvordan man kan teste løsningen

## Documentation

(API-dokumentasjon, spørs hvor generelt dette blir)

## Sources

[https://wiki.c2.com/?TwoPhaseCommit](https://wiki.c2.com/?TwoPhaseCommit)

