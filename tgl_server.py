import os
import argparse
import json
import subprocess


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TGL server script to start the docker server with the specific hf LLM")
    
    parser.add_argument("--model", type=str, required=True, help="The model id name in the huggingface hub")
    parser.add_argument("--volume", type=str, default="$PWD/data", help="The docker volume path to avoid download the model weights every run, default is '$PWD/data/'")

    args = parser.parse_args()
    
    model_id = args.model
    volume = args.volume.replace("$PWD", os.getcwd()) if args.volume.startswith("$PWD") else args.volume
    
    docker_command = [
        "docker", "run", 
        "--gpus", "all",
        "--shm-size", "1g",
        "-p", "8080:80",
        "-v", args.volume + ":/data",
        "ghcr.io/huggingface/text-generation-inference:1.3.4",
        "--model-id", model_id
    ]
    
    # docker run --gpus all --shm-size 1g -p 8080:80 -v $volume:/data ghcr.io/huggingface/text-generation-inference:1.3.4 --model-id $model
    try:
        result = subprocess.run(docker_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Some Error happened when trying to run the docker server:\n{e.stderr}")
