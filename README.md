### Audio file server
This is a minimal server that takes three kinds of audio file and store it in a postgresql database and also 
has an upload endpoint to be used to upload audio corresponding to the metatdata that will have been created initially

Endpoints:
There are only four endpoints on the server and each of them accepts query or update or creation of the three audio file kind 
* audio_book
* podcast
* song

> POST /api/audio/create
> 
> endpoint takes a json structure that will include the audio type to be created and custom body of the audio metadata. 
> i.e
```json
    {
    "filetype": "song",
    "duration": 123456,
    "name": "lionand hare",
    "host": "joe rogan",
    "participants": ["dan peterson", "olsp"]
}
```
the file type can be varying based on the three accepted file types.

> GET /api/audio/<audio_kind>/audio_id
> 
> This endpoint returns the corresponding data referenced by the <audio_id> given its filetype if it exist on the server otherwise 404.
> The other variant of this is calling the endpoint without the <audio_id> will return the list of audio data given that valid audio type

> PUT /api/audio/<audio_kind>/audio_id 
> 
> This endpoint takes a valid audio file as multipart form data body, and the path parametre that references a file metadata on the server.
> it stores the file locally.

### How to run
requirements:
* postgresql 
* python >= 3.8
* pip 
* virtualenv

##### prepare database
create two database one for testing and one the other for normal server running.
```sql
    CREATE DATABASE audio_file_server;
    CREATE DATABASE audio_file_server_test;
    GRANT ALL PRIVILEGES ON DATABASE audio_file_server_test TO <insert db user here>
    GRANT ALL PRIVILEGES ON DATABASE audio_file_server TO <insert db user here>
```

##### create a virtual env and activate it
assumming the code will be run on a unix system. create a directory and move in to it
```shell
    mkdir audio-file-server-env
    cd audio-file-server-env
    virtualenv --python python3.9  .
    source bin/activate
```

##### Install requirements and run
before running make sure env variables are set. below is a set of required env variables, you can either create a .env file and put them inside
or export them from the terminal.

```shell
   export  DATABASE_URL='postgresql://<postgres_user>:<postgres_password>@<postgres_host>:5432/audio_file_server'

   export SECRET_KEY="secret"

   export FLASK_CONFIG=development

   export FLASK_APP=application

FLASK_ENV="development"

```
```shell
    pip install -r requirements.txt
    make run
```

#### Test
```shell
    make test
```