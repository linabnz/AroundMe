#!/bin/bash

echo "Welcome to the Streamlit application!"
echo "Choose an option:"
echo "1) Launch the application in terminal mode (launch.sh)"
echo "2) Launch the application with a graphical interface (launch_app.sh)"
read -p "Your choice (1 or 2): " choice

case $choice in
  1)
    read -p "Enter the street name to get the information: " street
    if [ -z "$street" ]; then
      echo "Error: You must enter a street name."
      exit 1
    fi
    echo "You chose: $street"
    bash bin/launch.sh "$street"
    ;;
  2)
    echo "Launching the graphical application..."
    bash bin/launch_app.sh
    ;;
  *)
    echo "Invalid choice. Please restart the container."
    exit 1
    ;;
esac
