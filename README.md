# pyworkshopsystem

### A micropython object model for the Music Thing Modular Workshop System Computer module.

This repo contains an initial attempt at an object model for the
Music Thing Modular Workshop System's Computer module. In abstracting 
away much of the micropython specifics, it aims to allow a user to 
interact directly with the components of the module (knobs, sockets, 
switches and LEDs) in software.

This is a first attempt based on the supplied documentation without the benefit
of access to a working system for testing and mainly contains the beginnings of
various class definitions, along with some functionality inspired by the [rwmodular
computer repo](https://github.com/rwmodular/computer/tree/main).