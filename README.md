# Shamzam-Coursework

### User Stories
This is a repository for my course work for the Enterprise Computing module at the University of Exeter. 
The specification should show:
 - S1 As an administrator, I want to add a music track to the catalogue, so that a user can listen to it.
 - S2 As an administrator, I want to remove a music track from the catalogue, so that a user cannot listen to it.
 - S3 As an administrator, I want to list the names of the music tracks in the catalogue, so that I know what it contains.
 - S4 As a user, I want to convert a music fragment to a music track in the catalogue, so that I can listen to it.

### Microservices
The microservices are:
- Admin Microservice, implements S1, S2, S3 user stories
- User Microservice, implements S4 user story

These are split up so the user and admin can be directed to their own endpoints and will have the functions that they will need.

### Running the project

Run commands, 
- python3 -m unittest S1_tests.py
- python3 -m unittest S2_tests.py
- python3 -m unittest S3_tests.py
- python3 -m unittest S4_tests.py

