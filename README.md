# comp7940_cloud_group_project


## Link to the dataset: 
- https://recipenlg.cs.put.poznan.pl/dataset 


## How to start the application 

### Using docker compose: 
0. Prerequesites: You have to create a environment file .env. The envirionment file must contain the connection credentials for the database and the API Token for the telegram chatbot. You can just use the env-example.txt as orientation. 
1. To use docker compose you have to build the image first, as we currently don't store the docker image in a registry: 
    - docker-compose up --build -d 
2. How to start the container: 
    - docker-compose up 
3. The container is now accesible and you can test it with telegram on your smartphone 