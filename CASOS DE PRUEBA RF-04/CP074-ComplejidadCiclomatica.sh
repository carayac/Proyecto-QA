#!/bin/bash
echo "  --------------------------------  "
echo "      Complejidad ciclomatica"
echo "  --------------------------------  "
radon cc ../stock/views.py -s -a 

read -p "Presiona Enter para salir"
