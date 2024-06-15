#!/bin/bash

# Directorio raíz del proyecto
project_dir="$HOME/proyecto"

# Estructura de carpetas a crear
folders=(
  "src/application/useCases"
  "src/application/controllers"
  "src/application/ports"
  "src/domain/entities"
  "src/domain/valueObjects"
  "src/domain/services"
  "src/infrastructure/datasets"
  "src/infrastructure/models"
  "src/infrastructure/training"
  "src/infrastructure/database"
  "src/infrastructure/repositories"
  "tests/application"
  "tests/domain"
  "tests/infrastructure"
  "models/pre-entrenados"  # Opcional
)

# Recorrer y crear carpetas faltantes
for folder in "${folders[@]}"; do
  if [ ! -d "$project_dir/$folder" ]; then
    mkdir -p "$project_dir/$folder"
  fi
done

# Mensaje de finalización
echo "Carpetas faltantes creadas exitosamente en: $project_dir"
