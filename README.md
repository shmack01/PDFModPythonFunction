

There are 2 solutions to deploy: 
- Directly to a Function App
- Via a container. 


Version: Python 3.8. <br/><br/>

# Function App

The following line will install Ghostscript. 

```
command = subprocess.run(["apt-get", "-y", "install", "ghostscript"], check=True)
```
> Note this should not execute if using Docker container.

<br/><br/>
# Docker

The code contains a DOCKERFILE that can be used with deploying to a Function App container. The file installs Ghostscript with the following command: 

```
  RUN sudo apt-get -y install ghostscript 
  ```


**Build the requirements.txt** (This step is optional since the requirements.txt file is already provided)

```
  pip install ghostscript==0.7
  pip freeze > requirements.txt
```

**Create ACR**
- Enable Admin user under the Access Keys blade


**Build Image Locally**

``` 
docker build --no-cache --tag pdfmodpython.azurecr.io/pdfcompression:latest .
```

**Push to ACR**

```
  az acr login --name acr_name
  docker push  acr_name.azurecr.io/pdfcompression:latest
  ```

**Create Function App with Container** (Note: need to more computer resources to execute process: EP3)**
- Deployment Center Blade -> Use Container Registry
- Fill out the settings and turn on "Continuous Deployment"
- Add the Storage Connection String to your App Settings. 
  
 **Don't forget to add the settings for the storage**
` func settings add AzureWebJobsStorage "<string>"`





