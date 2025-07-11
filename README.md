# Agronova


# Correr proyecto 1 vez
cd project 
python -m venv env 
env/scripts/activate
pip install -r requirementes.txt

# Empezar a trabajar
git pull origin main
env/scripts/activate
pip install -r requirementes.txt
hacer cambios
git add archivo/s
git commit -m "Nombre del commit"
git push origin nombre_rama

# Crear ramas
git switch -c nombre_rama
git push origin nombre_rama

# clonar el repositorio
git clone link
