#!/bin/bash

# Create or overwrite the .env file
> .env

# Loop over environment variables and write them to the .env file
for var in $(env | grep -Eo '^[A-Za-z_]+=.+'); do
  echo "$var" >> .env
done
