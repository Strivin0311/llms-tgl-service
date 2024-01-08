model=HuggingFaceH4/zephyr-7b-beta
volume=$PWD/data

docker run --gpus all --shm-size 1g -p 8080:80 -v $volume:/data ghcr.io/huggingface/text-generation-inference:1.3.4 --model-id $model