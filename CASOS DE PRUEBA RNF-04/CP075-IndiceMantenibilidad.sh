#!/bin/bash
echo "  --------------------------------  "
echo "      Indice de mantenibilidad"
echo "  --------------------------------  "
radon mi ../stock/models.py -s
radon mi ../stock/form.py -s
radon mi ../stock/views.py -s
radon mi ../stock/urls.py -s
read -p "Presiona Enter para salir"
