# llms-tgl-service
Based upon the LLMs Text Generation Inference (TGI) server tool built by HuggingFace, this repo offers some simple additional codes for more convenience


### Source

*TGL is a Rust, Python and gRPC server for text generation inference, built by HuggingFace and used in production to power Hugging Chat, the Inference API and Inference Endpoint*

* github repo link: [here](https://github.com/huggingface/text-generation-inference)

* huggingface quick tour: [here](https://huggingface.co/docs/text-generation-inference/quicktour)


### Preparation

* pull the huggingface tgl docker image with the specific `version` like `1.3.4` in the script `tgl_pull.sh`:
    ```sh
    sh tgl_pull.sh # => docker pull ghcr.io/huggingface/text-generation-inference:$version
    ```
* (*optional*) then you can save the docker image as a tarball and load it in any machine you want to import the image (*assuming version=1.3.4*):
    ```sh
    docker save -o llms-tgl-server-v1_3_4.tar ghcr.io/huggingface/text-generation-inference:1.3.4
    docker load -i llms-tgl-server-v1_3_4.tar
    ```

### Usage1 (official, shell script)

* specify the `model` you want to use and the `volume` (*to share with the docker container to avoid downloading weights every run*) in the script `tgl_server.sh`:
    ```sh
    model=HuggingFaceH4/zephyr-7b-beta
    volume=$PWD/data
    ```
* then run the docker container to start the server at `http://127.0.0.1:8080/generate`:
    ```sh
    sh tgl_server.sh # => docker run --model-id $model -v $volume:/data ghcr.io/huggingface/text-generation-inference:1.3 --gpus all -p 8080:80 --shm-size 1g
    ```
* now you can think of the `inputs` you'd like to query the model and the generation parameters like `max_new_tokens` in the script `tgl_client.sh`:
    ```sh
    inputs="Which team won the NBA Championship the year when Lebron James was born?"
    max_new_tokens=200
    ```
* then use the curl to make a `POST` request in json style to interact with the model you want:
    ```sh
    sh tgl_client.sh # => curl 127.0.0.1:8080/generate -X POST -d '{"inputs":"$inputs","parameters":{"max_new_tokens":$max_new_tokens}}' -H 'Content-Type: application/json'
    ```

### Usage2 (own, python script)

* start the docker server, with the arguments for the `model` (*required*) and `volume` (*optional*) by running the python script `tgl_server.py`:
  ```sh
  python tgl_server.py --model HuggingFaceH4/zephyr-7b-beta --volume $PWD/data
  ```
* query the model with the `prompt` (*required*) and some other generation parameters defined in the `transformers.GenerationConfig` (*optional*) by running the python script `tgl_client.py`: 
  ```sh
  python tgl_client.py \
  --prompt "Which team won the NBA Championship the year when Lebron James was born?" \
  --max_new_tokens=200
  ```