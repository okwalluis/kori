# Estructurar proyecto
- Cambiar el nombre app a config
- Realizar el refactor en los archivos afectados como; settings wsgi y otros.

# Crear archivo DOCKER-COMPOSE para levantar contenedores de PG y PGADMIN
- docker-compose.yml

# Versionado con Gitlab y git
- Instalar Git
- Generar Key SSH
  - Abrir Git Bash
  - Ejecutar el siguiente comando
```
ssh-keygen -t rsa -b 4096 -C "okwalluis@gmail.com"
```
- Copiar el key SSH generado
``` 
cat /c/Users/user/.ssh/id_rsa.pub
```
- Crear cuenta en Gitlab
  - En GitLab, ingresar a Preferences >> Key SSH >> Agregar nueva Key SSH
  - Pegar Key SSH
- Descargar proyecto a Workspace local
  - Copiar link "Clone with SSH"
  - Abrir Git Bash en la carpeta donde se desea descargar el proyecto
  - Ejecutar el siguiente código
```bash
git clone git@gitlab.com:checode/horus.git
```
```bash
Cloning into 'horus'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.
```
# Versionar cambios
- Abrir Git bash en la carpeta del proyecto
  - Ejecutar el siguiente código
```bash
git add -f app/
```
```bash
git commit -m "Se ha agregado folder del proyecto"
```
```bash
git push
```
