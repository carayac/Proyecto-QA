#!/bin/bash
echo "  ----------------------------------------------  "
echo "    Complejidad ciclomatica para StockHistory"
echo "  ----------------------------------------------  "
radon cc ../stock/views.py -s -a | grep view_history
read -p "Presiona Enter para salir"